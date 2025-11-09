from flask import Flask, jsonify
from config import config
from models.user import db
from routes.users import users_bp

def create_app(config_name='default'):
    """Application factory function"""
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    
    # Register blueprints
    app.register_blueprint(users_bp, url_prefix='/')
    
    @app.route('/test', methods=['GET'])
    def test():
        return jsonify({'message': 'Server is running'})
    
    return app

# Create the Flask application
app = create_app('development')

if __name__ == '__main__':
    app.run(debug=True)