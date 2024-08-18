import requests
import json

class KeycloakRealm:
    def __init__(self, auth):
        self.auth = auth

    def create_realm(self, realm_name, realm_config=None):
        url = f"{self.auth.base_url}/admin/realms"
        if realm_config is None:
            realm_config = {
                "realm": realm_name,
                "enabled": True
            }
        else:
            realm_config["realm"] = realm_name
        response = requests.post(url, headers=self.auth.get_headers(), json=realm_config)
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

    def update_realm(self, realm_name, realm_config):
        realm = self.get_realm(realm_name)
        if realm:
            realm_id = realm["id"]
            url = f"{self.auth.base_url}/admin/realms/{realm_name}/"
            data = realm_config
            response = requests.put(url, headers=self.auth.get_headers(), json=data)
            return response
    
    def upload_realm(self, realm_name, file_path):
        with open(file_path, 'r') as file:
            realm_config = json.load(file)
        realm_config["realm"] = realm_name
        # if realm exists, update it
        realm = self.get_realm(realm_name)
        if realm:
            return self.update_realm(realm_name, realm_config)
        # if realmd does not exist, create it
        else:
            return self.create_realm(realm_name, realm_config)

    # TODO: support entire configuration for a realm
    # Realm configuration dictionary