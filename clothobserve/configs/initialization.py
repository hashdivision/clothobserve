"""
    clothobserve.configs.initialization
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Creation of default roles and admin user, registering server blueprints.

    :copyright: © 2018 HashDivision OU.

    :license: Apache License 2.0, see *LICENSE* for more details.

    |

"""
from flask import Flask
from core.users.account import ACCOUNT_BP

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
    # TODO: Fill this docstring.
    """
    pass

def create_admin_user() -> None:
    """
    # TODO: Fill this docstring.
    """
    pass

def register_blueprints(server: Flask) -> None:
    """
    # TODO: Fill this docstring.
    """
    server.register_blueprint(ACCOUNT_BP, url_prefix="/account")
