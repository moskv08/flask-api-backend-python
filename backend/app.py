from flask import Flask, jsonify
from config import config
from models import db
from models.token_blocklist import TokenBlocklist
from routes import routes_bp
from flask_jwt_extended import JWTManager
from exceptions import ValidationError, NotFoundError, DuplicateError, DatabaseError

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

    # Error handlers
    @app.errorhandler(ValidationError)
    def handle_validation_error(error):
        return jsonify({
            'error': str(error),
            'code': error.code
        }), 400

    @app.errorhandler(DuplicateError)
    def handle_duplicate_error(error):
        return jsonify({
            'error': str(error),
            'code': error.code
        }), 409

    @app.errorhandler(NotFoundError)
    def handle_not_found_error(error):
        return jsonify({
            'error': str(error),
            'code': error.code
        }), 404

    @app.errorhandler(DatabaseError)
    def handle_database_error(error):
        return jsonify({
            'error': str(error),
            'code': error.code
        }), 500

    @app.errorhandler(Exception)
    def handle_general_error(error):
        return jsonify({
            'error': 'Internal server error',
            'code': 'INTERNAL_ERROR'
        }), 500

    return app

app = create_app('development')

if __name__ == '__main__':
    app.run(debug=True)