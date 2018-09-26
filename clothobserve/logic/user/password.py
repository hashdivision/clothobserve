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
from data.constants.mail.password import RESTORATION_MESSAGE
from logic.mail.sender import send_html_mail
from logic.utils.random import generate_random_token

def send_restoration_link(email: str) -> None:
    """
    # TODO: Fill this docstring.
    """
    user = User.find_by_email(email)
    if user and not user.password_reset_token:
        token = generate_random_token()
        user.password_reset_token = token
        user.password_reset_date = datetime.now()
        send_html_mail("Password Restoration", RESTORATION_MESSAGE % token, email)
