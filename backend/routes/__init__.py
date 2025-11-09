from flask import Blueprint

# Import your route blueprints here
from .users import users_bp

# Create a blueprint for the routes
routes_bp = Blueprint('routes', __name__)

# Register the individual blueprints (no url_prefix needed since it's already in users.py)
routes_bp.register_blueprint(users_bp)

# Export the blueprint so it can be imported in app.py
__all__ = ['routes_bp']