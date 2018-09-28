"""
    clothobserve.logic.initialization
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Datastore with methods that manipulate user's data.

    :copyright: © 2018 HashDivision OU.

    :license: Apache License 2.0, see *LICENSE* for more details.

    |

"""
from flask_security.datastore import MongoEngineUserDatastore
from flask_security.utils import hash_password, verify_password
from data.models.user import User, Role, Profile
from data.database.mongo import MONGO_DB
from logic.user.email import send_confirmation_link

class ClothobserveUserDatastore(MongoEngineUserDatastore):
    """Slightly tweaked MongoEngineUserDatastore with new functionality."""

    def create_new_user(self, email: str, password: str) -> User:
        """
        Creates new user with username ``user[number_of_users_total+1]``.

        :param email: unique email for new user.
        :param password: plain text password that will be hashed.

        Returns:
            User object if new user is created. Otherwise - None.
        """
        if not User.find_by_email(email):
            username = "user" + str(User.objects.count()+1)
            user = self.create_user(email=email, password=hash_password(password), \
                                    username=username)
            if user:
                self.add_role_to_user(user, Role.find_by_name("user"))
                profile = Profile(user=user)
                profile.save()
                user.profile = profile
                user.create_profile_json()
                # When generating and sending link - user.save() is called
                send_confirmation_link(user)
                return user

        return None

    def create_admin_user(self, email: str, password: str, username: str) -> None:
        """
        Creates admin user.

        :param email: unique email for the admin user.
        :param password: plain text password that will be hashed.
        :param username: unique username for admin user.
        """
        admin = self.create_user(email=email, password=hash_password(password), \
                                confirmed=True, username=username)
        if admin:
            self.add_role_to_user(admin, Role.find_by_name("admin"))
            profile = Profile(user=admin)
            profile.save()
            admin.profile = profile
            admin.create_profile_json()
            admin.save()

    @staticmethod
    def change_user_password(user: User, old_password: str, new_password: str) -> bool:
        """
        Changes user password if old password is correct.

        Returns:
            True if old password was correct (password was changed). Otherwise - False.
        """
        if verify_password(old_password, user.password):
            user.password = hash_password(new_password)
            user.save()
            return True

        return False

    @staticmethod
    def add_role_to_user(user: User, role: Role) -> bool:
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

    @staticmethod
    def remove_role_from_user(user: User, role: Role) -> bool:
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

    @staticmethod
    def deactivate_user(user: User) -> bool:
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

    @staticmethod
    def activate_user(user: User) -> bool:
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

    @staticmethod
    def change_profile_visibility(user: User, public: bool) -> None:
        """
        Changes visibility of user's profile.
        """
        if user:
            profile = user.profile
            profile.public = public
            profile.save()
            user.create_profile_json()
            user.save()

#: Custom user datastore based on MongoEngineUserDatastore.
USER_DATASTORE = ClothobserveUserDatastore(MONGO_DB, User, Role)
