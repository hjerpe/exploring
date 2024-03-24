#!/bin/bash

# stop on error
set -e
source docker-name.sh
export PYTHON_APP_IMAGE="$image_name"

# Copy files into the current directory (Docker context)
cp .docker_requirements.txt notebook/
cp .docker_requirements_scientific.txt notebook/

docker-compose up --build
rm notebook/.docker_requirements.txt
rm notebook/.docker_requirements_scientific.txt
