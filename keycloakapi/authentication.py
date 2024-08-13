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

    def get_flows(self, realm_name, flow_alias):
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