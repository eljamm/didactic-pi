#!/bin/bash

# Get Machine Architecture
ARCH=$(uname -m)
COMPOSE_VERSION="2.8.0"

# Install docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install docker-compose
sudo curl -L --fail "https://github.com/docker/compose/releases/download/v${COMPOSE_VERSION}/docker-compose-linux-${ARCH}" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Add user to docker group
sudo usermod -aG docker $USER

# Activate changes to groups
newgrp docker
