"""
    clothobserve.core.database.user_models
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # TODO: Fill this docstring.

    :copyright: © 2018 HashDivision OU.

    :license: Apache License 2.0, see *LICENSE* for more details.

    |

"""
from datetime import datetime
from flask_security.datastore import MongoEngineUserDatastore
from flask_security import UserMixin, RoleMixin
from core.database.mongo import MONGO_DB

class Role(MONGO_DB.Document, RoleMixin):
    """Role model for Clothobserve MongoDB."""

    #: Name of the role is restricted to 32 symbols.
    #: It should be unique and descriptive.
    name = MONGO_DB.StringField(max_length=32, unique=True, required=True)
    #: Description is restricted to 128 symbols
    #: just in case (it will probably never be this long)
    description = MONGO_DB.StringField(max_length=128, required=True)

class User(MONGO_DB.Document, UserMixin):
    """User model for Clothobserve MongoDB."""

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

class ClothobserveUserDatastore(MongoEngineUserDatastore):
    """Slightly tweaked MongoEngineUserDatastore with new functionality."""

    def add_role_to_user(self, user: User, role: Role) -> bool:
        """
        Adds role to user if it is not in his roles yet.

        Returns:
            True if role was added and False otherwise.
        """
        if role and role not in user.roles:
            user.roles.append(role)
            user.save()
            return True

        return False

    def remove_role_from_user(self, user: User, role: Role) -> bool:
        """
        Removes role from user if it is in his roles.

        Returns:
            True if role was removed and False otherwise.
        """
        if role and role in user.roles:
            user.roles.remove(role)
            user.save()
            return True

        return False

    def deactivate_user(self, user: User) -> bool:
        """
        Deactivates user if he is active.

        Returns:
            True if user was deactivated and False otherwise.
        """
        if user.active:
            user.active = False
            user.save()
            return True

        return False

    def activate_user(self, user: User) -> bool:
        """
        Activates user if he is inactive.

        Returns:
            True if user was activated and False otherwise.
        """
        if not user.active:
            user.active = True
            user.save()
            return True

        return False

#: Custom user datastore based on MongoEngineUserDatastore.
USER_DATASTORE = ClothobserveUserDatastore(MONGO_DB, User, Role)