import requests
import json
from dataclasses import dataclass, field, asdict
from typing import Optional, List

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

