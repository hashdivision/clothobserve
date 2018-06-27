from flask import Flask, Response
from flask_api import status

server = Flask("clothobserve", root_path="/clothobserve/")

#: This response is only used for testing to make sure
#: version is the right one and that app is working.
VERSION = Response("0.30.1", status=status.HTTP_200_OK)

@server.route("/version")
def version_endpoint() -> Response:
    """Version endpoint (**/version**) for testing purposes."""
    return VERSION
