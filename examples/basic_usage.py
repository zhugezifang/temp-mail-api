#!/usr/bin/env python3
"""
Basic usage example for temp-mail-api.

This script demonstrates how to use the temp-mail-api library
to create temporary email addresses and check for messages.
"""

import time
from temp_mail_api import TempMailClient


def main():
    """Main example function."""
    print("🔥 Temp Mail API Example")
    print("=" * 50)
    
    # Create a client
    client = TempMailClient()
    
    # Get available domains
    print("\n📧 Available domains:")
    domains = client.get_domains()
    for domain in domains[:3]:  # Show first 3 domains
        print(f"  - {domain.name}")
    
    # Create a temporary email address
    print("\n✨ Creating temporary email address...")
    email_addr = client.create_email_address()
    print(f"📩 Created: {email_addr.email}")
    print(f"🔑 Token: {email_addr.token}")
    print(f"📅 Created at: {email_addr.created_at}")
    
    # Check for existing messages
    print("\n📬 Checking for messages...")
    messages = client.get_messages(email_addr.email)
    print(f"Found {len(messages)} messages")
    
    # Display messages
    for i, message in enumerate(messages, 1):
        print(f"\n📨 Message {i}:")
        print(f"  From: {message.sender}")
        print(f"  Subject: {message.subject}")
        print(f"  Body: {message.body[:100]}...")
        print(f"  Received: {message.received_at}")
    
    # Wait for a new message (demo with short timeout)
    print("\n⏳ Waiting for new message (5 seconds)...")
    new_message = client.wait_for_message(email_addr.email, timeout=5.0)
    
    if new_message:
        print(f"📨 New message arrived!")
        print(f"  Subject: {new_message.subject}")
    else:
        print("⏰ No new messages within timeout period")
    
    # Example of using specific domain
    print("\n🎯 Creating email with specific domain...")
    custom_email = client.create_email_address(domain="tempmail.org")
    print(f"📧 Custom email: {custom_email.email}")
    
    # Context manager usage
    print("\n🔧 Using context manager...")
    with TempMailClient() as temp_client:
        another_email = temp_client.create_email_address()
        print(f"📧 Another email: {another_email.email}")
    
    print("\n✅ Example completed!")


if __name__ == "__main__":
    main() 