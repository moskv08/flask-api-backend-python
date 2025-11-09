from flask import Blueprint, request, jsonify, make_response
from models.user import User
from services.user_service import UserService

# Create blueprint for user routes
users_bp = Blueprint('users', __name__)

# User creation endpoint
@users_bp.route('/api/flask/users', methods=['POST'])
def create_user():
    try:
        data = request.get_json()
        
        # Input validation
        if not data or not isinstance(data, dict):
            return make_response(jsonify({'message': 'Invalid request data'}), 400)
        
        name = data.get('name')
        email = data.get('email')
        
        if not name or not email:
            return make_response(jsonify({'message': 'Name and email are required'}), 400)
        
        # Create user through service
        user = UserService.create_user(name, email)
        
        return jsonify(user.json()), 201
        
    except ValueError as e:
        return make_response(jsonify({'message': str(e)}), 409)
    except Exception as e:
        return make_response(jsonify({
            'message': 'Error creating user',
            'error': str(e)
        }), 500)

@users_bp.route('/api/flask/users', methods=['GET'])
def get_all_users():
    try:
        users = User.query.all()
        users_data = [user.json() for user in users]
        return jsonify(users_data), 200
        
    except Exception as e:
        return make_response(jsonify({
            'message': 'Error getting users',
            'error': str(e)
        }), 500)

@users_bp.route('/api/flask/users/<int:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    try:
        user = User.query.get_or_404(user_id, description='User not found')
        return jsonify(user.json()), 200
        
    except Exception as e:
        return make_response(jsonify({
            'message': 'Error getting user',
            'error': str(e)
        }), 500)

@users_bp.route('/api/flask/users/<int:user_id>', methods=['PUT'])
def update_user_by_id(user_id):
    try:
        user = User.query.get_or_404(user_id, description='User not found')
        data = request.get_json()
        
        if not data or not isinstance(data, dict):
            return make_response(jsonify({'message': 'Invalid request data'}), 400)
        
        # Update user through service
        updated_user = UserService.update_user(user, data)
        
        return make_response(jsonify({'message': 'User updated successfully'}), 200)
        
    except ValueError as e:
        return make_response(jsonify({'message': str(e)}), 409)
    except Exception as e:
        return make_response(jsonify({
            'message': 'Error updating user',
            'error': str(e)
        }), 500)

@users_bp.route('/api/flask/users/<int:user_id>', methods=['DELETE'])
def delete_user_by_id(user_id):
    try:
        user = User.query.get_or_404(user_id, description='User not found')
        
        # Delete user through service
        UserService.delete_user(user)
        
        return make_response(jsonify({'message': 'User deleted successfully'}), 200)
        
    except Exception as e:
        return make_response(jsonify({
            'message': 'Error deleting user',
            'error': str(e)
        }), 500)