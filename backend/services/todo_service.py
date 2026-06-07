# backend/services/todo_service.py
from datetime import datetime
from models.todo import Todo, db
from exceptions import ValidationError, NotFoundError, DatabaseError

class TodoService:
    @staticmethod
    def get_todos_by_user(user_id):
        """Get all todos for a specific user"""
        try:
            return Todo.query.filter_by(user_id=user_id).all()
        except Exception as e:
            raise DatabaseError('Failed to retrieve todos')

    @staticmethod
    def create_todo(title, description, user_id, due_date=None, priority='medium'):
        """Create a new todo"""
        try:
            todo = Todo(
                title=title,
                description=description,
                user_id=user_id,
                due_date=due_date,
                priority=priority
            )
            
            db.session.add(todo)
            db.session.commit()
            return todo
        except Exception as e:
            db.session.rollback()
            raise DatabaseError('Failed to create todo')

    @staticmethod
    def update_todo(todo_id, user_id, data):
        """Update a todo"""
        try:
            todo = Todo.query.filter_by(id=todo_id, user_id=user_id).first()
            
            if not todo:
                raise NotFoundError("Todo not found")
            
            # Update fields
            if 'title' in data:
                todo.title = data['title']
            if 'description' in data:
                todo.description = data['description']
            if 'completed' in data:
                todo.completed = data['completed']
            if 'due_date' in data:
                # Handle date parsing
                if isinstance(data['due_date'], str):
                    try:
                        todo.due_date = datetime.fromisoformat(data['due_date'])
                    except ValueError:
                        raise ValidationError("Invalid date format")
                else:
                    todo.due_date = data['due_date']
            if 'priority' in data:
                priority = data['priority'].lower()
                if priority not in ['low', 'medium', 'high']:
                    raise ValidationError("Priority must be low, medium, or high")
                todo.priority = priority
            
            db.session.commit()
            return todo
        except Exception as e:
            db.session.rollback()
            raise DatabaseError('Failed to update todo')

    @staticmethod
    def delete_todo(todo_id, user_id):
        """Delete a todo"""
        try:
            todo = Todo.query.filter_by(id=todo_id, user_id=user_id).first()
            
            if not todo:
                raise NotFoundError("Todo not found")
            
            db.session.delete(todo)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise DatabaseError('Failed to delete todo')

    @staticmethod
    def search_todos(user_id, query):
        """Search todos by title or description"""
        try:
            if not query or len(query.strip()) < 2:
                raise ValidationError("Search query must be at least 2 characters")

            # Use LIKE with wildcards for partial matching (case-insensitive)
            search_pattern = f"%{query.lower()}%"
            return Todo.query.filter(
                Todo.user_id == user_id,
                db.or_(
                    db.func.lower(Todo.title).like(search_pattern),
                    db.func.lower(Todo.description).like(search_pattern)
                )
            ).all()
        except Exception as e:
            raise DatabaseError('Failed to search todos')
