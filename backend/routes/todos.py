from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from services.todo_service import TodoService
from services.user_service import UserService
from datetime import datetime

todo_bp = Blueprint('todos', __name__)

@todo_bp.route('/api/flask/users/<int:user_id>/todos', methods=['GET'])
@jwt_required()
def get_user_todos(user_id):
    """Get all todos for a specific user"""
    try:
        UserService.get_user_by_id(user_id)

        todos = TodoService.get_todos_by_user(user_id)
        return jsonify([todo.json() for todo in todos]), 200

    except ValueError as e:
        return jsonify({'error': str(e)}), 400


@todo_bp.route('/api/flask/users/<int:user_id>/todos', methods=['POST'])
@jwt_required()
def create_todo(user_id):
    """Create a new todo for a specific user"""
    try:
        UserService.get_user_by_id(user_id)

        data = request.get_json()
        
        # Validate required fields
        if not data or 'title' not in data:
            return jsonify({'error': 'Title is required'}), 400
        
        # Parse due_date if provided
        due_date = None
        if 'due_date' in data and data['due_date']:
            try:
                due_date = datetime.fromisoformat(data['due_date'])
            except ValueError:
                return jsonify({'error': 'Invalid date format. Use ISO format'}), 400
        
        # Validate priority
        priority = data.get('priority', 'medium').lower()
        if priority not in ['low', 'medium', 'high']:
            return jsonify({'error': 'Priority must be low, medium, or high'}), 400
        
        todo = TodoService.create_todo(
            title=data['title'],
            description=data.get('description', ''),
            user_id=user_id,
            due_date=due_date,
            priority=priority
        )
        
        return jsonify(todo.json()), 201

    except ValueError as e:
        return jsonify({'error': str(e)}), 400


@todo_bp.route('/api/flask/users/<int:user_id>/todos/<int:todo_id>', methods=['PUT'])
@jwt_required()
def update_todo(user_id, todo_id):
    """Update a specific todo"""
    try:
        UserService.get_user_by_id(user_id)

        data = request.get_json()
        
        # Handle date parsing
        if 'due_date' in data and data['due_date']:
            try:
                due_date = datetime.fromisoformat(data['due_date'])
                data['due_date'] = due_date
            except ValueError:
                return jsonify({'error': 'Invalid date format. Use ISO format'}), 400
        
        todo = TodoService.update_todo(todo_id, user_id, data)
        
        return jsonify(todo.json()), 200

    except ValueError as e:
        return jsonify({'error': str(e)}), 400


@todo_bp.route('/api/flask/users/<int:user_id>/todos/<int:todo_id>', methods=['DELETE'])
@jwt_required()
def delete_todo(user_id, todo_id):
    """Delete a specific todo"""
    try:
        UserService.get_user_by_id(user_id)

        TodoService.delete_todo(todo_id, user_id)
        
        return jsonify({'message': 'Todo deleted successfully'}), 200

    except ValueError as e:
        return jsonify({'error': str(e)}), 400