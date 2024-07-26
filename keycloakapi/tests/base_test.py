import unittest
from keycloakapi.utils.auth import KeycloakAuth

class BaseTestKeycloak(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        base_url = "http://localhost:8080"
        realm = "master"
        username = "admin"
        password = "admin"
        
        cls.auth = KeycloakAuth(base_url, realm, username, password)
        cls.token = cls.auth.get_token()
        
        # Ensure the token is a non-empty string
        assert cls.token is not None
        assert isinstance(cls.token, str)
        assert len(cls.token) > 0

        # Ensure the headers contain the correct Authorization token
        assert "Authorization" in cls.auth.headers
        assert cls.auth.headers["Authorization"] == f"Bearer {cls.token}"