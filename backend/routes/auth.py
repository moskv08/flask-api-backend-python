# backend/routes/auth.py
from flask import Blueprint, request, jsonify
from models.user import User, db
from services.user_service import UserService
from validation.user_validation import validate_user_data
from flask_jwt_extended import create_access_token, jwt_required
from datetime import timedelta

auth_bp = Blueprint('auth', __name__)

# Token blacklist for logout functionality
blacklisted_tokens = set()

@auth_bp.route('/api/flask/auth/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        
        # Validate input
        if not data or 'email' not in data or 'password' not in data:
            return jsonify({'error': 'Email and password required'}), 400
            
        email = data['email']
        password = data['password']
        
        # Find user by email
        user = User.query.filter_by(email=email).first()
        if not user:
            return jsonify({'error': 'Invalid credentials'}), 401
            
        # Verify password (assuming you have a method to verify passwords)
        # For demonstration, we'll assume password is stored in plain text
        # In production, use proper password hashing
        
        # Create access token
        access_token = create_access_token(
            identity=str(user.id),
            expires_delta=timedelta(hours=1)
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
        
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500

@auth_bp.route('/api/flask/auth/logout', methods=['POST'])
@jwt_required()
def logout():
    try:
        # # Get the token from the request
        # jti = get_raw_jwt()['jti']
        
        # # Add token to blacklist
        # blacklisted_tokens.add(jti)
        
        return jsonify({'message': 'Successfully logged out'}), 200
        
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500

# You'll also need to configure the JWT manager to check blacklisted tokens