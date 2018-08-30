"""
    clothobserve.logic.mail.sender
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Sending mail to recipients through Flask-Mail.

    :copyright: © 2018 HashDivision OU.

    :license: Apache License 2.0, see *LICENSE* for more details.

    |

"""
from flask_mail import Mail, Message

#: Flask-Mail instance to send mail.
MAIL = Mail()

def send_html_mail(subject: str, body_html: str, recipient: str) -> None:
    """
    Sends HTML mail to one recipient.

    :param subject: subject of the email.
    :param body_html: HTML body.
    :param recipient: who will receive this message.
    """
    message = Message(subject, recipients=[recipient])
    message.html = body_html
    MAIL.send(message)
