"""Data models for temp mail API."""

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, validator


class EmailAddress(BaseModel):
    """Represents a temporary email address."""
    
    email: str = Field(..., description="The email address")
    domain: str = Field(..., description="The domain part of the email")
    token: Optional[str] = Field(None, description="Token for accessing the mailbox")
    created_at: datetime = Field(default_factory=datetime.now, description="Creation timestamp")
    
    @validator('email')
    def validate_email_format(cls, v):
        """Validate email format."""
        if '@' not in v:
            raise ValueError('Invalid email format')
        return v.lower()
    
    @property
    def username(self) -> str:
        """Get the username part of the email."""
        return self.email.split('@')[0]
    
    def __str__(self) -> str:
        return self.email


class EmailMessage(BaseModel):
    """Represents an email message."""
    
    id: str = Field(..., description="Message ID")
    sender: str = Field(..., description="Sender email address")
    recipient: str = Field(..., description="Recipient email address")
    subject: str = Field(..., description="Email subject")
    body: str = Field(..., description="Email body content")
    html_body: Optional[str] = Field(None, description="HTML body content")
    received_at: datetime = Field(..., description="Message received timestamp")
    is_read: bool = Field(default=False, description="Whether the message has been read")
    attachments: List[str] = Field(default_factory=list, description="List of attachment filenames")
    
    class Config:
        """Pydantic configuration."""
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
    
    def __str__(self) -> str:
        return f"Email from {self.sender}: {self.subject}"


class Domain(BaseModel):
    """Represents an available email domain."""
    
    name: str = Field(..., description="Domain name")
    is_active: bool = Field(True, description="Whether the domain is active")
    
    def __str__(self) -> str:
        return self.name 