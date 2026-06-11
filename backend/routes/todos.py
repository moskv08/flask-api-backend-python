from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from services.todo_service import TodoService
from services.user_service import UserService
from exceptions import ValidationError, NotFoundError, DatabaseError
from datetime import datetime
from utils.response_formatter import format_success, format_error
from utils.auth_utils import require_owner_or_admin

todo_bp = Blueprint('todos', __name__)

@todo_bp.route('/users/<int:user_id>/todos', methods=['GET'])
@jwt_required()
def get_user_todos(user_id):
    """Get all todos for a specific user"""
    try:
        # Check authorization - user must be the owner of the resource
        require_owner_or_admin('user_id', user_id)
        
        UserService.get_user_by_id(user_id)

        todos = TodoService.get_todos_by_user(user_id)
        return jsonify(format_success(
            data=[todo.json() for todo in todos],
            message='Todos retrieved successfully'
        )), 200

    except ValidationError as e:
        return jsonify(format_error(str(e), 'VALIDATION_ERROR', 400)), 400
    except DatabaseError as e:
        return jsonify(format_error(str(e), 'DATABASE_ERROR', 500)), 500
    except Exception as e:
        return jsonify(format_error('Internal server error', 'INTERNAL_ERROR', 500)), 500


@todo_bp.route('/users/<int:user_id>/todos', methods=['POST'])
@jwt_required()
def create_todo(user_id):
    """Create a new todo for a specific user"""
    try:
        # Check authorization - user must be the owner of the resource
        require_owner_or_admin('user_id', user_id)
        
        UserService.get_user_by_id(user_id)

        data = request.get_json()
        
        # Validate required fields
        if not data:
            return jsonify(format_error('Request body is required', 'VALIDATION_ERROR', 400)), 400
        
        if 'title' not in data or not data['title'].strip():
            return jsonify(format_error('Title is required and cannot be empty', 'VALIDATION_ERROR', 400)), 400
        
        # Validate title length (prevent DoS attacks)
        if len(data['title']) > 255:
            return jsonify(format_error('Title must be less than 255 characters', 'VALIDATION_ERROR', 400)), 400
        
        # Parse due_date if provided
        due_date = None
        if 'due_date' in data and data['due_date']:
            try:
                due_date = datetime.fromisoformat(data['due_date'])
            except ValueError:
                return jsonify(format_error('Invalid date format. Use ISO format', 'VALIDATION_ERROR', 400)), 400
        
        # Validate priority
        priority = data.get('priority', 'medium').lower()
        if priority not in ['low', 'medium', 'high']:
            return jsonify(format_error('Priority must be low, medium, or high', 'VALIDATION_ERROR', 400)), 400
        
        todo = TodoService.create_todo(
            title=data['title'],
            description=data.get('description', ''),
            user_id=user_id,
            due_date=due_date,
            priority=priority
        )
        
        return jsonify(format_success(
            data=todo.json(),
            message='Todo created successfully',
            status_code=201
        )), 201

    except ValidationError as e:
        return jsonify(format_error(str(e), 'VALIDATION_ERROR', 400)), 400
    except DatabaseError as e:
        return jsonify(format_error(str(e), 'DATABASE_ERROR', 500)), 500
    except Exception as e:
        return jsonify(format_error('Internal server error', 'INTERNAL_ERROR', 500)), 500


@todo_bp.route('/users/<int:user_id>/todos/<int:todo_id>', methods=['PUT'])
@jwt_required()
def update_todo(user_id, todo_id):
    """Update a specific todo"""
    try:
        # Check authorization - user must be the owner of the resource
        require_owner_or_admin('user_id', user_id)
        
        UserService.get_user_by_id(user_id)

        data = request.get_json()
        
        # Handle date parsing
        if 'due_date' in data and data['due_date']:
            try:
                due_date = datetime.fromisoformat(data['due_date'])
                data['due_date'] = due_date
            except ValueError:
                return jsonify(format_error('Invalid date format. Use ISO format', 'VALIDATION_ERROR', 400)), 400
        
        todo = TodoService.update_todo(todo_id, user_id, data)
        
        return jsonify(format_success(
            data=todo.json(),
            message='Todo updated successfully',
            status_code=200
        )), 200

    except ValidationError as e:
        return jsonify(format_error(str(e), 'VALIDATION_ERROR', 400)), 400
    except DatabaseError as e:
        return jsonify(format_error(str(e), 'DATABASE_ERROR', 500)), 500
    except Exception as e:
        return jsonify(format_error('Internal server error', 'INTERNAL_ERROR', 500)), 500


@todo_bp.route('/users/<int:user_id>/todos/<int:todo_id>', methods=['DELETE'])
@jwt_required()
def delete_todo(user_id, todo_id):
    """Delete a specific todo"""
    try:
        # Check authorization - user must be the owner of the resource
        require_owner_or_admin('user_id', user_id)
        
        UserService.get_user_by_id(user_id)

        TodoService.delete_todo(todo_id, user_id)
        
        return jsonify(format_success(
            message='Todo deleted successfully',
            status_code=200
        )), 200

    except ValidationError as e:
        return jsonify(format_error(str(e), 'VALIDATION_ERROR', 400)), 400
    except DatabaseError as e:
        return jsonify(format_error(str(e), 'DATABASE_ERROR', 500)), 500
    except Exception as e:
        return jsonify(format_error('Internal server error', 'INTERNAL_ERROR', 500)), 500

@todo_bp.route('/users/<int:user_id>/todos/search', methods=['GET'])
@jwt_required()
def search_todos(user_id):
    """Search todos for a specific user"""
    try:
        # Check authorization - user must be the owner of the resource
        require_owner_or_admin('user_id', user_id)
        
        UserService.get_user_by_id(user_id)
        
        query = request.args.get('q', '').strip()
        
        # Validate search query
        if not query:
            return jsonify(format_error('Query parameter is required', 'VALIDATION_ERROR', 400)), 400
        
        if len(query) < 2:
            return jsonify(format_error('Query must be at least 2 characters', 'VALIDATION_ERROR', 400)), 400
        
        if len(query) > 100:
            return jsonify(format_error('Query must be less than 100 characters', 'VALIDATION_ERROR', 400)), 400
        
        todos = TodoService.search_todos(user_id, query)
        
        return jsonify(format_success(
            data={
                'todos': [todo.json() for todo in todos],
                'count': len(todos)
            },
            message='Todos search results',
            status_code=200
        )), 200

    except ValidationError as e:
        return jsonify(format_error(str(e), 'VALIDATION_ERROR', 400)), 400
    except DatabaseError as e:
        return jsonify(format_error(str(e), 'DATABASE_ERROR', 500)), 500
    except Exception as e:
        return jsonify(format_error('Internal server error', 'INTERNAL_ERROR', 500)), 500