import os
import unittest
from flask_security.utils import verify_password
from main import SERVER
from data.models.user import User, Role

class InitializationTestCase(unittest.TestCase):
    """
    Testing that initialization.py do initialize defaults and blueprints.
    """
    
    def test_create_default_user_roles(self):
        """
        Make sure that all default roles are created.
        """
        self.assertIsNotNone(Role.find_by_name('admin'))
        self.assertIsNotNone(Role.find_by_name('tester'))
        self.assertIsNotNone(Role.find_by_name('user'))
        self.assertIsNotNone(Role.find_by_name('superuser'))

    def test_create_admin_user(self):
        """
        Make sure that default admin user is created with right role, email and password.
        """
        admin_email = os.getenv('ADMIN_EMAIL', 'admin@example.com')
        admin_password = os.getenv('ADMIN_PASSWORD', 'ChangeMeASAP')
        admin_role = Role.find_by_name('admin')
        admin = User.find_by_email(admin_email)

        self.assertIsNotNone(admin)
        self.assertTrue(admin.confirmed)
        self.assertIn(admin_role, admin.roles)
        with SERVER.app_context():
            self.assertTrue(verify_password(admin_password, admin.password))
