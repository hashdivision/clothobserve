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
from data.constants.responses.user_profile import PROFILE_NOT_FOUND

#: Blueprint of this profile module.
PROFILE_BP = Blueprint("profile", __name__)

@PROFILE_BP.route("/")
@login_required(silent=True)
def root_profile_endpoint() -> Response:
    """
    # TODO: Fill this docstring.
    """
    user = User.find_by_email(current_user.email)
    return Profile.find_by_user(user).to_response_json()

@PROFILE_BP.route("/user/<username>")
@login_required(silent=True)
def user_endpoint(username: str) -> Response:
    """
    # TODO: Fill this docstring.
    """
    user = User.find_by_username(username)
    if user:
        profile = Profile.find_public_by_user(user)
        if profile:
            return profile.to_response_json()

    return PROFILE_NOT_FOUND
