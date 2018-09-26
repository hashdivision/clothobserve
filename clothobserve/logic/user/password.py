"""
    clothobserve.logic.user.password
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Password related logic for account.

    :copyright: © 2018 HashDivision OU.

    :license: Apache License 2.0, see *LICENSE* for more details.

    |

"""
from datetime import datetime
from data.models.user import User
from logic.mail.sender import send_html_mail

#: Message which will be sent to user's email upon restoration request.
_RESTORATION_MESSAGE = "Restoration link: localhost/restore/%s"

def generate_random_token(email: str) -> str:
    """
    # TODO: Fill this docstring.
    # TODO: Implement.
    # TODO: Move to utils.
    """
    return "random"

def send_restoration_link(email: str) -> None:
    """
    # TODO: Fill this docstring.
    """
    user = User.find_by_email(email)
    if user and not user.password_reset_token:
        token = generate_random_token(email)
        user.password_reset_token = token
        user.password_reset_date = datetime.now()
        send_html_mail("Password Restoration", _RESTORATION_MESSAGE % token, email)
