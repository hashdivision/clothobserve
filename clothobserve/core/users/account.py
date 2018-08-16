from flask import Blueprint, Response, request
from flask_security.core import current_user
from flask_security.utils import logout_user, verify_password
from flask_api import status
from core.database.user_models import User

ACCOUNT_BP = Blueprint("account", __name__)

SIGNED_IN = Response(status=status.HTTP_204_NO_CONTENT)
USER_INACTIVE = Response("User Is Inactive", status=status.HTTP_403_FORBIDDEN)
WRONG_CREDENTIALS = Response("Wrong Credentials", status=status.HTTP_401_UNAUTHORIZED)
SIGNIN_SUCCESS = Response("User Signed In", status=status.HTTP_200_OK)
SIGNIN_BAD_REQUEST = Response("Bad Request", status=status.HTTP_400_BAD_REQUEST)

LOGOUT_SUCCESS = Response("Logout Success", status=status.HTTP_200_OK)
LOGOUT_FAIL = Response("Logout Fail", status=status.HTTP_401_UNAUTHORIZED)

@ACCOUNT_BP.route("/signin", methods=['POST'])
def signin_endpoint() -> Response:
    if current_user.is_authenticated:
        return SIGNED_IN

    if "email" in request.form and "password" in request.form:
        user = User.find_by_email(request.form["email"])
        if user and verify_password(request.form["password"], user.password):
            if user.active:
                login_user(user, remember=True)
                return SIGNIN_SUCCESS

            return USER_INACTIVE

        return WRONG_CREDENTIALS

    return SIGNIN_BAD_REQUEST


@ACCOUNT_BP.route("/logout")
def logout_endpoint() -> Response:
	if current_user.is_authenticated:
		logout_user()
		return LOGOUT_SUCCESS
	
	return LOGOUT_FAIL
