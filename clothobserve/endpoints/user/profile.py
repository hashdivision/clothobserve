"""
    clothobserve.endpoints.user.profile
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # TODO: Fill this docstring.

    :copyright: © 2018 HashDivision OU.

    :license: Apache License 2.0, see *LICENSE* for more details.

    |

"""
from flask import Blueprint, Response, abort
from flask_security.core import current_user
from endpoints.decorators.auth import login_required
from endpoints.decorators.data import form_required, form_fields_max_length
from data.models.user import User
from data.constants.responses.user_profile import PROFILE_NOT_FOUND, \
    PUBLIC, PRIVATE
from logic.user.datastore import USER_DATASTORE

#: Blueprint of this profile module.
PROFILE_BP = Blueprint("profile", __name__)

@PROFILE_BP.route("/")
@login_required(silent=True)
def own_profile_endpoint() -> Response:
    """
    # TODO: Fill this docstring.
    """
    return current_user.create_profile_json()

@PROFILE_BP.route("/user/<username>")
@login_required(silent=True)
def user_endpoint(username: str) -> Response:
    """
    # TODO: Fill this docstring.
    """
    user = User.find_by_username(username)
    if user and user.profile.public:
        return user.create_profile_json()

    return PROFILE_NOT_FOUND

@PROFILE_BP.route("/visibility")
@login_required(silent=True)
def visibility_endpoint() -> Response:
    """
    # TODO: Fill this docstring.
    """
    return PUBLIC if current_user.profile.public else PRIVATE

@PROFILE_BP.route("/visibility/<int:state>", methods=['POST'])
@login_required(silent=True)
def visibility_change_endpoint(state: int) -> Response:
    """
    # TODO: Fill this docstring.
    """
    USER_DATASTORE.change_profile_visibility(current_user, public=bool(state))
    return PUBLIC if state else PRIVATE

@PROFILE_BP.route("/change", methods=['POST'])
@login_required(silent=True)
@form_required("name", "date_of_birth", "about_me", "username")
@form_fields_max_length(name=64, date_of_birth=24, about_me=200, username=32)
def profile_change_endpoint() -> Response:
    """
    # TODO: Fill this docstring.
    """
    abort(501)
