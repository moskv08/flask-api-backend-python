# backend/routes/auth.py
from flask import Blueprint, request, jsonify
from models.user import User, db
from services.user_service import UserService
from validation.user_validation import validate_user_data
from flask_jwt_extended import create_access_token, jwt_required, get_jwt
from exceptions import ValidationError, NotFoundError
from datetime import timedelta

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/auth/login', methods=['POST'])
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
        
    except ValidationError as e:
        return jsonify({'error': str(e), 'code': 'VALIDATION_ERROR'}), 400
    except NotFoundError as e:
        return jsonify({'error': str(e), 'code': 'NOT_FOUND'}), 401
    except Exception as e:
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
        
        return jsonify({'message': 'Successfully logged out'}), 200
        
    except Exception as e:
        # Log the error for debugging purposes
        print(f"Logout error: {e}")
        try:
            db.session.rollback()
        except:
            pass
        return jsonify({'error': 'Internal server error', 'code': 'INTERNAL_ERROR'}), 500