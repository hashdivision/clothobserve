"""
    clothobserve.data.constants.responses.user_profile
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # TODO: Fill this docstring.

    :copyright: © 2018 HashDivision OU.

    :license: Apache License 2.0, see *LICENSE* for more details.

    |

"""
from flask import Response
from flask_api import status

#: Response for user profile search that was unsuccessful.
PROFILE_NOT_FOUND = Response("Profile Not Found", status=status.HTTP_404_NOT_FOUND)
#: Response for successful profile visibility change.
VISIBILITY_CHANGE_SUCCESS = Response("Visibility Changed", status=status.HTTP_200_OK)
