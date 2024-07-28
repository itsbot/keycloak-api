import requests

class KeycloakClient:
    def __init__(self, auth):
        self.auth = auth

    # Create a client
    def create_client(self, realm_name, client_config):
        url = f"{self.auth.base_url}/admin/realms/{realm_name}/clients"
        data = {
            "clientId": client_config.clientId,
            "name": client_config.name,
            "description": client_config.description,
            "rootUrl": client_config.rootUrl
        }
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

class ClientConfig:
    def __init__(self, clientId, name="", description="", rootUrl=""):
        self.clientId = clientId
        self.name = name
        self.description = description
        self.rootUrl = rootUrl
#         self.adminUrl = adminUrl
#         self.baseUrl = baseUrl
#         self.surrogateAuthRequired = surrogateAuthRequired
#         self.enabled = enabled
#         self.alwaysDisplayInConsole = alwaysDisplayInConsole
#         self.clientAuthenticatorType = clientAuthenticatorType
#         self.secret = secret
#         self.registrationAccessToken = registrationAccessToken
#         self.redirectUris = redirectUris
#         self.webOrigins = webOrigins
#         self.notBefore = notBefore
#         self.bearerOnly = bearerOnly
#         self.consentRequired = consentRequired
#         self.standardFlowEnabled = standardFlowEnabled
#         self.implicitFlowEnabled = implicitFlowEnabled
#         self.directAccessGrantsEnabled = directAccessGrantsEnabled
#         self.serviceAccountsEnabled = serviceAccountsEnabled
#         self.authorizationServicesEnabled = authorizationServicesEnabled
#         self.directGrantsOnly = directGrantsOnly
#         self.publicClient = publicClient
#         self.frontchannelLogout = frontchannelLogout
#         self.protocol = protocol
#         self.attributes = attributes
#         self.authenticationFlowBindingOverrides = authenticationFlowBindingOverrides
#         self.fullScopeAllowed = fullScopeAllowed
#         self.nodeReRegistrationTimeout = nodeReRegistrationTimeout
#         self.registeredNodes = registeredNodes
#         self.protocolMappers = protocolMappers <more>
#         self.defaultClientScopes = defaultClientScopes
#         self.optionalClientScopes = optionalClientScopes
#         self.authorizationSettings = authorizationSettings <more>
#         self.access = access
#         self.origin = origin

