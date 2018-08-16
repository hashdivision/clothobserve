from flask import Blueprint, Response, request, current_app
from flask_security.core import current_user
from flask_security.utils import logout_user, verify_password
from flask_api import status
from core.database.user_models import User, USER_DATASTORE

ACCOUNT_BP = Blueprint("account", __name__)

SIGNED_IN = Response(status=status.HTTP_204_NO_CONTENT)
USER_INACTIVE = Response("User Is Inactive", status=status.HTTP_403_FORBIDDEN)
WRONG_CREDENTIALS = Response("Wrong Credentials", status=status.HTTP_401_UNAUTHORIZED)
SIGNIN_SUCCESS = Response("User Signed In", status=status.HTTP_200_OK)
SIGNIN_BAD_REQUEST = Response("Bad Request", status=status.HTTP_400_BAD_REQUEST)

NOT_FOUND = Response ("Not Found", status=status.HTTP_404_NOT_FOUND)
CAPTCHA_FAIL = Response ("Captcha fail", status=status.HTTP_401_UNAUTHORIZED)
REGISTRATION_SUCCESSFUL = Response("Registered Successfully", status=status.HTTP_200_OK)
EMAIL_IS_REGISTERED = Response("Email Is Already Registered", status=status.HTTP_401_UNAUTHORIZED)
REGISTRATION_BAD_REQUEST = Response("Bad Request", status=status.HTTP_400_BAD_REQUEST)

LOGOUT_SUCCESS = Response("Logout Success", status=status.HTTP_200_OK)
LOGOUT_FAIL = Response("Logout Fail", status=status.HTTP_401_UNAUTHORIZED)

@ACCOUNT_BP.route("/register", methods=['POST'])
def register_endpoint() -> Response:
	"""
	# TODO: Fill this docstring.
	"""
	if current_user.is_authenticated:
		return NOT_FOUND

	if not current_app.config['RECAPTCHA'] or "g-recaptcha-response" in request.form:
        if current_app.config['RECAPTCHA'] and \
            not is_recaptcha_passed(request.form["g-recaptcha-response"]):
            return CAPTCHA_FAIL # pragma: no cover 
		
		if "email" in request.form and "password" in request.form:
            if create_new_user(request.form["email"], request.form["password"]):
                user = User.find_by_email(request.form["email"])
                send_confirmation_link(user)
                login_user(user, remember=True)
                return REGISTRATION_SUCCESSFUL

            return EMAIL_IS_REGISTERED
	
	return REGISTRATION_BAD_REQUEST


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
