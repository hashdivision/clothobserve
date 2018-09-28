"""
    clothobserve.data.constants.responses.user_account
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Constant responses for /account/ endpoints.

    :copyright: © 2018 HashDivision OU.

    :license: Apache License 2.0, see *LICENSE* for more details.

    |

"""
from flask import Response
from flask_api import status

#: Response for users that signed in successfully, but are flagged as inactive.
USER_INACTIVE = Response("User Is Inactive", status=status.HTTP_403_FORBIDDEN)
#: Response for wrong email or password.
WRONG_CREDENTIALS = Response("Wrong Credentials", status=status.HTTP_401_UNAUTHORIZED)
#: Response in case email is already registered.
EMAIL_IS_REGISTERED = Response("Email Is Registered", status=status.HTTP_401_UNAUTHORIZED)
#: Response for successful logging out.
LOGGED_OUT = Response("Goodbye", status=status.HTTP_200_OK)
