"""
    clothobserve.configs.initialization
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Creation of default roles and admin user, registering server blueprints.

    :copyright: © 2018 HashDivision OU.

    :license: Apache License 2.0, see *LICENSE* for more details.

    |

"""
from core.server import ClothobserveServer
from core.users.user import create_new_user, create_new_role, USER_BP
from core.auth.authentication import AUTH_BP
from core.auth.registration import REGISTER_BP
from core.security.confirmation import CONFIRM_BP
from core.module.control import register_module, MODULE_BP
from modules.self_management_module import self_management_module
from modules.todo_module import todo_module
from ui.web.web_root import webroot_bp

def initialize(server: ClothobserveServer) -> None:
    """
    Initializes ``Flask`` server by calling 3 methods of this module:
        - ``create_default_user_roles``
        - ``create_admin_user``
        - ``register_blueprints``

    :param server: ``Flask`` object created by calling ``config.create_server()`` method.
    """
    create_default_user_roles()
    create_admin_user()
    register_blueprints(server)
    register_modules()

def create_default_user_roles() -> None:
    """
    Creates 4 main default roles:
        - ``admin``
        - ``tester``
        - ``user``
        - ``superuser``
    """
    create_new_role(name='admin', \
                    description='Administrator of Clothobserve. Role with access to everything.')
    create_new_role(name='tester', \
                    description='Tester of Clothobserve. Has access to test methods.')
    create_new_role(name='user', \
                    description='User of Clothobserve.')
    create_new_role(name='superuser', \
                    description='Super user of Clothobserve. Has access to premium features')

def create_admin_user() -> None:
    """
    Creates admin user with email ``root@clothobserve.com`` and password ``ChangeMeASAP``

    User is auto-confirmed by default and has the highest privileges.
    """
    create_new_user(email="root@clothobserve.com", password="ChangeMeASAP", \
                    default_role="admin", auto_confirm=True)

def register_blueprints(server: ClothobserveServer) -> None:
    """
    Registers all blueprints that Clothobserve has.

    :param server: ``Flask`` object created by calling ``config.create_server()`` method.
    """
    server.register_blueprint(AUTH_BP, url_prefix="/auth")
    server.register_blueprint(REGISTER_BP, url_prefix="/register")
    server.register_blueprint(USER_BP, url_prefix="/user")
    server.register_blueprint(CONFIRM_BP, url_prefix="/confirm")
    server.register_blueprint(MODULE_BP, url_prefix="/module")
    server.register_blueprint(webroot_bp, url_prefix="/ui/web")

def register_modules() -> None:
    """
    # TODO: Fill in this docstring
    """
    register_module(self_management_module())
    register_module(todo_module())