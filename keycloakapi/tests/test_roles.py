import unittest
from keycloakapi import KeycloakRealm
from keycloakapi.utils.auth import KeycloakAuth
from keycloakapi import KeycloakRoles

class TestRoles(unittest.TestCase):
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

    def test_1create_role(self):
        response = KeycloakRoles(self.auth).create_role('test', 'test_role')
        self.assertEqual(response.status_code, 201)

    def test_2get_roles(self):
        roles = KeycloakRoles(self.auth).get_roles('test')
        self.assertTrue(len(roles) > 0)

    def test_3get_role(self):
        role = KeycloakRoles(self.auth).get_role('test', 'test_role')
        print("ROLE:")
        print(role)
        self.assertEqual(role['name'], 'test_role')

    def test_4delete_role(self):
        response = KeycloakRoles(self.auth).delete_role('test', 'test_role')
        print(response)
        self.assertEqual(response.status_code, 204)