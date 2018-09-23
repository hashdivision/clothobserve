"""
    clothobserve.endpoints.user.account
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Auth related endpoints for account.

    :copyright: © 2018 HashDivision OU.

    :license: Apache License 2.0, see *LICENSE* for more details.

    |

"""
from flask import Blueprint, Response, request, abort
from flask_security.utils import login_user, logout_user, verify_password
from endpoints.decorators.auth import login_required, anonymous_required
from endpoints.decorators.data import form_required, form_fields_max_length
from data.models.user import User
from data.constants.responses.user_account import EMAIL_IS_REGISTERED, \
    USER_INACTIVE, WRONG_CREDENTIALS, LOGGED_OUT
from logic.user.datastore import USER_DATASTORE

#: Blueprint of this account module.
ACCOUNT_BP = Blueprint("account", __name__)

@ACCOUNT_BP.route("/register", methods=['POST'])
@anonymous_required
@form_required("email", "password")
@form_fields_max_length(email=255, password=255)
def register_endpoint() -> Response:
    """
    Registration POST endpoint (**/account/register**) for account registration.
    You MUST not be logged in to use it.
    Requires form data:
    - email
    - password

    Returns:
        Success (200 OK): JSON string with username.
        Fail (401 UNAUTHORIZED): Email Is Registered.
        Fail (404 NOT FOUND): if logged in user uses this endpoint.
        Fail (400 BAD REQUEST): if form does not contain email and password
        Fail (413 REQUEST ENTITY TOO LARGE): if form fields have wrong length.
    """
    user = USER_DATASTORE.create_new_user(request.form["email"], request.form["password"])
    if user:
        login_user(user, remember=True)
        return '{"username":"' + user.username + '"}'

    return EMAIL_IS_REGISTERED

@ACCOUNT_BP.route("/signin", methods=['POST'])
@anonymous_required
@form_required("email", "password")
@form_fields_max_length(email=255, password=255)
def signin_endpoint() -> Response:
    """
    Sign in POST endpoint (**/account/signin**) for sign in to account.
    You MUST not be logged in to use it.
    Requires form data:
    - email
    - password

    Returns:
        Success (200 OK): JSON string with username.
        Fail (403 FORBIDDEN): User Is Inactive.
        Fail (401 UNAUTHORIZED): Wrong Credentials.
        Fail (404 NOT FOUND): if logged in user uses this endpoint.
        Fail (400 BAD REQUEST): if form does not contain email and password.
        Fail (413 REQUEST ENTITY TOO LARGE): if form fields have wrong length.
    """
    user = User.find_by_email(request.form["email"])
    if user and verify_password(request.form["password"], user.password):
        if user.active:
            login_user(user, remember=True)
            return '{"username":"' + user.username + '"}'

        return USER_INACTIVE

    return WRONG_CREDENTIALS

@ACCOUNT_BP.route("/logout")
@login_required(silent=True)
def logout_endpoint() -> Response:
    """
    Logout GET endpoint (**/account/logout**) for logout.
    You MUST be logged in to use it.

    Returns:
        Success (200 OK): Goodbye.
        Fail (404 NOT FOUND): if not logged in user uses this endpoint.
    """
    logout_user()
    return LOGGED_OUT
