# backend/models/__init__.py
from .user import User
from .todo import Todo

__all__ = ['User', 'Todo'] # Exports the User model for use in other modules