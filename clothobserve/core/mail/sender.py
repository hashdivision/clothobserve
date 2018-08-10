"""
    clothobserve.core.mail.sender
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Sending mail to recipients through Flask-Mail.

    :copyright: © 2018 HashDivision OU.

    :license: Apache License 2.0, see *LICENSE* for more details.

    |

"""
from flask_mail import Mail

#: Flask-Mail instance to send mail.
MAIL = Mail()

