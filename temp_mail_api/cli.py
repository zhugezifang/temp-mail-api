#!/usr/bin/env python3
"""
Command-line interface for temp-mail-api.
"""

import argparse
import sys
import json
from typing import Optional

from .client import TempMailClient
from .exceptions import TempMailError


def create_email(args) -> None:
    """Create a new temporary email address."""
    try:
        client = TempMailClient(api_key=args.api_key)
        email = client.create_email_address(domain=args.domain)
        
        if args.json:
            print(json.dumps({
                "email": email.email,
                "domain": email.domain,
                "token": email.token,
                "created_at": email.created_at.isoformat()
            }, indent=2))
        else:
            print(f"📧 Email: {email.email}")
            print(f"🔑 Token: {email.token}")
            print(f"📅 Created: {email.created_at}")
            
    except TempMailError as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


def list_messages(args) -> None:
    """List messages for an email address."""
    try:
        client = TempMailClient(api_key=args.api_key)
        messages = client.get_messages(args.email, limit=args.limit)
        
        if args.json:
            message_data = []
            for msg in messages:
                message_data.append({
                    "id": msg.id,
                    "sender": msg.sender,
                    "subject": msg.subject,
                    "body": msg.body,
                    "received_at": msg.received_at.isoformat(),
                    "is_read": msg.is_read
                })
            print(json.dumps(message_data, indent=2))
        else:
            if not messages:
                print("📪 No messages found")
            else:
                print(f"📬 Found {len(messages)} message(s):")
                for i, msg in enumerate(messages, 1):
                    print(f"\n📨 Message {i}:")
                    print(f"  From: {msg.sender}")
                    print(f"  Subject: {msg.subject}")
                    print(f"  Received: {msg.received_at}")
                    print(f"  Body: {msg.body[:100]}...")
                    
    except TempMailError as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


def get_message(args) -> None:
    """Get a specific message."""
    try:
        client = TempMailClient(api_key=args.api_key)
        message = client.get_message(args.message_id)
        
        if not message:
            print("❌ Message not found", file=sys.stderr)
            sys.exit(1)
            
        if args.json:
            print(json.dumps({
                "id": message.id,
                "sender": message.sender,
                "recipient": message.recipient,
                "subject": message.subject,
                "body": message.body,
                "html_body": message.html_body,
                "received_at": message.received_at.isoformat(),
                "is_read": message.is_read,
                "attachments": message.attachments
            }, indent=2))
        else:
            print(f"📨 Message ID: {message.id}")
            print(f"📧 From: {message.sender}")
            print(f"📧 To: {message.recipient}")
            print(f"📝 Subject: {message.subject}")
            print(f"📅 Received: {message.received_at}")
            print(f"📄 Body:\n{message.body}")
            
    except TempMailError as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


def list_domains(args) -> None:
    """List available domains."""
    try:
        client = TempMailClient(api_key=args.api_key)
        domains = client.get_domains()
        
        if args.json:
            domain_data = [{"name": d.name, "is_active": d.is_active} for d in domains]
            print(json.dumps(domain_data, indent=2))
        else:
            print("📧 Available domains:")
            for domain in domains:
                status = "✅" if domain.is_active else "❌"
                print(f"  {status} {domain.name}")
                
    except TempMailError as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


def wait_for_message(args) -> None:
    """Wait for a new message."""
    try:
        client = TempMailClient(api_key=args.api_key)
        
        print(f"⏳ Waiting for message to {args.email} (timeout: {args.timeout}s)...")
        message = client.wait_for_message(args.email, timeout=args.timeout)
        
        if not message:
            print("⏰ No message received within timeout period")
            return
            
        if args.json:
            print(json.dumps({
                "id": message.id,
                "sender": message.sender,
                "subject": message.subject,
                "body": message.body,
                "received_at": message.received_at.isoformat()
            }, indent=2))
        else:
            print(f"📨 New message received!")
            print(f"📧 From: {message.sender}")
            print(f"📝 Subject: {message.subject}")
            print(f"📄 Body: {message.body}")
            
    except TempMailError as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


def main() -> None:
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Temp Mail API - Command Line Interface",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    # Global arguments
    parser.add_argument(
        "--api-key", 
        help="API key for authentication"
    )
    parser.add_argument(
        "--json", 
        action="store_true",
        help="Output in JSON format"
    )
    
    # Subcommands
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Create email command
    create_parser = subparsers.add_parser("create", help="Create a new temporary email")
    create_parser.add_argument(
        "--domain", 
        help="Specific domain to use"
    )
    create_parser.set_defaults(func=create_email)
    
    # List messages command
    list_parser = subparsers.add_parser("messages", help="List messages for an email")
    list_parser.add_argument(
        "email", 
        help="Email address to check"
    )
    list_parser.add_argument(
        "--limit", 
        type=int, 
        default=10,
        help="Maximum number of messages to return"
    )
    list_parser.set_defaults(func=list_messages)
    
    # Get message command
    get_parser = subparsers.add_parser("get", help="Get a specific message")
    get_parser.add_argument(
        "message_id", 
        help="Message ID to retrieve"
    )
    get_parser.set_defaults(func=get_message)
    
    # List domains command
    domains_parser = subparsers.add_parser("domains", help="List available domains")
    domains_parser.set_defaults(func=list_domains)
    
    # Wait for message command
    wait_parser = subparsers.add_parser("wait", help="Wait for a new message")
    wait_parser.add_argument(
        "email", 
        help="Email address to monitor"
    )
    wait_parser.add_argument(
        "--timeout", 
        type=float, 
        default=60.0,
        help="Timeout in seconds"
    )
    wait_parser.set_defaults(func=wait_for_message)
    
    # Parse arguments
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    # Execute command
    args.func(args)


if __name__ == "__main__":
    main() 