"""
    clothobserve.data.constants.responses.generic
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # TODO: Fill this docstring.

    :copyright: © 2018 HashDivision OU.

    :license: Apache License 2.0, see *LICENSE* for more details.

    |

"""
from flask import Response
from flask_api import status

#: # TODO: Fill this docstring.
BAD_REQUEST = Response("Bad Request", status=status.HTTP_400_BAD_REQUEST)
#: # TODO: Fill this docstring.
NOT_FOUND = Response("Not Found", status=status.HTTP_404_NOT_FOUND)
