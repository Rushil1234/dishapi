#!/bin/bash

# Activate virtual environment
source dish_venv/bin/activate

# Install required packages
echo "Installing required packages..."
pip install -r requirements-streamlit.txt

# Start the mock API server in the background
echo "Starting mock API server..."
python src/mock_services.py &
MOCK_API_PID=$!

# Give the server a moment to start
sleep 3

# Start Streamlit app
echo "Starting Streamlit app..."
streamlit run streamlit_app.py

# Cleanup function to stop the mock API server when the script exits
cleanup() {
    echo "Stopping mock API server (PID: $MOCK_API_PID)"
    kill $MOCK_API_PID
}

# Set trap to ensure cleanup runs when the script exits
trap cleanup EXIT
