"""
Structured logging configuration for Flask API
"""
import logging
import logging.config
from flask import request, g
from datetime import datetime
import json

def setup_logging(app):
    """Setup structured logging for the Flask application"""
    
    # Configure root logger
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Create a custom formatter for structured logging
    class StructuredFormatter(logging.Formatter):
        def format(self, record):
            # Get the request context if available
            request_data = {}
            if hasattr(request, 'method') and hasattr(request, 'url'):
                request_data = {
                    'method': request.method,
                    'url': request.url,
                    'user_agent': getattr(request, 'user_agent', None),
                    'remote_addr': getattr(request, 'remote_addr', None)
                }
            
            # Get the current user if available
            user_data = {}
            if hasattr(g, 'current_user'):
                user_data = {
                    'user_id': getattr(g.current_user, 'id', None),
                    'user_name': getattr(g.current_user, 'name', None)
                }
            
            # Create structured log entry
            log_entry = {
                'timestamp': datetime.utcnow().isoformat() + 'Z',
                'level': record.levelname,
                'logger': record.name,
                'message': record.getMessage(),
                'module': record.module,
                'function': record.funcName,
                'line_number': record.lineno,
                'request': request_data,
                'user': user_data,
                'exception': record.exc_text if record.exc_text else None
            }
            
            # Add extra fields from the log record
            if hasattr(record, 'extra_data'):
                log_entry.update(record.extra_data)
            
            return json.dumps(log_entry)
    
    # Configure the application logger
    app.logger.setLevel(logging.INFO)
    
    # Remove default handlers to avoid duplicate logs
    if app.logger.handlers:
        for handler in app.logger.handlers:
            app.logger.removeHandler(handler)
    
    # Create a console handler with structured formatting
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(StructuredFormatter())
    app.logger.addHandler(console_handler)
    
    # Prevent propagation to avoid duplicate logs
    app.logger.propagate = False
    
    return app

def log_request_start():
    """Log request start"""
    if request.method and request.url:
        app.logger.info(
            "Request started",
            extra={'extra_data': {
                'event': 'request_start',
                'method': request.method,
                'url': request.url,
                'user_agent': getattr(request, 'user_agent', None),
                'remote_addr': getattr(request, 'remote_addr', None)
            }}
        )

def log_request_end(response):
    """Log request end"""
    if hasattr(request, 'method') and hasattr(request, 'url'):
        app.logger.info(
            "Request completed",
            extra={'extra_data': {
                'event': 'request_end',
                'method': request.method,
                'url': request.url,
                'status_code': response.status_code
            }}
        )
    return response

def log_error(error):
    """Log error with context"""
    app.logger.error(
        "Error occurred",
        extra={'extra_data': {
            'event': 'error',
            'error_type': type(error).__name__,
            'message': str(error),
            'traceback': getattr(error, '__traceback__', None)
        }},
        exc_info=True
    )