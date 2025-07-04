# Temp Mail API

[![PyPI version](https://badge.fury.io/py/temp-mail-api.svg)](https://badge.fury.io/py/temp-mail-api)
[![Python Support](https://img.shields.io/pypi/pyversions/temp-mail-api.svg)](https://pypi.org/project/temp-mail-api/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A Python library for temporary email services. Create disposable email addresses and retrieve messages programmatically.

## Features

- 🔥 **Easy to use**: Simple, intuitive API
- 📧 **Multiple domains**: Support for various temporary email domains
- ⚡ **Async support**: Built with modern Python practices
- 🔒 **Type hints**: Full type annotation support
- 🧪 **Well tested**: Comprehensive test suite
- 📦 **Zero dependencies**: Lightweight with minimal external dependencies

## Installation

```bash
pip install temp-mail-api
```

## Quick Start

```python
from temp_mail_api import TempMailClient

# Create a client
client = TempMailClient()

# Create a temporary email address
email = client.create_email_address()
print(f"Created: {email.email}")

# Get messages
messages = client.get_messages(email.email)
for message in messages:
    print(f"From: {message.sender}")
    print(f"Subject: {message.subject}")
    print(f"Body: {message.body}")
```

## Usage Examples

### Basic Usage

```python
from temp_mail_api import TempMailClient

# Initialize client
client = TempMailClient()

# Get available domains
domains = client.get_domains()
print("Available domains:", [d.name for d in domains])

# Create email with specific domain
email = client.create_email_address(domain="tempmail.org")
print(f"Email: {email.email}")
print(f"Token: {email.token}")
```

### Checking Messages

```python
# Get all messages
messages = client.get_messages(email.email)

# Get messages with pagination
messages = client.get_messages(email.email, limit=5, offset=0)

# Get specific message
message = client.get_message("message_id")
if message:
    print(f"Subject: {message.subject}")
    print(f"Body: {message.body}")
```

### Waiting for Messages

```python
# Wait for new message (blocking)
new_message = client.wait_for_message(
    email.email, 
    timeout=60.0,  # Wait up to 60 seconds
    check_interval=2.0  # Check every 2 seconds
)

if new_message:
    print("New message received!")
    print(f"From: {new_message.sender}")
else:
    print("No message received within timeout")
```

### Context Manager

```python
# Use context manager for automatic cleanup
with TempMailClient() as client:
    email = client.create_email_address()
    messages = client.get_messages(email.email)
    # Client will be automatically closed
```

### Error Handling

```python
from temp_mail_api import TempMailClient, TempMailAPIError, TempMailTimeoutError

try:
    client = TempMailClient()
    email = client.create_email_address()
    messages = client.get_messages(email.email)
except TempMailAPIError as e:
    print(f"API Error: {e}")
except TempMailTimeoutError as e:
    print(f"Timeout Error: {e}")
```

## API Reference

### TempMailClient

The main client class for interacting with temporary email services.

#### Methods

- `__init__(base_url, api_key, timeout, max_retries, backoff_factor)`
- `get_domains() -> List[Domain]`
- `create_email_address(domain=None) -> EmailAddress`
- `get_messages(email_address, limit=10, offset=0) -> List[EmailMessage]`
- `get_message(message_id) -> Optional[EmailMessage]`
- `delete_message(message_id) -> bool`
- `wait_for_message(email_address, timeout=60.0, check_interval=2.0) -> Optional[EmailMessage]`

### Models

#### EmailAddress

Represents a temporary email address.

```python
class EmailAddress:
    email: str
    domain: str
    token: Optional[str]
    created_at: datetime
    
    @property
    def username(self) -> str:
        """Get username part of email"""
```

#### EmailMessage

Represents an email message.

```python
class EmailMessage:
    id: str
    sender: str
    recipient: str
    subject: str
    body: str
    html_body: Optional[str]
    received_at: datetime
    is_read: bool
    attachments: List[str]
```

#### Domain

Represents an available email domain.

```python
class Domain:
    name: str
    is_active: bool
```

### Exceptions

- `TempMailError`: Base exception class
- `TempMailAPIError`: API-related errors
- `TempMailTimeoutError`: Timeout-related errors  
- `TempMailAuthenticationError`: Authentication failures
- `TempMailRateLimitError`: Rate limiting errors

## Configuration

### Environment Variables

You can configure the client using environment variables:

```bash
export TEMP_MAIL_API_KEY="your-api-key"
export TEMP_MAIL_BASE_URL="https://api.tempmail.org/v1"
export TEMP_MAIL_TIMEOUT="30"
```

### Client Configuration

```python
client = TempMailClient(
    base_url="https://api.tempmail.org/v1",
    api_key="your-api-key",
    timeout=30.0,
    max_retries=3,
    backoff_factor=0.3
)
```

## Development

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/yourusername/temp-mail-api.git
cd temp-mail-api

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -e ".[dev]"
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=temp_mail_api --cov-report=html

# Run specific test file
pytest tests/test_client.py

# Run with verbose output
pytest -v
```

### Code Quality

```bash
# Format code
black temp_mail_api tests examples

# Check code style
flake8 temp_mail_api tests examples

# Type checking
mypy temp_mail_api
```

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass: `pytest`
6. Commit your changes: `git commit -am 'Add feature'`
7. Push to the branch: `git push origin feature-name`
8. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Changelog

### 0.1.0 (2024-01-01)

- Initial release
- Basic temporary email functionality
- Support for multiple domains
- Message retrieval and management
- Comprehensive test suite

## Related Projects

- [Temp Mail](https://tempmailto.online/) - Web interface for temp mail