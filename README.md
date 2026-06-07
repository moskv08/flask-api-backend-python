# Fullstack Flask Application

This is a fullstack Flask application built with Docker orchestration. It demonstrates a complete web application structure with backend and database services.

## Project Structure

```
.
├── backend/
│   ├── app.py
│   ├── pyproject.toml
│   └── flask.dockerfile
├── compose.yml
├── README.md
└── ROADMAP.md
```

## Services

### Backend Service (Flask)
- Built with Flask web framework
- Runs on port 4000
- Uses PostgreSQL database
- Dockerized with flask.dockerfile
- Implements a layered architecture (Routes → Services → Models)
- Uses uv for fast Python dependency management

### Database Service (PostgreSQL)
- Runs on port 5432
- Uses PostgreSQL 13
- Data persisted in named volume

## Getting Started

### Prerequisites
- Docker and Docker Compose installed
- uv (for local development)

### Running the Application

1. Start all services:
   ```bash
   docker-compose -f compose.yml up
   ```

2. Access the application:
   - Backend API: http://localhost:4000
   - Database: http://localhost:5432

### Development

To rebuild and start services after changes:
```bash
docker-compose -f compose.yml up --build
```

## Backend

The backend is built with Flask and includes:
- RESTful API endpoints (users, todos, auth, test)
- Database integration (PostgreSQL)
- Docker configuration
- Layered architecture pattern (Routes → Services → Models)
- uv dependency management

### Setup Instructions

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Install dependencies (if running without Docker):
   ```bash
   uv sync
   ```

3. Run the application:
   ```bash
   uv run flask run
   ```

### API Endpoints

- `GET /api/users` - Retrieve all users
- `POST /api/users` - Create a new user
- `GET /api/users/{id}` - Retrieve a specific user
- `PUT /api/users/{id}` - Update a specific user
- `DELETE /api/users/{id}` - Delete a specific user

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m 'Add some feature'`
4. Push to the branch: `git push origin feature/your-feature`
5. Open a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.