"""
    clothobserve.configs.initialization
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Creation of default roles and admin user, registering server blueprints.

    :copyright: © 2018 HashDivision OU.

    :license: Apache License 2.0, see *LICENSE* for more details.

    |

"""
import os
from flask import Flask
from data.models.user import User
from endpoints.user.account import ACCOUNT_BP
from endpoints.user.profile import PROFILE_BP
from endpoints.user.password import PASSWORD_BP
from endpoints.user.email import EMAIL_BP
from endpoints.admin.users import ADMIN_USERS_BP
from logic.user.datastore import USER_DATASTORE

def initialize(server: Flask) -> None:
    """
    Initializes ``Flask`` server by calling 3 methods of this module:
        - ``create_default_user_roles``
        - ``create_admin_user``
        - ``register_blueprints``

    :param server: ``Flask`` object created by calling ``configs.config.create_server()`` method.
    """
    create_default_user_roles()
    create_admin_user()
    register_blueprints(server)

def create_default_user_roles() -> None:
    """
    Creates 4 main default roles:
        - ``admin``
        - ``tester``
        - ``user``
        - ``superuser``
    """
    USER_DATASTORE.find_or_create_role(name='admin', \
                                        description='Administrator of Clothobserve.')
    USER_DATASTORE.find_or_create_role(name='tester', \
                                        description='Tester of Clothobserve.')
    USER_DATASTORE.find_or_create_role(name='user', \
                                        description='User of Clothobserve.')
    USER_DATASTORE.find_or_create_role(name='superuser', \
                                        description='Premium user of Clothobserve.')

def create_admin_user() -> None:
    """
    Creates admin user.
    User is confirmed by default and has the highest privileges.
    """
    email = os.getenv('ADMIN_EMAIL', 'admin@example.com')
    password = os.getenv('ADMIN_PASSWORD', 'ChangeMeASAP')
    username = os.getenv('ADMIN_USERNAME', 'Admin')
    if not User.find_by_email(email):
        USER_DATASTORE.create_admin_user(email=email, password=password, username=username)

def register_blueprints(server: Flask) -> None:
    """
    Registering Blueprints with all service endpoints.
    """
    server.register_blueprint(EMAIL_BP, url_prefix="/account/email")
    server.register_blueprint(PASSWORD_BP, url_prefix="/account/password")
    server.register_blueprint(PROFILE_BP, url_prefix="/account/profile")
    server.register_blueprint(ACCOUNT_BP, url_prefix="/account")
    server.register_blueprint(ADMIN_USERS_BP, url_prefix="/admin/users")
