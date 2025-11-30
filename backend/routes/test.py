from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

# Create blueprint for test routes
test_bp = Blueprint('test', __name__)

@test_bp.route('/test', methods=['GET'])
def test():
    try:
        # Simulate some operation that could fail
        result = {'message': 'Server is running'}
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500

@test_bp.route('/protected', methods=['GET'])
@jwt_required()
def protected_route():
    current_user_id = get_jwt_identity()
    return jsonify({'message': f'Hello user {current_user_id}'})