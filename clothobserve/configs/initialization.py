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
from core.database.user_models import USER_DATASTORE

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
                    description='Administrator of Clothobserve. Role with access to everything.')
    USER_DATASTORE.find_or_create_role(name='tester', \
                    description='Tester of Clothobserve. Has access to test methods.')
    USER_DATASTORE.find_or_create_role(name='user', \
                    description='User of Clothobserve.')
    USER_DATASTORE.find_or_create_role(name='superuser', \
                    description='Super user of Clothobserve. Has access to premium features')


def create_admin_user() -> None:
    """
    Creates admin user.
    User is auto-confirmed by default and has the highest privileges.
    """
    email = os.getenv('ADMIN_EMAIL', 'admin@example.com')
    password = os.getenv('ADMIN_PASSWORD', 'ChangeMeASAP')
    USER_DATASTORE.create_new_user(email=email, password=password, \
                    default_role="admin", auto_confirm=True)

def register_blueprints(server: Flask) -> None:
    """
    # TODO: Fill this docstring.
    """
    pass
