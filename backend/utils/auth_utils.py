# backend/utils/auth_utils.py
"""Authentication and authorization utility functions for the Flask API."""

from flask_jwt_extended import get_jwt_identity
from models.user import User
from exceptions import ValidationError

def get_current_user():
    """Get the currently authenticated user object."""
    current_user_id = get_jwt_identity()
    return User.query.get(current_user_id)

def is_owner_or_admin(resource_owner_id):
    """Check if the authenticated user is the owner of a resource or an admin."""
    current_user_id = get_jwt_identity()
    
    # For now, we only check ownership - admin functionality can be added later
    return current_user_id == resource_owner_id

def require_owner_or_admin(resource_owner_field, resource_owner_id):
    """Validate that the authenticated user is the owner of a resource."""
    current_user_id = get_jwt_identity()
    
    if current_user_id != resource_owner_id:
        raise ValidationError("Access denied", "ACCESS_DENIED", 403)
        
    return True

def validate_user_id_in_url(user_id):
    """Validate that a user_id parameter in URL is a valid integer."""
    try:
        int(user_id)
        return True
    except (ValueError, TypeError):
        raise ValidationError("Invalid user ID format", "INVALID_USER_ID", 400)