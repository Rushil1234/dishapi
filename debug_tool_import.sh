#!/bin/bash
#
# This script attempts to import a single tool for debugging purposes.

# Activate local environment
echo "Activating local watsonx Orchestrate environment..."
source dish_venv/bin/activate

# Import a single tool
echo "\nImporting a single tool for debugging..."
orchestrate tools import -f src/tools/dish_network_api.py --kind python

echo "\nDebug script complete."
