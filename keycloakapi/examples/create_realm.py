from keycloakapi import KeycloakAuth
from keycloakapi import KeycloakRealm

auth = KeycloakAuth(base_url='http://localhost:8080', realm='master', username='admin', password='admin')
print(auth.get_token())

response = KeycloakRealm(auth).create_realm('test')
print(response.status_code)

realm_details = KeycloakRealm(auth).get_realm('test')
print(realm_details)

response = KeycloakRealm(auth).delete_realm('test')
print(response.status_code)