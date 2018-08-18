from flask import Response
from flask_api import status

SUCCESS = Response("Success", status=status.HTTP_200_OK)
BAD_REQUEST = Response("Bad Request", status=status.HTTP_400_BAD_REQUEST)
NOT_FOUND = Response("Not Found", status=status.HTTP_404_NOT_FOUND)
