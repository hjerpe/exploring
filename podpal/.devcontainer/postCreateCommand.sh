#!/bin/bash
#project_name="PodPal"
SCRIPT_DIR_PARENT=$( cd -- "$( dirname -- "$(dirname -- "${BASH_SOURCE[0]}")" )" &> /dev/null && pwd )
echo source $SCRIPT_DIR_PARENT/tools/initialize_venv.sh >> ~/.bashrc
sudo apt-get --yes update && sudo apt-get --yes upgrade
