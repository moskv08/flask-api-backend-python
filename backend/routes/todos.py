from flask import Blueprint, request, jsonify
from services.todo_service import TodoService
from services.user_service import UserService
from models.user import User

todo_bp = Blueprint('todos', __name__)

# Helper function to get current user (you'll need to implement authentication)
def get_current_user_id():
    """This should be replaced with actual authentication logic"""
    # For now, we'll assume user_id is passed in request context
    # In a real app, you'd extract this from JWT token or session
    return request.headers.get('user_id') or 1

@todo_bp.route('/api/flask/users/<int:user_id>/todos', methods=['GET'])
def get_user_todos(user_id):
    """Get all todos for a specific user"""
    try:
        # Verify the user exists
        user = UserService.get_user_by_id(user_id)
        
        todos = TodoService.get_todos_by_user(user_id)
        return jsonify(todos), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404

@todo_bp.route('/api/flask/users/<int:user_id>/todos', methods=['POST'])
def create_todo(user_id):
    """Create a new todo for a specific user"""
    try:
        # Verify the user exists
        user = UserService.get_user_by_id(user_id)
        
        data = request.get_json()
        title = data.get('title')
        description = data.get('description', '')
        
        if not title:
            return jsonify({'error': 'Title is required'}), 400
        
        todo = TodoService.create_todo(title, description, user_id)
        return jsonify(todo.json()), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@todo_bp.route('/api/flask/users/<int:user_id>/todos/<int:todo_id>', methods=['PUT'])
def update_todo(user_id, todo_id):
    """Update a todo for the specified user"""
    try:
        # Verify the user exists
        user = UserService.get_user_by_id(user_id)
        
        data = request.get_json()
        todo = TodoService.update_todo(todo_id, user_id, data)
        return jsonify(todo.json()), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404

@todo_bp.route('/api/flask/users/<int:user_id>/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(user_id, todo_id):
    """Delete a todo for the specified user"""
    try:
        # Verify the user exists
        user = UserService.get_user_by_id(user_id)
        
        TodoService.delete_todo(todo_id, user_id)
        return jsonify({'message': 'Todo deleted successfully'}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404