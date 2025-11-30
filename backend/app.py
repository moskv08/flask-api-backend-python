# backend/app.py
from flask import Flask, jsonify
from config import config
from models.user import db
from routes import routes_bp
from flask_jwt_extended import JWTManager


def create_app(config_name='default'):
    """Application factory function"""
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)

    JWTManager(app)
    
    # Register blueprints
    app.register_blueprint(routes_bp, url_prefix='/')
    
    # Global error handlers
    @app.errorhandler(ValueError)
    def handle_value_error(error):
        return jsonify({'error': str(error)}), 400
    
    @app.errorhandler(Exception)
    def handle_general_error(error):
        return jsonify({'error': 'Internal server error', 'details': str(error)}), 500
    
    return app

# Create the Flask application
app = create_app('development')

if __name__ == '__main__':
    app.run(debug=True)
