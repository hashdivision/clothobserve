"""
    clothobserve.data.constants.responses.user_password
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Constant responses for /account/password/ endpoints.

    :copyright: © 2018 HashDivision OU.

    :license: Apache License 2.0, see *LICENSE* for more details.

    |

"""
from flask import Response
from flask_api import status

#: Response for attempt to change password with wrong old password.
WRONG_OLD_PASSWORD = Response("Wrong Old Password", status=status.HTTP_403_FORBIDDEN)
#: Response for successful change of password.
CHANGE_SUCCESS = Response("Password Changed", status=status.HTTP_200_OK)
#: Response for attempt to send restoration link to email.
CHECK_EMAIL = Response("Check Your Email", status=status.HTTP_200_OK)
