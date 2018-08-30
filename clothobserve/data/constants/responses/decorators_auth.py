"""
    clothobserve.data.constants.responses.decorators_auth
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # TODO: Fill this docstring.

    :copyright: © 2018 HashDivision OU.

    :license: Apache License 2.0, see *LICENSE* for more details.

    |

"""
from flask import Response
from flask_api import status

#: Response for case where user is not logged in while accessing endpoint.
LOGIN_REQUIRED = Response("Login Required", status=status.HTTP_401_UNAUTHORIZED)
#: Response for case where user has no permission (role needed) to access the endpoint.
NO_PERMISSION = Response("No Permission", status=status.HTTP_403_FORBIDDEN)
