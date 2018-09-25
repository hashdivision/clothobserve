"""
    clothobserve.endpoints.user.account
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Email related endpoints for account.

    :copyright: © 2018 HashDivision OU.

    :license: Apache License 2.0, see *LICENSE* for more details.

    |

"""
from flask import Blueprint, Response, abort
from endpoints.decorators.auth import anonymous_required

#: Blueprint of this email module.
EMAIL_BP = Blueprint("email", __name__)

@EMAIL_BP.route("/confirm/<random_key>", methods=['POST'])
@anonymous_required
def email_confirmation_endpoint(random_key: str) -> Response:
    """
    # TODO: Fill this docstring.
    """
    abort(501)
