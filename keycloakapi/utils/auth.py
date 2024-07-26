import requests
import json

class KeycloakAuth:
    def __init__(self, base_url, realm, username, password, client_id="admin-cli"):
        self.base_url = base_url
        self.realm = realm
        self.username = username
        self.password = password
        self.client_id = client_id
        self.token = None
    
    def get_token(self):
        url = f"{self.base_url}/realms/{self.realm}/protocol/openid-connect/token"
        data = {
            'client_id': 'admin-cli',
            'username': self.username,
            'password': self.password,
            'grant_type': 'password'
        }
        response = requests.post(url, data=data)
        response.raise_for_status()
        self.token = response.json()['access_token']
        return self.token

    def get_headers(self):
        if not self.token:
            self.get_token()
        return {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }