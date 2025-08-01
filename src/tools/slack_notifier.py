#!/usr/bin/env python3
"""
Slack Notifier Tool for watsonx Orchestrate

This tool sends notifications to a Slack channel and also sends SMS notifications.
"""

import os
from datetime import datetime
from ibm_watsonx_orchestrate.agent_builder.tools import tool

# Import libraries needed for sending email
import smtplib
from email.message import EmailMessage

# --- SMS NOTIFICATION CONFIGURATION ---
# Your email credentials
EMAIL_ADDRESS = "rushilkakkad1234@gmail.com"
# IMPORTANT: This must be a Gmail "App Password", NOT your regular password.
EMAIL_PASSWORD = "pbcmzyktqlfejgzf"

# Recipient's phone number and carrier gateway for T-Mobile
RECIPIENT_PHONE_NUMBER = "4127373376"
RECIPIENT_CARRIER_GATEWAY = "tmomail.net"
# --- END CONFIGURATION ---

# Function to send the text message via email
def send_text_notification(channel, message):
    """Sends a text message notification using an email-to-sms gateway."""
    
    # Construct the recipient's email address for the SMS gateway
    recipient_email = f"{RECIPIENT_PHONE_NUMBER}@{RECIPIENT_CARRIER_GATEWAY}"
    
    # Construct the body of the text message
    message_body = f"Slack Alert from {channel}:\n{message}"
    
    # Create the email message object
    msg = EmailMessage()
    msg.set_content(message_body)
    msg['Subject'] = f"Alert from {channel}" # Subject line
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = recipient_email
    
    print(f"Preparing to send SMS to {recipient_email}...")
    
    try:
        # Connect securely to the Gmail SMTP server
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            # Log in to your email account
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            # Send the email
            smtp.send_message(msg)
        print("✅ SMS notification sent successfully!")
    except Exception as e:
        # If sending fails, print the error but don't stop the whole tool
        print(f"❌ Failed to send SMS notification. Error: {e}")


@tool(
    name="send_slack_notification",
    description="Sends a mock notification to a Slack channel and sends a text notification."
)
def send_slack_notification(channel: str, message: str):
    """
    Sends a mock notification to a Slack channel.

    :param channel: The Slack channel to send the message to (e.g., #noc-alerts).
    :type channel: str
    :param message: The message to send.
    :type message: str
    :return: A dictionary confirming the message was sent.
    :rtype: dict
    """
    print(f"Sending Slack notification to {channel}:")
    print(f"  Message: {message}\n")

    # --- NEW: Call the function to send the text message ---
    send_text_notification(channel, message)
    
    # In a real scenario, this would involve an API call to Slack.
    # For this mock, we'll just return a confirmation.
    return {
        "status": "sent",
        "channel": channel,
        "message": message
    }
