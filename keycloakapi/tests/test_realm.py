import unittest
import os
from keycloakapi.utils.auth import KeycloakAuth
from keycloakapi import KeycloakRealm

class TestKeycloakRealm(unittest.TestCase):
    def setUp(self):
        base_url = "http://localhost:8080"
        realm = "master"
        username = "admin"
        password = "admin"
        
        self.auth = KeycloakAuth(base_url, realm, username, password)
        self.token = self.auth.get_token()

    def test_1create_realm(self):
        # Create the realm
        response = KeycloakRealm(self.auth).create_realm('dev')
        print(f"Create Realm Response: {response}")
        self.assertEqual(response.status_code, 201)

        response = KeycloakRealm(self.auth).create_realm('staging')
        self.assertEqual(response.status_code, 201)

        response = KeycloakRealm(self.auth).create_realm('prod')
        self.assertEqual(response.status_code, 201)
    
    def test_2delete_realm(self):
        # Delete the realm
        response = KeycloakRealm(self.auth).delete_realm('dev')
        self.assertEqual(response.status_code, 204)

        response = KeycloakRealm(self.auth).delete_realm('staging')
        self.assertEqual(response.status_code, 204)

        response = KeycloakRealm(self.auth).delete_realm('prod')
        self.assertEqual(response.status_code, 204)

    def test_3get_realm(self):
        # Get the realm
        response = KeycloakRealm(self.auth).get_realm('master')
        self.assertIsNotNone(response)
        self.assertEqual(response['realm'], 'master')

    def test_4get_realm_id(self):
        # Get the realm id
        response = KeycloakRealm(self.auth).get_realm_id('master')
        self.assertIsNotNone(response)

    def test_5upload_realm(self):
        # Upload the realm
        realm_file = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'examples', 'test-files', 'realm-export.json'))        
        response = KeycloakRealm(self.auth).upload_realm('uploadedrealm', realm_file)
        self.assertEqual(response.status_code, 201)

        response = KeycloakRealm(self.auth).get_realm('uploadedrealm')
        self.assertIsNotNone(response)

    def test_6update_realm_name(self):
        # Update the realm name
        realm = KeycloakRealm(self.auth).get_realm('uploadedrealm')
        realm['realm'] = 'test2'
        response = KeycloakRealm(self.auth).update_realm('uploadedrealm', realm)
        self.assertEqual(response.status_code, 204)

        response = KeycloakRealm(self.auth).get_realm('test2')
        self.assertIsNotNone(response)

    def test_7update_realm_config(self):
        # Update the realm config
        realm = KeycloakRealm(self.auth).get_realm('test2')
        realm['enabled'] = False
        response = KeycloakRealm(self.auth).update_realm('test2', {"realm": "test2", "enabled": False})
        self.assertEqual(response.status_code, 204)

        response = KeycloakRealm(self.auth).get_realm('test2')
        self.assertIsNotNone(response)
        self.assertFalse(response['enabled'])

        response = KeycloakRealm(self.auth).delete_realm('test2')


if __name__ == '__main__':
    unittest.main()