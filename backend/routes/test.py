from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token

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

# @test_bp.route('/login', methods=['POST'])
# def login():
#     # Example authentication logic
#     email = request.json.get('email')
#     password = request.json.get('password')
    
#     # Validate credentials (replace with actual DB lookup)
#     if email == 'user@example.com' and password == 'password':
#         # Create token
#         access_token = create_access_token(identity=123)  # User ID
#         return jsonify({'access_token': access_token})
    
#     return jsonify({'error': 'Invalid credentials'}), 401