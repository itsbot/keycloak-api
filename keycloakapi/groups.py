import requests 
from keycloakapi import KeycloakRoles
import logging

class KeycloakGroups:
    def __init__(self, auth):
        self.auth = auth

    def create_group(self, realm_name, group_name):
        url = f"{self.auth.base_url}/admin/realms/{realm_name}/groups"
        data = {
            "name": group_name
        }
        response = requests.post(url, headers=self.auth.get_headers(), json=data)
        return response
    
    def get_groups(self, realm_name):
        url = f"{self.auth.base_url}/admin/realms/{realm_name}/groups"
        response = requests.get(url, headers=self.auth.get_headers())
        return response.json()
    
    def get_group(self, realm_name, group_name):
        groups = self.get_groups(realm_name)
        for group in groups:
            if group["name"] == group_name:
                group_id = group["id"]
        url = f"{self.auth.base_url}/admin/realms/{realm_name}/groups/{group_id}"
        response = requests.get(url, headers=self.auth.get_headers())
        return response.json()

    def delete_group(self, realm_name, group_name):
        groups = self.get_groups(realm_name)
        for group in groups:
            if group["name"] == group_name:
                group_id = group["id"]
        url = f"{self.auth.base_url}/admin/realms/{realm_name}/groups/{group_id}"
        response = requests.delete(url, headers=self.auth.get_headers())
        return response

    def get_rolemappings(self, realm_name, group_name):
        group = self.get_group(realm_name, group_name)
        group_id = group["id"]
        url = f"{self.auth.base_url}/admin/realms/{realm_name}/groups/{group_id}/role-mappings/realm"
        response = requests.get(url, headers=self.auth.get_headers())
        return response.json()

    # this should probably go in the role class, but its fine
    def add_rolemapping(self, realm_name, group_name, role_name):
        group = self.get_group(realm_name, group_name)
        group_id = group["id"]
        # Get role details
        role = KeycloakRoles(self.auth).get_role(realm_name, role_name)
        data = [role]
        url = f"{self.auth.base_url}/admin/realms/{realm_name}/groups/{group_id}/role-mappings/realm"
        headers = self.auth.get_headers()
        response = requests.post(url, headers=headers, json=data)
        return response