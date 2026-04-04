# Repository Overview

## Project Description
This is a fullstack Flask application built with Docker orchestration that demonstrates a complete web application structure with backend and database services. The application provides a RESTful API for managing users and todos, built with modern Python technologies.

Main purpose and goals:
- Demonstrate a layered Flask architecture with clear separation of concerns
- Provide a complete development environment using Docker
- Implement RESTful API endpoints for CRUD operations on users and todos
- Use modern Python tools like uv for dependency management
- Include proper database migrations with Alembic

Key technologies used:
- Flask (Python web framework)
- PostgreSQL database
- Docker and Docker Compose for orchestration
- uv for fast Python dependency management
- Alembic for database migrations
- Flask-JWT-Extended for authentication
- Marshmallow for data validation
- SQLAlchemy for ORM

## Architecture Overview
The application follows a layered architecture pattern:
- **API Routes**: HTTP request parsing and response formatting (in `/routes`)
- **Services**: Core business logic orchestration (in `/services`)  
- **Models**: Data structures and persistence logic (in `/models`)

Data flow:
1. HTTP requests are handled by Flask routes in `/routes`
2. Routes delegate to services in `/services` for business logic
3. Services interact with models in `/models` for data persistence
4. Models use SQLAlchemy ORM to communicate with PostgreSQL database

## Directory Structure
- `/backend`: Core API implementation with Flask application and database integration
  - `/routes`: HTTP endpoint definitions (users, todos, auth, test)
  - `/services`: Business logic implementation and orchestration
  - `/models`: SQLAlchemy models and database schema definitions  
  - `/validation`: Pydantic/Marshmallow models for request/response validation
  - `flask.dockerfile`: Docker configuration for the Flask app
- `/compose.yml`: Multi-container orchestration for the entire stack
- `/ROADMAP.md`: Development roadmap and future enhancements

Key files and configuration:
- `backend/app.py`: Main Flask application entry point with configuration and extensions
- `backend/config.py`: Configuration management for different environments (dev, prod, test)
- `backend/pyproject.toml`: Project dependencies and configuration using uv
- `backend/alembic.ini`: Alembic database migration configuration
- `backend/flask.dockerfile`: Docker image build configuration

## Development Workflow
To build/run the project:
1. Use `docker compose up -d` to start all services (Flask API and PostgreSQL database)
2. Access the API at http://localhost:4000
3. Database is accessible at port 5432

To run without Docker (development):
1. Navigate to backend directory
2. Run `uv sync` to install dependencies 
3. Run `uv run flask run` to start the Flask app

Testing approach:
- No explicit test files found, but the structure supports unit testing of services and models
- Authentication is handled via JWT tokens (flask-jwt-extended)

Development environment setup:
- Requires Docker and Docker Compose for full-stack local environment
- Uses uv for fast Python dependency management
- Follows layered architecture pattern

Lint and format commands:
- No explicit linting/formatting configuration found in the project
- The codebase appears to follow Python standards but no specific linter is configured