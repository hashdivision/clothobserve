"""
    clothobserve.endpoints.user.password
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Password related endpoints for account (``/account/password/``).

    :copyright: © 2018 HashDivision OU.

    :license: Apache License 2.0, see *LICENSE* for more details.

    |

"""
from flask import Blueprint, Response, request, abort
from flask_security.core import current_user
from endpoints.decorators.auth import login_required, anonymous_required
from endpoints.decorators.data import form_required, form_fields_max_length
from data.constants.responses.user_password import CHANGE_SUCCESS, WRONG_OLD_PASSWORD, \
    CHECK_EMAIL
from logic.user.datastore import USER_DATASTORE
from logic.user.password import send_restoration_link

#: Blueprint of this password module.
PASSWORD_BP = Blueprint("password", __name__)

@PASSWORD_BP.route("/restore", methods=['POST'])
@anonymous_required
@form_required("email")
@form_fields_max_length(email=255)
def restore_send_link_endpoint() -> Response:
    """
    Password restore POST endpoint (**/account/password/restore**)
    for sending restoration link to email.
    You MUST not be logged in to use it.

    Returns:
        Success (200 OK): Check Your Email.
        Fail (404 NOT FOUND): if logged in user uses this endpoint.
        Fail (400 BAD REQUEST): if form does not contain email.
        Fail (413 REQUEST ENTITY TOO LARGE): if form fields have wrong length.
    """
    send_restoration_link(request.form["email"])
    return CHECK_EMAIL


@PASSWORD_BP.route("/restore/<token>", methods=['POST'])
@anonymous_required
@form_required("new_password")
@form_fields_max_length(new_password=255)
def restore_set_new_endpoint(token: str) -> Response:
    """
    Password restore POST endpoint (**/account/password/restore/<token>**)
    for setting new password securely.
    You MUST not be logged in to use it.

    Returns:
        Success (200 OK): ?.
        Fail (404 NOT FOUND): if logged in user uses this endpoint.
        Fail (400 BAD REQUEST): if form does not contain new_password.
        Fail (413 REQUEST ENTITY TOO LARGE): if form fields have wrong length.
    """
    abort(501)

@PASSWORD_BP.route("/change", methods=['POST'])
@login_required(silent=True)
@form_required("old_password", "new_password")
@form_fields_max_length(old_password=255, new_password=255)
def change_endpoint() -> Response:
    """
    Password change POST endpoint (**/account/password/change**)
    for changing old password.
    You MUST be logged in to use it.

    Returns:
        Success (200 OK): Password Changed.
        Fail (403 FORBIDDEN): Wrong Old Password
        Fail (404 NOT FOUND): if not logged in user uses this endpoint.
        Fail (400 BAD REQUEST): if form does not contain old_password or new_password.
        Fail (413 REQUEST ENTITY TOO LARGE): if form fields have wrong length.
    """
    if USER_DATASTORE.change_user_password(current_user, request.form["old_password"], \
                                            request.form["new_password"]):
        return CHANGE_SUCCESS

    return WRONG_OLD_PASSWORD
