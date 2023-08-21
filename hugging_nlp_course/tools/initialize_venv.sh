#!/bin/bash

# Set the path to your virtual environment
venv_path="/workspaces/exploring/hugging_nlp_course/venvs"
default_venv="default_venv"
echo "$venv_path/$default_venv"
# Check if the virtual environment directory does not exists
if [ ! -d "$venv_path/$default_venv" ] ; then
    echo "Virtual environment does not exis"
    echo "Create environment $venv_path/$default_venv"
    python3 -m venv $venv_path/$default_venv --system-site-packages --upgrade-deps
    echo "Installing requirements.txt"
    pip install -r requirements.txt
    # Install ipykernel
fi
# Activate and install packages
echo "Activating environment: $venv_path/$default_venv/bin/activate"
source "$venv_path/$default_venv/bin/activate"
python -m ipykernel install --user --name=$default_venv
