from keycloakapi import KeycloakAuth
from keycloakapi import KeycloakRealm
from keycloakapi import KeycloakClient
from keycloakapi import ClientConfig

auth = KeycloakAuth(base_url='http://localhost:8080', realm='master', username='admin', password='admin')
print(auth.get_token())

response = KeycloakRealm(auth).create_realm('test')
print(response.status_code)

realm_details = KeycloakRealm(auth).get_realm('test')
print(realm_details)

#response = KeycloakRealm(auth).delete_realm('test')
#print(response.status_code)

#client_config = ClientConfig(clientId='test', name='test_client', description='Test Client', rootUrl='http://test.example.com')
client_config = ClientConfig(clientId='test')

response = KeycloakClient(auth).create_client("test", client_config)
print("Create client: ")
print(response.status_code)
print(response)

clients = KeycloakClient(auth).get_clients("test")
print("Get clients: ")
print(clients)

client = KeycloakClient(auth).get_client("test", "test")
print("Get client: ")
print(client)

response = KeycloakClient(auth).delete_client("test", "test")
print("Delete client: ")
print(response)