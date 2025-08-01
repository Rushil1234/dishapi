#!/bin/bash
#
# This script configures and sets credentials for the imported connections.
#

# Define the path to the orchestrate executable
ORCHESTRATE_CMD="./dish_venv/bin/orchestrate"

# Load environment variables from .env file
if [ -f .env ]; then
  export $(grep -v '^#' .env | xargs)
fi

# Configure and set credentials for dish-api
echo "\nConfiguring dish-api connection..."
$ORCHESTRATE_CMD connections configure --app-id dish-api --environment draft --type team --kind api_key --server-url "${DISH_API_BASE_URL:-http://localhost:8080/api}"
echo "Setting credentials for dish-api..."
$ORCHESTRATE_CMD connections set-credentials --app-id dish-api --environment draft --api-key "$DISH_API_KEY"

# Configure and set credentials for servicenow
echo "\nConfiguring servicenow connection..."
$ORCHESTRATE_CMD connections configure --app-id servicenow --environment draft --type team --kind basic --server-url "https://your-instance.service-now.com"
echo "Setting credentials for servicenow..."
$ORCHESTRATE_CMD connections set-credentials --app-id servicenow --environment draft --username "$SERVICENOW_USERNAME" --password "$SERVICENOW_PASSWORD"

# Configure and set credentials for slack
echo "\nConfiguring slack connection..."
$ORCHESTRATE_CMD connections configure --app-id slack --environment draft --type team --kind bearer --server-url "https://slack.com/api"
echo "Setting credentials for slack..."
$ORCHESTRATE_CMD connections set-credentials --app-id slack --environment draft --token "$SLACK_API_TOKEN"

echo "\n✅ Connections configured and credentials set successfully!"
