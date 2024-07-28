import unittest
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

    def test_create_realm(self):
        # Create the realm
        response = KeycloakRealm(self.auth).create_realm('dev')
        print(f"Create Realm Response: {response}")
        self.assertEqual(response.status_code, 201)

        response = KeycloakRealm(self.auth).create_realm('staging')
        self.assertEqual(response.status_code, 201)

        response = KeycloakRealm(self.auth).create_realm('prod')
        self.assertEqual(response.status_code, 201)
    
    def test_delete_realm(self):
        # Delete the realm
        response = KeycloakRealm(self.auth).delete_realm('dev')
        self.assertEqual(response.status_code, 204)

        response = KeycloakRealm(self.auth).delete_realm('staging')
        self.assertEqual(response.status_code, 204)

        response = KeycloakRealm(self.auth).delete_realm('prod')
        self.assertEqual(response.status_code, 204)

if __name__ == '__main__':
    unittest.main()