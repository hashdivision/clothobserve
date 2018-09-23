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
