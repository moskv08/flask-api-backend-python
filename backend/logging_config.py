"""
Structured logging configuration for Flask API
"""
import logging
import json
from datetime import datetime

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
            # Create structured log entry
            log_entry = {
                'timestamp': datetime.utcnow().isoformat() + 'Z',
                'level': record.levelname,
                'logger': record.name,
                'message': record.getMessage(),
                'module': record.module,
                'function': record.funcName,
                'line_number': record.lineno,
            }
            
            # Handle exception info if present
            if record.exc_text:
                log_entry['exception'] = record.exc_text
            
            # Add extra fields from the log record if they exist
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
    """Log request start - this will be called in middleware"""
    pass

def log_request_end():
    """Log request end - this will be called in middleware"""
    pass

def log_error(error, context=None):
    """Log error with context"""
    # Create a logger for this module
    logger = logging.getLogger(__name__)
    
    error_info = {
        'event': 'error',
        'error_type': type(error).__name__,
        'message': str(error),
    }
    
    if context:
        error_info.update(context)
        
    logger.error(
        "Error occurred",
        extra={'extra_data': error_info},
        exc_info=True
    )