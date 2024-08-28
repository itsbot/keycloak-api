#!/bin/bash
# Syntax changes for macos

# List of Keycloak versions to test against
keycloak_versions=("18.0.2" "25.0.2" "latest")

# Function to wait for Keycloak to be responsive
wait_for_keycloak() {
    url=$1
    echo "Waiting for Keycloak at $url to be responsive..."
    while ! curl -s $url > /dev/null; do
        sleep 1
    done
}

# Loop through each version
for version in "${keycloak_versions[@]}"; do
    echo "Testing against Keycloak version $version"

    # Update the docker-compose file to use the specific Keycloak version
    sed -i "" "s|/keycloak:.*|/keycloak:$version|g" docker-compose.yml

    # Start Keycloak container
    docker compose up -d

    # Wait for Keycloak to be responsive
    wait_for_keycloak "http://localhost:8080/"

    # Run tests
    pytest

    # Stop Keycloak container
    docker compose down
done
