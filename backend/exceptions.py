# backend/exceptions.py
"""
Custom exception classes for the Flask API project.
These exceptions provide consistent error handling and categorization
across all modules.
"""

class ValidationError(Exception):
    """Exception raised for validation errors."""
    def __init__(self, message, code="VALIDATION_ERROR"):
        self.message = message
        self.code = code
        super().__init__(self.message)

class NotFoundError(Exception):
    """Exception raised when a resource is not found."""
    def __init__(self, message, code="NOT_FOUND"):
        self.message = message
        self.code = code
        super().__init__(self.message)

class DuplicateError(Exception):
    """Exception raised when a duplicate resource is detected."""
    def __init__(self, message, code="DUPLICATE_ERROR"):
        self.message = message
        self.code = code
        super().__init__(self.message)

class DatabaseError(Exception):
    """Exception raised for database-related errors."""
    def __init__(self, message, code="DATABASE_ERROR"):
        self.message = message
        self.code = code
        super().__init__(self.message)