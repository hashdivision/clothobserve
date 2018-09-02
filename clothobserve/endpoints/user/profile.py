"""
    clothobserve.endpoints.user.profile
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # TODO: Fill this docstring.

    :copyright: © 2018 HashDivision OU.

    :license: Apache License 2.0, see *LICENSE* for more details.

    |

"""
from flask import Blueprint, Response
from flask_security.core import current_user
from endpoints.decorators.auth import login_required
from data.models.user import User, Profile
from data.constants.responses.user_profile import PROFILE_NOT_FOUND, \
    VISIBILITY_CHANGE_SUCCESS
from logic.user.datastore import USER_DATASTORE

#: Blueprint of this profile module.
PROFILE_BP = Blueprint("profile", __name__)

@PROFILE_BP.route("/")
@login_required(silent=True)
def root_profile_endpoint() -> Response:
    """
    # TODO: Fill this docstring.
    """
    return current_user.profile.to_response_json()

@PROFILE_BP.route("/user/<username>")
@login_required(silent=True)
def user_endpoint(username: str) -> Response:
    """
    # TODO: Fill this docstring.
    """
    user = User.find_by_username(username)
    if user and user.profile.public:
        return user.profile.to_response_json()

    return PROFILE_NOT_FOUND

@PROFILE_BP.route("/visibility/<int:state>")
@login_required(silent=True)
def visibility_endpoint(state: int) -> Response:
    """
    # TODO: Fill this docstring.
    """
    USER_DATASTORE.change_profile_visibility(current_user, public=bool(state))
    return VISIBILITY_CHANGE_SUCCESS
