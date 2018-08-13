from flask import Blueprint, Response, abort
from flask_security.core import current_user
from flask_security.utils import logout_user
from flask_api import status

ACCOUNT_BP = Blueprint("account", __name__)

LOGOUT_SUCCESS = Response("Logout Success", status=status.HTTP_200_OK)
LOGOUT_FAIL = Response("Logout Fail", status=status.HTTP_401_UNAUTHORIZED)

@ACCOUNT_BP.route("/logout")
def logout_endpoint():
	if current_user.is_authenticated:
		logout_user()
		return LOGOUT_SUCCESS
	
	return LOGOUT_FAIL
