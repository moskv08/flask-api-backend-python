# backend/services/user_service.py
from models.user import User,db
from exceptions import ValidationError, DuplicateError, DatabaseError
import logging
from werkzeug.security import generate_password_hash

logger = logging.getLogger(__name__)

class UserService:
    @staticmethod
    def create_user(name, email):
        """Create a new user with validation"""
        logger.info(
            "Creating user",
            extra={'extra_data': {
                'event': 'user_creation_start',
                'name': name,
                'email': email
            }}
        )
        # Validate input parameters
        if not name or not email:
            logger.error(
                "User creation failed - missing required fields",
                extra={'extra_data': {
                    'event': 'user_creation_failed',
                    'reason': 'missing_required_fields',
                    'name': name,
                    'email': email
                }}
            )
            raise ValidationError('Name and email are required')
        
        # Validate email format (basic validation)
        if '@' not in email:
            logger.error(
                "User creation failed - invalid email format",
                extra={'extra_data': {
                    'event': 'user_creation_failed',
                    'reason': 'invalid_email_format',
                    'name': name,
                    'email': email
                }}
            )
            raise ValidationError('Invalid email format')
        
        # Check for existing user with same name or email
        existing_user = User.query.filter(
            (User.name == name) | (User.email == email)
        ).first()
        
        if existing_user:
            logger.error(
                "User creation failed - duplicate user",
                extra={'extra_data': {
                    'event': 'user_creation_failed',
                    'reason': 'duplicate_user',
                    'name': name,
                    'email': email
                }}
            )
            raise DuplicateError('User with this name or email already exists')
        
        # Create user with hashed password (empty string as placeholder)
        # This will be updated in the signup flow when password is provided
        new_user = User(name=name, email=email, password_hash=generate_password_hash(''))
        db.session.add(new_user)
        try:
            db.session.commit()
            logger.info(
                "User created successfully",
                extra={'extra_data': {
                    'event': 'user_created',
                    'user_id': new_user.id,
                    'name': name,
                    'email': email
                }}
            )
        except Exception as e:
            db.session.rollback()
            logger.error(
                "User creation failed - database error",
                extra={'extra_data': {
                    'event': 'user_creation_failed',
                    'reason': 'database_error',
                    'name': name,
                    'email': email
                }},
                exc_info=True
            )
            raise DatabaseError('Failed to create user')
        return new_user

    @staticmethod
    def get_all_users():
        """Get all users"""
        logger.info(
            "Fetching all users",
            extra={'extra_data': {
                'event': 'get_all_users_start'
            }}
        )
        try:
            users = User.query.all()
            logger.info(
                "Fetched all users successfully",
                extra={'extra_data': {
                    'event': 'get_all_users_success',
                    'count': len(users)
                }}
            )
            return [user.json() for user in users]
        except Exception as e:
            logger.error(
                "Failed to retrieve users",
                extra={'extra_data': {
                    'event': 'get_all_users_failed',
                    'reason': 'database_error'
                }},
                exc_info=True
            )
            raise DatabaseError('Failed to retrieve users')
    
    @staticmethod
    def get_user_by_id(user_id):
        """Get a user by ID"""
        logger.info(
            "Fetching user by ID",
            extra={'extra_data': {
                'event': 'get_user_by_id_start',
                'user_id': user_id
            }}
        )
        try:
            user = User.query.get(user_id)
            if not user:
                logger.info(
                    "User not found",
                    extra={'extra_data': {
                        'event': 'user_not_found',
                        'user_id': user_id
                    }}
                )
                raise NotFoundError('User not found')
            logger.info(
                "Fetched user by ID successfully",
                extra={'extra_data': {
                    'event': 'get_user_by_id_success',
                    'user_id': user_id
                }}
            )
            return user
        except Exception as e:
            logger.error(
                "Failed to retrieve user by ID",
                extra={'extra_data': {
                    'event': 'get_user_by_id_failed',
                    'reason': 'database_error',
                    'user_id': user_id
                }},
                exc_info=True
            )
            raise DatabaseError('Failed to retrieve user')

    @staticmethod
    def update_user(user, data):
        """Update user with validation"""
        name = data.get('name')
        email = data.get('email')
        
        # Validate that user exists
        if not user:
            logger.error(
                "User update failed - user not found",
                extra={'extra_data': {
                    'event': 'user_update_failed',
                    'reason': 'user_not_found'
                }}
            )
            raise NotFoundError('User not found')
        
        # Validate input parameters if they're being updated
        if name is not None and not name.strip():
            logger.error(
                "User update failed - empty name",
                extra={'extra_data': {
                    'event': 'user_update_failed',
                    'reason': 'empty_name',
                    'user_id': user.id
                }}
            )
            raise ValidationError('Name cannot be empty')
        
        if email is not None and '@' not in email:
            logger.error(
                "User update failed - invalid email format",
                extra={'extra_data': {
                    'event': 'user_update_failed',
                    'reason': 'invalid_email_format',
                    'user_id': user.id
                }}
            )
            raise ValidationError('Invalid email format')
        
        if name is not None:
            # Check for duplicate name
            existing_user = User.query.filter(
                User.name == name,
                User.id != user.id
            ).first()
            
            if existing_user:
                logger.error(
                    "User update failed - duplicate name",
                    extra={'extra_data': {
                        'event': 'user_update_failed',
                        'reason': 'duplicate_name',
                        'user_id': user.id,
                        'name': name
                    }}
                )
                raise DuplicateError('User with this name already exists')
            
            user.name = name
        
        if email is not None:
            # Check for duplicate email
            existing_user = User.query.filter(
                User.email == email,
                User.id != user.id
            ).first()
            
            if existing_user:
                logger.error(
                    "User update failed - duplicate email",
                    extra={'extra_data': {
                        'event': 'user_update_failed',
                        'reason': 'duplicate_email',
                        'user_id': user.id,
                        'email': email
                    }}
                )
                raise DuplicateError('User with this email already exists')
            user.email = email
        
        try:
            db.session.commit()
            logger.info(
                "User updated successfully",
                extra={'extra_data': {
                    'event': 'user_updated',
                    'user_id': user.id,
                    'name': user.name,
                    'email': user.email
                }}
            )
            return user
        except Exception as e:
            db.session.rollback()
            logger.error(
                "User update failed - database error",
                extra={'extra_data': {
                    'event': 'user_update_failed',
                    'reason': 'database_error',
                    'user_id': user.id
                }},
                exc_info=True
            )
            raise DatabaseError('Failed to update user')

    @staticmethod
    def delete_user(user):
        """Delete a user"""
        # Validate that user exists
        if not user:
            logger.error(
                "User deletion failed - user not found",
                extra={'extra_data': {
                    'event': 'user_deletion_failed',
                    'reason': 'user_not_found'
                }}
            )
            raise NotFoundError('User not found')
        
        try:
            db.session.delete(user)
            db.session.commit()
            logger.info(
                "User deleted successfully",
                extra={'extra_data': {
                    'event': 'user_deleted',
                    'user_id': user.id
                }}
            )
        except Exception as e:
            db.session.rollback()
            logger.error(
                "User deletion failed - database error",
                extra={'extra_data': {
                    'event': 'user_deletion_failed',
                    'reason': 'database_error',
                    'user_id': user.id
                }},
                exc_info=True
            )
            raise DatabaseError('Failed to delete user')