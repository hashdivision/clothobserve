"""
    clothobserve.configs.config
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Configurations for different environments:
        - production
        - development
        - test

    and initialization of ``Flask`` server.

    :copyright: © 2018 HashDivision OU.

    :license: Apache License 2.0, see *LICENSE* for more details.

    |

"""
from flask_security import Security
from werkzeug.contrib.fixers import ProxyFix
from core.server import ClothobserveServer
from core.database.mongo import MONGO_DB
from core.database.mongo_user_models import USER_DATASTORE
from core.mail.sender import MAIL

def create_server(config_object: str = "configs.config.DevelopmentLocalConfig", \
                root_path: str = "/clothobserve/") -> ClothobserveServer:
    """Creates and initializes ``Flask`` server.

    Configuration is loaded from ``config_object`` class,
    which should be subclassed from ``Config`` class.
    Configuration in HTTP proxy environment (``ProxyFix``) is done
    because original Clothobserve app is behind the proxy.

    Libraries that are initialized for Clothobserve are:
        - ``Flask-Security``,
        - ``Flask-MongoEngine``,
        - ``Flask-Mail``,
        - ``apscheduler``

    :param config_object: "Full address" of a class to use as configuration,
        which should be subclassed from ``Config`` class.
        Defaults to ``configs.config.DevelopmentLocalConfig``.

    :param root_path: Path on OS where all application code and folders
        like templates are. Defaults to ``/clothobserve/``.

    Returns:
        The ``Flask`` class object.
    """
    server = ClothobserveServer('clothobserve', root_path=root_path)
    server.config.from_object(config_object)
    server.wsgi_app = ProxyFix(server.wsgi_app, num_proxies=1)
    MONGO_DB.init_app(server)
    MAIL.init_app(server)
    Security(server, USER_DATASTORE)
    server.start_scheduler()

    return server

class Config(object): # pylint: disable=too-few-public-methods
    """
    Base class for configuration.
    Most of default configuration is for production.
    """
    #: Config type is useful for debug purposes
    #: (*to determine, what configuration is used*).
    CONFIG_TYPE = 'base'
    #: Debug is turned off in production for security reasons.
    DEBUG = False
    #: Testing is turned off in production for security reasons.
    TESTING = False
    #: Secret key should be at least 32 characters long and as random as possible.
    SECRET_KEY = 'not-secret-enough'
    #: Are ReCAPTCHA checks turned on.
    RECAPTCHA = True
    #: MongoDB database named clothobserve, it should be already created.
    MONGODB_DB = 'clothobserve'
    #: Host IP from Docker container perspective
    #: (*on production server MongoDB server is installed directly on server*).
    MONGODB_HOST = '172.17.0.1'
    #: Port 27017 is default and should be changed to random number in production.
    MONGODB_PORT = 27017
    #: User with *readWrite* and *dbAdmin* privileges for clothobserve database
    #: (**dbOwner privilege is bad for security**).
    MONGODB_USERNAME = 'clothobserveadmin'
    #: Default MongoDB password, should be changed to random in production.
    MONGODB_PASSWORD = 'clothobserveadmin'
    #: Sending mail is suppressed by default, because it is only used in production.
    MAIL_SUPPRESS_SEND = False
    #: Default sender of mail, can be overriden.
    MAIL_DEFAULT_SENDER = 'Clothobserve <noreply@clothobserve.com>'
    #: Clothobserve server uses TLS to secure mail.
    MAIL_USE_TLS = True
    #: Host IP from Docker container perspective
    #: (*on production server mail server is installed directly on server*).
    MAIL_SERVER = '172.17.0.1'
    #: For secure passwords PBKDF2_SHA512 algorithm is used for hashing.
    #: It gives the best result on 64-bit server.
    SECURITY_PASSWORD_HASH = 'pbkdf2_sha512'
    #: Hashing schemes have only PBKDF2_SHA512 algorithm,
    #: since this is the only thing we use for password hashing.
    SECURITY_HASHING_SCHEMES = ['pbkdf2_sha512']
    #: Deprecated hashing schemes are empty, because we don't use MD5 or SHA1 anyway.
    SECURITY_DEPRECATED_HASHING_SCHEMES = []
    #: This flag is set to True, because Flask-Security
    #: unnecessary salts password twice, second time with salt from config.
    SECURITY_PASSWORD_SINGLE_HASH = True
    #: This flag tells browser to only send this cookie via HTTPS
    #: (*should be used with HTTPS or browsers will ignore Set-Cookie header*).
    SESSION_COOKIE_SECURE = True
    #: This flag tells browser that cookie cannot be retrieved
    #: via Javascript and should only be used in HTTP queries.
    SESSION_COOKIE_HTTPONLY = True
    #: This flag tells browser, that cookie cannot be used
    #: on other sites in requests to our site.
    SESSION_COOKIE_SAMESITE = "Strict"
    #: Session lifetime is set to 2 weeks, as it is the ideal duration.
    REMEMBER_COOKIE_DURATION = 1209600
    #: Session domain is written with dot to use session in subdomains.
    SESSION_COOKIE_DOMAIN = '.clothobserve.com'
    #: We enable tracking of users logins,
    #: as this information can be useful for security.
    SECURITY_TRACKABLE = True

class ProductionConfig(Config): # pylint: disable=too-few-public-methods
    """Production configuration class."""
    #: Config type is useful for debug purposes
    #: (*to determine, what configuration is used*).
    CONFIG_TYPE = 'production'
    #: Random, 64 symbols long secret key.
    SECRET_KEY = 'long-secret-key'
    #: Random port for MongoDB.
    MONGODB_PORT = 59429
    #: Random password for MongoDB.
    MONGODB_PASSWORD = 'long-secret-key'

class DevelopmentConfig(Config): # pylint: disable=too-few-public-methods
    """Base configuration for development."""
    #: In development environment debug is turned on for better debugging.
    DEBUG = True
    #: Loading of templates is explained for better debugging.
    EXPLAIN_TEMPLATE_LOADING = True
    #: In development environment MongoDB is in Docker container,
    #: so we use name instead of IP.
    MONGODB_HOST = 'mongodb'

class DevelopmentServerConfig(DevelopmentConfig): # pylint: disable=too-few-public-methods
    """
    Configuration for development server,
    which is used for testing features on a special development server.
    """
    #: Config type is useful for debug purposes
    #: (*to determine, what configuration is used*).
    CONFIG_TYPE = 'development-server'
    #: Random, 64 symbols long secret key.
    SECRET_KEY = 'long-secret-key'

class DevelopmentLocalConfig(DevelopmentConfig): # pylint: disable=too-few-public-methods
    """
    Configuration for local development,
    which is used for testing features locally.
    """
    #: Config type is useful for debug purposes
    #: (*to determine, what configuration is used*).
    CONFIG_TYPE = 'development-local'
    #: Random, 64 symbols long secret key.
    SECRET_KEY = 'long-secret-key'
    #: Bad request errors are trapped for better debugging.
    TRAP_BAD_REQUEST_ERRORS = True
    #: HTTP exceptions (errors) are trapped for better debugging.
    TRAP_HTTP_EXCEPTIONS = True
    #: Sending mail is suppressed, because
    #: local development environment should not send mail.
    MAIL_SUPPRESS_SEND = True
    #: Local development environment does not has domain name,
    #: so for cookies 127.0.0.1 is used.
    SESSION_COOKIE_DOMAIN = '127.0.0.1'
    #: Local development environment is
    #: not using HTTPS connection, so ``Secure`` flag is not set.
    SESSION_COOKIE_SECURE = False

class TestingConfig(Config): # pylint: disable=too-few-public-methods
    """Configuration for running tests (unittest & coverage)."""
    #: Config type is useful for debug purposes
    #: (*to determine, what configuration is used*).
    CONFIG_TYPE = 'testing'
    #: In testing environment debug is turned on for better debugging.
    DEBUG = True
    #: In testing environment testing is turned on for better debugging.
    TESTING = True
    #: Random, 64 symbols long secret key.
    SECRET_KEY = 'long-secret-key'
    #: In testing environment ReCAPTCHA checks turned off.
    RECAPTCHA = False
    #: Bad request errors are trapped for better debugging.
    TRAP_BAD_REQUEST_ERRORS = True
    #: HTTP exceptions (errors) are trapped for better debugging.
    TRAP_HTTP_EXCEPTIONS = True
    #: Loading of templates is explained for better debugging.
    EXPLAIN_TEMPLATE_LOADING = True
    #: In testing environment MongoDB is in Docker container,
    #: so we use name instead of IP.
    MONGODB_HOST = 'mongodb'
    #: Sending mail is suppressed, because
    #: testing environment should not send mail.
    MAIL_SUPPRESS_SEND = True
    #: Testing environment does not has domain name,
    #: so for cookies 127.0.0.1 is used.
    SESSION_COOKIE_DOMAIN = '127.0.0.1'
    #: Local development environment is
    #: not using HTTPS connection, so ``Secure`` flag is not set.
    SESSION_COOKIE_SECURE = False