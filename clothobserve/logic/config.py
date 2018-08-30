"""
    clothobserve.logic.config
    ~~~~~~~~~~~~~~~~~~~~~~~~~
    Initialization of ``Flask`` server.

    :copyright: © 2018 HashDivision OU.

    :license: Apache License 2.0, see *LICENSE* for more details.

    |

"""
import os
from flask import Flask
from flask_security import Security
from werkzeug.contrib.fixers import ProxyFix
from data.database.mongo import MONGO_DB
from logic.user.datastore import USER_DATASTORE
from logic.mail.sender import MAIL

def create_server() -> Flask:
    """Creates and initializes ``Flask`` server.

    Configuration is loaded from class (name should be
    in environment variable CONFIG_TYPE), which should be
    subclassed from ``Config`` class.
    Configuration in HTTP proxy environment (``ProxyFix``) is done
    because original Clothobserve app is behind the proxy.

    Returns:
        The ``Flask`` class object.
    """
    root_path = os.getenv('ROOT_PATH', '/clothobserve/')
    config_object = 'data.config.' + os.getenv('CONFIG_TYPE', 'DevelopmentLocalConfig')

    server = Flask('clothobserve', root_path=root_path)
    server.config.from_object(config_object)
    server.wsgi_app = ProxyFix(server.wsgi_app, num_proxies=1)
    MONGO_DB.init_app(server)
    MAIL.init_app(server)
    Security(server, USER_DATASTORE)

    return server
