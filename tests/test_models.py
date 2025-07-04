"""Tests for data models."""

import pytest
from datetime import datetime
from pydantic import ValidationError

from temp_mail_api.models import EmailAddress, EmailMessage, Domain


class TestEmailAddress:
    """Test cases for EmailAddress model."""
    
    def test_valid_email_address(self):
        """Test creating valid email address."""
        email_addr = EmailAddress(
            email="test@example.com",
            domain="example.com"
        )
        
        assert email_addr.email == "test@example.com"
        assert email_addr.domain == "example.com"
        assert email_addr.username == "test"
        assert isinstance(email_addr.created_at, datetime)
    
    def test_email_validation(self):
        """Test email format validation."""
        with pytest.raises(ValidationError):
            EmailAddress(
                email="invalid-email",
                domain="example.com"
            )
    
    def test_email_lowercase(self):
        """Test email is converted to lowercase."""
        email_addr = EmailAddress(
            email="TEST@EXAMPLE.COM",
            domain="example.com"
        )
        
        assert email_addr.email == "test@example.com"
    
    def test_username_property(self):
        """Test username property extraction."""
        email_addr = EmailAddress(
            email="testuser@example.com",
            domain="example.com"
        )
        
        assert email_addr.username == "testuser"
    
    def test_str_representation(self):
        """Test string representation."""
        email_addr = EmailAddress(
            email="test@example.com",
            domain="example.com"
        )
        
        assert str(email_addr) == "test@example.com"
    
    def test_with_token(self):
        """Test email address with token."""
        email_addr = EmailAddress(
            email="test@example.com",
            domain="example.com",
            token="abc123"
        )
        
        assert email_addr.token == "abc123"


class TestEmailMessage:
    """Test cases for EmailMessage model."""
    
    def test_valid_message(self):
        """Test creating valid email message."""
        message = EmailMessage(
            id="msg123",
            sender="sender@example.com",
            recipient="recipient@example.com",
            subject="Test Subject",
            body="Test body",
            received_at=datetime.now()
        )
        
        assert message.id == "msg123"
        assert message.sender == "sender@example.com"
        assert message.recipient == "recipient@example.com"
        assert message.subject == "Test Subject"
        assert message.body == "Test body"
        assert message.is_read is False
        assert message.attachments == []
    
    def test_message_with_html_body(self):
        """Test message with HTML body."""
        message = EmailMessage(
            id="msg123",
            sender="sender@example.com",
            recipient="recipient@example.com",
            subject="Test Subject",
            body="Test body",
            html_body="<p>Test HTML body</p>",
            received_at=datetime.now()
        )
        
        assert message.html_body == "<p>Test HTML body</p>"
    
    def test_message_with_attachments(self):
        """Test message with attachments."""
        attachments = ["file1.pdf", "file2.jpg"]
        message = EmailMessage(
            id="msg123",
            sender="sender@example.com",
            recipient="recipient@example.com",
            subject="Test Subject",
            body="Test body",
            received_at=datetime.now(),
            attachments=attachments
        )
        
        assert message.attachments == attachments
    
    def test_str_representation(self):
        """Test string representation."""
        message = EmailMessage(
            id="msg123",
            sender="sender@example.com",
            recipient="recipient@example.com",
            subject="Test Subject",
            body="Test body",
            received_at=datetime.now()
        )
        
        assert str(message) == "Email from sender@example.com: Test Subject"
    
    def test_json_encoding(self):
        """Test JSON encoding of datetime."""
        message = EmailMessage(
            id="msg123",
            sender="sender@example.com",
            recipient="recipient@example.com",
            subject="Test Subject",
            body="Test body",
            received_at=datetime.now()
        )
        
        json_data = message.json()
        assert isinstance(json_data, str)
        
        # Parse back to verify datetime encoding
        import json
        parsed = json.loads(json_data)
        assert "received_at" in parsed
        assert isinstance(parsed["received_at"], str)


class TestDomain:
    """Test cases for Domain model."""
    
    def test_valid_domain(self):
        """Test creating valid domain."""
        domain = Domain(name="example.com")
        
        assert domain.name == "example.com"
        assert domain.is_active is True
    
    def test_inactive_domain(self):
        """Test creating inactive domain."""
        domain = Domain(name="example.com", is_active=False)
        
        assert domain.name == "example.com"
        assert domain.is_active is False
    
    def test_str_representation(self):
        """Test string representation."""
        domain = Domain(name="example.com")
        
        assert str(domain) == "example.com"


if __name__ == "__main__":
    pytest.main([__file__]) 