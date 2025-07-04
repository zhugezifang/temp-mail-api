"""Custom exceptions for temp mail API."""


class TempMailError(Exception):
    """Base exception for temp mail API errors."""
    
    def __init__(self, message: str, code: str = None):
        super().__init__(message)
        self.message = message
        self.code = code
    
    def __str__(self) -> str:
        if self.code:
            return f"[{self.code}] {self.message}"
        return self.message


class TempMailAPIError(TempMailError):
    """Exception raised when API returns an error."""
    
    def __init__(self, message: str, status_code: int = None, response_data: dict = None):
        super().__init__(message)
        self.status_code = status_code
        self.response_data = response_data or {}
    
    def __str__(self) -> str:
        if self.status_code:
            return f"API Error [{self.status_code}]: {self.message}"
        return f"API Error: {self.message}"


class TempMailTimeoutError(TempMailError):
    """Exception raised when API request times out."""
    
    def __init__(self, message: str = "Request timed out", timeout: float = None):
        super().__init__(message)
        self.timeout = timeout
    
    def __str__(self) -> str:
        if self.timeout:
            return f"Timeout Error ({self.timeout}s): {self.message}"
        return f"Timeout Error: {self.message}"


class TempMailAuthenticationError(TempMailError):
    """Exception raised when authentication fails."""
    
    def __init__(self, message: str = "Authentication failed"):
        super().__init__(message, code="AUTH_ERROR")


class TempMailRateLimitError(TempMailError):
    """Exception raised when rate limit is exceeded."""
    
    def __init__(self, message: str = "Rate limit exceeded", retry_after: int = None):
        super().__init__(message, code="RATE_LIMIT")
        self.retry_after = retry_after
    
    def __str__(self) -> str:
        if self.retry_after:
            return f"Rate Limit Error: {self.message} (retry after {self.retry_after}s)"
        return f"Rate Limit Error: {self.message}" 