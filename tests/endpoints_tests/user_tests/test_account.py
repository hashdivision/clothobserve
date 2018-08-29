from main import SERVER
import unittest
from flask import Response
from flask_security.core import current_user

def register(client, email, password):
    """Fast method for using ``/account/register`` endpoint"""
    form_data = 'email=' + email +'&password=' + password
    return client.post('/account/register', data=form_data, content_type='application/x-www-form-urlencoded')

def signin(client, email, password):
    """Fast method for using ``/account/signin`` endpoint"""
    form_data = 'email=' + email +'&password=' + password
    return client.post('/account/signin', data=form_data, content_type='application/x-www-form-urlencoded')

def logout(client):
    """Fast method for using ``/account/logout`` endpoint"""
    return client.get('/account/logout')

class UserAccountTestCase(unittest.TestCase):
    """
    # TODO: Fill this docstring.
    """
    
    __REGISTER_SUCCESS_EMAIL = 'success@example.com'
    __RANDOM_PASSWORD = 'RandomPassword'

    def test_register_success(self):
        """
        # TODO: Fill this docstring.
        """
        with SERVER.test_client() as client:
            register_result = register(client, self.__REGISTER_SUCCESS_EMAIL, self.__RANDOM_PASSWORD)
            self.assertEqual(register_result.status_code, 200)
            self.assertTrue(current_user.is_authenticated)
            self.assertEqual(current_user.email, self.__REGISTER_SUCCESS_EMAIL)

            logout_result = logout(client)
            self.assertEqual(logout_result.status_code, 200)
            self.assertFalse(current_user.is_authenticated)

            check_result = signin(client, self.__REGISTER_SUCCESS_EMAIL, self.__RANDOM_PASSWORD)
            self.assertEqual(check_result.status_code, 200)
            self.assertTrue(current_user.is_authenticated)
            self.assertEqual(current_user.email, self.__REGISTER_SUCCESS_EMAIL)
