import unittest
from keycloakapi.utils.auth import KeycloakAuth
from keycloakapi import KeycloakRealm
from keycloakapi import KeycloakAuthentication

class TestAuthentication(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        base_url = "http://localhost:8080"
        realm = "master"
        username = "admin"
        password = "admin"
        
        cls.auth = KeycloakAuth(base_url, realm, username, password)
        cls.token = cls.auth.get_token()

        KeycloakRealm(cls.auth).create_realm('test')
        print("Realm created")

    @classmethod
    def tearDownClass(cls):
        #KeycloakRealm(cls.auth).delete_realm('test')
        print("Realm deleted")

    def test_1copy_flow(self):
        response = KeycloakAuthentication(self.auth).copy_flow("test", "browser", "browser2")
        self.assertEqual(response.status_code, 201)

    def test_2get_flow(self):
        response = KeycloakAuthentication(self.auth).get_flow("test", "browser2")
        self.assertIsNotNone(response)
        self.assertEqual(response["alias"], "browser2")

    def test_3get_flows(self):
        response = KeycloakAuthentication(self.auth).get_flows("test")
        self.assertIsNotNone(response)
        default_browser = any(flow["alias"] == "browser" for flow in response)
        self.assertTrue(default_browser)

    def test_4delete_flow(self):
        response = KeycloakAuthentication(self.auth).delete_flow("test", "browser2")
        self.assertEqual(response.status_code, 204)

    def test_5create_flow_blank(self):
        response = KeycloakAuthentication(self.auth).create_flow("test", "test-flow", "basic-flow")
        self.assertEqual(response.status_code, 201)

    
    def test_7add_execution_full(self):
        execution_config = {
            "provider": "no-cookie-redirect"
        }
        response = KeycloakAuthentication(self.auth).add_execution("test", "test-flow", execution_config)
        self.assertEqual(response.status_code, 201)
    
    def test_9add_flowfull(self):
        execution_config = {
            "alias": "flow-alias",
            "type": "basic-flow",
            "description": "flow description"
        }
        response = KeycloakAuthentication(self.auth).add_flow("test", "test-flow", execution_config)
        self.assertEqual(response.status_code, 201)

    def test_get_authenticator_providers(self):
        response = KeycloakAuthentication(self.auth).get_authenticator_providers("test")
        self.assertIsNotNone(response)

    def test_get_authenticator_providers(self):
        response = KeycloakAuthentication(self.auth).get_authenticator_providers("test")
        self.assertIsNotNone(response)

    def test_get_executions(self):
        response = KeycloakAuthentication(self.auth).get_executions("test", "browser")
        self.assertIsNotNone(response)