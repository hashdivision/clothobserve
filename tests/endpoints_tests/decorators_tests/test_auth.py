import os
import unittest
from flask import Response
from flask_api import status
from flask.testing import FlaskClient
from main import SERVER
from data.models.user import User, Role
from data.constants.responses.generic import NOT_FOUND
from data.constants.responses.decorators_auth import LOGIN_REQUIRED, \
    NO_PERMISSION
from endpoints.decorators.auth import login_required, anonymous_required, \
                                        roles_accepted, roles_required
from logic.user.datastore import USER_DATASTORE

_REACHED = Response("Reached", status=status.HTTP_200_OK)

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

@SERVER.route("/auth_test/anonymous_required")
@anonymous_required
def anonymous_required_endpoint():
	return _REACHED

@SERVER.route("/auth_test/login_required")
@login_required()
def login_required_endpoint():
	return _REACHED

@SERVER.route("/auth_test/login_required_silent")
@login_required(silent=True)
def login_required_silent_endpoint():
	return _REACHED

@SERVER.route("/auth_test/roles_accepted")
@login_required()
@roles_accepted('admin', 'superuser')
def roles_accepted_endpoint():
	return _REACHED

@SERVER.route("/auth_test/roles_accepted_silent")
@login_required()
@roles_accepted('admin', 'superuser', silent=True)
def roles_accepted_silent_endpoint():
	return _REACHED

@SERVER.route("/auth_test/roles_required")
@login_required()
@roles_required('admin', 'superuser')
def roles_required_endpoint():
	return _REACHED

@SERVER.route("/auth_test/roles_required_silent")
@login_required()
@roles_required('admin', 'superuser', silent=True)
def roles_required_silent_endpoint():
	return _REACHED

class AuthDecoratorsTestCase(unittest.TestCase):
    """
    # TODO: Fill this docstring.
    """

    __ROLES_ACCEPTED_TESTER_EMAIL = 'roles.accepted.tester@example.com'
    __ROLES_REQUIRED_TESTER_EMAIL = 'roles.required.tester@example.com'
    __RANDOM_PASSWORD = 'RandomPassword'

    def test_anonymous_required(self):
        """
        # TODO: Fill this docstring.
        """
        with SERVER.test_client() as client:
            success_result = client.get("/auth_test/anonymous_required")
            self.assertEqual(success_result.status_code, _REACHED.status_code)
            self.assertEqual(success_result.get_data(as_text=True), _REACHED.get_data(as_text=True))

            admin_email = os.getenv('ADMIN_EMAIL', 'admin@example.com')
            admin_password = os.getenv('ADMIN_PASSWORD', 'ChangeMeASAP')
            signin(client, admin_email, admin_password)
            fail_result = client.get("/auth_test/anonymous_required")
            self.assertEqual(fail_result.status_code, NOT_FOUND.status_code)
            self.assertEqual(fail_result.get_data(as_text=True), NOT_FOUND.get_data(as_text=True))

    def test_login_required(self):
        """
        # TODO: Fill this docstring.
        """
        with SERVER.test_client() as client:
            fail_result = client.get("/auth_test/login_required")
            self.assertEqual(fail_result.status_code, LOGIN_REQUIRED.status_code)
            self.assertEqual(fail_result.get_data(as_text=True), LOGIN_REQUIRED.get_data(as_text=True))
            fail_result_silent = client.get("/auth_test/login_required_silent")
            self.assertEqual(fail_result_silent.status_code, NOT_FOUND.status_code)
            self.assertEqual(fail_result_silent.get_data(as_text=True), NOT_FOUND.get_data(as_text=True))

            admin_email = os.getenv('ADMIN_EMAIL', 'admin@example.com')
            admin_password = os.getenv('ADMIN_PASSWORD', 'ChangeMeASAP')
            signin(client, admin_email, admin_password)
            success_result = client.get("/auth_test/login_required")
            self.assertEqual(success_result.status_code, _REACHED.status_code)
            self.assertEqual(success_result.get_data(as_text=True), _REACHED.get_data(as_text=True))
            success_result_silent = client.get("/auth_test/login_required_silent")
            self.assertEqual(success_result_silent.status_code, _REACHED.status_code)
            self.assertEqual(success_result_silent.get_data(as_text=True), _REACHED.get_data(as_text=True))

    def test_roles_accepted(self):
        """
        # TODO: Fill this docstring.
        """
        with SERVER.test_client() as client:
            register(client, self.__ROLES_ACCEPTED_TESTER_EMAIL, self.__RANDOM_PASSWORD)
            
            tester = User.find_by_email(self.__ROLES_ACCEPTED_TESTER_EMAIL)
            USER_DATASTORE.remove_role_from_user(tester, Role.find_by_name('user'))
            USER_DATASTORE.add_role_to_user(tester, Role.find_by_name('tester'))

            fail_result = client.get("/auth_test/roles_accepted")
            self.assertEqual(fail_result.status_code, NO_PERMISSION.status_code)
            self.assertEqual(fail_result.get_data(as_text=True), NO_PERMISSION.get_data(as_text=True))
            fail_result_silent = client.get("/auth_test/roles_accepted_silent")
            self.assertEqual(fail_result_silent.status_code, NOT_FOUND.status_code)
            self.assertEqual(fail_result_silent.get_data(as_text=True), NOT_FOUND.get_data(as_text=True))

            USER_DATASTORE.add_role_to_user(tester, Role.find_by_name('superuser'))
            superuser_success_result = client.get("/auth_test/roles_accepted")
            self.assertEqual(superuser_success_result.status_code, _REACHED.status_code)
            self.assertEqual(superuser_success_result.get_data(as_text=True), _REACHED.get_data(as_text=True))
            superuser_success_result_silent = client.get("/auth_test/roles_accepted_silent")
            self.assertEqual(superuser_success_result_silent.status_code, _REACHED.status_code)
            self.assertEqual(superuser_success_result_silent.get_data(as_text=True), _REACHED.get_data(as_text=True))

            USER_DATASTORE.add_role_to_user(tester, Role.find_by_name('admin'))
            both_success_result = client.get("/auth_test/roles_accepted")
            self.assertEqual(both_success_result.status_code, _REACHED.status_code)
            self.assertEqual(both_success_result.get_data(as_text=True), _REACHED.get_data(as_text=True))
            both_success_result_silent = client.get("/auth_test/roles_accepted_silent")
            self.assertEqual(both_success_result_silent.status_code, _REACHED.status_code)
            self.assertEqual(both_success_result_silent.get_data(as_text=True), _REACHED.get_data(as_text=True))

            USER_DATASTORE.remove_role_from_user(tester, Role.find_by_name('superuser'))
            admin_success_result = client.get("/auth_test/roles_accepted")
            self.assertEqual(admin_success_result.status_code, _REACHED.status_code)
            self.assertEqual(admin_success_result.get_data(as_text=True), _REACHED.get_data(as_text=True))
            admin_success_result_silent = client.get("/auth_test/roles_accepted_silent")
            self.assertEqual(admin_success_result_silent.status_code, _REACHED.status_code)
            self.assertEqual(admin_success_result_silent.get_data(as_text=True), _REACHED.get_data(as_text=True))
    
    def test_roles_required(self):
        """
        # TODO: Fill this docstring.
        """
        with SERVER.test_client() as client:
            register(client, self.__ROLES_REQUIRED_TESTER_EMAIL, self.__RANDOM_PASSWORD)
            
            tester = User.find_by_email(self.__ROLES_REQUIRED_TESTER_EMAIL)
            USER_DATASTORE.remove_role_from_user(tester, Role.find_by_name('user'))
            USER_DATASTORE.add_role_to_user(tester, Role.find_by_name('tester'))

            fail_result = client.get("/auth_test/roles_required")
            self.assertEqual(fail_result.status_code, NO_PERMISSION.status_code)
            self.assertEqual(fail_result.get_data(as_text=True), NO_PERMISSION.get_data(as_text=True))
            fail_result_silent = client.get("/auth_test/roles_required_silent")
            self.assertEqual(fail_result_silent.status_code, NOT_FOUND.status_code)
            self.assertEqual(fail_result_silent.get_data(as_text=True), NOT_FOUND.get_data(as_text=True))

            USER_DATASTORE.add_role_to_user(tester, Role.find_by_name('superuser'))
            superuser_fail_result = client.get("/auth_test/roles_required")
            self.assertEqual(superuser_fail_result.status_code, NO_PERMISSION.status_code)
            self.assertEqual(superuser_fail_result.get_data(as_text=True), NO_PERMISSION.get_data(as_text=True))
            superuser_fail_result_silent = client.get("/auth_test/roles_required_silent")
            self.assertEqual(superuser_fail_result_silent.status_code, NOT_FOUND.status_code)
            self.assertEqual(superuser_fail_result_silent.get_data(as_text=True), NOT_FOUND.get_data(as_text=True))

            USER_DATASTORE.add_role_to_user(tester, Role.find_by_name('admin'))
            both_success_result = client.get("/auth_test/roles_required")
            self.assertEqual(both_success_result.status_code, _REACHED.status_code)
            self.assertEqual(both_success_result.get_data(as_text=True), _REACHED.get_data(as_text=True))
            both_success_result_silent = client.get("/auth_test/roles_required_silent")
            self.assertEqual(both_success_result_silent.status_code, _REACHED.status_code)
            self.assertEqual(both_success_result_silent.get_data(as_text=True), _REACHED.get_data(as_text=True))

            USER_DATASTORE.remove_role_from_user(tester, Role.find_by_name('superuser'))
            admin_fail_result = client.get("/auth_test/roles_required")
            self.assertEqual(admin_fail_result.status_code, NO_PERMISSION.status_code)
            self.assertEqual(admin_fail_result.get_data(as_text=True), NO_PERMISSION.get_data(as_text=True))
            admin_fail_result_silent = client.get("/auth_test/roles_required_silent")
            self.assertEqual(admin_fail_result_silent.status_code, NOT_FOUND.status_code)
            self.assertEqual(admin_fail_result_silent.get_data(as_text=True), NOT_FOUND.get_data(as_text=True))
