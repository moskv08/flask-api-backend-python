# backend/utils/response_formatter.py
"""Standardized response formatting utilities for the Flask API."""

from flask import jsonify


def format_success(data=None, message=None, status_code=200):
    """
    Format a successful API response.
    
    Args:
        data: The response data (optional)
        message: A success message (optional)
        status_code: HTTP status code (default 200)
    
    Returns:
        JSON response with standardized format
    """
    response = {
        "data": data,
        "error": None,
        "message": message,
        "status": status_code
    }
    
    # Remove None values to keep response clean
    return {k: v for k, v in response.items() if v is not None}


def format_error(message, code=None, status_code=500):
    """
    Format an error API response.
    
    Args:
        message: Error description
        code: Error code (optional)
        status_code: HTTP status code (default 500)
    
    Returns:
        JSON response with standardized format
    """
    response = {
        "data": None,
        "error": message,
        "code": code,
        "status": status_code
    }
    
    # Remove None values to keep response clean
    return {k: v for k, v in response.items() if v is not None}


def format_validation_error(messages, status_code=400):
    """
    Format a validation error response.
    
    Args:
        messages: Validation error messages
        status_code: HTTP status code (default 400)
    
    Returns:
        JSON response with standardized format
    """
    return format_error(messages, 'VALIDATION_ERROR', status_code)