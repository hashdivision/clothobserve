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
from flask_security import UserMixin, RoleMixin
from data.database.mongo import MONGO_DB
from utils.date import convert_to_string

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
    #: Profile reference for fast access.
    profile = MONGO_DB.ReferenceField('Profile', unique=True)
    #: JSON of profile information for other users to see.
    profile_json = MONGO_DB.StringField()

    def update_username(self, username: str) -> bool:
        """Updates username if it is new and alphanumeric."""
        if username and username != self.username and username.isalnum():
            self.username = username
            return True

        return False

    def create_profile_json(self) -> None:
        """Creates cached JSON string in profile_json."""
        self.profile_json = '{"name":"' + self.profile.name + '",' \
            + '"public":' + "true" if self.profile.public else "false" + ',' \
            + '"date_of_birth":"' + convert_to_string(self.profile.date_of_birth) + '",' \
            + '"about_me":"' + self.profile.about_me + '",' \
            + '"reg_date":"' + str(self.reg_date) + '",' \
            + '"active":"' + "true" if self.active else "false" + '",' \
            + '"roles":' + str([str(r.name) for r in self.roles]) + ',' \
            + '"username":"' + self.username + '"}'

    def update_profile(self, name: str, date_of_birth: datetime, \
                        about_me: str, username: str) -> None:
        """Updates user profile if everything is ok with arguments."""
        updated = self.profile.update_name(name)
        updated = True if self.profile.update_dob(date_of_birth) else updated
        updated = True if self.profile.update_about_me(about_me) else updated
        if updated:
            self.profile.save()

        if self.update_username(username) or updated:
            self.create_profile_json()
            self.save()

class Profile(MONGO_DB.Document):
    """Profile information about users of Clothobserve."""

    #: Reference to user this personal information is about.
    #: If user is deleted - this document is deleted too.
    user = MONGO_DB.LazyReferenceField(User, reverse_delete_rule=mongoengine.CASCADE, \
                                    unique=True, required=True, passthrough=True)
    #: Real name and surname of user.
    name = MONGO_DB.StringField(max_length=64, default="")
    #: Date of birth of user.
    date_of_birth = MONGO_DB.DateTimeField()
    #: A bit of information about user, that he writes himself.
    about_me = MONGO_DB.StringField(max_length=200, default="")
    #: Is user profile public and can be seen by other users.
    #: By default user profile is private.
    public = MONGO_DB.BooleanField(default=False)

    def update_name(self, name: str) -> bool:
        """Updates name if it is new and consist of two words."""
        if name and name != self.name and len(name.split()) == 2:
            self.name = name
            return True

        return False

    def update_dob(self, date_of_birth: datetime) -> bool:
        """Updates date_of_birth if it is new."""
        if date_of_birth and date_of_birth != self.date_of_birth:
            self.date_of_birth = date_of_birth
            return True

        return False

    def update_about_me(self, about_me: str) -> bool:
        """Updates about_me if it is new."""
        if about_me and about_me != self.about_me:
            self.about_me = about_me
            return True

        return False
