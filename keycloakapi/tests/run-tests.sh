#!/bin/bash

# Start Keycloak container
docker-compose up -d

# Wait for Keycloak to be ready
echo "Waiting for Keycloak to start..."
sleep 10 

# Run tests
pytest

# Stop Keycloak container
docker-compose down