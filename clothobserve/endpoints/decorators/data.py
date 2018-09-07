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

def form_fields_max_length(**form_fields_length): # pylint: disable=inconsistent-return-statements
    """
    Decorator for endpoints that have maximum length
    for form fields which should not be exceeded.
    400 HTTP code is sent if one of fields has not appropriate length.
    """
    def wrapper(function): # pylint: disable=missing-docstring
        @wraps(function)
        def decorated_view(*args, **kwargs): # pylint: disable=missing-docstring
            for key, value in form_fields_length.items():
                if len(request.form[key]) > value:
                    abort(status.HTTP_413_REQUEST_ENTITY_TOO_LARGE)

            return function(*args, **kwargs)

        return decorated_view

    return wrapper
