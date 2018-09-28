"""
    clothobserve.endpoints.user.email
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Email related endpoints for account (``/account/email/``).

    :copyright: © 2018 HashDivision OU.

    :license: Apache License 2.0, see *LICENSE* for more details.

    |

"""
from flask import Blueprint, Response, abort
from endpoints.decorators.auth import anonymous_required
from data.constants.responses.generic import NOT_FOUND
from data.constants.responses.user_email import CONFIRMATION_SUCCESS
from logic.user.email import confirm_email

#: Blueprint of this email module.
EMAIL_BP = Blueprint("email", __name__)

@EMAIL_BP.route("/confirm/<token>")
@anonymous_required
def email_confirmation_endpoint(token: str) -> Response:
    """
    Email confirmation GET endpoint (**/account/email/confirm/<token>**)
    for confirming that you own the email securely.
    You MUST not be logged in to use it.

    Returns:
        Success (200 OK): Email Confirmed.
        Fail (404 NOT FOUND): if token is wrong or expired.
        Fail (404 NOT FOUND): if logged in user uses this endpoint.
    """
    if confirm_email(token):
        return CONFIRMATION_SUCCESS

    return NOT_FOUND
