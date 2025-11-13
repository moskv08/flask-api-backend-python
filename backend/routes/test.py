from flask import Blueprint, jsonify

# Create blueprint for test routes
test_bp = Blueprint('test', __name__)

@test_bp.route('/test', methods=['GET'])
def test():
    return jsonify({'message': 'Server is running'})