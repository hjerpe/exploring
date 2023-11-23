#!/bin/bash
sudo apt-get --yes install python3.8-venv
SCRIPT_DIR_PARENT=$( cd -- "$( dirname -- "$(dirname -- "${BASH_SOURCE[0]}")" )" &> /dev/null && pwd )
echo source $SCRIPT_DIR_PARENT/tools/initialize_venv.sh >> ~/.bashrc
sudo apt-get --yes update && sudo apt-get --yes upgrade && sudo apt-get install -y python3.8-venv
