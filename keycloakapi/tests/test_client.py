import unittest
from keycloakapi.utils.auth import KeycloakAuth
from keycloakapi import KeycloakRealm
from keycloakapi import KeycloakClient
from keycloakapi import ClientConfig

class TestKeycloakRealm(unittest.TestCase):
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

    def test_create_client_blank(self):
        blank_client_config = ClientConfig(clientId='test1')
        response = KeycloakClient(self.auth).create_client("test", blank_client_config)
        self.assertEqual(response.status_code, 201)
    
    def test_create_client_full(self):
        full_client_config = ClientConfig(clientId='test2', name='test2', description='Test Client2', rootUrl='http://test.example.com')
        response = KeycloakClient(self.auth).create_client("test", full_client_config)
        self.assertEqual(response.status_code, 201)

    def test_get_client(self):
        client = KeycloakClient(self.auth).get_client("test", "test1")
        self.assertIsNotNone(client)
        self.assertEqual(client["clientId"], "test1")

    def test_get_clients(self):
        clients = KeycloakClient(self.auth).get_clients("test")
        self.assertIsNotNone(clients)
        for client in clients:
            print(client["clientId"])

    # TODO: fix test order/dependencies
    def test_zdelete_client(self):
        print("Deleting client")
        response = KeycloakClient(self.auth).delete_client("test", "test1")
        self.assertEqual(response.status_code, 204)
        
        

    
