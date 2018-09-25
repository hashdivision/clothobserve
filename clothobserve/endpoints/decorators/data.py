"""
    clothobserve.endpoints.decorators.data
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Module for data decorators. To ensure endpoints get data from request.

    :copyright: © 2018 HashDivision OU.

    :license: Apache License 2.0, see *LICENSE* for more details.

    |

"""
from functools import wraps
from flask import request
from data.constants.responses.decorators_data import BAD_FORM, \
    LARGE_FIELD_LENGTH

def form_required(*form_keys):
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
                    return BAD_FORM

            return function(*args, **kwargs)

        return decorated_view

    return wrapper

def form_fields_max_length(**form_fields_length):
    """
    Decorator for endpoints that have maximum length
    for form fields which should not be exceeded.
    413 HTTP code is sent if one of fields has not appropriate length.
    """
    def wrapper(function): # pylint: disable=missing-docstring
        @wraps(function)
        def decorated_view(*args, **kwargs): # pylint: disable=missing-docstring
            for key, value in form_fields_length.items():
                if len(request.form[key]) > value:
                    return LARGE_FIELD_LENGTH

            return function(*args, **kwargs)

        return decorated_view

    return wrapper
