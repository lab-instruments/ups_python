#!/bin/bash

# Install the Virtual Environment Here
python3 -m venv ./venv

# Start Virtual Environment
source ./venv/bin/activate

# Setup Packages
pip install -r requirements.txt

# Exit Python VENV
deactivate
