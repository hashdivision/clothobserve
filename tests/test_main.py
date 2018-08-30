import unittest
from flask_api import status
from main import SERVER

class MainTestCase(unittest.TestCase):
    """
    Import is ``from main import SERVER`` because here we test that particular ``SERVER``.
    We just test that version is the one we need when tests are running.
    """
    
    def test_version(self):
        """
        Make sure ``/version`` endpoint gives correct version.
        """
        result = SERVER.test_client().get('/version')
        self.assertEqual(result.status_code, status.HTTP_200_OK)
        self.assertEqual(result.get_data(as_text=True), '0.27.0')
