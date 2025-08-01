#!/usr/bin/env python3
"""
ServiceNow Ticket Creator Tool for watsonx Orchestrate

This tool simulates creating an incident ticket in ServiceNow.
"""

import os
from datetime import datetime
from ibm_watsonx_orchestrate.agent_builder.tools import tool

# Mock function to simulate ticket creation
@tool(
    name="create_incident_ticket",
    description="Creates a mock ServiceNow incident ticket."
)
def create_incident_ticket(short_description: str, long_description: str, priority: int = 3):
    """
    Creates a mock ServiceNow incident ticket.

    :param short_description: A short summary of the incident.
    :type short_description: str
    :param long_description: A detailed description of the incident.
    :type long_description: str
    :param priority: The priority of the ticket (1-5).
    :type priority: int
    :return: A dictionary representing the created ticket.
    :rtype: dict
    """
    ticket_id = f"INC{datetime.now().strftime('%Y%m%d%H%M%S')}"
    print(f"Creating ServiceNow ticket {ticket_id} with priority {priority}:")
    print(f"  Short Description: {short_description}")
    print(f"  Long Description: {long_description}\n")

    # In a real scenario, this would involve an API call to ServiceNow.
    # For this mock, we'll just return a dictionary.
    return {
        "ticket_id": ticket_id,
        "status": "New",
        "short_description": short_description,
        "priority": priority
    }
