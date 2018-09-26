"""
    clothobserve.data.constants.responses.generic
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Generic constant responses.

    :copyright: © 2018 HashDivision OU.

    :license: Apache License 2.0, see *LICENSE* for more details.

    |

"""
from flask import Response
from flask_api import status

#: Generic ``400 Bad Request`` response.
BAD_REQUEST = Response("Bad Request", status=status.HTTP_400_BAD_REQUEST)
#: Generic ``404 Not Found`` response.
NOT_FOUND = Response("Not Found", status=status.HTTP_404_NOT_FOUND)
