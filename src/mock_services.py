#!/usr/bin/env python3
"""
Flask Mock Server for Dish Network Outage Detection Demo

This server provides three endpoints that simulate real network monitoring APIs:
1. GET /api/outages - Returns current outage events
2. POST /api/correlate - Correlates tower IDs with geographic coordinates
3. POST /api/impact - Calculates business impact of outages
"""

from flask import Flask, request, jsonify
from datetime import datetime, timezone
import json

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health_check():
    """GET /health - Health check endpoint"""
    return jsonify({"status": "ok"}), 200

@app.route('/api/outages', methods=['GET'])
def get_outages():
    """GET /api/outages - Returns current outage events"""
    print(f"[{datetime.now()}] GET /api/outages - Returning outage events")
    
    # Simulate two towers offline in Denver
    current_time = datetime.now(timezone.utc).isoformat()
    
    outages = {
        "events": [
            {
                "towerId": "DEN-001",
                "status": "offline",
                "timestamp": "2025-07-28T14:00:00Z"
            },
            {
                "towerId": "DEN-002", 
                "status": "offline",
                "timestamp": "2025-07-28T14:01:00Z"
            }
        ]
    }
    
    print(f"[{datetime.now()}] Response: {json.dumps(outages, indent=2)}")
    return jsonify(outages)

@app.route('/api/correlate', methods=['POST'])
def correlate_towers():
    """POST /api/correlate - Correlates tower IDs with geographic coordinates"""
    print(f"[{datetime.now()}] POST /api/correlate")
    print(f"[{datetime.now()}] Request body: {json.dumps(request.get_json(), indent=2)}")
    
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
    
    response = {"towers": towers}
    print(f"[{datetime.now()}] Response: {json.dumps(response, indent=2)}")
    return jsonify(response)

@app.route('/api/impact', methods=['POST'])
def calculate_impact():
    """POST /api/impact - Calculates business impact of outages"""
    print(f"[{datetime.now()}] POST /api/impact")
    print(f"[{datetime.now()}] Request body: {json.dumps(request.get_json(), indent=2)}")
    
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
    
    affected_enterprise_customers = []
    for tower in towers:
        affected_enterprise_customers.extend(enterprise_mapping.get(tower.get('id'), []))

    response = {
        "subscribers": total_subscribers,
        "enterprise_customers": list(set(affected_enterprise_customers)),
        "revenue_impact": daily_revenue_impact
    }
    
    print(f"[{datetime.now()}] Response: {json.dumps(response, indent=2)}")
    return jsonify(response)

if __name__ == '__main__':
    print("🔥 Starting Dish Network Mock API Server...")
    app.run(host='0.0.0.0', port=8081)
