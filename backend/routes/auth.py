# backend/routes/auth.py
from flask import Blueprint, request, jsonify, g
from models.user import User, db
from services.user_service import UserService
from validation.user_validation import validate_user_data
from flask_jwt_extended import create_access_token, jwt_required, get_jwt
from exceptions import ValidationError, NotFoundError
from datetime import timedelta
import logging

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
            return jsonify({'error': 'Email and password required'}), 400
            
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
            return jsonify({'error': 'Invalid credentials'}), 401
            
        # Verify password (assuming you have a method to verify passwords)
        # For demonstration, we'll assume password is stored in plain text
        # In production, use proper password hashing
        
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
        
        return jsonify({
            'message': 'Login successful',
            'access_token': access_token,
            'user': {
                'id': user.id,
                'name': user.name,
                'email': user.email
            }
        }), 200
        
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
        return jsonify({'error': str(e), 'code': 'VALIDATION_ERROR'}), 400
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
        return jsonify({'error': str(e), 'code': 'NOT_FOUND'}), 401
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
        return jsonify({'error': 'Internal server error', 'code': 'INTERNAL_ERROR'}), 500

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
        
        return jsonify({'message': 'Successfully logged out'}), 200
        
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
        return jsonify({'error': 'Internal server error', 'code': 'INTERNAL_ERROR'}), 500