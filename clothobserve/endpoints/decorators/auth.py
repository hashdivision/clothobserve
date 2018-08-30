"""
    clothobserve.endpoints.decorators.auth
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Module for custom auth decorators. To ensure endpoints are secured.

    :copyright: © 2018 HashDivision OU.

    :license: Apache License 2.0, see *LICENSE* for more details.

    |

"""
from functools import wraps
from flask import abort
from flask_api import status
from flask_principal import Permission, RoleNeed
from flask_security.core import current_user
from data.constants.responses.decorators_auth import LOGIN_REQUIRED, \
    NO_PERMISSION

def login_required(silent: bool = False): # pylint: disable=inconsistent-return-statements
    """
    Decorator for endpoints that require user to be logged in.
    If silent is set to True - 404 HTTP code is sent if user is not logged in.

    :param silent: should user know that this endpoint
        even exists if he is not logged in.
    """
    def wrapper(function): # pylint: disable=missing-docstring
        @wraps(function)
        def decorated_view(*args, **kwargs): # pylint: disable=missing-docstring
            if not current_user.is_authenticated:
                if silent:
                    abort(status.HTTP_404_NOT_FOUND)

                return LOGIN_REQUIRED

            return function(*args, **kwargs)

        return decorated_view

    return wrapper

def anonymous_required(function): # pylint: disable=inconsistent-return-statements
    """
    Decorator for endpoints that require user not to be logged in.
    404 HTTP code is sent if user is logged in.
    """
    @wraps(function)
    def decorated_view(*args, **kwargs): # pylint: disable=missing-docstring
        if current_user.is_authenticated:
            abort(status.HTTP_404_NOT_FOUND)

        return function(*args, **kwargs)

    return decorated_view

def roles_accepted(*roles, silent: bool = False): # pylint: disable=inconsistent-return-statements
    """
    Decorator for endpoints that require user to
    have one of the roles provided as ``*roles``.
    If silent is set to True - 404 HTTP code
    is sent if user doesn't have any of the roles.

    :param silent: should user know that this endpoint
        even exists if he doesn't have any of the roles.
    """
    def wrapper(function): # pylint: disable=missing-docstring
        @wraps(function)
        def decorated_view(*args, **kwargs): # pylint: disable=missing-docstring
            permission = Permission(*[RoleNeed(role) for role in roles])
            if not permission.can():
                if silent:
                    abort(status.HTTP_404_NOT_FOUND)

                return NO_PERMISSION

            return function(*args, **kwargs)

        return decorated_view

    return wrapper

def roles_required(*roles, silent: bool = False): # pylint: disable=inconsistent-return-statements
    """
    Decorator for endpoints that require user to
    have all of the roles provided as ``*roles``.
    If silent is set to True - 404 HTTP code
    is sent if user doesn't have all of the roles.

    :param silent: should user know that this endpoint
        even exists if he doesn't have all of the roles.
    """
    def wrapper(function): # pylint: disable=missing-docstring
        @wraps(function)
        def decorated_view(*args, **kwargs): # pylint: disable=missing-docstring
            permissions = [Permission(RoleNeed(role)) for role in roles]
            for permission in permissions:
                if not permission.can():
                    if silent:
                        abort(status.HTTP_404_NOT_FOUND)

                    return NO_PERMISSION

            return function(*args, **kwargs)

        return decorated_view

    return wrapper
