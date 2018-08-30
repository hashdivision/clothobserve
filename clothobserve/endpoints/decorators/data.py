"""
    clothobserve.endpoints.decorators.data
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Module for data decorators. To ensure endpoints get data from request.

    :copyright: © 2018 HashDivision OU.

    :license: Apache License 2.0, see *LICENSE* for more details.

    |

"""
from functools import wraps
from flask import abort, request
from flask_api import status

def form_required(*form_keys): # pylint: disable=inconsistent-return-statements
    """
    Decorator for endpoints that require user to
    POST form with keys specified in ``*form_keys``.
    400 HTTP code is sent if one of keys is not in form.
    """
    def wrapper(function): # pylint: disable=missing-docstring
        @wraps(function)
        def decorated_view(*args, **kwargs): # pylint: disable=missing-docstring
            for key in form_keys:
                if not key in request.form:
                    abort(status.HTTP_400_BAD_REQUEST)

            return function(*args, **kwargs)

        return decorated_view

    return wrapper
