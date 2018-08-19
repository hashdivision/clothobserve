from flask import Blueprint, Response, request, current_app
from flask_security.core import current_user
from flask_security.utils import logout_user, login_user, verify_password
from flask_api import status
from core.database.user_models import User, USER_DATASTORE
from utils.responses import SUCCESS, BAD_REQUEST, NOT_FOUND

ACCOUNT_BP = Blueprint("account", __name__)

EMAIL_IS_REGISTERED = Response("Email Is Registered", status=status.HTTP_401_UNAUTHORIZED)
USER_INACTIVE = Response("User Is Inactive", status=status.HTTP_403_FORBIDDEN)
WRONG_CREDENTIALS = Response("Wrong Credentials", status=status.HTTP_401_UNAUTHORIZED)

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
            return SUCCESS

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
                return SUCCESS

            return USER_INACTIVE

        return WRONG_CREDENTIALS

    return BAD_REQUEST


@ACCOUNT_BP.route("/logout")
def logout_endpoint() -> Response:
    """
    # TODO: Fill this docstring.
    """
    if current_user.is_authenticated:
        logout_user()
        return SUCCESS
	
    return NOT_FOUND
