"""Tests for TempMailClient."""

import pytest
from unittest.mock import Mock, patch
from datetime import datetime
import requests

from temp_mail_api.client import TempMailClient
from temp_mail_api.models import EmailAddress, EmailMessage, Domain
from temp_mail_api.exceptions import (
    TempMailAPIError,
    TempMailTimeoutError,
    TempMailRateLimitError,
    TempMailAuthenticationError,
)


class TestTempMailClient:
    """Test cases for TempMailClient."""
    
    def test_init_default_values(self):
        """Test client initialization with default values."""
        client = TempMailClient()
        
        assert client.base_url == "https://api.tempmail.org/v1"
        assert client.api_key is None
        assert client.timeout == 30.0
        assert "User-Agent" in client.session.headers
        assert client.session.headers["Content-Type"] == "application/json"
    
    def test_init_with_api_key(self):
        """Test client initialization with API key."""
        api_key = "test-api-key"
        client = TempMailClient(api_key=api_key)
        
        assert client.api_key == api_key
        assert client.session.headers["Authorization"] == f"Bearer {api_key}"
    
    def test_get_domains(self):
        """Test getting available domains."""
        client = TempMailClient()
        domains = client.get_domains()
        
        assert isinstance(domains, list)
        assert len(domains) > 0
        assert all(isinstance(domain, Domain) for domain in domains)
        assert "tempmail.org" in [domain.name for domain in domains]
    
    def test_create_email_address_default_domain(self):
        """Test creating email address with default domain."""
        client = TempMailClient()
        email_addr = client.create_email_address()
        
        assert isinstance(email_addr, EmailAddress)
        assert "@" in email_addr.email
        assert email_addr.domain in email_addr.email
        assert email_addr.token is not None
        assert isinstance(email_addr.created_at, datetime)
    
    def test_create_email_address_specific_domain(self):
        """Test creating email address with specific domain."""
        client = TempMailClient()
        domain = "example.com"
        email_addr = client.create_email_address(domain=domain)
        
        assert email_addr.domain == domain
        assert email_addr.email.endswith(f"@{domain}")
    
    def test_get_messages(self):
        """Test getting messages for an email address."""
        client = TempMailClient()
        email_address = "test@example.com"
        messages = client.get_messages(email_address)
        
        assert isinstance(messages, list)
        assert all(isinstance(msg, EmailMessage) for msg in messages)
        
        if messages:
            msg = messages[0]
            assert msg.recipient == email_address
            assert msg.id is not None
            assert msg.sender is not None
            assert msg.subject is not None
            assert msg.body is not None
    
    def test_get_messages_with_limit(self):
        """Test getting messages with limit parameter."""
        client = TempMailClient()
        email_address = "test@example.com"
        limit = 2
        messages = client.get_messages(email_address, limit=limit)
        
        assert len(messages) <= limit
    
    def test_get_message(self):
        """Test getting a specific message."""
        client = TempMailClient()
        message_id = "test-message-id"
        message = client.get_message(message_id)
        
        assert isinstance(message, EmailMessage)
        assert message.id == message_id
    
    def test_delete_message(self):
        """Test deleting a message."""
        client = TempMailClient()
        message_id = "test-message-id"
        result = client.delete_message(message_id)
        
        assert result is True
    
    @patch('time.sleep')
    def test_wait_for_message_timeout(self, mock_sleep):
        """Test waiting for message with timeout."""
        client = TempMailClient()
        email_address = "test@example.com"
        
        with patch.object(client, 'get_messages', return_value=[]):
            result = client.wait_for_message(email_address, timeout=0.1)
            assert result is None
    
    @patch('time.sleep')
    def test_wait_for_message_success(self, mock_sleep):
        """Test waiting for message with successful result."""
        client = TempMailClient()
        email_address = "test@example.com"
        
        mock_message = EmailMessage(
            id="test-id",
            sender="sender@example.com",
            recipient=email_address,
            subject="Test",
            body="Test body",
            received_at=datetime.now()
        )
        
        with patch.object(client, 'get_messages', return_value=[mock_message]):
            result = client.wait_for_message(email_address, timeout=1.0)
            assert result == mock_message
    
    def test_context_manager(self):
        """Test client as context manager."""
        with TempMailClient() as client:
            assert isinstance(client, TempMailClient)
            assert client.session is not None
    
    @patch('requests.Session.request')
    def test_make_request_success(self, mock_request):
        """Test successful API request."""
        mock_response = Mock()
        mock_response.ok = True
        mock_response.json.return_value = {"success": True}
        mock_request.return_value = mock_response
        
        client = TempMailClient()
        result = client._make_request("GET", "/test")
        
        assert result == {"success": True}
    
    @patch('requests.Session.request')
    def test_make_request_timeout(self, mock_request):
        """Test API request timeout."""
        mock_request.side_effect = requests.exceptions.Timeout()
        
        client = TempMailClient()
        
        with pytest.raises(TempMailTimeoutError):
            client._make_request("GET", "/test")
    
    @patch('requests.Session.request')
    def test_make_request_rate_limit(self, mock_request):
        """Test API request rate limit."""
        mock_response = Mock()
        mock_response.status_code = 429
        mock_response.headers = {"Retry-After": "60"}
        mock_request.return_value = mock_response
        
        client = TempMailClient()
        
        with pytest.raises(TempMailRateLimitError) as exc_info:
            client._make_request("GET", "/test")
        
        assert exc_info.value.retry_after == 60
    
    @patch('requests.Session.request')
    def test_make_request_auth_error(self, mock_request):
        """Test API request authentication error."""
        mock_response = Mock()
        mock_response.status_code = 401
        mock_response.ok = False
        mock_request.return_value = mock_response
        
        client = TempMailClient()
        
        with pytest.raises(TempMailAuthenticationError):
            client._make_request("GET", "/test")
    
    @patch('requests.Session.request')
    def test_make_request_api_error(self, mock_request):
        """Test API request general error."""
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.ok = False
        mock_response.json.return_value = {"message": "Server error"}
        mock_request.return_value = mock_response
        
        client = TempMailClient()
        
        with pytest.raises(TempMailAPIError) as exc_info:
            client._make_request("GET", "/test")
        
        assert exc_info.value.status_code == 500
        assert "Server error" in str(exc_info.value)


if __name__ == "__main__":
    pytest.main([__file__]) 