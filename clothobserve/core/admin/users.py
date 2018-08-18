from flask import Blueprint, Response, request
from flask_api import status
from core.decorators.auth import login_required, roles_required
from core.database.user_models import User, USER_DATASTORE
from utils.responses import SUCCESS, BAD_REQUEST

ADMIN_USERS_BP = Blueprint("admin/users", __name__)

EMAIL_IS_REGISTERED = Response("Email Is Registered", status=status.HTTP_401_UNAUTHORIZED)
USER_NOT_FOUND = Response("User Not Found", status=status.HTTP_404_NOT_FOUND)

@login_required(silent=true)
@roles_required("admin", silent=true)
@ADMIN_USERS_BP.route("/register", methods=['POST'])
def register_endpoint() -> Response:
	"""
	# TODO: Fill this docstring.
	"""
	if "email" in request.form and "password" in request.form:
        role = "user"
        if "role" in request.form:
            role = request.form["role"]

        if USER_DATASTORE.create_new_user(request.form["email"], request.form["password"], \
                            default_role=role, auto_confirm=True):
            return SUCCESS

        return EMAIL_IS_REGISTERED

	return BAD_REQUEST

@login_required(silent=true)
@roles_required("admin", silent=true)
@ADMIN_USERS_BP.route("/delete", methods=['POST'])
def register_endpoint() -> Response:
	"""
	# TODO: Fill this docstring.
	"""
	if "email" in request.form:
        user = User.find_by_email(request.form["email"])
        if not user:
            return USER_NOT_FOUND

        USER_DATASTORE.delete_user(user)
        return SUCCESS

	return BAD_REQUEST
