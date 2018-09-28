"""
    clothobserve.logic.user.email
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Email related logic for account.

    :copyright: © 2018 HashDivision OU.

    :license: Apache License 2.0, see *LICENSE* for more details.

    |

"""
from datetime import datetime
from data.models.user import User
from data.constants.mail.email import CONFIRMATION_MESSAGE
from logic.mail.sender import send_html_mail
from logic.utils.random import generate_random_token
from logic.utils.date import is_timestamp_expired

def send_confirmation_link(user: User) -> None:
    """
    Send confirmation link to just created (we assume) user.

    :param user: just created user, the message with confirmation link will be sent to him.
    """
    token = generate_random_token()
    user.confirm_token = token
    user.confirm_date = datetime.now()
    user.save()
    send_html_mail("Email Confirmation", CONFIRMATION_MESSAGE % (token, token), user.email)

def confirm_email(token: str) -> bool:
    """
    Confirm email of user who has provided confirmation token.

    :param token: confirmation token which was assigned to user on registration.
    """
    user = User.find_by_confirm_token(token)
    if user and not is_timestamp_expired(user.confirm_date, days=2):
        user.confirm_token = None
        user.confirm_date = None
        user.confirmed = True
        user.save()
        return True

    return False
