import requests
import json
from dataclasses import dataclass, field, asdict
from typing import Optional, List
import logging

class KeycloakClient:
    def __init__(self, auth):
        self.auth = auth

    # Create a client
    def create_client(self, realm_name, client_config):
        url = f"{self.auth.base_url}/admin/realms/{realm_name}/clients"
        if isinstance(client_config, ClientConfig):
            data = {
                "clientId": client_config.clientId,
                "name": client_config.name,
                "description": client_config.description,
                "rootUrl": client_config.rootUrl
            }
        else:
            data = client_config
        response = requests.post(url, headers=self.auth.get_headers(), json=data)
        return response

    # Delete a client. Deleting requires the client id, not the client name
    def delete_client(self, realm_name, client_name):
        client = self.get_client(realm_name, client_name)
        if client:
            client_id = client["id"]
            url = f"{self.auth.base_url}/admin/realms/{realm_name}/clients/{client_id}"
            response = requests.delete(url, headers=self.auth.get_headers())
            return response

    # Get a singular client in a realm
    def get_client(self, realm_name, client_name):
        url = f"{self.auth.base_url}/admin/realms/{realm_name}/clients"
        response = requests.get(url, headers=self.auth.get_headers())
        if response.status_code == 200:
            clients = response.json()
            for client in clients:
                if client["clientId"] == client_name:
                    return client
        return None

    # Get all clients in a realm
    def get_clients(self, realm_name):
        url = f"{self.auth.base_url}/admin/realms/{realm_name}/clients"
        response = requests.get(url, headers=self.auth.get_headers())
        return response.json()
    
    # Update a client
    # expects client_config as JSON
    def update_client(self, realm_name, client_name, client_config):
        client = self.get_client(realm_name, client_name)
        if client:
            client_id = client["id"]
            url = f"{self.auth.base_url}/admin/realms/{realm_name}/clients/{client_id}"
            data = client_config
            response = requests.put(url, headers=self.auth.get_headers(), json=data)
            return response

    # Upload a client from a file
    def upload_client(self, realm_name, client_name, file_path):
        with open(file_path, 'r') as file:
            client_config = json.load(file)
        client_config["clientId"] = client_name
        # if client exists, update it
        client = self.get_client(realm_name, client_name)
        if client:
            return self.update_client(realm_name, client_name, client_config)
        # if client does not exist, create it 
        else:
            return self.create_client(realm_name, client_config)
        
    def get_service_account_user_id(self, realm_name, client_name):
        client_id = self.get_client(realm_name, client_name)["id"]
        url = f"{self.auth.base_url}/admin/realms/{realm_name}/clients/{client_id}/service-account-user"
        response = requests.get(url, headers=self.auth.get_headers())
        response.raise_for_status()
        user_info = response.json()  # Parse the JSON content
        
        # Log the response content
        logging.debug(f"Service Account User Info: {user_info}")
        
        if 'id' in user_info:
            return user_info['id']
        else:
            logging.error(f"ID not found in service account user info: {user_info}")
            raise KeyError("ID not found in service account user info")
        
    # Add a role to a service account in a client
    # This should probably be under Users, but this is a start
    def add_service_account_realm_role(self, realm_name, client_name, role_name):
        service_account_id = self.get_service_account_user_id(realm_name, client_name)
        from keycloakapi.roles import KeycloakRoles
        role = KeycloakRoles(self.auth).get_role(realm_name, role_name)
        data = {
            "id": role["id"],
            "name": role_name
        }
        url = f"{self.auth.base_url}/admin/realms/{realm_name}/users/{service_account_id}/role-mappings/realm"
        response = requests.post(url, headers=self.auth.get_headers(), json=[data])  # Send as a list
        response.raise_for_status()
        return response

    # Add a client role to a client
    def add_client_role(self, realm_name, client_name, role_name):
        client = self.get_client(realm_name, client_name)
        client_id = client["id"]
        data = {
            "name": role_name
        }
        url = f"{self.auth.base_url}/admin/realms/{realm_name}/clients/{client_id}/roles"
        response = requests.post(url, headers=self.auth.get_headers(), json=data)
        return response
    
    # Add client role to a service account
    def add_service_account_client_role(self, realm_name, client_name, client_role_client_name, client_role_name):
        service_account_id = self.get_service_account_user_id(realm_name, client_name)
        client_id = self.get_client(realm_name, client_name)["id"]
        
        # Get client role client id
        client_role_client_id = self.get_client(realm_name, client_role_client_name)["id"]
        
        # Get client role details
        url = f"{self.auth.base_url}/admin/realms/{realm_name}/clients/{client_role_client_id}/roles/{client_role_name}"
        response = requests.get(url, headers=self.auth.get_headers())
        response.raise_for_status()
        client_role = response.json()
        
        data = {
            "id": client_role["id"],
            "name": client_role_name,
            "description": client_role.get("description", ""),
            "composite": client_role.get("composite", False),
            "clientRole": client_role.get("clientRole", True),
            "containerId": client_role_client_id
        }
        
        # Add client role to service account
        url = f"{self.auth.base_url}/admin/realms/{realm_name}/users/{service_account_id}/role-mappings/clients/{client_role_client_id}"
        response = requests.post(url, headers=self.auth.get_headers(), json=[data])  # Send as a list
        response.raise_for_status()
        return response

class ClientConfig:
    def __init__(self, clientId, name="", description="", rootUrl=""):
        self.clientId = clientId
        self.name = name
        self.description = description
        self.rootUrl = rootUrl

# @dataclass
# class ClientConfig:
#         clientId: Optional[str] = ""
#         name: Optional[str] = "" 
#         description: Optional[str] = ""
#         rootUrl: Optional[str] = ""
#         adminUrl: Optional[str] = ""
#         baseUrl: Optional[str] = ""
#         surrogateAuthRequired: Optional[bool] = False
#         enabled: Optional[bool] = True
#         alwaysDisplayInConsole: Optional[bool] = False
#         clientAuthenticatorType: Optional[str] = "client-secret"
#         # secret: Optional[str] =  ""
#         registrationAccessToken: Optional[str] = ""
#         defaultRoles: Optional[List[str]] = field(default_factory=list)
#         redirectUris: Optional[List[str]] = field(default_factory=list)
#         webOrigins: Optional[List[str]] = field(default_factory=list)
#         notBefore: Optional[int] =
#         bearerOnly: Optional[bool] = False
#         consentRequired: Optional[bool] = False
#         standardFlowEnabled: Optional[bool] = True
#         implicitFlowEnabled: Optional[bool] = False
#         directAccessGrantsEnabled: Optional[bool] = True
#         serviceAccountsEnabled: Optional[bool] = False
#         authorizationServicesEnabled: Optional[bool] =
#         directGrantsOnly: Optional[bool] = False
#         publicClient: Optional[bool] = True
#         frontchannelLogout: Optional[bool] = False
#         protocol: Optional[str] = "openid-connect"
#         attributes: Optional[] =
#         authenticationFlowBindingOverrides: Optional[] =
#         fullScopeAllowed: Optional[bool] = True
#         nodeReRegistrationTimeout: Optional[int] = -1
#         registeredNodes: Optional[] =
#         protocolMappers = protocolMappers <more>
#         clientTemplate: Optional[str] =
#         useTemplateConfig: Optional[bool] =
#         useTemplateScope: Optional[bool] =
#         useTemplateMappers: Optional[bool] =
#         defaultClientScopes: Optional[List[str]] = field(default_factory=list)
#         optionalClientScopes: Optional[List[str]] = field(default_factory=list)
#         authorizationSettings = authorizationSettings <more>
#         access: Optional[] =
#         origin: Optional[str] =

