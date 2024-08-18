from keycloakapi import KeycloakAuth
from keycloakapi import KeycloakRealm
from keycloakapi import KeycloakClient
import os

auth = KeycloakAuth(base_url='http://localhost:8080', realm='master', username='admin', password='admin')

response = KeycloakRealm(auth).create_realm('test')

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