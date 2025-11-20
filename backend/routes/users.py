# backend/routes/users.py
from flask import Blueprint, request, jsonify
from marshmallow import Schema, fields, ValidationError
from models.user import User, db
from services.user_service import UserService

users_bp = Blueprint('users', __name__)

class UserSchema(Schema):
    name = fields.Str(required=True, validate=lambda x: len(x) >= 2)
    email = fields.Email(required=True)

# Validate request data
def validate_user_data(data):
    schema = UserSchema()
    try:
        result = schema.load(data)
        return True, result
    except ValidationError as err:
        return False, err.messages

@users_bp.route('/api/flask/users', methods=['POST'])
def create_user():

    try:
        data = request.get_json()

        # Input validation with Marshmallow
        is_valid, result = validate_user_data(data)
        if not is_valid:
            return jsonify({'error': 'Validation failed', 'details': result}), 400
    
        name = result.get('name')
        email = result.get('email')

        # Check for existing user
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return jsonify({'error': 'User with this email already exists'}), 409
        
        user = UserService.create_user(name, email)
        # Assuming you have a way to save the user to database
        
        return jsonify({
            'message': 'User created successfully',
            'user': {
                'id': user.id,
                'name': user.name,
                'email': user.email
            }
        }), 201
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500

@users_bp.route('/api/flask/users', methods=['GET'])
def get_all_users():
    users = User.query.all()
    return jsonify([user.json() for user in users])

@users_bp.route('/api/flask/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
            
        data = request.get_json()
        updated_user = UserService.update_user(user, data)
        
        return jsonify({
            'message': 'User updated successfully',
            'user': {
                'id': updated_user.id,
                'name': updated_user.name,
                'email': updated_user.email
            }
        }), 200
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500
    
def update_user(user_id):
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
            
        data = request.get_json()
        updated_user = UserService.update_user(user, data)
        
        return jsonify({
            'message': 'User updated successfully',
            'user': {
                'id': updated_user.id,
                'name': updated_user.name,
                'email': updated_user.email
            }
        }), 200
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500

@users_bp.route('/api/flask/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    
    try:
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'User deleted successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to delete user'}), 500