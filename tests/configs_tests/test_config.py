import unittest
import os
from configs.config import create_server

class ConfigTestCase(unittest.TestCase):
    """
    Here we test that server can be created with different configurations.
    We use ``create_server`` method and then check if ``CONFIG_TYPE`` is right.
    """

    __PRODUCTION_CONFIG_CLASSPATH = 'configs.config.ProductionConfig'
    __PRODUCTION_CONFIG_EXPECTED_TYPE = 'production'
    __DEVELOPMENT_SERVER_CONFIG_CLASSPATH = 'configs.config.DevelopmentServerConfig'
    __DEVELOPMENT_SERVER_CONFIG_EXPECTED_TYPE = 'development-server'
    __DEVELOPMENT_LOCAL_CONFIG_CLASSPATH = 'configs.config.DevelopmentLocalConfig'
    __DEVELOPMENT_LOCAL_CONFIG_EXPECTED_TYPE = 'development-local'
    __TESTING_CONFIG_CLASSPATH = 'configs.config.TestingConfig'
    __TESTING_CONFIG_EXPECTED_TYPE = 'testing'

    def tearDown(self):
        os.environ['CONFIG_OBJECT'] = 'configs.config.TestingConfig'
    
    def test_production_config(self):
        os.environ['CONFIG_OBJECT'] = self.__PRODUCTION_CONFIG_CLASSPATH
        server = create_server()
        self.assertEqual(server.config['CONFIG_TYPE'], self.__PRODUCTION_CONFIG_EXPECTED_TYPE)
    
    def test_development_server_config(self):
        os.environ['CONFIG_OBJECT'] = self.__DEVELOPMENT_SERVER_CONFIG_CLASSPATH
        server = create_server()
        self.assertEqual(server.config['CONFIG_TYPE'], self.__DEVELOPMENT_SERVER_CONFIG_EXPECTED_TYPE)
    
    def test_development_local_config(self):
        os.environ['CONFIG_OBJECT'] = self.__DEVELOPMENT_LOCAL_CONFIG_CLASSPATH
        server = create_server()
        self.assertEqual(server.config['CONFIG_TYPE'], self.__DEVELOPMENT_LOCAL_CONFIG_EXPECTED_TYPE)
    
    def test_testing_config(self):
        os.environ['CONFIG_OBJECT'] = self.__TESTING_CONFIG_CLASSPATH
        server = create_server()
        self.assertEqual(server.config['CONFIG_TYPE'], self.__TESTING_CONFIG_EXPECTED_TYPE)
