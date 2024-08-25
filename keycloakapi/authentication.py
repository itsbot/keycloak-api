import requests

class KeycloakAuthentication:
    def __init__(self, auth):
        self.auth = auth

    def copy_flow(self, realm_name, flow_alias, new_flow_alias):
        url = f"{self.auth.base_url}/admin/realms/{realm_name}/authentication/flows/{flow_alias}/copy"
        data = {
            "newName": new_flow_alias
        }
        response = requests.post(url, headers=self.auth.get_headers(), json=data)
        return response

    def get_flow(self, realm_name, flow_alias):
        url = f"{self.auth.base_url}/admin/realms/{realm_name}/authentication/flows"
        response = requests.get(url, headers=self.auth.get_headers())
        if response.status_code == 200:
            flows = response.json()
            for flow in flows:
                if flow["alias"] == flow_alias:
                    return flow
        return response

    def get_flows(self, realm_name):
        url = f"{self.auth.base_url}/admin/realms/{realm_name}/authentication/flows"
        response = requests.get(url, headers=self.auth.get_headers())
        return response.json()
    
    def delete_flow(self, realm_name, flow_alias):
        flow = self.get_flow(realm_name, flow_alias)
        if flow:
            flow_id = flow["id"]
            url = f"{self.auth.base_url}/admin/realms/{realm_name}/authentication/flows/{flow_id}"
            response = requests.delete(url, headers=self.auth.get_headers())
            return response
        
    def create_flow(self, realm_name, flow_alias, flow_type, flow_config=None):
        url = f"{self.auth.base_url}/admin/realms/{realm_name}/authentication/flows"
        if flow_config is None:
            data = {
                "alias": flow_alias,
                "description": "",
                "providerId": flow_type, # client-flow or basic-flow
                "topLevel": True,
                "builtIn": False,
            }
        else:
            data = flow_config
        response = requests.post(url, headers=self.auth.get_headers(), json=data)
        return response

    def add_execution(self, realm_name, flow_alias, execution_config=None):
        url = f"{self.auth.base_url}/admin/realms/{realm_name}/authentication/flows/{flow_alias}/executions/execution"
        response = requests.post(url, headers=self.auth.get_headers(), json=execution_config)
        return response

    def add_flow(self, realm_name, flow_alias, flow_config=None):
        url = f"{self.auth.base_url}/admin/realms/{realm_name}/authentication/flows/{flow_alias}/executions/flow"
        response = requests.post(url, headers=self.auth.get_headers(), json=flow_config)
        return response

    def get_executions(self, realm_name, flow_alias):
        url = f"{self.auth.base_url}/admin/realms/{realm_name}/authentication/flows/{flow_alias}/executions"
        response = requests.get(url, headers=self.auth.get_headers())
        return response.json()
    
    def get_authenticator_providers(self, realm_name):
        url = f"{self.auth.base_url}/admin/realms/{realm_name}/authentication/authenticator-providers"
        response = requests.get(url, headers=self.auth.get_headers())
        return response.json()
    
    def get_client_authenticator_providers(self, realm_name):
        url = f"{self.auth.base_url}/admin/realms/{realm_name}/authentication/client-authenticator-providers"
        response = requests.get(url, headers=self.auth.get_headers())
        return response.json()
    

# {
#     "id": "184b7a3b-f2f3-416b-bcef-52d54a694f6e",
#     "alias": "browser",
#     "description": "browser based authentication",
#     "providerId": "basic-flow",
#     "topLevel": true,
#     "builtIn": true,
#     "authenticationExecutions": [
#         {
#             "authenticator": "auth-cookie",
#             "authenticatorFlow": false,
#             "requirement": "ALTERNATIVE",
#             "priority": 10,
#             "autheticatorFlow": false,
#             "userSetupAllowed": false
#         },
#         {
#             "authenticator": "auth-spnego",
#             "authenticatorFlow": false,
#             "requirement": "DISABLED",
#             "priority": 20,
#             "autheticatorFlow": false,
#             "userSetupAllowed": false
#         },
#         {
#             "authenticator": "identity-provider-redirector",
#             "authenticatorFlow": false,
#             "requirement": "ALTERNATIVE",
#             "priority": 25,
#             "autheticatorFlow": false,
#             "userSetupAllowed": false
#         },
#         {
#             "authenticatorFlow": true,
#             "requirement": "ALTERNATIVE",
#             "priority": 30,
#             "autheticatorFlow": true,
#             "flowAlias": "forms",
#             "userSetupAllowed": false
#         }
#     ]
# }