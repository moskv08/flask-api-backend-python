from flask import Flask, jsonify
from config import config
from models import db
from routes import routes_bp
from flask_jwt_extended import JWTManager

def create_app(config_name='default'):
    app = Flask(__name__)

    # Load configuration
    app.config.from_object(config[config_name])

    # Initialize extensions
    db.init_app(app)
    JWTManager(app)

    # 🔑 Ensure models are loaded
    with app.app_context():
        from models import User, Todo
        db.create_all()

    # Register blueprints
    app.register_blueprint(routes_bp, url_prefix='/api')

    # Error handlers
    @app.errorhandler(ValueError)
    def handle_value_error(error):
        return jsonify({'error': str(error)}), 400

    @app.errorhandler(Exception)
    def handle_general_error(error):
        return jsonify({
            'error': 'Internal server error',
            'details': str(error)
        }), 500

    return app

app = create_app('development')

if __name__ == '__main__':
    app.run(debug=True)