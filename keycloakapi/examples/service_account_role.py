from keycloakapi import KeycloakAuth
from keycloakapi import KeycloakRealm
from keycloakapi import KeycloakClient
from keycloakapi import KeycloakRoles
import os

auth = KeycloakAuth(base_url='http://localhost:8080', realm='master', username='admin', password='admin')

response = KeycloakRealm(auth).create_realm('test')
print(response.status_code)

response = KeycloakRoles(auth).create_role('test', 'test_role')
print(response.status_code)

# Use the correct absolute path to the client file
client_file = os.path.join(os.path.dirname(__file__), 'test-files', 'test-client.json')

# Print current working directory and client file path
print("Current Working Directory:", os.getcwd())
print("Client File Path:", client_file)

# Check if the file exists
if not os.path.isfile(client_file):
    print(f"File not found: {client_file}")
else:
    response = KeycloakClient(auth).upload_client("test", "test-client", client_file)
    print(response.status_code)
    print(response)


# add service account realm role to client
response = KeycloakClient(auth).add_service_account_realm_role('test', 'test-client', 'test_role')
print(response)

# Add client role
response = KeycloakClient(auth).add_client_role('test', 'test-client', 'test_role')
print(response)

# Add service account client role
response = KeycloakClient(auth).add_service_account_client_role('test', 'test-client', 'realm-management','create-client')
print(response)

