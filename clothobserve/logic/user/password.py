"""
    clothobserve.logic.user.password
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Password related logic for account.

    :copyright: © 2018 HashDivision OU.

    :license: Apache License 2.0, see *LICENSE* for more details.

    |

"""
from datetime import datetime
from flask_security.utils import hash_password
from data.models.user import User
from data.constants.mail.password import RESTORATION_MESSAGE
from logic.mail.sender import send_html_mail
from logic.utils.random import generate_random_token
from logic.utils.date import is_timestamp_expired

def send_restoration_link(email: str) -> None:
    """
    Send restoration link to provided email.

    :param email: where the message with restoration link will be sent.
    """
    user = User.find_by_email(email)
    if user and not user.password_reset_token:
        token = generate_random_token()
        user.password_reset_token = token
        user.password_reset_date = datetime.now()
        user.save()
        send_html_mail("Password Restoration", RESTORATION_MESSAGE % (token, token), email)

def reset_password(token: str, password: str) -> None:
    """
    Reset password of user who has provided password token.

    :param token: password reset token which was assigned to user on reset request.
    :param password: password that will be set if token is right and not expired.
    """
    user = User.find_by_password_token(token)
    if user and not is_timestamp_expired(user.password_reset_date, days=1):
        user.password_reset_token = None
        user.password_reset_date = None
        user.password = hash_password(password)
        user.save()