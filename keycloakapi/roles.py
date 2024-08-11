import requests

class KeycloakRoles:
    def __init__(self, auth):
        self.auth = auth

    def create_role(self, realm_name, role_name):
        url = f"{self.auth.base_url}/admin/realms/{realm_name}/roles"
        data = {
            "name": role_name
        }
        response = requests.post(url, headers=self.auth.get_headers(), json=data)
        return response

    def get_roles(self, realm_name):
        url = f"{self.auth.base_url}/admin/realms/{realm_name}/roles"
        response = requests.get(url, headers=self.auth.get_headers())
        return response.json()

    def get_role(self, realm_name, role_name):
        roles = self.get_roles(realm_name)
        for role in roles:
            if role["name"] == role_name:
                role_id = role["id"]
        url = f"{self.auth.base_url}/admin/realms/{realm_name}/roles-by-id/{role_id}"
        response = requests.get(url, headers=self.auth.get_headers())
        return response.json()
    
    def delete_role(self, realm_name, role_name):
        role = self.get_role(realm_name, role_name)
        role_id = role["id"]
        url = f"{self.auth.base_url}/admin/realms/{realm_name}/roles/{role_id}"
        response = requests.delete(url, headers=self.auth.get_headers())
        return response