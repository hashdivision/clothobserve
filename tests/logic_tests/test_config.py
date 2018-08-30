import os
import unittest
from logic.config import create_server

class ConfigTestCase(unittest.TestCase):
    """
    Here we test that server can be created with different configurations.
    We use ``create_server`` method and then check if ``CONFIG_TYPE`` is right.
    """

    __PRODUCTION_CONFIG_CLASS = 'ProductionConfig'
    __PRODUCTION_CONFIG_EXPECTED_TYPE = 'production'
    __DEVELOPMENT_SERVER_CONFIG_CLASS = 'DevelopmentServerConfig'
    __DEVELOPMENT_SERVER_CONFIG_EXPECTED_TYPE = 'development-server'
    __DEVELOPMENT_LOCAL_CONFIG_CLASS = 'DevelopmentLocalConfig'
    __DEVELOPMENT_LOCAL_CONFIG_EXPECTED_TYPE = 'development-local'
    __TESTING_CONFIG_CLASS = 'TestingConfig'
    __TESTING_CONFIG_EXPECTED_TYPE = 'testing'

    def tearDown(self):
        os.environ['CONFIG_TYPE'] = self.__TESTING_CONFIG_CLASS
    
    def test_production_config(self):
        os.environ['CONFIG_TYPE'] = self.__PRODUCTION_CONFIG_CLASS
        server = create_server()
        self.assertEqual(server.config['CONFIG_TYPE'], self.__PRODUCTION_CONFIG_EXPECTED_TYPE)
    
    def test_development_server_config(self):
        os.environ['CONFIG_TYPE'] = self.__DEVELOPMENT_SERVER_CONFIG_CLASS
        server = create_server()
        self.assertEqual(server.config['CONFIG_TYPE'], self.__DEVELOPMENT_SERVER_CONFIG_EXPECTED_TYPE)
    
    def test_development_local_config(self):
        os.environ['CONFIG_TYPE'] = self.__DEVELOPMENT_LOCAL_CONFIG_CLASS
        server = create_server()
        self.assertEqual(server.config['CONFIG_TYPE'], self.__DEVELOPMENT_LOCAL_CONFIG_EXPECTED_TYPE)
    
    def test_testing_config(self):
        os.environ['CONFIG_TYPE'] = self.__TESTING_CONFIG_CLASS
        server = create_server()
        self.assertEqual(server.config['CONFIG_TYPE'], self.__TESTING_CONFIG_EXPECTED_TYPE)
