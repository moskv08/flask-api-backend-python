# backend/routes/users.py
from flask import Blueprint, request, jsonify, g
from flask_jwt_extended import jwt_required
from models.user import User, db
from services.user_service import UserService
from validation.user_validation import validate_user_data, validate_password
from exceptions import ValidationError, NotFoundError, DuplicateError
import logging
from utils.response_formatter import format_success, format_error, format_validation_error
from utils.auth_utils import require_owner_or_admin
from werkzeug.security import generate_password_hash

users_bp = Blueprint('users', __name__)
logger = logging.getLogger(__name__)

@users_bp.route('/users', methods=['POST'])
@jwt_required()
def create_user():
    try:
        data = request.get_json()

        # Handle case where JSON parsing fails or returns None
        if not data:
            logger.info(
                "User creation failed - invalid JSON or missing data",
                extra={'extra_data': {
                    'event': 'user_creation_invalid_json',
                    'reason': 'invalid_json_or_missing_data'
                }}
            )
            return jsonify(format_error('Invalid JSON or missing data', 'INVALID_JSON', 400)), 400

        # Input validation with Marshmallow
        is_valid, result = validate_user_data(data)
        if not is_valid:
            logger.info(
                "User creation failed - validation error",
                extra={'extra_data': {
                    'event': 'user_creation_validation_failed',
                    'reason': 'validation_error',
                    'details': result
                }}
            )
            return jsonify(format_validation_error(result, 400)), 400
    
        name = result.get('name')
        email = result.get('email')

        user = UserService.create_user(name, email)
        
        logger.info(
            "User created successfully",
            extra={'extra_data': {
                'event': 'user_created',
                'user_id': user.id,
                'name': name,
                'email': email
            }}
        )
        
        return jsonify(format_success(
            data={
                'id': user.id,
                'name': user.name,
                'email': user.email
            },
            message='User created successfully',
            status_code=201
        )), 201
        
    except ValidationError as e:
        logger.error(
            "User creation validation error",
            extra={'extra_data': {
                'event': 'user_creation_validation_error',
                'error_type': 'ValidationError',
                'message': str(e),
                'code': 'VALIDATION_ERROR'
            }}
        )
        return jsonify(format_error(str(e), 'VALIDATION_ERROR', 400)), 400
    except DuplicateError as e:
        logger.error(
            "User creation duplicate error",
            extra={'extra_data': {
                'event': 'user_creation_duplicate_error',
                'error_type': 'DuplicateError',
                'message': str(e),
                'code': 'DUPLICATE_ERROR'
            }}
        )
        return jsonify(format_error(str(e), 'DUPLICATE_ERROR', 409)), 409
    except Exception as e:
        logger.error(
            "User creation general error",
            extra={'extra_data': {
                'event': 'user_creation_general_error',
                'error_type': 'Exception',
                'message': 'Internal server error',
                'code': 'INTERNAL_ERROR'
            }},
            exc_info=True
        )
        return jsonify(format_error('Internal server error', 'INTERNAL_ERROR', 500)), 500

@users_bp.route('/users', methods=['GET'])
@jwt_required()
def get_all_users():
    try:
        logger.info(
            "Fetching all users",
            extra={'extra_data': {
                'event': 'get_all_users'
            }}
        )
        users = UserService.get_all_users()
        return jsonify(format_success(data=users, message='Users retrieved successfully')), 200
    except Exception as e:
        logger.error(
            "Get all users general error",
            extra={'extra_data': {
                'event': 'get_all_users_general_error',
                'error_type': 'Exception',
                'message': 'Internal server error'
            }},
            exc_info=True
        )
        return jsonify(format_error('Internal server error', 'INTERNAL_ERROR', 500)), 500

@users_bp.route('/users/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user_by_id(user_id):
    try:
        # Check authorization - user must be the owner of the resource
        require_owner_or_admin('user_id', user_id)
        
        logger.info(
            "Fetching user by ID",
            extra={'extra_data': {
                'event': 'get_user_by_id',
                'user_id': user_id
            }}
        )
        user = UserService.get_user_by_id(user_id)
        if not user:
            logger.info(
                "User not found",
                extra={'extra_data': {
                    'event': 'user_not_found',
                    'user_id': user_id
                }}
            )
            return jsonify(format_error('User not found', 'NOT_FOUND', 404)), 404
            
        return jsonify(format_success(
            data={
                'id': user.id,
                'name': user.name,
                'email': user.email
            },
            message='User retrieved successfully',
            status_code=200
        )), 200
        
    except ValidationError as e:
        logger.error(
            "Get user by ID validation error",
            extra={'extra_data': {
                'event': 'get_user_by_id_validation_error',
                'error_type': 'ValidationError',
                'message': str(e),
                'code': 'VALIDATION_ERROR'
            }}
        )
        return jsonify(format_error(str(e), 'VALIDATION_ERROR', 400)), 400
    except NotFoundError as e:
        logger.error(
            "Get user by ID not found error",
            extra={'extra_data': {
                'event': 'get_user_by_id_not_found_error',
                'error_type': 'NotFoundError',
                'message': str(e),
                'code': 'NOT_FOUND'
            }}
        )
        return jsonify(format_error(str(e), 'NOT_FOUND', 404)), 404
    except Exception as e:
        logger.error(
            "Get user by ID general error",
            extra={'extra_data': {
                'event': 'get_user_by_id_general_error',
                'error_type': 'Exception',
                'message': 'Internal server error',
                'code': 'INTERNAL_ERROR'
            }},
            exc_info=True
        )
        return jsonify(format_error('Internal server error', 'INTERNAL_ERROR', 500)), 500

@users_bp.route('/users/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    try:
        # Check authorization - user must be the owner of the resource
        require_owner_or_admin('user_id', user_id)
        
        logger.info(
            "Updating user",
            extra={'extra_data': {
                'event': 'update_user',
                'user_id': user_id
            }}
        )
        user = User.query.get(user_id)
        if not user:
            logger.info(
                "User not found for update",
                extra={'extra_data': {
                    'event': 'user_not_found_update',
                    'user_id': user_id
                }}
            )
            return jsonify(format_error('User not found', 'NOT_FOUND', 404)), 404
            
        data = request.get_json()
        
        # Handle case where JSON parsing fails or returns None
        if not data:
            logger.info(
                "User update failed - invalid JSON or missing data",
                extra={'extra_data': {
                    'event': 'user_update_invalid_json',
                    'reason': 'invalid_json_or_missing_data'
                }}
            )
            return jsonify(format_error('Invalid JSON or missing data', 'INVALID_JSON', 400)), 400
            
        # Validate update data
        is_valid, result = validate_user_data(data)
        if not is_valid:
            logger.info(
                "User update failed - validation error",
                extra={'extra_data': {
                    'event': 'user_update_validation_failed',
                    'reason': 'validation_error',
                    'details': result
                }}
            )
            return jsonify(format_validation_error(result, 400)), 400
            
        updated_user = UserService.update_user(user, data)
        
        logger.info(
            "User updated successfully",
            extra={'extra_data': {
                'event': 'user_updated',
                'user_id': updated_user.id,
                'name': updated_user.name,
                'email': updated_user.email
            }}
        )
        
        return jsonify(format_success(
            data={
                'id': updated_user.id,
                'name': updated_user.name,
                'email': updated_user.email
            },
            message='User updated successfully',
            status_code=200
        )), 200
        
    except ValidationError as e:
        logger.error(
            "User update validation error",
            extra={'extra_data': {
                'event': 'user_update_validation_error',
                'error_type': 'ValidationError',
                'message': str(e),
                'code': 'VALIDATION_ERROR'
            }}
        )
        return jsonify(format_error(str(e), 'VALIDATION_ERROR', 400)), 400
    except DuplicateError as e:
        logger.error(
            "User update duplicate error",
            extra={'extra_data': {
                'event': 'user_update_duplicate_error',
                'error_type': 'DuplicateError',
                'message': str(e),
                'code': 'DUPLICATE_ERROR'
            }}
        )
        return jsonify(format_error(str(e), 'DUPLICATE_ERROR', 409)), 409
    except NotFoundError as e:
        logger.error(
            "User update not found error",
            extra={'extra_data': {
                'event': 'user_update_not_found_error',
                'error_type': 'NotFoundError',
                'message': str(e),
                'code': 'NOT_FOUND'
            }}
        )
        return jsonify(format_error(str(e), 'NOT_FOUND', 404)), 404
    except Exception as e:
        logger.error(
            "User update general error",
            extra={'extra_data': {
                'event': 'user_update_general_error',
                'error_type': 'Exception',
                'message': 'Internal server error',
                'code': 'INTERNAL_ERROR'
            }},
            exc_info=True
        )
        return jsonify(format_error('Internal server error', 'INTERNAL_ERROR', 500)), 500

@users_bp.route('/users/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    try:
        # Check authorization - user must be the owner of the resource
        require_owner_or_admin('user_id', user_id)
        
        logger.info(
            "Deleting user",
            extra={'extra_data': {
                'event': 'delete_user',
                'user_id': user_id
            }}
        )
        user = User.query.get(user_id)
        if not user:
            logger.info(
                "User not found for deletion",
                extra={'extra_data': {
                    'event': 'user_not_found_delete',
                    'user_id': user_id
                }}
            )
            return jsonify(format_error('User not found', 'NOT_FOUND', 404)), 404
            
        UserService.delete_user(user)
        
        logger.info(
            "User deleted successfully",
            extra={'extra_data': {
                'event': 'user_deleted',
                'user_id': user_id
            }}
        )
        
        return jsonify(format_success(
            message='User deleted successfully',
            status_code=200
        )), 200
        
    except ValidationError as e:
        logger.error(
            "User delete validation error",
            extra={'extra_data': {
                'event': 'user_delete_validation_error',
                'error_type': 'ValidationError',
                'message': str(e),
                'code': 'VALIDATION_ERROR'
            }}
        )
        return jsonify(format_error(str(e), 'VALIDATION_ERROR', 400)), 400
    except NotFoundError as e:
        logger.error(
            "User delete not found error",
            extra={'extra_data': {
                'event': 'user_delete_not_found_error',
                'error_type': 'NotFoundError',
                'message': str(e),
                'code': 'NOT_FOUND'
            }}
        )
        return jsonify(format_error(str(e), 'NOT_FOUND', 404)), 404
    except Exception as e:
        logger.error(
            "User delete general error",
            extra={'extra_data': {
                'event': 'user_delete_general_error',
                'error_type': 'Exception',
                'message': 'Internal server error',
                'code': 'INTERNAL_ERROR'
            }},
            exc_info=True
        )
        return jsonify(format_error('Internal server error', 'INTERNAL_ERROR', 500)), 500