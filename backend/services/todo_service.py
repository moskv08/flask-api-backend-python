from datetime import datetime
from models.todo import Todo, db

class TodoService:
    @staticmethod
    def get_todos_by_user(user_id):
        """Get all todos for a specific user"""
        return Todo.query.filter_by(user_id=user_id).all()

    @staticmethod
    def create_todo(title, description, user_id, due_date=None, priority='medium'):
        """Create a new todo"""
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

    @staticmethod
    def update_todo(todo_id, user_id, data):
        """Update a todo"""
        todo = Todo.query.filter_by(id=todo_id, user_id=user_id).first()
        
        if not todo:
            raise ValueError("Todo not found")
        
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
                    raise ValueError("Invalid date format")
            else:
                todo.due_date = data['due_date']
        if 'priority' in data:
            priority = data['priority'].lower()
            if priority not in ['low', 'medium', 'high']:
                raise ValueError("Priority must be low, medium, or high")
            todo.priority = priority
        
        db.session.commit()
        return todo

    @staticmethod
    def delete_todo(todo_id, user_id):
        """Delete a todo"""
        todo = Todo.query.filter_by(id=todo_id, user_id=user_id).first()
        
        if not todo:
            raise ValueError("Todo not found")
        
        db.session.delete(todo)
        db.session.commit()