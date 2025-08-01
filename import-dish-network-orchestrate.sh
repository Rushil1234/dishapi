#!/bin/bash
#
# This script imports all necessary components for the Dish Network Outage Detection System
# into the local watsonx Orchestrate environment.

# Define the path to the orchestrate executable
ORCHESTRATE_CMD="./dish_venv/bin/orchestrate"

# Import Connections
echo "\nImporting connections..."
$ORCHESTRATE_CMD connections import -f src/connections/dish_api-openapi.json
$ORCHESTRATE_CMD connections import -f src/connections/servicenow-openapi.json
$ORCHESTRATE_CMD connections import -f src/connections/slack-openapi.json

# Import Tools
echo "\nImporting tools..."
$ORCHESTRATE_CMD tools import -f src/tools/dish_network_api.py --kind python --app-id dish-api --package-root src/tools
$ORCHESTRATE_CMD tools import -f src/tools/servicenow_ticket_creator.py --kind python --app-id servicenow --package-root src/tools
$ORCHESTRATE_CMD tools import -f src/tools/slack_notifier.py --kind python --app-id slack --package-root src/tools

# Import Agents
echo "\nImporting agents..."
$ORCHESTRATE_CMD agents import -f src/agents/dish_outage_detection_agent.yaml
$ORCHESTRATE_CMD agents import -f src/agents/dish_incident_management_agent.yaml
$ORCHESTRATE_CMD agents import -f src/agents/dish_noc_supervisor_agent.yaml

echo "\n✅ Import complete!"
echo "Next steps:"
echo "1. Set credentials using ./set-dish-credentials-orchestrate.sh"
echo "2. Start the mock API server: python3 src/mock_services.py &"
echo "3. Start the chat: $ORCHESTRATE_CMD chat start --env-file .env"
