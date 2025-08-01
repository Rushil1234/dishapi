#!/usr/bin/env python3
"""
Agent Workflow Simulation Script

This script simulates the workflow of our watsonx Orchestrate agents
using the locally tested tools.
"""

import sys
import os

# Add the src directory to the path so we can import our tools
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from tools.dish_network_api import get_network_outages, correlate_tower_locations, calculate_business_impact
from tools.servicenow_ticket_creator import create_incident_ticket
from tools.slack_notifier import send_slack_notification

def simulate_outage_detection_agent():
    """Simulate the Dish Outage Detection Agent workflow"""
    print("=== Simulating Dish Outage Detection Agent ===\n")
    
    # Step 1: Get current network outages
    print("1. Checking for current network outages...")
    outages = get_network_outages()
    print(f"   Found {len(outages.get('events', []))} outage events\n")
    
    if not outages.get('events'):
        print("No outages detected. Workflow complete.\n")
        return
    
    # Step 2: Correlate tower locations
    print("2. Correlating tower locations...")
    correlated = correlate_tower_locations(outages['events'])
    print(f"   Correlated {len(correlated.get('towers', []))} towers\n")
    
    # Step 3: Calculate business impact
    print("3. Calculating business impact...")
    impact = calculate_business_impact(correlated['towers'])
    print(f"   Affected subscribers: {impact.get('subscribers', 0)}")
    print(f"   Revenue impact: ${impact.get('revenue_impact', 0):,.2f}")
    print(f"   Affected enterprise customers: {len(impact.get('enterprise_customers', []))}\n")
    
    return outages, correlated, impact

def simulate_incident_management_agent(impact):
    """Simulate the Dish Incident Management Agent workflow"""
    print("=== Simulating Dish Incident Management Agent ===\n")
    
    # Step 1: Create ServiceNow ticket
    print("1. Creating ServiceNow incident ticket...")
    description = f"Network outage affecting {impact.get('subscribers', 0)} subscribers " \
                  f"and {len(impact.get('enterprise_customers', []))} enterprise customers. " \
                  f"Estimated revenue impact: ${impact.get('revenue_impact', 0):,.2f}"
    
    # Set priority based on impact
    priority = 1 if impact.get('revenue_impact', 0) > 10000 else 2
    
    ticket = create_incident_ticket(
        short_description="Network Outage Detected",
        long_description=description,
        priority=priority
    )
    print(f"   Created ticket: {ticket.get('ticket_id')}\n")
    
    return ticket

def simulate_noc_supervisor_agent(outages, correlated, impact, ticket):
    """Simulate the Dish NOC Supervisor Agent workflow"""
    print("=== Simulating Dish NOC Supervisor Agent ===\n")
    
    # Step 1: Send Slack notification
    print("1. Sending Slack notification to NOC team...")
    message = f"🚨 NETWORK OUTAGE ALERT 🚨\n\n" \
              f"Outage Details:\n" \
              f"- Affected towers: {len(correlated.get('towers', []))}\n" \
              f"- Affected subscribers: {impact.get('subscribers', 0):,}\n" \
              f"- Enterprise customers affected: {len(impact.get('enterprise_customers', []))}\n" \
              f"- Estimated revenue impact: ${impact.get('revenue_impact', 0):,.2f}\n\n" \
              f"ServiceNow Ticket: {ticket.get('ticket_id')}\n" \
              f"Please investigate immediately."
    
    notification = send_slack_notification("#noc-alerts", message)
    print(f"   {notification.get('message')}\n")

def main():
    """Main function to run the complete agent workflow simulation"""
    print("🚀 Starting Dish Network Outage Detection System Simulation\n")
    
    # Run the outage detection agent
    result = simulate_outage_detection_agent()
    if not result:
        print("No outages detected. System is operating normally.")
        return
    
    outages, correlated, impact = result
    
    # Run the incident management agent
    ticket = simulate_incident_management_agent(impact)
    
    # Run the NOC supervisor agent
    simulate_noc_supervisor_agent(outages, correlated, impact, ticket)
    
    print("✅ Simulation complete. All agents have successfully executed their workflows.")

if __name__ == "__main__":
    main()
