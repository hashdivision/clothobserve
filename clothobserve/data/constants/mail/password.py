"""
    clothobserve.data.constants.mail.password
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Universal password related mail bodies.

    :copyright: © 2018 HashDivision OU.

    :license: Apache License 2.0, see *LICENSE* for more details.

    |

"""
from os import getenv

#: This URL + token will be sent to email of password restoring user.
#: URL + token should give user a form with password input that POSTs to
#: endpoint ``/account/password/restore/<token>``.
_RESTORE_URL = getenv('PASSWORD_RESTORE_URL', 'https://example.com/restore')

#: Message which will be sent to user's email upon restoration request.
#: You should provide token via ``RESTORATION_MESSAGE % (token, token)``.
RESTORATION_MESSAGE = ("<b>Hello!</b></br>"
                       "Password reset was requested for this email.</br>"
                       "<u>Please ignore this email if You did not request it</u>.</br>"
                       "Use link below to set new password (valid for 24 hours).</br></br>"
                       '<a href="') + _RESTORE_URL + '/%s">Restoration Link</a></br></br>' \
                       + "Or copy this link and paste into browser:</br>" \
                       + _RESTORE_URL + "/%s"
