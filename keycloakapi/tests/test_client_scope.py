import unittest
from keycloakapi.utils.auth import KeycloakAuth
from keycloakapi import KeycloakRealm
from keycloakapi import KeycloakClientScope

class TestKeycloakClientScope(unittest.TestCase):
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
        KeycloakRealm(cls.auth).delete_realm('test')
        print("Realm deleted")

    def test_1create_client_scope_blank(self):
        response = KeycloakClientScope(self.auth).create_client_scope("test", "test1")
        self.assertEqual(response.status_code, 201)
    
    def test_2create_client_scope_full(self):
        client_scope_config = {
            "name": "test2",
            "description": "Test Client Scope2",
            "protocol": "openid-connect"
        }
        response = KeycloakClientScope(self.auth).create_client_scope("test", "test2", client_scope_config)
        self.assertEqual(response.status_code, 201)

    def test_3get_client_scope(self):
        client_scope = KeycloakClientScope(self.auth).get_client_scope("test", "test1")
        self.assertIsNotNone(client_scope)
        self.assertEqual(client_scope["name"], "test1")

        client_scope = KeycloakClientScope(self.auth).get_client_scope("test", "test2")
        self.assertIsNotNone(client_scope)
        self.assertEqual(client_scope["name"], "test2")

    def test_4get_client_scopes(self):
        client_scopes = KeycloakClientScope(self.auth).get_client_scopes("test")
        self.assertIsNotNone(client_scopes)

    def test_5delete_client_scope(self):
        response = KeycloakClientScope(self.auth).delete_client_scope("test", "test1")
        self.assertEqual(response.status_code, 204)