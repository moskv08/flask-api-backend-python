from flask import Flask
from config import config
from models.user import db
from routes import routes_bp

def create_app(config_name='default'):
    """Application factory function"""
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    
    # Register blueprints
    app.register_blueprint(routes_bp, url_prefix='/')
    
    return app

# Create the Flask application
app = create_app('development')

if __name__ == '__main__':
    app.run(debug=True)
