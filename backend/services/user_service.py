from models.user import User

class UserService:
    @staticmethod
    def create_user(name, email):
        """Create a new user with validation"""
        # Check for existing user with same name or email
        existing_user = User.query.filter(
            (User.name == name) | (User.email == email)
        ).first()
        
        if existing_user:
            raise ValueError('User with this name or email already exists')
        
        new_user = User(name=name, email=email)
        # Add to session (assuming you have access to db session)
        return new_user

    @staticmethod
    def update_user(user, data):
        """Update user with validation"""
        name = data.get('name')
        email = data.get('email')
        
        if name is not None:
            # Check for duplicate name
            existing_user = User.query.filter(
                User.name == name,
                User.id != user.id
            ).first()
            
            if existing_user:
                raise ValueError('User with this name already exists')
            
            user.name = name
        
        if email is not None:
            # Check for duplicate email
            existing_user = User.query.filter(
                User.email == email,
                User.id != user.id
            ).first()
            
            if existing_user:
                raise ValueError('User with this email already exists')
            
            user.email = email
        
        return user

    @staticmethod
    def delete_user(user):
        """Delete a user"""
        # Delete logic here (assuming db session is managed elsewhere)
        pass