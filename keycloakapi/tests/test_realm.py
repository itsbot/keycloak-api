import unittest
from base_test import BaseTestKeycloak
from keycloakapi import KeycloakRealm

class TestKeycloakRealm(BaseTestKeycloak):
    def setUp(self):
        super().setUp()
        self.realms = KeycloakRealm(self.auth)

    def test_create_realm(self):
        # Create the realm
        response = self.realms.create_realm('example_realm', 'Example Realm')
        self.assertEqual(response['realm'], 'example_realm')

        # Verify the realm exists
        realm_exists = self.realms.get_realm('example_realm')
        self.assertIsNotNone(realm_exists)

        # Clean up by deleting the realm
        self.realms.delete_realm('example_realm')

    def test_delete_realm(self):
        # Create the realm to ensure it exists
        self.realms.create_realm('example_realm', 'Example Realm')

        # Delete the realm
        self.realms.delete_realm('example_realm')


if __name__ == '__main__':
    unittest.main()