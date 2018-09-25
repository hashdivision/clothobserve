"""
    clothobserve.endpoints.user.account
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Password related endpoints for account.

    :copyright: © 2018 HashDivision OU.

    :license: Apache License 2.0, see *LICENSE* for more details.

    |

"""
from flask import Blueprint, Response, request, abort
from flask_security.core import current_user
from endpoints.decorators.auth import login_required, anonymous_required
from endpoints.decorators.data import form_required, form_fields_max_length
from data.constants.responses.user_password import CHANGE_SUCCESS, WRONG_OLD_PASSWORD
from logic.user.datastore import USER_DATASTORE

#: Blueprint of this password module.
PASSWORD_BP = Blueprint("password", __name__)

@PASSWORD_BP.route("/restore", methods=['POST'])
@anonymous_required
@form_required("email")
@form_fields_max_length(email=255)
def restore_send_link_endpoint() -> Response:
    """
    # TODO: Fill this docstring.
    """
    abort(501)

@PASSWORD_BP.route("/restore/<token>", methods=['POST'])
@anonymous_required
@form_required("new_password")
@form_fields_max_length(new_password=255)
def restore_set_new_endpoint(token: str) -> Response:
    """
    # TODO: Fill this docstring.
    """
    abort(501)

@PASSWORD_BP.route("/change", methods=['POST'])
@login_required(silent=True)
@form_required("old_password", "new_password")
@form_fields_max_length(old_password=255, new_password=255)
def change_endpoint() -> Response:
    """
    # TODO: Fill this docstring.
    """
    if USER_DATASTORE.change_user_password(current_user, request.form["old_password"], \
                                            request.form["new_password"]):
        return CHANGE_SUCCESS

    return WRONG_OLD_PASSWORD
