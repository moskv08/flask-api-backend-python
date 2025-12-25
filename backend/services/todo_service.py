# backend/services/todo_service.py
from models.todo import Todo, db

class TodoService:
    @staticmethod
    def create_todo(title, description, user_id):
        """Create a new todo for a specific user"""
        # Validate input parameters
        if not title:
            raise ValueError('Title is required')
        
        # Create new todo associated with the user
        new_todo = Todo(
            title=title,
            description=description or '',
            completed=False,
            user_id=user_id
        )
        
        db.session.add(new_todo)
        db.session.commit()

        return new_todo

    @staticmethod
    def get_todos_by_user(user_id):
        """Get all todos for a specific user"""
        todos = Todo.query.filter_by(user_id=user_id).all()
        return [todo.json() for todo in todos]
    
    @staticmethod
    def get_todo_by_id(todo_id, user_id):
        """Get a specific todo by ID for the specified user"""
        todo = Todo.query.filter_by(id=todo_id, user_id=user_id).first()
        if not todo:
            raise ValueError('Todo not found for this user')
        return todo

    @staticmethod
    def update_todo(todo_id, user_id, updates):
        """Update a todo for the specified user"""
        todo = Todo.query.filter_by(id=todo_id, user_id=user_id).first()
        
        if not todo:
            raise ValueError('Todo not found for this user')
        
        # Update fields if provided
        if 'title' in updates:
            todo.title = updates['title']
        
        if 'description' in updates:
            todo.description = updates['description']
        
        if 'completed' in updates:
            todo.completed = bool(updates['completed'])
        
        db.session.commit()
        return todo

    @staticmethod
    def delete_todo(todo_id, user_id):
        """Delete a todo for the specified user"""
        todo = Todo.query.filter_by(id=todo_id, user_id=user_id).first()
        
        if not todo:
            raise ValueError('Todo not found for this user')
        
        db.session.delete(todo)
        db.session.commit()
        return True