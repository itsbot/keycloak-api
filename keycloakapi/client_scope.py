import requests

class KeycloakClientScope:
    def __init__(self, auth):
        self.auth = auth

    def create_client_scope(self, realm_name, client_scope_name, client_scope_config=None):
        url = f"{self.auth.base_url}/admin/realms/{realm_name}/client-scopes"
        if client_scope_config is None:
            client_scope_config = {
                "name": client_scope_name,
                "protocol": "openid-connect"
            }
        else:
            client_scope_config["name"] = client_scope_name
        response = requests.post(url, headers=self.auth.get_headers(), json=client_scope_config)
        return response
    
    def delete_client_scope(self, realm_name, client_scope_name):
        client_scope = self.get_client_scope(realm_name, client_scope_name)
        if client_scope:
            client_scope_id = client_scope["id"]
            url = f"{self.auth.base_url}/admin/realms/{realm_name}/client-scopes/{client_scope_id}"
            response = requests.delete(url, headers=self.auth.get_headers())
            return response
        
    def get_client_scope(self, realm_name, client_scope_name):
        client_scope_id = self.get_client_scope_id(realm_name, client_scope_name)
        url = f"{self.auth.base_url}/admin/realms/{realm_name}/client-scopes/{client_scope_id}"
        response = requests.get(url, headers=self.auth.get_headers())
        return response.json()

    def get_client_scope_id(self, realm_name, client_scope_name):
        client_scopes = self.get_client_scopes(realm_name)
        for client_scope in client_scopes:
            if client_scope["name"] == client_scope_name:
                return client_scope["id"]
        return None
    
    def get_client_scopes(self, realm_name):
        url = f"{self.auth.base_url}/admin/realms/{realm_name}/client-scopes"
        response = requests.get(url, headers=self.auth.get_headers())
        return response.json()
    
    def update_client_scope(self, realm_name, client_scope_name, client_scope_config):
        client_scope = self.get_client_scope(realm_name, client_scope_name)
        if client_scope:
            client_scope_id = client_scope["id"]
            url = f"{self.auth.base_url}/admin/realms/{realm_name}/client-scopes/{client_scope_id}"
            response = requests.put(url, headers=self.auth.get_headers(), json=client_scope_config)
            return response
        