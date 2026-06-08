from flask import Flask, jsonify
from config import config
from models import db
from models.token_blocklist import TokenBlocklist
from routes import routes_bp
from flask_jwt_extended import JWTManager
from exceptions import ValidationError, NotFoundError, DuplicateError, DatabaseError
from logging_config import setup_logging

def create_app(config_name='default'):
    app = Flask(__name__)

    # Load configuration
    app.config.from_object(config[config_name])

    # Initialize extensions
    db.init_app(app)
    
    # Configure JWT Manager with token blocklist loader
    jwt = JWTManager(app)
    
    @jwt.token_in_blocklist_loader
    def check_if_token_revoked(jwt_header, jwt_payload):
        jti = jwt_payload['jti']
        token = db.session.query(TokenBlocklist.id).filter_by(jti=jti).scalar()
        return token is not None

    # Register blueprints
    app.register_blueprint(routes_bp, url_prefix='/api')

    # Setup structured logging
    setup_logging(app)

    # Error handlers
    @app.errorhandler(ValidationError)
    def handle_validation_error(error):
        app.logger.error(
            "Validation error occurred",
            extra={'extra_data': {
                'event': 'validation_error',
                'error_type': 'ValidationError',
                'message': str(error),
                'code': error.code
            }}
        )
        return jsonify({
            'error': str(error),
            'code': error.code
        }), 400

    @app.errorhandler(DuplicateError)
    def handle_duplicate_error(error):
        app.logger.error(
            "Duplicate error occurred",
            extra={'extra_data': {
                'event': 'duplicate_error',
                'error_type': 'DuplicateError',
                'message': str(error),
                'code': error.code
            }}
        )
        return jsonify({
            'error': str(error),
            'code': error.code
        }), 409

    @app.errorhandler(NotFoundError)
    def handle_not_found_error(error):
        app.logger.error(
            "Not found error occurred",
            extra={'extra_data': {
                'event': 'not_found_error',
                'error_type': 'NotFoundError',
                'message': str(error),
                'code': error.code
            }}
        )
        return jsonify({
            'error': str(error),
            'code': error.code
        }), 404

    @app.errorhandler(DatabaseError)
    def handle_database_error(error):
        app.logger.error(
            "Database error occurred",
            extra={'extra_data': {
                'event': 'database_error',
                'error_type': 'DatabaseError',
                'message': str(error),
                'code': error.code
            }}
        )
        return jsonify({
            'error': str(error),
            'code': error.code
        }), 500

    @app.errorhandler(Exception)
    def handle_general_error(error):
        app.logger.error(
            "General error occurred",
            extra={'extra_data': {
                'event': 'general_error',
                'error_type': 'Exception',
                'message': 'Internal server error',
                'code': 'INTERNAL_ERROR'
            }},
            exc_info=True
        )
        return jsonify({
            'error': 'Internal server error',
            'code': 'INTERNAL_ERROR'
        }), 500

    return app

app = create_app('development')

if __name__ == '__main__':
    app.run(debug=True)