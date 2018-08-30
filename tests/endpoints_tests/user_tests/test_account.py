import unittest
from flask import Response
from flask.testing import FlaskClient
from flask_security.core import current_user
from flask_api import status
from main import SERVER
from data.constants.responses.user_account import EMAIL_IS_REGISTERED, \
    WRONG_CREDENTIALS, USER_INACTIVE
from data.models.user import User
from logic.user.datastore import USER_DATASTORE

def register(client: FlaskClient, email: str, password: str) -> Response:
    """Fast method for using ``/account/register`` endpoint"""
    form_data = 'email=' + email +'&password=' + password
    return client.post('/account/register', data=form_data, content_type='application/x-www-form-urlencoded')

def signin(client: FlaskClient, email: str, password: str) -> Response:
    """Fast method for using ``/account/signin`` endpoint"""
    form_data = 'email=' + email +'&password=' + password
    return client.post('/account/signin', data=form_data, content_type='application/x-www-form-urlencoded')

def logout(client: FlaskClient) -> Response:
    """Fast method for using ``/account/logout`` endpoint"""
    return client.get('/account/logout')

class UserAccountTestCase(unittest.TestCase):
    """
    # TODO: Fill this docstring.
    """
    
    __REGISTER_SUCCESS_EMAIL = 'success@example.com'
    __REGISTER_TWICE_EMAIL = 'twice@example.com'
    __SIGNIN_RIGHT_EMAIL = 'signin@example.com'
    __SIGNIN_WRONG_EMAIL = 'ningis@example.com'
    __SIGNIN_INACTIVE_EMAIL = 'inactive@example.com'
    __RANDOM_PASSWORD = 'RandomPassword'
    __WRONG_PASSWORD = 'WrongPassword'

    def test_register_and_signin_and_logout_success(self):
        """
        # TODO: Fill this docstring.
        """
        with SERVER.test_client() as client:
            register_result = register(client, self.__REGISTER_SUCCESS_EMAIL, self.__RANDOM_PASSWORD)
            self.assertEqual(register_result.status_code, status.HTTP_200_OK)
            self.assertTrue(current_user.is_authenticated)
            self.assertEqual(current_user.email, self.__REGISTER_SUCCESS_EMAIL)

            logout_result = logout(client)
            self.assertEqual(logout_result.status_code, status.HTTP_200_OK)
            self.assertFalse(current_user.is_authenticated)

            signin_result = signin(client, self.__REGISTER_SUCCESS_EMAIL, self.__RANDOM_PASSWORD)
            self.assertEqual(signin_result.status_code, status.HTTP_200_OK)
            self.assertTrue(current_user.is_authenticated)
            self.assertEqual(current_user.email, self.__REGISTER_SUCCESS_EMAIL)

    def test_register_twice(self):
        """
        # TODO: Fill this docstring.
        """
        with SERVER.test_client() as client:
            register_result = register(client, self.__REGISTER_TWICE_EMAIL, self.__RANDOM_PASSWORD)
            self.assertEqual(register_result.status_code, status.HTTP_200_OK)
            self.assertTrue(current_user.is_authenticated)
            self.assertEqual(current_user.email, self.__REGISTER_TWICE_EMAIL)

            logout(client)

            second_register_result = register(client, self.__REGISTER_TWICE_EMAIL, self.__RANDOM_PASSWORD)
            self.assertNotEqual(second_register_result.status_code, status.HTTP_200_OK)
            self.assertEqual(second_register_result.status_code, EMAIL_IS_REGISTERED.status_code)
            self.assertFalse(current_user.is_authenticated)

    def test_signin_wrong_credentials(self):
        """
        # TODO: Fill this docstring.
        """
        with SERVER.test_client() as client:
            register(client, self.__SIGNIN_RIGHT_EMAIL, self.__RANDOM_PASSWORD)
            logout(client)

            wrong_password_result = signin(client, self.__SIGNIN_RIGHT_EMAIL, self.__WRONG_PASSWORD)
            self.assertNotEqual(wrong_password_result.status_code, status.HTTP_200_OK)
            self.assertEqual(wrong_password_result.status_code, WRONG_CREDENTIALS.status_code)
            self.assertFalse(current_user.is_authenticated)

            wrong_username_result = signin(client, self.__SIGNIN_WRONG_EMAIL, self.__RANDOM_PASSWORD)
            self.assertNotEqual(wrong_username_result.status_code, status.HTTP_200_OK)
            self.assertEqual(wrong_username_result.status_code, WRONG_CREDENTIALS.status_code)
            self.assertFalse(current_user.is_authenticated)

    def test_signin_inactive_user(self):
        """
        # TODO: Fill this docstring.
        """
        with SERVER.test_client() as client:
            register(client, self.__SIGNIN_INACTIVE_EMAIL, self.__RANDOM_PASSWORD)
            logout(client)
            
            user = User.find_by_email(self.__SIGNIN_INACTIVE_EMAIL)
            USER_DATASTORE.deactivate_user(user)

            inactive_signin_result = signin(client, self.__SIGNIN_INACTIVE_EMAIL, self.__RANDOM_PASSWORD)
            self.assertNotEqual(inactive_signin_result.status_code, status.HTTP_200_OK)
            self.assertEqual(inactive_signin_result.status_code, USER_INACTIVE.status_code)
            self.assertFalse(current_user.is_authenticated)

            USER_DATASTORE.activate_user(user)

            active_signin_result = signin(client, self.__SIGNIN_INACTIVE_EMAIL, self.__RANDOM_PASSWORD)
            self.assertEqual(active_signin_result.status_code, status.HTTP_200_OK)
            self.assertTrue(current_user.is_authenticated)
