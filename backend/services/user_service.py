# backend/services/user_service.py
from models.user import User,db
from exceptions import ValidationError, DuplicateError, DatabaseError

class UserService:
    @staticmethod
    def create_user(name, email):
        """Create a new user with validation"""
        # Validate input parameters
        if not name or not email:
            raise ValidationError('Name and email are required')
        
        # Validate email format (basic validation)
        if '@' not in email:
            raise ValidationError('Invalid email format')
        
        # Check for existing user with same name or email
        existing_user = User.query.filter(
            (User.name == name) | (User.email == email)
        ).first()
        
        if existing_user:
            raise DuplicateError('User with this name or email already exists')
        
        new_user = User(name=name, email=email)
        db.session.add(new_user)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise DatabaseError('Failed to create user')
        return new_user

    @staticmethod
    def get_all_users():
        """Get all users"""
        try:
            users = User.query.all()
            return [user.json() for user in users]
        except Exception as e:
            raise DatabaseError('Failed to retrieve users')
    
    @staticmethod
    def get_user_by_id(user_id):
        """Get a user by ID"""
        try:
            user = User.query.get(user_id)
            if not user:
                raise NotFoundError('User not found')
            return user
        except Exception as e:
            raise DatabaseError('Failed to retrieve user')

    @staticmethod
    def update_user(user, data):
        """Update user with validation"""
        name = data.get('name')
        email = data.get('email')
        
        # Validate that user exists
        if not user:
            raise NotFoundError('User not found')
        
        # Validate input parameters if they're being updated
        if name is not None and not name.strip():
            raise ValidationError('Name cannot be empty')
        
        if email is not None and '@' not in email:
            raise ValidationError('Invalid email format')
        
        if name is not None:
            # Check for duplicate name
            existing_user = User.query.filter(
                User.name == name,
                User.id != user.id
            ).first()
            
            if existing_user:
                raise DuplicateError('User with this name already exists')
            
            user.name = name
        
        if email is not None:
            # Check for duplicate email
            existing_user = User.query.filter(
                User.email == email,
                User.id != user.id
            ).first()
            
            if existing_user:
                raise DuplicateError('User with this email already exists')
            user.email = email
        
        try:
            db.session.commit()
            return user
        except Exception as e:
            db.session.rollback()
            raise DatabaseError('Failed to update user')

    @staticmethod
    def delete_user(user):
        """Delete a user"""
        # Validate that user exists
        if not user:
            raise NotFoundError('User not found')
        
        try:
            db.session.delete(user)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise DatabaseError('Failed to delete user')