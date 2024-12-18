from typing import Optional

class MeinETAError(Exception):
    """General exception for meinETA related errors."""
    def __init__(self, message: str, error_code: Optional[int] = None, details: Optional[str] = None):
        super().__init__(message)
        self.message = message
        self.error_code = error_code
        self.details = details

class ConnectionError(MeinETAError):
    """Exception raised for connection-related issues."""
    def __init__(self, message: str, error_code: Optional[int] = None, details: Optional[str] = None):
        super().__init__(message, error_code, details)

class ParsingError(MeinETAError):
    """Exception raised for XML parsing-related issues."""
    def __init__(self, message: str, error_code: Optional[int] = None, details: Optional[str] = None):
        super().__init__(message, error_code, details)

class InvalidResponseError(MeinETAError):
    """Exception raised for unexpected or invalid responses from the API."""
    def __init__(self, message: str, error_code: Optional[int] = None, details: Optional[str] = None):
        super().__init__(message, error_code, details)
