"""
    clothobserve.main
    ~~~~~~~~~~~~~~~~~
    # TODO: Fill this docstring.

    :copyright: © 2018 HashDivision OU.

    :license: Apache License 2.0, see *LICENSE* for more details.

    |

"""
from flask import Response
from flask_api import status
from logic.config import create_server
from logic.initialization import initialize

SERVER = create_server()
with SERVER.app_context():
    initialize(SERVER)

#: This response is only used for testing to make sure
#: version is the right one and that app is working.
VERSION = Response("0.27.0", status=status.HTTP_200_OK)

@SERVER.route("/version")
def version_endpoint() -> Response:
    """Version endpoint (**/version**) for testing purposes."""
    return VERSION
