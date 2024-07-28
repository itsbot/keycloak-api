import requests
from dataclasses import dataclass, field

class KeycloakUserFederation:
    def __init__(self, auth):
        self.auth = auth

    # Works, but is a little janky
    def create_userFederation(self, realm_name, userFederation_config):
        url = f"{self.auth.base_url}/admin/realms/{realm_name}/components"
        config_dict = userFederation_config.__dict__.copy()
        config_dict['config'] = userFederation_config.config.to_dict()
        response = requests.post(url, headers=self.auth.get_headers(), json=config_dict)
        return response
    
    def delete_userFederation(self, realm_name, userFederation_name):
        component = self.get_userFederation(realm_name, userFederation_name)
        if component:
            component_id = component["id"]
            url = f"{self.auth.base_url}/admin/realms/{realm_name}/components/{component_id}"
            response = requests.delete(url, headers=self.auth.get_headers())
            return response
    
    # Get a singular userFederation in a realm
    def get_userFederation(self, realm_name, userFederation_name):
        url = f"{self.auth.base_url}/admin/realms/{realm_name}/components"
        response = requests.get(url, headers=self.auth.get_headers())
        if response.status_code == 200:
            components = response.json()
            for component in components:
                if component["name"] == userFederation_name:
                    return component

class Config:
    def __init__(self, initial_config):
        self._config = initial_config

    def __getattr__(self, item):
        return self._config.get(item, None)

    def __setattr__(self, key, value):
        if key == "_config":
            super().__setattr__(key, value)
        else:
            self._config[key] = value

    def to_dict(self):
        return self._config

# TODO: Clean up default values
# TODO: support for non-ldap?
@dataclass
class UserFederationConfig:
    name: str = "ldap"
    providerId: str = "ldap"
    providerType: str = "org.keycloak.storage.UserStorageProvider"
    parentId: str = ""
    config: Config = field(default_factory=lambda: Config({
        "enabled": ["true"],
        "priority": ["0"],
        "fullSyncPeriod": ["-1"],
        "changedSyncPeriod": ["-1"],
        "cachePolicy": ["DEFAULT"],
        "evictionDay": [],
        "evictionHour": [],
        "evictionMinute": [],
        "maxLifespan": [],
        "batchSizeForSync": ["1000"],
        "editMode": ["WRITABLE"],
        "importEnabled": ["true"],
        "syncRegistrations": ["false"],
        "vendor": ["rhds"],
        "usePasswordModifyExtendedOp": [],
        "usernameLDAPAttribute": ["uid"],
        "rdnLDAPAttribute": ["uid"],
        "uuidLDAPAttribute": ["nsuniqueid"],
        "userObjectClasses": ["inetOrgPerson, organizationalPerson"],
        "connectionUrl": ["ldaps://ldap.example.com"],
        "usersDn": ["ou=users,dc=example,dc=com"],
        "authType": ["simple"],
        "startTls": [],
        "bindDn": ["bind.svc"],
        "bindCredential": ["password"],
        "customUserSearchFilter": [],
        "searchScope": ["1"],
        "validatePasswordPolicy": ["false"],
        "trustEmail": ["false"],
        "useTruststoreSpi": ["ldapsOnly"],
        "connectionPooling": ["true"],
        "connectionPoolingAuthentication": [],
        "connectionPoolingDebug": [],
        "connectionPoolingInitSize": [],
        "connectionPoolingMaxSize": [],
        "connectionPoolingPrefSize": [],
        "connectionPoolingProtocol": [],
        "connectionPoolingTimeout": [],
        "connectionTimeout": [],
        "readTimeout": [],
        "pagination": ["true"],
        "allowKerberosAuthentication": ["false"],
        "serverPrincipal": [],
        "keyTab": [],
        "kerberosRealm": [],
        "debug": ["false"],
        "useKerberosForPasswordAuthentication": ["false"]
    }))

#     {
#     "name": "ldap",
#     "providerId": "ldap",
#     "providerType": "org.keycloak.storage.UserStorageProvider",
#     "parentId": "0620dce6-83fd-47a6-8d51-914ff891f100",
#     "config": {
#         "enabled": ["true"],
#         "priority": ["0"],
#         "fullSyncPeriod": ["-1"],
#         "changedSyncPeriod": ["-1"],
#         "cachePolicy": ["DEFAULT"],
#         "evictionDay": [],
#         "evictionHour": [],
#         "evictionMinute": [],
#         "maxLifespan": [],
#         "batchSizeForSync": ["1000"],
#         "editMode": ["WRITABLE"],
#         "importEnabled": ["true"],
#         "syncRegistrations": ["false"],
#         "vendor": ["rhds"],
#         "usePasswordModifyExtendedOp": [],
#         "usernameLDAPAttribute": ["uid"],
#         "rdnLDAPAttribute": ["uid"],
#         "uuidLDAPAttribute": ["nsuniqueid"],
#         "userObjectClasses": ["inetOrgPerson, organizationalPerson"],
#         "connectionUrl": ["ldaps://ldap.example.com"],
#         "usersDn": ["ou=users,dc=example,dc=com"],
#         "authType": ["simple"],
#         "startTls": [],
#         "bindDn": ["bind.svc"],
#         "bindCredential": ["password"],
#         "customUserSearchFilter": [],
#         "searchScope": ["1"],
#         "validatePasswordPolicy": ["false"],
#         "trustEmail": ["false"],
#         "useTruststoreSpi": ["ldapsOnly"],
#         "connectionPooling": ["true"],
#         "connectionPoolingAuthentication": [],
#         "connectionPoolingDebug": [],
#         "connectionPoolingInitSize": [],
#         "connectionPoolingMaxSize": [],
#         "connectionPoolingPrefSize": [],
#         "connectionPoolingProtocol": [],
#         "connectionPoolingTimeout": [],
#         "connectionTimeout": [],
#         "readTimeout": [],
#         "pagination": ["true"],
#         "allowKerberosAuthentication": ["false"],
#         "serverPrincipal": [],
#         "keyTab": [],
#         "kerberosRealm": [],
#         "debug": ["false"],
#         "useKerberosForPasswordAuthentication": ["false"]
#     }
# }