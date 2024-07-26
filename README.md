# Keycloak API Library
This Library is intended to work with Keycloak 18.0 or Red Hat Single Sign-On 7.6

## Project Structure
```
├── LICENSE
├── README.md
├── keycloak-api
│   ├── __init__.py
│   ├── authentication.py           # Interacts with authentication
│   ├── client-scope.py             # Interacts with client scope
│   ├── client.py
│   ├── identity-providers.py
│   ├── realm.py                    # Interacts with realms
│   ├── roles.py
│   ├── setup.py
│   ├── user-federation.py
│   └── utils
│       └── auth.py                 # Used for authenticating with the Keycloak server
├── requirements.txt
└── setup.py
```

## Convention
- All functions should be in the format of `action_object`