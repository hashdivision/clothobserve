"""
    clothobserve.data.constants.mail.email
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Universal email related mail bodies.

    :copyright: © 2018 HashDivision OU.

    :license: Apache License 2.0, see *LICENSE* for more details.

    |

"""
from os import getenv

#: This URL + token will be sent to email of password restoring user.
_WEBSITE_URL = getenv('WEBSITE_URL', 'https://example.com') + "/account/email/confirm"

#: Message which will be sent to user's email upon registration for confirmation.
#: You should provide token via ``CONFIRMATION_MESSAGE % (token, token)``.
CONFIRMATION_MESSAGE = ("<b>Hello!</b></br>"
                       "User was registered with Your email and we need to confirm it.</br>"
                       "<u>Please ignore this email if You did not register user</u>.</br>"
                       "Use link below to confirm Your email (valid for 48 hours).</br></br>"
                       '<a href="') + _WEBSITE_URL + '/%s">Confirmation Link</a></br></br>' \
                       + "Or copy this link and paste into browser:</br>" \
                       + _WEBSITE_URL + "/%s"
