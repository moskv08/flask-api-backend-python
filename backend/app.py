from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from os import environ

app = Flask(__name__)

# Enables cors for all routes
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE_URL')
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, primary_key=False)  # Unique identifier for the user
    email = db.Column(db.String(120), unique=True, primary_key=False)  # Unique email address for the user

    def json(self):
        return {'id': self.id, 'name': self.name, 'email': self.email}  # Returns a dictionary representation of the user

db.create_all()  # Creates all tables defined by the models in this application

# Create a Test route
@app.route('/test', methods=['GET'])
def test():
    return jsonify({'message': 'Server is running'})  # Returns a simple message indicating that the server is running

# Create a user in Database
@app.route('/api/flask/users', methods=['POST'])
def create_user():
    try:
        data = request.get_json()  # Retrieves JSON data from the request
        new_user = User(name=data['name'], email=data['email'])  # Creates a new user instance with the provided data
        db.session.add(new_user)  # Adds the new user to the session
        db.session.commit()  # Commits the changes to the database
        return jsonify({
            'id': new_user.id,
            'name': new_user.name,
            'email': new_user.email
        }), 201  # Returns the created user data with a 201 Created status code
    except Exception as e:
        return make_response(jsonify({'message': 'Error creating user', 'error': str(e)}), 500)

# Get all users
@app.route('/api/flask/users', methods=['GET'])
def get_all_users():
    try:
        # Retrieves all users from the database
        users = User.query.all()

        # Serializes each user to JSON and returns them as a list
        users_data = [user.json() for user in users]
        return jsonify(users_data), 200
    
    except Exception as e:
        return make_response(jsonify({'message': 'Error getting users', 'error': str(e)}), 500)
    
# Get User By Id
@app.route('/api/flask/users/<int:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    try:
        # Retrieves a user by their ID from the database
        user = User.query.get(user_id)
        if not user:
            return make_response(jsonify({'message': 'User not found'}), 404)
        return jsonify(user.json()), 200
    
    except Exception as e:
        return make_response(jsonify({'message': 'Error getting user', 'error': str(e)}), 500)

# Update User By Id
@app.route('/api/flask/users/<int:user_id>', methods=['PUT'])
def update_user_by_id(user_id):
    try:
        # Retrieves a user by their ID from the database
        user = User.query.get(user_id)
        if not user:
            return make_response(jsonify({'message': 'User not found'}), 404)
        # Updates the user's information from the request data
        data = request.get_json()
        user.name = data.get('name', user.name)
        user.email = data.get('email', user.email)
        db.session.commit()
        return make_response(jsonify({'message': 'User updated successfully'}), 200)
    except Exception as e:
        return make_response(jsonify({'message': 'Error updating user', 'error': str(e)}), 500)

# Delete User By Id
@app.route('/api/flask/users/<int:user_id>', methods=['DELETE'])
def delete_user_by_id(user_id):
    try:
        # Retrieves a user by their ID from the database
        user = User.query.get(user_id)
        if not user:
            return make_response(jsonify({'message': 'User not found'}), 404)
        
        # Deletes the user from the database
        db.session.delete(user)
        db.session.commit()
        return make_response(jsonify({'message': 'User deleted successfully'}), 200)
    except Exception as e:
        return make_response(jsonify({'message': 'Error deleting user', 'error': str(e)}), 500)