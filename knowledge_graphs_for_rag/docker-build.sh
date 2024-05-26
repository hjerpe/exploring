#!/bin/bash

# stop on error
set -e
source docker-name.sh
source .neo4j-env.sh
export PYTHON_APP_IMAGE="$image_name"
export NEO4J_PASSWORD="$NEO4J_PASSWORD"

docker-compose up --build
