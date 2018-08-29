"""
    clothobserve.endpoints.user.account
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # TODO: Fill this docstring.

    :copyright: © 2018 HashDivision OU.

    :license: Apache License 2.0, see *LICENSE* for more details.

    |

"""
from flask import Blueprint, Response, request
from flask_security.core import current_user
from flask_security.utils import login_user, logout_user, verify_password
from endpoints.decorators.auth import login_required
from data.models.user import User
from data.constants.responses.generic import NOT_FOUND, BAD_REQUEST
from data.constants.responses.user_account import EMAIL_IS_REGISTERED, \
    USER_INACTIVE, WRONG_CREDENTIALS, LOGGED_OUT
from logic.user.datastore import USER_DATASTORE

#: Blueprint of this authentication module.
ACCOUNT_BP = Blueprint("account", __name__)

@ACCOUNT_BP.route("/register", methods=['POST'])
def register_endpoint() -> Response:
    """
    # TODO: Fill this docstring.
    """
    if current_user.is_authenticated:
        return NOT_FOUND

    if "email" in request.form and "password" in request.form:
        if USER_DATASTORE.create_new_user(request.form["email"], request.form["password"]):
            user = User.find_by_email(request.form["email"])
            login_user(user, remember=True)
            return '{"username":"' + user.username + '"}'

        return EMAIL_IS_REGISTERED

    return BAD_REQUEST

@ACCOUNT_BP.route("/signin", methods=['POST'])
def signin_endpoint() -> Response:
    """
    # TODO: Fill this docstring.
    """
    if current_user.is_authenticated:
        return NOT_FOUND

    if "email" in request.form and "password" in request.form:
        user = User.find_by_email(request.form["email"])
        if user and verify_password(request.form["password"], user.password):
            if user.active:
                login_user(user, remember=True)
                return '{"username":"' + user.username + '"}'

            return USER_INACTIVE

        return WRONG_CREDENTIALS

    return BAD_REQUEST

@ACCOUNT_BP.route("/logout")
@login_required(silent=True)
def logout_endpoint() -> Response:
    """
    # TODO: Fill this docstring.
    """
    logout_user()
    return LOGGED_OUT
