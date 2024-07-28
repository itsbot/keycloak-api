import requests
import json

class KeycloakRealm:
    def __init__(self, auth):
        self.auth = auth

    def create_realm(self, realm_name):
        url = f"{self.auth.base_url}/admin/realms"
        data = {
            "realm": realm_name,
            "enabled": True
        }
        response = requests.post(url, headers=self.auth.get_headers(), json=data)
        response.raise_for_status()
        return response

    def delete_realm(self, realm_name):
        url = f"{self.auth.base_url}/admin/realms/{realm_name}"
        response = requests.delete(url, headers=self.auth.get_headers())
        response.raise_for_status()
        return response
    
    def get_realm(self, realm_name):
        url = f"{self.auth.base_url}/admin/realms/{realm_name}"
        response = requests.get(url, headers=self.auth.get_headers())
        if response.status_code == 404:
            return None
        response.raise_for_status()
        return response.json()
    
    def get_realm_id(self, realm_name):
        realm = self.get_realm(realm_name)
        realm_id = realm.get('id')
        return realm_id
    
    def get_realms(self):
        url = f"{self.auth.base_url}/admin/realms"
        response = requests.get(url, headers=self.auth.get_headers())
        response.raise_for_status()
        return response.json()
    
    # TODO: Implement update_realm

    # TODO: support entire configuration for a realm
    # Realm configuration dictionary