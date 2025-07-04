"""
Temp Mail API - A Python library for temporary email services.

This library provides a simple interface to work with temporary email services,
allowing you to create temporary email addresses and retrieve messages.
"""

__version__ = "0.1.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"

from .client import TempMailClient
from .models import EmailAddress, EmailMessage
from .exceptions import TempMailError, TempMailAPIError, TempMailTimeoutError

__all__ = [
    "TempMailClient",
    "EmailAddress", 
    "EmailMessage",
    "TempMailError",
    "TempMailAPIError", 
    "TempMailTimeoutError",
] 