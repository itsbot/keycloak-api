import requests

class KeycloakClient:
    def __init__(self, auth):
        self.auth = auth

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



class ClientConfig:
    def __init__(self, clientId, name, description, rootUrl):
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

