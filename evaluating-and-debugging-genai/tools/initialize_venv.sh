#!/bin/bash

# Set the path to your virtual environment
project_name="evaluating-and-debugging-genai"
venv_path="/workspaces/exploring/$project_name/venvs"
default_venv="default_venv"
echo "$venv_path/$default_venv"
# Check if the virtual environment directory exists
if [ ! -d "$venv_path/$default_venv" ] ; then
    echo "Virtual environment does not exis"
    echo "Create environment $venv_path/$default_venv"
    python3 -m venv $venv_path/$default_venv --system-site-packages --upgrade-deps
fi
# Activate and install packages
echo "Activating environment: $venv_path/$default_venv/bin/activate"
source "$venv_path/$default_venv/bin/activate"
echo "Installing requirements.txt"
pip install -r requirements.txt
# Install ipykernel
python -m ipykernel install --user --name=$default_venv
