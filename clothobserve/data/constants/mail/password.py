"""
    clothobserve.data.constants.mail.password
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Password related mail bodies.

    :copyright: © 2018 HashDivision OU.

    :license: Apache License 2.0, see *LICENSE* for more details.

    |

"""
#: Message which will be sent to user's email upon restoration request.
#: You should provide token via ``RESTORATION_MESSAGE % token``.
RESTORATION_MESSAGE = "Restoration link: localhost/restore/%s"