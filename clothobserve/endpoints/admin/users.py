"""
    clothobserve.endpoints.admin.users
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # TODO: Fill this docstring.

    :copyright: © 2018 HashDivision OU.

    :license: Apache License 2.0, see *LICENSE* for more details.

    |

"""
from flask import Blueprint, Response, request
from flask_api import status
from endpoints.decorators.auth import login_required, roles_required
from data.models.user import User
from data.constants.responses.generic import BAD_REQUEST
from logic.user.datastore import USER_DATASTORE

ADMIN_USERS_BP = Blueprint("admin/users", __name__)

EMAIL_IS_REGISTERED = Response("Email Is Registered", status=status.HTTP_401_UNAUTHORIZED)
USER_NOT_FOUND = Response("User Not Found", status=status.HTTP_404_NOT_FOUND)
USER_DELETED = Response("User Deleted", status=status.HTTP_200_OK)

@ADMIN_USERS_BP.route("/register", methods=['POST'])
@login_required(silent=True)
@roles_required("admin", silent=True)
def register_endpoint() -> Response:
    """
    # TODO: Fill this docstring.
    """
    if "email" in request.form and "password" in request.form:
        user = USER_DATASTORE.create_new_user(request.form["email"], request.form["password"]):
        if user:
            return '{"username":' + user.username'"}'

        return EMAIL_IS_REGISTERED

    return BAD_REQUEST

@ADMIN_USERS_BP.route("/delete", methods=['POST'])
@login_required(silent=True)
@roles_required("admin", silent=True)
def delete_endpoint() -> Response:
    """
    # TODO: Fill this docstring.
    """
    if "email" in request.form:
        user = User.find_by_email(request.form["email"])
        if not user:
            return USER_NOT_FOUND

        USER_DATASTORE.delete_user(user)
        return USER_DELETED

    return BAD_REQUEST
