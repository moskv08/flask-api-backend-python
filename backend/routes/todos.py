from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from services.todo_service import TodoService
from services.user_service import UserService

todo_bp = Blueprint('todos', __name__)

@todo_bp.route('/api/flask/users/<int:user_id>/todos', methods=['GET'])
@jwt_required()
def get_user_todos(user_id):
    """Get all todos for a specific user"""
    try:
        UserService.get_user_by_id(user_id)

        todos = TodoService.get_todos_by_user(user_id)
        return jsonify(todos), 200

    except ValueError as e:
        return jsonify({'error': str(e)}), 404


@todo_bp.route('/api/flask/users/<int:user_id>/todos', methods=['POST'])
@jwt_required()
def create_todo(user_id):
    """Create a new todo for a specific user"""
    try:
        UserService.get_user_by_id(user_id)

        data = request.get_json() or {}
        title = data.get('title')
        description = data.get('description', '')

        if not title:
            return jsonify({'error': 'Title is required'}), 400

        todo = TodoService.create_todo(title, description, user_id)
        return jsonify(todo.json()), 201

    except ValueError as e:
        return jsonify({'error': str(e)}), 400


@todo_bp.route('/api/flask/users/<int:user_id>/todos/<int:todo_id>', methods=['PUT'])
@jwt_required()
def update_todo(user_id, todo_id):
    """Update a todo for the specified user"""
    try:
        UserService.get_user_by_id(user_id)

        data = request.get_json() or {}
        todo = TodoService.update_todo(todo_id, user_id, data)
        return jsonify(todo.json()), 200

    except ValueError as e:
        return jsonify({'error': str(e)}), 404


@todo_bp.route('/api/flask/users/<int:user_id>/todos/<int:todo_id>', methods=['DELETE'])
@jwt_required()
def delete_todo(user_id, todo_id):
    """Delete a todo for the specified user"""
    try:
        UserService.get_user_by_id(user_id)

        TodoService.delete_todo(todo_id, user_id)
        return jsonify({'message': 'Todo deleted successfully'}), 200

    except ValueError as e:
        return jsonify({'error': str(e)}), 404