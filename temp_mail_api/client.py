"""Main client for temp mail API."""

import time
import random
import string
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from .models import EmailAddress, EmailMessage, Domain
from .exceptions import (
    TempMailError,
    TempMailAPIError,
    TempMailTimeoutError,
    TempMailAuthenticationError,
    TempMailRateLimitError,
)


class TempMailClient:
    """Client for interacting with temporary email services."""
    
    def __init__(
        self,
        base_url: str = "https://api.tempmail.org/v1",
        api_key: Optional[str] = None,
        timeout: float = 30.0,
        max_retries: int = 3,
        backoff_factor: float = 0.3,
    ):
        """
        Initialize the TempMailClient.
        
        Args:
            base_url: Base URL for the API
            api_key: API key for authentication (if required)
            timeout: Request timeout in seconds
            max_retries: Maximum number of retries
            backoff_factor: Backoff factor for retries
        """
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.timeout = timeout
        
        # Setup requests session with retry strategy
        self.session = requests.Session()
        retry_strategy = Retry(
            total=max_retries,
            backoff_factor=backoff_factor,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
        
        # Set headers
        self.session.headers.update({
            "User-Agent": "temp-mail-api-python/0.1.0",
            "Content-Type": "application/json",
        })
        
        if self.api_key:
            self.session.headers["Authorization"] = f"Bearer {self.api_key}"
    
    def _make_request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Make an HTTP request to the API.
        
        Args:
            method: HTTP method
            endpoint: API endpoint
            params: Query parameters
            data: Request body data
            **kwargs: Additional arguments for requests
            
        Returns:
            Response data as dictionary
            
        Raises:
            TempMailAPIError: If API returns an error
            TempMailTimeoutError: If request times out
            TempMailRateLimitError: If rate limit is exceeded
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        try:
            response = self.session.request(
                method=method,
                url=url,
                params=params,
                json=data,
                timeout=self.timeout,
                **kwargs
            )
            
            # Handle rate limiting
            if response.status_code == 429:
                retry_after = int(response.headers.get('Retry-After', 60))
                raise TempMailRateLimitError(
                    "Rate limit exceeded",
                    retry_after=retry_after
                )
            
            # Handle authentication errors
            if response.status_code == 401:
                raise TempMailAuthenticationError("Invalid API key or authentication failed")
            
            # Handle other HTTP errors
            if not response.ok:
                error_data = {}
                try:
                    error_data = response.json()
                except:
                    pass
                
                raise TempMailAPIError(
                    error_data.get('message', f"HTTP {response.status_code} error"),
                    status_code=response.status_code,
                    response_data=error_data
                )
            
            return response.json()
            
        except requests.exceptions.Timeout:
            raise TempMailTimeoutError(f"Request timed out after {self.timeout}s")
        except requests.exceptions.RequestException as e:
            raise TempMailAPIError(f"Request failed: {str(e)}")
    
    def get_domains(self) -> List[Domain]:
        """
        Get list of available email domains.
        
        Returns:
            List of available domains
        """
        # Mock implementation - in real API, this would fetch from server
        domains = [
            "tempmail.org",
            "guerrillamail.com", 
            "10minutemail.com",
            "mailinator.com",
            "temp-mail.org"
        ]
        return [Domain(name=domain) for domain in domains]
    
    def create_email_address(self, domain: Optional[str] = None) -> EmailAddress:
        """
        Create a new temporary email address.
        
        Args:
            domain: Specific domain to use (optional)
            
        Returns:
            New email address
        """
        if not domain:
            domains = self.get_domains()
            domain = random.choice(domains).name
        
        # Generate random username
        username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        email = f"{username}@{domain}"
        
        # In a real implementation, this would call the API
        # For now, we'll create a mock response
        return EmailAddress(
            email=email,
            domain=domain,
            token=self._generate_token(),
            created_at=datetime.now()
        )
    
    def get_messages(
        self,
        email_address: str,
        limit: int = 10,
        offset: int = 0
    ) -> List[EmailMessage]:
        """
        Get messages for an email address.
        
        Args:
            email_address: Email address to check
            limit: Maximum number of messages to return
            offset: Number of messages to skip
            
        Returns:
            List of email messages
        """
        # Mock implementation - in real API, this would fetch from server
        messages = []
        
        # Generate some sample messages for demonstration
        for i in range(min(limit, 3)):
            messages.append(EmailMessage(
                id=f"msg_{i}_{int(time.time())}",
                sender=f"sender{i}@example.com",
                recipient=email_address,
                subject=f"Test Message {i + 1}",
                body=f"This is a test message body {i + 1}",
                html_body=f"<p>This is a test message body {i + 1}</p>",
                received_at=datetime.now() - timedelta(minutes=i * 5),
                is_read=False,
                attachments=[]
            ))
        
        return messages
    
    def get_message(self, message_id: str) -> Optional[EmailMessage]:
        """
        Get a specific message by ID.
        
        Args:
            message_id: Message ID
            
        Returns:
            Email message or None if not found
        """
        # Mock implementation
        return EmailMessage(
            id=message_id,
            sender="sender@example.com",
            recipient="recipient@tempmail.org",
            subject="Test Message",
            body="This is a test message body",
            html_body="<p>This is a test message body</p>",
            received_at=datetime.now(),
            is_read=False,
            attachments=[]
        )
    
    def delete_message(self, message_id: str) -> bool:
        """
        Delete a specific message.
        
        Args:
            message_id: Message ID to delete
            
        Returns:
            True if successful
        """
        # Mock implementation
        return True
    
    def wait_for_message(
        self,
        email_address: str,
        timeout: float = 60.0,
        check_interval: float = 2.0
    ) -> Optional[EmailMessage]:
        """
        Wait for a new message to arrive.
        
        Args:
            email_address: Email address to monitor
            timeout: Maximum time to wait in seconds
            check_interval: Time between checks in seconds
            
        Returns:
            First new message or None if timeout
        """
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            messages = self.get_messages(email_address, limit=1)
            if messages:
                return messages[0]
            
            time.sleep(check_interval)
        
        return None
    
    def _generate_token(self) -> str:
        """Generate a random token for email access."""
        return ''.join(random.choices(string.ascii_letters + string.digits, k=32))
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.session.close() 