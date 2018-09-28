"""
    clothobserve.data.constants.responses.user_email
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Constant responses for /account/email/ endpoints.

    :copyright: © 2018 HashDivision OU.

    :license: Apache License 2.0, see *LICENSE* for more details.

    |

"""
from flask import Response
from flask_api import status

#: Response for successful confirmation of email.
CONFIRMATION_SUCCESS = Response("Email Confirmed", status=status.HTTP_200_OK)
