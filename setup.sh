#!/bin/bash

# This script ensures the Streamlit app can access the mock API in the cloud environment

echo "Setting up environment for Streamlit Cloud..."

# Set the IS_STREAMLIT_CLOUD environment variable
export IS_STREAMLIT_CLOUD="true"

# Start the Streamlit app
streamlit run streamlit_app.py
