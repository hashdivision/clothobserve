"""
    clothobserve.data.constants.responses.decorators_data
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Constant responses for data related decorators.

    :copyright: © 2018 HashDivision OU.

    :license: Apache License 2.0, see *LICENSE* for more details.

    |

"""
from flask import Response
from flask_api import status

#: Response for case when form does not have needed fields.
BAD_FORM = Response("Bad Form", status=status.HTTP_400_BAD_REQUEST)
#: Response for case when form field maximum length is exceeded.
LARGE_FIELD_LENGTH = Response("Large Field Length", status=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE)
