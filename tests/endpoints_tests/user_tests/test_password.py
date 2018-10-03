import unittest
from flask import Response
from flask.testing import FlaskClient
from main import SERVER
from data.constants.responses.user_password import CHANGE_SUCCESS, WRONG_OLD_PASSWORD, \
    CHECK_EMAIL

def restore_send_link(client: FlaskClient, email: str) -> Response:
    """Fast method for using ``/account/password/restore`` endpoint"""
    form_data = 'email=' + email
    return client.post('/account/password/restore', data=form_data, content_type='application/x-www-form-urlencoded')

class UserPasswordTestCase(unittest.TestCase):
    """
    # TODO: Fill this docstring.
    """

    def test_restore_send_link_endpoint(self):
        """
        # TODO: Fill this docstring.
        """
        with SERVER.test_client() as client:
            # TODO: Test if email was sent and if token and date was added
            result = restore_send_link(client, "random.email@example.com")
            self.assertEqual(result.status_code, CHECK_EMAIL.status_code)
            self.assertEqual(result.get_data(as_text=True), CHECK_EMAIL.get_data(as_text=True))
