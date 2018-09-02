import os
import unittest
from flask import Response
from flask.testing import FlaskClient
from flask_api import status
from flask_security.core import current_user
from main import SERVER
from data.models.user import User
from data.constants.responses.user_profile import PROFILE_NOT_FOUND
from logic.user.datastore import USER_DATASTORE

def visibility(client: FlaskClient, state: int) -> Response:
    """Fast method for using ``/profile/visibility/<int: state>`` endpoint"""
    return client.get('/profile/visibility/' + str(state))

def user(client: FlaskClient, username: str) -> Response:
    """Fast method for using ``/profile/user/<username>`` endpoint"""
    return client.get('/profile/user/' + username)

def root_profile(client: FlaskClient) -> Response:
    """Fast method for using ``/profile/`` endpoint"""
    return client.get('/profile/')

def register(client: FlaskClient, email: str, password: str) -> None:
    """Fast method for using ``/account/register`` endpoint"""
    form_data = 'email=' + email +'&password=' + password
    client.post('/account/register', data=form_data, content_type='application/x-www-form-urlencoded')

def signin(client: FlaskClient, email: str, password: str) -> Response:
    """Fast method for using ``/account/signin`` endpoint"""
    form_data = 'email=' + email +'&password=' + password
    return client.post('/account/signin', data=form_data, content_type='application/x-www-form-urlencoded')

class UserProfileTestCase(unittest.TestCase):
    """
    # TODO: Fill this docstring.
    """

    __RANDOM_PROFILE_TEST_EMAIL = 'random.profile.test@example.com'
    __RANDOM_PASSWORD = 'RandomPassword'
    __FALSE = 0
    __TRUE = 1
    __TRUE_BIG = 253567

    def test_user_endpoint(self):
        """
        # TODO: Fill this docstring.
        """
        with SERVER.test_client() as client:
            admin_username = os.getenv('ADMIN_USERNAME', 'Admin')
            admin_email = os.getenv('ADMIN_EMAIL', 'admin@example.com')
            admin = User.find_by_email(admin_email)

            register(client, self.__RANDOM_PROFILE_TEST_EMAIL, self.__RANDOM_PASSWORD)

            USER_DATASTORE.change_profile_visibility(admin, public=True)
            success_result = user(client, admin_username)
            self.assertEqual(success_result.status_code, status.HTTP_200_OK)

            USER_DATASTORE.change_profile_visibility(admin, public=False)
            failed_result = user(client, admin_username)
            self.assertEqual(failed_result.status_code, PROFILE_NOT_FOUND.status_code)

    def test_root_profile_endpoint(self):
        """
        # TODO: Fill this docstring.
        """
        with SERVER.test_client() as client:
            admin_email = os.getenv('ADMIN_EMAIL', 'admin@example.com')
            admin_password = os.getenv('ADMIN_PASSWORD', 'ChangeMeASAP')

            signin(client, admin_email, admin_password)
            result = root_profile(client)
            self.assertEqual(result.status_code, status.HTTP_200_OK)

    def test_visibility_endpoint(self):
        """
        # TODO: Fill this docstring.
        """
        with SERVER.test_client() as client:
            admin_email = os.getenv('ADMIN_EMAIL', 'admin@example.com')
            admin_password = os.getenv('ADMIN_PASSWORD', 'ChangeMeASAP')

            signin(client, admin_email, admin_password)

            visibility(client, self.__TRUE)
            self.assertTrue(current_user.profile.public)
            visibility(client, self.__FALSE)
            self.assertFalse(current_user.profile.public)
            visibility(client, self.__TRUE_BIG)
            self.assertTrue(current_user.profile.public)

            visibility(client, self.__FALSE)
