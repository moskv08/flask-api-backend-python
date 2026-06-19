from flask import Flask, jsonify, request, g
from config import config
from models import db
from models.token_blocklist import TokenBlocklist
from routes import routes_bp
from flask_jwt_extended import JWTManager
from exceptions import ValidationError, NotFoundError, DuplicateError, DatabaseError
from logging_config import setup_logging
import logging

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

    # Request logging middleware - simplified approach to avoid circular imports
    @app.before_request
    def log_request_start():
        # Log basic request info at the beginning of each request
        if request.method and request.url:
            logger = logging.getLogger(__name__)
            logger.info(
                "Request started",
                extra={'extra_data': {
                    'event': 'request_start',
                    'method': request.method,
                    'url': request.url,
                    'user_agent': getattr(request, 'user_agent', None),
                    'remote_addr': getattr(request, 'remote_addr', None)
                }}
            )

    @app.after_request
    def log_request_end(response):
        # Log basic request info at the end of each request
        if hasattr(request, 'method') and hasattr(request, 'url'):
            logger = logging.getLogger(__name__)
            logger.info(
                "Request completed",
                extra={'extra_data': {
                    'event': 'request_end',
                    'method': request.method,
                    'url': request.url,
                    'status_code': response.status_code
                }}
            )
        return response

    # Error handlers - using consistent error response format
    @app.errorhandler(ValidationError)
    def handle_validation_error(error):
        # Log the error with structured logging
        logger = logging.getLogger(__name__)
        logger.error(
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
        # Log the error with structured logging
        logger = logging.getLogger(__name__)
        logger.error(
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
        # Log the error with structured logging
        logger = logging.getLogger(__name__)
        logger.error(
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
        # Log the error with structured logging
        logger = logging.getLogger(__name__)
        logger.error(
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
        # Log the error with structured logging
        logger = logging.getLogger(__name__)
        logger.error(
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