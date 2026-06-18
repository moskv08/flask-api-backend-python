# backend/routes/auth.py
from flask import Blueprint, request, jsonify, g
from models.user import User, db
from services.user_service import UserService
from validation.user_validation import validate_user_data, validate_password
from flask_jwt_extended import create_access_token, jwt_required, get_jwt
from exceptions import ValidationError, NotFoundError
from datetime import timedelta
import logging
from utils.response_formatter import format_success, format_error
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint('auth', __name__)
logger = logging.getLogger(__name__)

@auth_bp.route('/auth/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        
        # Validate input
        if not data or 'email' not in data or 'password' not in data:
            logger.info(
                "Login failed - missing credentials",
                extra={'extra_data': {
                    'event': 'login_failed',
                    'reason': 'missing_credentials'
                }}
            )
            return jsonify(format_error('Email and password required', 'VALIDATION_ERROR', 400)), 400
            
        email = data['email']
        password = data['password']
        
        # Find user by email
        user = User.query.filter_by(email=email).first()
        if not user:
            logger.info(
                "Login failed - invalid credentials",
                extra={'extra_data': {
                    'event': 'login_failed',
                    'reason': 'invalid_credentials',
                    'email': email
                }}
            )
            return jsonify(format_error('Invalid credentials', 'INVALID_CREDENTIALS', 401)), 401
            
        # Verify password using werkzeug security
        try:
            # Handle case where user has no password hash (should not happen in properly set up system)
            if not user.password_hash:
                logger.error(
                    "Login failed - user missing password hash",
                    extra={'extra_data': {
                        'event': 'login_failed',
                        'reason': 'user_missing_password_hash',
                        'email': email
                    }}
                )
                return jsonify(format_error('Internal server error', 'INTERNAL_ERROR', 500)), 500
                
            if not check_password_hash(user.password_hash, password):
                logger.info(
                    "Login failed - invalid credentials",
                    extra={'extra_data': {
                        'event': 'login_failed',
                        'reason': 'invalid_credentials',
                        'email': email
                    }}
                )
                return jsonify(format_error('Invalid credentials', 'INVALID_CREDENTIALS', 401)), 401
        except Exception as e:
            logger.error(
                "Login password verification error",
                extra={'extra_data': {
                    'event': 'login_password_error',
                    'error_type': 'Exception',
                    'message': f'Password verification failed: {str(e)}',
                    'code': 'PASSWORD_ERROR'
                }},
                exc_info=True
            )
            return jsonify(format_error('Internal server error', 'INTERNAL_ERROR', 500)), 500
            
        # Create access token
        access_token = create_access_token(
            identity=str(user.id),
            expires_delta=timedelta(hours=1)
        )
        
        logger.info(
            "Login successful",
            extra={'extra_data': {
                'event': 'login_success',
                'user_id': user.id,
                'email': email
            }}
        )
        
        return jsonify(format_success(
            data={
                'access_token': access_token,
                'user': {
                    'id': user.id,
                    'name': user.name,
                    'email': user.email
                }
            },
            message='Login successful',
            status_code=200
        )), 200
        
    except ValidationError as e:
        logger.error(
            "Login validation error",
            extra={'extra_data': {
                'event': 'login_validation_error',
                'error_type': 'ValidationError',
                'message': str(e),
                'code': 'VALIDATION_ERROR'
            }}
        )
        return jsonify(format_error(str(e), 'VALIDATION_ERROR', 400)), 400
    except NotFoundError as e:
        logger.error(
            "Login not found error",
            extra={'extra_data': {
                'event': 'login_not_found_error',
                'error_type': 'NotFoundError',
                'message': str(e),
                'code': 'NOT_FOUND'
            }}
        )
        return jsonify(format_error(str(e), 'NOT_FOUND', 401)), 401
    except Exception as e:
        logger.error(
            "Login general error",
            extra={'extra_data': {
                'event': 'login_general_error',
                'error_type': 'Exception',
                'message': 'Internal server error',
                'code': 'INTERNAL_ERROR'
            }},
            exc_info=True
        )
        return jsonify(format_error('Internal server error', 'INTERNAL_ERROR', 500)), 500

@auth_bp.route('/auth/signup', methods=['POST'])
def signup():
    try:
        data = request.get_json()
        
        # Validate input
        if not data or 'name' not in data or 'email' not in data or 'password' not in data:
            logger.info(
                "Signup failed - missing required fields",
                extra={'extra_data': {
                    'event': 'signup_failed',
                    'reason': 'missing_required_fields'
                }}
            )
            return jsonify(format_error('Name, email and password required', 'VALIDATION_ERROR', 400)), 400
            
        name = data['name']
        email = data['email']
        password = data['password']
        
        # Validate password strength
        is_valid, error_msg = validate_password(password)
        if not is_valid:
            logger.info(
                "Signup failed - invalid password",
                extra={'extra_data': {
                    'event': 'signup_failed',
                    'reason': 'invalid_password',
                    'message': error_msg
                }}
            )
            return jsonify(format_error(error_msg, 'VALIDATION_ERROR', 400)), 400
            
        # Check if user already exists
        existing_user = User.query.filter(
            (User.name == name) | (User.email == email)
        ).first()
        
        if existing_user:
            logger.info(
                "Signup failed - duplicate user",
                extra={'extra_data': {
                    'event': 'signup_failed',
                    'reason': 'duplicate_user',
                    'name': name,
                    'email': email
                }}
            )
            return jsonify(format_error('User with this name or email already exists', 'DUPLICATE_ERROR', 409)), 409
            
        # Create new user with hashed password
        hashed_password = generate_password_hash(password)
        new_user = User(
            name=name,
            email=email,
            password_hash=hashed_password
        )
        
        db.session.add(new_user)
        db.session.commit()
        
        logger.info(
            "Signup successful",
            extra={'extra_data': {
                'event': 'signup_success',
                'user_id': new_user.id,
                'name': name,
                'email': email
            }}
        )
        
        # Create access token for immediate login
        access_token = create_access_token(
            identity=str(new_user.id),
            expires_delta=timedelta(hours=1)
        )
        
        return jsonify(format_success(
            data={
                'access_token': access_token,
                'user': {
                    'id': new_user.id,
                    'name': new_user.name,
                    'email': new_user.email
                }
            },
            message='Signup successful',
            status_code=201
        )), 201
        
    except Exception as e:
        db.session.rollback()
        logger.error(
            "Signup general error",
            extra={'extra_data': {
                'event': 'signup_general_error',
                'error_type': 'Exception',
                'message': 'Internal server error',
                'code': 'INTERNAL_ERROR'
            }},
            exc_info=True
        )
        return jsonify(format_error('Internal server error', 'INTERNAL_ERROR', 500)), 500

@auth_bp.route('/auth/logout', methods=['POST'])
@jwt_required()
def logout():
    try:
        # Get the token's JTI (JWT ID) and add it to the blocklist
        jti = get_jwt()['jti']
        
        # Create a new session to ensure clean state
        from models.token_blocklist import TokenBlocklist
        token_blocklist_entry = TokenBlocklist(jti=jti)
        db.session.add(token_blocklist_entry)
        db.session.commit()
        
        logger.info(
            "Logout successful",
            extra={'extra_data': {
                'event': 'logout_success',
                'jti': jti
            }}
        )
        
        return jsonify(format_success(
            message='Successfully logged out',
            status_code=200
        )), 200
        
    except Exception as e:
        # Log the error for debugging purposes
        logger.error(
            "Logout error",
            extra={'extra_data': {
                'event': 'logout_error',
                'error_type': 'Exception',
                'message': f'Logout failed: {e}',
                'jti': jti if 'jti' in locals() else None
            }},
            exc_info=True
        )
        try:
            db.session.rollback()
        except:
            pass
        return jsonify(format_error('Internal server error', 'INTERNAL_ERROR', 500)), 500