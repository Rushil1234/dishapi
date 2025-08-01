#!/usr/bin/env python3
"""
Dish Network API Tool for watsonx Orchestrate

This tool provides a set of functions to interact with the Dish Network Mock API.
It allows agents to:
- Get current network outages
- Correlate tower locations
- Calculate the business impact of an outage
"""

import requests
import os
from ibm_watsonx_orchestrate.agent_builder.tools import tool

@tool(
    name="get_network_outages",
    description="Retrieves current network outage events from the Dish Network API."
)
def get_network_outages():
    """
    Retrieves current network outage events from the Dish Network API.

    :return: A dictionary containing a list of outage events.
    :rtype: dict
    """
    base_url = os.environ.get("DISH_API_BASE_URL", "http://192.168.1.111:8081/api")
    response = requests.get(f"{base_url}/outages")
    response.raise_for_status()  # Raise an exception for bad status codes
    return response.json()

@tool(
    name="correlate_tower_locations",
    description="Correlates a list of outage events with their geographic tower locations."
)
def correlate_tower_locations(events: list):
    """
    Correlates a list of outage events with their geographic tower locations.

    :param events: A list of outage event dictionaries.
    :type events: list
    :return: A dictionary containing a list of towers with their location data.
    :rtype: dict
    """
    base_url = os.environ.get("DISH_API_BASE_URL", "http://192.168.1.111:8081/api")
    response = requests.post(f"{base_url}/correlate", json={"events": events})
    response.raise_for_status()
    return response.json()

@tool(
    name="calculate_business_impact",
    description="Calculates the business impact of an outage based on the affected towers."
)
def calculate_business_impact(towers: list):
    """
    Calculates the business impact of an outage based on the affected towers.

    :param towers: A list of tower dictionaries with location data.
    :type towers: list
    :return: A dictionary containing the calculated business impact.
    :rtype: dict
    """
    base_url = os.environ.get("DISH_API_BASE_URL", "http://192.168.1.111:8081/api")
    response = requests.post(f"{base_url}/impact", json={"towers": towers})
    response.raise_for_status()
    return response.json()
