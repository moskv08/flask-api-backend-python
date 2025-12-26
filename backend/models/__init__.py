# backend/models/__init__.py
from .db import db
from .user import User
from .todo import Todo

__all__ = ['db', 'User', 'Todo'] # Exports the User model for use in other modules