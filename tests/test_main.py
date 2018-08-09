import unittest
from main import SERVER

class MainTestCase(unittest.TestCase):
    """
    First import is ``from main import SERVER`` because here we test that particular ``SERVER``.
    We just test that version is updated when tests are running. Can be frustrating.
    """
    
    def test_version(self):
        """
        Make sure ``/version`` endpoint gives correct version.
        """
        result = SERVER.test_client().get('/version')
        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.get_data(as_text=True), "0.27.0")
