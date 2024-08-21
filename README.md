# Keycloak API Library
This Library is intended to work with Keycloak 18.0 or Red Hat Single Sign-On 7.6

## Project Structure
```
├── LICENSE
├── README.md
├── keycloakapi
│   ├── __init__.py
│   ├── authentication.py           # Interacts with authentication, flows, and executions
│   ├── client.py                   # Interacts with clients
│   ├── client_scope.py             # Interacts with client scope
│   ├── identity_providers.py       # Interacts with identity providers (RHDS only currently)
│   ├── realm.py                    # Interacts with realms
│   ├── roles.py                    # Interacts with roles
│   ├── user_federation.py          # not yet supported
│   └── utils
│       └── auth.py                 # Used for authenticating with the Keycloak server
├── requirements.txt
└── setup.py
```

## Convention
- All functions should be in the format of `action_object`
- Any function that returns an object should return `response.json()` format
  - Exception: get_*_id functions should return the id of the object
- Any function that isn't a `GET` request should return the raw response