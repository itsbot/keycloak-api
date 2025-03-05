from keycloakapi import KeycloakAuth
from keycloakapi import KeycloakRealm
from keycloakapi import KeycloakClientScope
import os
import json
import logging

auth = KeycloakAuth(base_url='http://localhost:8080', realm='master', username='admin', password='admin')

response = KeycloakRealm(auth).create_realm('test')

response = KeycloakClientScope(auth).create_client_scope('test', 'test_client_scope')
print(response)

response = KeycloakClientScope(auth).get_client_scope('test', 'test_client_scope')
print(response)


mapper_file = os.path.join(os.path.dirname(__file__), 'test-files', 'client-scope-mapper.json')
mapper_config = json.load(open(mapper_file))
print(mapper_config)




# Extract values from the mapper configuration
realm_name = 'test'
client_scope_id = KeycloakClientScope(auth).get_client_scope_id(realm_name, 'test_client_scope')
mapper_name = mapper_config["name"]
user_attribute = mapper_config["config"]["user.attribute"]
claim_name = mapper_config["config"]["claim.name"]

# Add the client scope mapper
response = KeycloakClientScope(auth).add_client_scope_mapper(realm_name, client_scope_id, mapper_name, user_attribute, claim_name)
print(response.status_code)