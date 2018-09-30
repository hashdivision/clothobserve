import os
import unittest
from flask import Response
from flask_api import status
from flask.testing import FlaskClient
from main import SERVER
from data.constants.responses.decorators_data import BAD_FORM, \
    LARGE_FIELD_LENGTH
from endpoints.decorators.data import form_required, form_fields_max_length

_REACHED = Response("Reached", status=status.HTTP_200_OK)

def form_required_get_with_form(client: FlaskClient, test_field1: str = None, test_field2: str = None) -> Response:
    """Fast method for using ``/data_test/form_required`` endpoint"""
    form_data = ''
    if test_field1:
        form_data += 'test_field1=' + test_field1
        if test_field2:
            form_data += '&test_field2=' + test_field2
    elif test_field2:
        form_data += 'test_field2=' + test_field2
    else:
        return client.get('/data_test/form_required')

    return client.get('/data_test/form_required', data=form_data, content_type='application/x-www-form-urlencoded')

@SERVER.route("/data_test/form_required")
@form_required("test_field1", "test_field2")
@form_fields_max_length(test_field1=10, test_field2=15)
def form_required_endpoint():
    return _REACHED

class DataDecoratorsTestCase(unittest.TestCase):
    """
    # TODO: Fill this docstring.
    """

    def test_form_required(self):
        """
        # TODO: Fill this docstring.
        """
        with SERVER.test_client() as client:
            success_result = form_required_get_with_form(client, "test", "test")
            self.assertEqual(success_result.status_code, _REACHED.status_code)
            self.assertEqual(success_result.get_data(as_text=True), _REACHED.get_data(as_text=True))

            fail_no_form_result = form_required_get_with_form(client)
            self.assertEqual(fail_no_form_result.status_code, BAD_FORM.status_code)
            self.assertEqual(fail_no_form_result.get_data(as_text=True), BAD_FORM.get_data(as_text=True))

            fail_only_first_form_result = form_required_get_with_form(client, "only_this", None)
            self.assertEqual(fail_only_first_form_result.status_code, BAD_FORM.status_code)
            self.assertEqual(fail_only_first_form_result.get_data(as_text=True), BAD_FORM.get_data(as_text=True))

            fail_only_second_form_result = form_required_get_with_form(client, None, "only_this")
            self.assertEqual(fail_only_second_form_result.status_code, BAD_FORM.status_code)
            self.assertEqual(fail_only_second_form_result.get_data(as_text=True), BAD_FORM.get_data(as_text=True))

            fail_first_wrong_length_form_result = form_required_get_with_form(client, "this_is_too_much", "test")
            self.assertEqual(fail_first_wrong_length_form_result.status_code, LARGE_FIELD_LENGTH.status_code)
            self.assertEqual(fail_first_wrong_length_form_result.get_data(as_text=True), LARGE_FIELD_LENGTH.get_data(as_text=True))

            fail_second_wrong_length_form_result = form_required_get_with_form(client, "test", "this_is_too_much")
            self.assertEqual(fail_second_wrong_length_form_result.status_code, LARGE_FIELD_LENGTH.status_code)
            self.assertEqual(fail_second_wrong_length_form_result.get_data(as_text=True), LARGE_FIELD_LENGTH.get_data(as_text=True))

            fail_both_wrong_length_form_result = form_required_get_with_form(client, "this_is_too_much", "this_is_too_much")
            self.assertEqual(fail_both_wrong_length_form_result.status_code, LARGE_FIELD_LENGTH.status_code)
            self.assertEqual(fail_both_wrong_length_form_result.get_data(as_text=True), LARGE_FIELD_LENGTH.get_data(as_text=True))
