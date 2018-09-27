"""
    clothobserve.logic.user.password
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Password related logic for account.

    :copyright: © 2018 HashDivision OU.

    :license: Apache License 2.0, see *LICENSE* for more details.

    |

"""
from datetime import datetime, timedelta
from data.models.user import User
from data.constants.mail.password import RESTORATION_MESSAGE
from logic.mail.sender import send_html_mail
from logic.utils.random import generate_random_token

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
        send_html_mail("Password Restoration", RESTORATION_MESSAGE % token, email)

def is_timestamp_expired(timestamp: datetime, expiry_timedelta: timedelta) -> bool:
    """
    Determines if timedelta has passed from provided datetime.
    # TODO: Move to utils

    Returns:
        If expiry_timedelta did pass after timestamp.
    """
    return timestamp + expiry_timedelta < datetime.now()

def reset_password(token: str, password: str) -> None:
    """
    Reset password of user who has provided password token.
    # TODO: Refactor
    # TODO: Implement

    :param token: password reset token which was assigned to user on reset request.
    :param password: password that will be set if token is right and not expired.
    """
    user = User.find_by_password_token(token)
    if user and not is_timestamp_expired(user.password_reset_date, timedelta(days=1)):
        pass
