import unittest
from keycloakapi.utils.auth import KeycloakAuth

class TestKeycloakAuth(unittest.TestCase):
    def test_get_access_token(self):
        base_url = "http://localhost:8080"
        realm = "master"
        username = "admin"
        password = "admin"
        
        auth = KeycloakAuth(base_url, realm, username, password)
        token = auth.get_token()
        print(token)
        
        # Ensure the token is a non-empty string
        self.assertIsNotNone(token)
        self.assertIsInstance(token, str)
        self.assertTrue(len(token) > 0)
        
if __name__ == "__main__":
    unittest.main()