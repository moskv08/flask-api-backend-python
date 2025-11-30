from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token

# Create blueprint for test routes
login_bp = Blueprint('login', __name__)

@login_bp.route('/login', methods=['POST'])
def login():
    # Example authentication logic
    email = request.json.get('email')
    password = request.json.get('password')
    
    # Validate credentials (replace with actual DB lookup)
    if email == 'user@example.com' and password == 'password':
        # Create token
        access_token = create_access_token(identity=123)  # User ID
        return jsonify({'access_token': access_token})
    
    return jsonify({'error': 'Invalid credentials'}), 401