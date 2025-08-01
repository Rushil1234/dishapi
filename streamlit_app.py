#!/usr/bin/env python3
"""
Dish Network Outage Dashboard

A Streamlit application that provides a user-friendly interface for monitoring
and managing Dish Network outages and their business impact.
"""

import streamlit as st
import requests
from datetime import datetime, timezone
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dotenv import load_dotenv
import os
import threading
from flask import Flask, jsonify

# Check if we're running in Streamlit Cloud
IS_STREAMLIT_CLOUD = os.getenv('IS_STREAMLIT_CLOUD', 'false').lower() == 'true'

# Mock API Server (only runs when in Streamlit Cloud)
if IS_STREAMLIT_CLOUD:
    app = Flask(__name__)
    
    @app.route('/health', methods=['GET'])
    def health_check():
        return jsonify({"status": "ok"}), 200
        
    @app.route('/api/outages', methods=['GET'])
    def get_outages():
        current_time = datetime.now(timezone.utc).isoformat()
        outages = {
            "events": [
                {
                    "towerId": "DEN-001",
                    "status": "offline",
                    "timestamp": current_time
                },
                {
                    "towerId": "DEN-002", 
                    "status": "offline",
                    "timestamp": current_time
                }
            ]
        }
        return jsonify(outages)
    
    @app.route('/api/correlate', methods=['POST'])
    def correlate_towers():
        data = request.get_json()
        events = data.get('events', [])
        tower_ids = [event.get('towerId') for event in events if event.get('towerId')]
        
        tower_locations = {
            "DEN-001": {"lat": 39.74, "lon": -104.99},
            "DEN-002": {"lat": 39.75, "lon": -104.98},
        }
        
        towers = []
        for tower_id in tower_ids:
            if tower_id in tower_locations:
                towers.append({
                    "id": tower_id,
                    "lat": tower_locations[tower_id]["lat"],
                    "lon": tower_locations[tower_id]["lon"]
                })
        
        return jsonify({"towers": towers})
    
    @app.route('/api/impact', methods=['POST'])
    def calculate_impact():
        data = request.get_json()
        towers = data.get('towers', [])
        
        num_towers = len(towers)
        subscribers_per_tower = 25000
        enterprise_customers_per_tower = 2
        revenue_per_subscriber = 0.24
        
        total_subscribers = num_towers * subscribers_per_tower
        total_enterprise_customers = num_towers * enterprise_customers_per_tower
        daily_revenue_impact = total_subscribers * revenue_per_subscriber

        enterprise_mapping = {
            "DEN-001": ["Acme Corp", "Globex Inc"],
            "DEN-002": ["Initech", "Cyberdyne Systems"]
        }
        
        enterprise_customers = {}
        for tower in towers:
            if tower['id'] in enterprise_mapping:
                enterprise_customers[tower['id']] = enterprise_mapping[tower['id']]
        
        return jsonify({
            "subscribers_affected": total_subscribers,
            "enterprise_customers_affected": total_enterprise_customers,
            "daily_revenue_impact": daily_revenue_impact,
            "enterprise_customers": enterprise_customers,
            "affected_area": "Denver Metro Area"
        })
    
    def run_flask():
        app.run(host='0.0.0.0', port=8502)
    
    # Start Flask server in a separate thread
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    
    # Update API base URL to point to the embedded server
    API_BASE_URL = 'http://localhost:8502'
else:
    # Local development - use the existing mock server
    load_dotenv()
    API_BASE_URL = os.getenv('MOCK_API_URL', 'http://localhost:8081')

# Load environment variables
load_dotenv()

# Constants
API_BASE_URL = os.getenv('MOCK_API_URL', 'http://localhost:8081')

# Set page config
st.set_page_config(
    page_title="Dish Network Outage Dashboard",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
    <style>
        .main-header {color: #0033A0;}
        .metric-card {
            background-color: #f8f9fa;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }
        .stButton>button {
            background-color: #E31937;
            color: white;
            border: none;
            border-radius: 5px;
            padding: 10px 20px;
            font-weight: bold;
        }
        .stButton>button:hover {
            background-color: #C41234;
            color: white;
        }
        .outage-card {
            border-left: 5px solid #E31937;
            padding: 15px;
            margin-bottom: 10px;
            background-color: #f8f9fa;
            border-radius: 5px;
        }
    </style>
""", unsafe_allow_html=True)

def fetch_outages():
    """Fetch current outages from the mock API."""
    try:
        response = requests.get(f"{API_BASE_URL}/api/outages")
        response.raise_for_status()
        return response.json().get('events', [])
    except requests.RequestException as e:
        st.error(f"Error fetching outages: {e}")
        return []

def correlate_towers(tower_ids):
    """Get location data for tower IDs."""
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/correlate",
            json={"events": [{"towerId": tid} for tid in tower_ids]}
        )
        response.raise_for_status()
        return response.json().get('towers', [])
    except requests.RequestException as e:
        st.error(f"Error correlating towers: {e}")
        return []

def calculate_impact(towers):
    """Calculate business impact for affected towers."""
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/impact",
            json={"towers": towers}
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        st.error(f"Error calculating impact: {e}")
        return {}

def display_outage_map(towers):
    """Display an interactive map showing outage locations."""
    if not towers:
        return
        
    # Create a DataFrame for the map
    df = pd.DataFrame([{
        'Tower ID': t['id'],
        'Latitude': t['lat'],
        'Longitude': t['lon'],
        'Size': 10
    } for t in towers])
    
    # Create the map
    fig = px.scatter_mapbox(
        df,
        lat='Latitude',
        lon='Longitude',
        hover_name='Tower ID',
        size='Size',
        size_max=15,
        zoom=10,
        color_discrete_sequence=['#E31937'],
        title='Outage Locations'
    )
    
    # Update layout for better appearance
    fig.update_layout(
        mapbox_style="open-street-map",
        margin={"r": 0, "t": 30, "l": 0, "b": 0},
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)

def display_impact_metrics(impact_data):
    """Display business impact metrics."""
    if not impact_data:
        return
        
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Affected Subscribers", f"{impact_data.get('subscribers_affected', 0):,}")
    
    with col2:
        st.metric("Enterprise Impact", f"{impact_data.get('enterprise_customers_affected', 0)} companies")
    
    with col3:
        revenue_impact = impact_data.get('daily_revenue_impact', 0)
        st.metric("Daily Revenue Impact", f"${revenue_impact:,.2f}")

def main():
    """Main application function."""
    # Header
    st.title("📡 Dish Network Outage Dashboard")
    st.markdown("---")
    
    # Refresh button
    if st.button("🔄 Refresh Data"):
        st.experimental_rerun()
    
    # Fetch and display outages
    st.header("Current Outages")
    outages = fetch_outages()
    
    if not outages:
        st.info("No current outages detected.")
        return
    
    # Get unique tower IDs
    tower_ids = list({outage['towerId'] for outage in outages if 'towerId' in outage})
    
    # Get tower locations
    towers = correlate_towers(tower_ids)
    
    # Calculate impact
    impact_data = calculate_impact(towers)
    
    # Display impact metrics
    display_impact_metrics(impact_data)
    
    # Create two columns for the layout
    col1, col2 = st.columns([1, 2])
    
    with col1:
        # Display outage details
        st.subheader("Outage Details")
        for outage in outages:
            with st.expander(f"🚨 Tower {outage.get('towerId', 'Unknown')} - {outage.get('status', 'Unknown').title()}"):
                st.write(f"**Status:** {outage.get('status', 'Unknown').title()}")
                st.write(f"**Detected:** {outage.get('timestamp', 'Unknown')}")
                
                # Show enterprise customers if available
                if 'enterprise_customers' in impact_data and outage.get('towerId') in impact_data['enterprise_customers']:
                    st.write("**Affected Enterprise Customers:**")
                    for customer in impact_data['enterprise_customers'][outage['towerId']]:
                        st.write(f"- {customer}")
    
    with col2:
        # Display the map
        st.subheader("Outage Locations")
        display_outage_map(towers)
        
        # Display additional impact information
        if 'affected_area' in impact_data:
            st.subheader("Affected Area")
            st.write(impact_data['affected_area'])
    
    # Display raw data for debugging
    with st.expander("📊 View Raw Data"):
        tab1, tab2, tab3 = st.tabs(["Outages", "Tower Locations", "Impact"])
        
        with tab1:
            st.json(outages)
        
        with tab2:
            st.json(towers)
        
        with tab3:
            st.json(impact_data)
    
    # Footer
    st.markdown("---")
    st.markdown(
        "*Last updated: *" + 
        datetime.now().strftime("%Y-%m-%d %H:%M:%S") +
        " | [Dish Network](https://www.dish.com/)"
    )

if __name__ == "__main__":
    main()
