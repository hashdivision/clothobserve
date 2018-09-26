"""
    clothobserve.data.constants.responses.user_profile
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Constant responses for /account/profile/ endpoints.

    :copyright: © 2018 HashDivision OU.

    :license: Apache License 2.0, see *LICENSE* for more details.

    |

"""
from flask import Response
from flask_api import status

#: Response for user profile search that was unsuccessful.
PROFILE_NOT_FOUND = Response("Profile Not Found", status=status.HTTP_404_NOT_FOUND)
#: Response for profile which visibility is public.
PUBLIC = Response("public", status=status.HTTP_200_OK)
#: Response for profile which visibility is private.
PRIVATE = Response("private", status=status.HTTP_200_OK)
