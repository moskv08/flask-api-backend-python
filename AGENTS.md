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
- The project structure supports unit testing but no actual test files are present
- Authentication is handled via JWT tokens (flask-jwt-extended)

Development environment setup:
- Requires Docker and Docker Compose for full-stack local environment
- Uses uv for fast Python dependency management
- Follows layered architecture pattern

## Key Implementation Details

### Authentication and Security
- JWT-based authentication with token blocklist functionality in `/backend/models/token_blocklist.py`
- Password handling is not yet properly implemented (plain text passwords in auth route - needs fixing)
- Logout functionality requires proper token blacklisting implementation

### Database and Migrations
- SQLAlchemy models in `/backend/models/` with proper relationships
- Alembic database migrations in `/backend/alembic/`
- Indexes on frequently queried columns (user_id) should be added for performance
- Session management with proper transaction handling and rollback

### Testing
- No actual test files present in the codebase (though structure suggests testing patterns exist)
- Test infrastructure needs to be implemented for services and routes
- Authentication and user creation endpoints have critical logic issues that need testing

### API Design
- RESTful conventions with proper HTTP methods and status codes
- Consistent URL naming patterns (/users, /users/{id}/todos)
- Standardized error response format with proper HTTP status codes
- Input validation using Marshmallow in some routes and manual checks in others

### Environment Configuration
- Environment-based configuration for secrets (SECRET_KEY, DATABASE_URL)
- Support for development, production, and testing environments
- Configuration loading in `backend/app.py` using `config.py`

## Important Commands and Workflow

### Running the Application
- `docker compose up -d` to start all services
- `uv sync` in `/backend` to install dependencies for local development  
- `uv run flask run` in `/backend` to start the Flask dev server

### Database Operations
- Use `alembic` commands in `/backend` directory for database migrations:
  - `alembic revision --autogenerate -m "Migration message"` to create new migrations
  - `alembic upgrade head` to apply migrations

### Development Guidelines
1. Follow the layered architecture pattern (routes → services → models)
2. All database operations must use proper session handling with commit/rollback
3. Error handling should consistently use custom exceptions from `/backend/exceptions.py`
4. JWT authentication decorators must be applied to protected routes
5. Logging should use the structured logging configuration in `/backend/logging_config.py`