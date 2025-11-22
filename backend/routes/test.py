from flask import Blueprint, jsonify

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