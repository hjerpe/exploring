#!/bin/bash
project_name="evaluating-and-debugging-genai"
echo 'source /workspaces/exploring/$project_name/tools/initialize_venv.sh' >> ~/.bashrc
sudo apt-get --yes update && sudo apt-get --yes upgrade && sudo apt-get install --yes vim && sudo apt-get install --yes tree
