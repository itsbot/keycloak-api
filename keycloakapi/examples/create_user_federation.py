from keycloakapi import KeycloakAuth
from keycloakapi import KeycloakRealm
from keycloakapi import UserFederationConfig
from keycloakapi.user_federation import KeycloakUserFederation
import requests
import json

auth = KeycloakAuth(base_url='http://localhost:8080', realm='master', username='admin', password='admin')
KeycloakRealm(auth).create_realm('test')

# Fetch the realm ID
realm_url = f"{auth.base_url}/admin/realms/test"
headers = auth.get_headers()
realm_response = requests.get(realm_url, headers=headers)
realm_id = realm_response.json().get('id')

# Ensure realm ID is fetched correctly
if not realm_id:
    raise ValueError("Failed to fetch realm ID")

userFederation = UserFederationConfig()
userFederation.name = "idm"
userFederation.parentId = realm_id  # Use the fetched realm ID
userFederation.config.connectionUrl = ["ldap://ldap.example.com:389"]
userFederation.config.usersDn = ["ou=users,dc=example,dc=com"]
userFederation.config.bindDn = ["bind.svc"]
userFederation.config.bindCredential = ["password"]

print(userFederation)

response = KeycloakUserFederation(auth).create_userFederation('test', userFederation)
print(response.status_code)
print(response)

# url = f"{auth.base_url}/admin/realms/test/components"
# headers = auth.get_headers()
# response = requests.get(url, headers=headers)
# print(response.status_code)
# print(json.dumps(response.json(), indent=4))

response = KeycloakUserFederation(auth).get_userFederation('test', 'idm')
print(response)

#response = KeycloakUserFederation(auth).delete_userFederation('test', 'idm')
#print(response)