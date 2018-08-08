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
import os
from flask import Flask
from werkzeug.contrib.fixers import ProxyFix

def create_server() -> Flask:
    """Creates and initializes ``Flask`` server.

    Configuration is loaded from class (path to it should be
    in environment variable CONFIG_OBJECT), which should be
    subclassed from ``Config`` class.
    Configuration in HTTP proxy environment (``ProxyFix``) is done
    because original Clothobserve app is behind the proxy.

    Returns:
        The ``Flask`` class object.
    """
    root_path = os.getenv('ROOT_PATH', '/clothobserve/')
    config_object = os.getenv('CONFIG_OBJECT', 'configs.config.DevelopmentLocalConfig')

    server = Flask('clothobserve', root_path=root_path)
    server.config.from_object(config_object)
    server.wsgi_app = ProxyFix(server.wsgi_app, num_proxies=1)

    return server

class Config(): # pylint: disable=too-few-public-methods
    """
    Base class for configuration.
    Most of configuration is customizable.
    """
    #: Secret key should be at least 32 characters long and as random as possible.
    SECRET_KEY = os.getenv('SECRET_KEY', 'not-secret-enough-change-me-please')
    #: MongoDB database name (default - clothobserve), it should be already created.
    MONGODB_DB = os.getenv('MONGODB_DB', 'clothobserve')
    #: MongoDB host (default - mongodb).
    MONGODB_HOST = os.getenv('MONGODB_HOST', 'mongodb')
    #: MongoDB port  (default - 27017, **should be changed to random number in production**).
    MONGODB_PORT = int(os.getenv('MONGODB_PORT', '27017'))
    #: MongoDB user with *readWrite* and *dbAdmin* privileges for clothobserve database
    #: (**dbOwner privilege is bad for security**).
    MONGODB_USERNAME = os.getenv('MONGODB_USERNAME', 'clothobserveadmin')
    #: MongoDB password for MONGODB_USERNAME user.
    #: **Should be long and random in production**.
    MONGODB_PASSWORD = os.getenv('MONGODB_PASSWORD', 'clothobserveadmin')
    #: Sending mail is suppressed by default.
    MAIL_SUPPRESS_SEND = (os.getenv('MAIL_SUPPRESS_SEND', 'true') == 'true')
    #: Default sender of mail.
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_SENDER', 'Clothobserve <noreply@example.com>')
    #: Clothobserve server uses TLS to secure mail.
    MAIL_USE_TLS = True
    #: SMTP server (*example: Postfix*) host (default - host from Docker perspective).
    MAIL_SERVER = os.getenv('MAIL_SERVER', '172.17.0.1')
    #: For secure passwords PBKDF2_SHA512 algorithm is used for hashing.
    #: It gives the best result on 64-bit server.
    SECURITY_PASSWORD_HASH = 'pbkdf2_sha512'
    #: Hashing schemes have only PBKDF2_SHA512 algorithm,
    #: since this is the only thing we use for password hashing.
    SECURITY_HASHING_SCHEMES = ['pbkdf2_sha512']
    #: Deprecated hashing schemes are empty, because we don't use MD5 or SHA1 anyway.
    SECURITY_DEPRECATED_HASHING_SCHEMES = []
    #: Flask-Security unnecessary salts password twice, second time with salt from config.
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
    SESSION_COOKIE_DOMAIN = os.getenv('COOKIE_DOMAIN', '.example.com')
    #: We enable tracking of users logins,
    #: as this information can be useful for security.
    SECURITY_TRACKABLE = True

class ProductionConfig(Config): # pylint: disable=too-few-public-methods
    """Production configuration class."""
    #: Config type is useful for debug purposes
    #: (*to determine, what configuration is used*).
    CONFIG_TYPE = 'production'
    #: Debug is turned off in production for security reasons.
    DEBUG = False
    #: Testing is turned off in production for security reasons.
    TESTING = False

class DevelopmentConfig(Config): # pylint: disable=too-few-public-methods
    """Base configuration for development."""
    #: Debug in Development environment turned on by default.
    DEBUG = (os.getenv('DEV_DEBUG', 'true') == 'true')
    #: Testing in Development environment turned on by default.
    TESTING = (os.getenv('DEV_TESTING', 'true') == 'true')
    #: Loading of templates is explained for better debugging.
    EXPLAIN_TEMPLATE_LOADING = True

class DevelopmentServerConfig(DevelopmentConfig): # pylint: disable=too-few-public-methods
    """
    Configuration for development server.
    """
    #: Config type is useful for debug purposes
    #: (*to determine, what configuration is used*).
    CONFIG_TYPE = 'development-server'

class DevelopmentLocalConfig(DevelopmentConfig): # pylint: disable=too-few-public-methods
    """
    Configuration for local development,
    which is used for testing features locally.
    """
    #: Config type is useful for debug purposes
    #: (*to determine, what configuration is used*).
    CONFIG_TYPE = 'development-local'
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
    #: Bad request errors are trapped for better debugging.
    TRAP_BAD_REQUEST_ERRORS = True
    #: HTTP exceptions (errors) are trapped for better debugging.
    TRAP_HTTP_EXCEPTIONS = True
    #: Loading of templates is explained for better debugging.
    EXPLAIN_TEMPLATE_LOADING = True
    #: Sending mail is suppressed, because
    #: testing environment should not send mail.
    MAIL_SUPPRESS_SEND = True
    #: Testing environment does not has domain name,
    #: so for cookies 127.0.0.1 is used.
    SESSION_COOKIE_DOMAIN = '127.0.0.1'
    #: Local development environment is
    #: not using HTTPS connection, so ``Secure`` flag is not set.
    SESSION_COOKIE_SECURE = False
