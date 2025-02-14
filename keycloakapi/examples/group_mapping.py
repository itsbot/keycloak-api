from keycloakapi import KeycloakAuth
from keycloakapi import KeycloakRealm
from keycloakapi import KeycloakGroups
from keycloakapi import KeycloakRoles

auth = KeycloakAuth(base_url='http://localhost:8080', realm='master', username='admin', password='admin')

response = KeycloakRealm(auth).create_realm('test')
print(response.status_code)

group_response = KeycloakGroups(auth).create_group('test', 'test_group')

role_response = KeycloakRoles(auth).create_role('test', 'test_role')

get_groupmapping_response = KeycloakGroups(auth).get_rolemappings('test', 'test_group')
print(get_groupmapping_response)

role_mapping_response = KeycloakGroups(auth).add_rolemapping('test', 'test_group', 'test_role')
print(response.status_code)

get_groupmapping_response = KeycloakGroups(auth).get_rolemappings('test', 'test_group')
print(get_groupmapping_response)