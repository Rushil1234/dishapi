#!/usr/bin/env python3
"""
SMS Test Script for Slack Notifier

This script tests the SMS notification functionality directly.
"""

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

def test_sms_notification():
    """Test function to send an SMS notification."""
    
    # Test message details
    channel = "#test-channel"
    message = "This is a test SMS from your Dish Network Outage Detection System!"
    
    # Construct the recipient's email address for the SMS gateway
    recipient_email = f"{RECIPIENT_PHONE_NUMBER}@{RECIPIENT_CARRIER_GATEWAY}"
    
    # Construct the body of the text message
    message_body = f"Slack Alert from {channel}:\n{message}"
    
    # Create the email message object
    msg = EmailMessage()
    msg.set_content(message_body)
    msg['Subject'] = f"TEST Alert from {channel}"
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = recipient_email
    
    print(f"🧪 Testing SMS notification...")
    print(f"📧 Sending to: {recipient_email}")
    print(f"📱 Phone: {RECIPIENT_PHONE_NUMBER}")
    print(f"📨 Message: {message}")
    print(f"🔄 Attempting to send...")
    
    try:
        # Connect securely to the Gmail SMTP server
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            # Log in to your email account
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            # Send the email
            smtp.send_message(msg)
        print("✅ SMS notification sent successfully!")
        print("📱 Check your phone for the test message!")
        return True
    except Exception as e:
        # If sending fails, print the error
        print(f"❌ Failed to send SMS notification. Error: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Starting SMS Test...")
    success = test_sms_notification()
    if success:
        print("\n🎉 SMS test completed successfully!")
        print("📱 You should receive a text message shortly.")
    else:
        print("\n❌ SMS test failed. Check your credentials and try again.")
