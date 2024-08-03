import unittest
from keycloakapi import KeycloakRealm
from keycloakapi.utils.auth import KeycloakAuth
from keycloakapi import UserFederationConfig
from keycloakapi.user_federation import KeycloakUserFederation

class TestUserFederation(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        base_url = "http://localhost:8080"
        realm = "master"
        username = "admin"
        password = "admin"
        
        cls.auth = KeycloakAuth(base_url, realm, username, password)
        cls.token = cls.auth.get_token()

        KeycloakRealm(cls.auth).create_realm('test')
        print("Realm created")

    @classmethod
    def tearDownClass(cls):
        KeycloakRealm(cls.auth).delete_realm('test')
        print("Realm deleted")

    def test_acreate_user_federation(self):
        realm_id = KeycloakRealm(self.auth).get_realm_id('test')
        userFederation = UserFederationConfig()
        userFederation.name = "idm"
        userFederation.parentId = realm_id  # Use the fetched realm ID
        userFederation.config.connectionUrl = ["ldap://ldap.example.com:389"]
        userFederation.config.usersDn = ["ou=users,dc=example,dc=com"]
        userFederation.config.bindDn = ["bind.svc"]
        userFederation.config.bindCredential = ["password"]
        response = KeycloakUserFederation(self.auth).create_userFederation('test', userFederation)
        self.assertEqual(response.status_code, 201)

    def test_bget_user_federation(self):
        component = KeycloakUserFederation(self.auth).get_userFederation('test', 'idm')
        self.assertEqual(component['name'], 'idm')

    def test_ccreate_mapper(self):
        response = KeycloakUserFederation(self.auth).get_userFederation('test', 'idm')
        userFederationid = response['id']
        config = {
            "config": {
                "user.model.attribute": ["test"],
                "ldap.attribute": ["test"],
                "read.only": ["true"],
                "always.read.value.from.ldap": ["true"],
                "is.mandatory.in.ldap": ["true"],
                "attribute.default.value": [],
                "is.binary.attribute": ["false"]
            },
            "name": "test",
            "providerId": "user-attribute-ldap-mapper",
            "providerType": "org.keycloak.storage.ldap.mappers.LDAPStorageMapper",
            "parentId": userFederationid
        }
        response = KeycloakUserFederation(self.auth).create_mapper('test', config)
        self.assertEqual(response.status_code, 201)

    
    def test_ddelete_mapper(self):
        response = KeycloakUserFederation(self.auth).delete_mapper('test', 'test')
        self.assertEqual(response.status_code, 204)

