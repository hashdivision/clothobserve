"""
    clothobserve.data.models.user
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # TODO: Fill this docstring.

    :copyright: © 2018 HashDivision OU.

    :license: Apache License 2.0, see *LICENSE* for more details.

    |

"""
from datetime import datetime
import mongoengine
from mongoengine.queryset.visitor import Q
from flask_security import UserMixin, RoleMixin
from data.database.mongo import MONGO_DB

class Role(MONGO_DB.Document, RoleMixin):
    """Role model for Clothobserve MongoDB."""

    @staticmethod
    def find_by_name(name: str):
        """Search for role by it's unique name."""
        return Role.objects(name=name).first()

    #: Name of the role is restricted to 32 symbols.
    #: It should be unique and descriptive.
    name = MONGO_DB.StringField(max_length=32, unique=True, required=True)
    #: Description is restricted to 128 symbols
    #: just in case (it will probably never be this long)
    description = MONGO_DB.StringField(max_length=128, required=True)

class User(MONGO_DB.Document, UserMixin):
    """User model for Clothobserve MongoDB."""

    @staticmethod
    def find_by_email(email: str):
        """Search for user with unique email."""
        return User.objects(email=email).first()

    @staticmethod
    def find_by_username(username: str):
        """Search for user with username."""
        return User.objects(username=username).first()

    #: Email is restricted to 255 symbols (see ``RFC 3696``).
    #: It is the only mean of login via normal login form.
    email = MONGO_DB.StringField(max_length=255, unique=True, required=True)
    #: Username is restricted to 32 symbols.
    #: It should be unique and it is shown to other users instead of email.
    username = MONGO_DB.StringField(max_length=32, unique=True, required=True)
    #: Password is hashed with PBKDF2-SHA512, so it will always
    #: be around 130 characters, but maximum length is not restricted.
    password = MONGO_DB.StringField(required=True)
    #: Inactive users cannot login into Clothobserve service.
    active = MONGO_DB.BooleanField(default=True)
    #: Roles are used to restrict access to some functionality.
    roles = MONGO_DB.ListField(MONGO_DB.ReferenceField(Role), default=[])
    #: User registration date.
    reg_date = MONGO_DB.DateTimeField(default=datetime.now)
    #: Random hash that should be checked at
    #: confirmation endpoint in order to confirm email.
    confirm_hash = MONGO_DB.StringField()
    #: Date of generation of confirm hash to check for expiration.
    confirm_hash_date = MONGO_DB.DateTimeField()
    #: This flag shows if user's email is confirmed.
    confirmed = MONGO_DB.BooleanField(default=False)
    #: Last login time. Used for security.
    last_login_at = MONGO_DB.DateTimeField(default=datetime.now)
    #: Current login time. Used for security and to determine
    #: if user was inactive for a long period of time.
    current_login_at = MONGO_DB.DateTimeField(default=datetime.now)
    #: Last login IP address. Used for security.
    last_login_ip = MONGO_DB.StringField()
    #: Current login IP address. Used for security.
    current_login_ip = MONGO_DB.StringField()
    #: How many times user logged into the Clothobserve service.
    login_count = MONGO_DB.IntField()

class Profile(MONGO_DB.Document):
    """Profile information about users of Clothobserve."""

    @staticmethod
    def find_public_by_user(user: User):
        """Search for public Profile with User object."""
        return Profile.objects(Q(public=True) & Q(user=user)).first()

    @staticmethod
    def find_by_user(user: User):
        """Search for Profile with User object."""
        return Profile.objects(user=user).first()

    #: Reference to user this personal information is about.
    #: If user is deleted - this document is deleted too.
    user = MONGO_DB.ReferenceField(User, reverse_delete_rule=mongoengine.CASCADE, \
                                    unique=True, required=True)
    #: Real name and surname of user.
    name = MONGO_DB.StringField(max_length=64, default="")
    #: Date of birth of user.
    date_of_birth = MONGO_DB.DateTimeField()
    #: A bit of information about user, that he writes himself.
    about_me = MONGO_DB.StringField(max_length=200, default="")
    #: Is user profile public and can be seen by other users.
    #: By default user profile is private.
    public = MONGO_DB.BooleanField(default=False)

    def to_response_json(self):
        return '{"name":"' + self.name + '",' \
            + '"date_of_birth":"' + str(self.date_of_birth) + '",' \
            + '"about_me":"' + self.about_me + '",' \
            + '"reg_date":"' + str(self.user.reg_date) + '",' \
            + '"active":"' + str(self.user.active) + '",' \
            + '"roles":' + str([str(r.name) for r in self.user.roles]) + ',' \
            + '"username":"' + self.user.username + '"}'
