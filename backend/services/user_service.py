# backend/services/user_service.py
from models.user import User,db

class UserService:
    @staticmethod
    def create_user(name, email):
        """Create a new user with validation"""
        # Validate input parameters
        if not name or not email:
            raise ValueError('Name and email are required')
        
        # Validate email format (basic validation)
        if '@' not in email:
            raise ValueError('Invalid email format')
        
        # Check for existing user with same name or email
        existing_user = User.query.filter(
            (User.name == name) | (User.email == email)
        ).first()
        
        if existing_user:
            raise ValueError('User with this name or email already exists')
        
        new_user = User(name=name, email=email)
        db.session.add(new_user)
        db.session.commit()

        return new_user

    @staticmethod
    def update_user(user, data):
        """Update user with validation"""
        name = data.get('name')
        email = data.get('email')
        
        # Validate that user exists
        if not user:
            raise ValueError('User not found')
        
        # Validate input parameters if they're being updated
        if name is not None and not name.strip():
            raise ValueError('Name cannot be empty')
        
        if email is not None and '@' not in email:
            raise ValueError('Invalid email format')
        
        if name is not None:
            # Check for duplicate name
            existing_user = User.query.filter(
                User.name == name,
                User.id != user.id
            ).first()
            
            if existing_user:
                raise ValueError('User with this name already exists')
            
            user.name = name
        
        if email is not None:
            # Check for duplicate email
            existing_user = User.query.filter(
                User.email == email,
                User.id != user.id
            ).first()
            
            if existing_user:
                raise ValueError('User with this email already exists')
            
            user.email = email
        
        return user

    @staticmethod
    def delete_user(user):
        """Delete a user"""
        # Validate that user exists
        if not user:
            raise ValueError('User not found')
        
        # Delete logic here (assuming db session is managed elsewhere)
        pass