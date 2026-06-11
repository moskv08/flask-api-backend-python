# Flask API Service

A high-performance, layered Flask API application built with Python, utilizing `uv` for lightning-fast dependency management and `Docker` for containerized deployment.

## 🏗️ Architecture Overview
The application follows a strict layered architecture to ensure separation of concerns:
**API Routes** $\rightarrow$ **Services** $\rightarrow$ **Models**

- **Routes**: HTTP request parsing and response formatting.
- **Services**: Core business logic orchestration.
- **Models**: Data structures and persistence logic.

## 🛠️ Development Workflow

### Prerequisites
- [uv](https://github.com/astral-sh/uv) (Recommended for Python management)
- Docker & Docker Compose (For full-stack local environment)

### Local Setup
1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd <project-folder>
   ```

2. **Synchronize dependencies:**
   Using `uv`, this command creates a virtual environment and installs all required packages from `uv.lock`.
   ```bash
   uv sync
   ```

3. **Run the application:**
   ```bash
   uv run flask run
   ```

### Docker Deployment
To spin up the entire stack (API, Database, etc.) using the provided Compose configuration:
```bash
docker compose up -d
```

To stop the stack:
```bash
docker compose down
```

## 🚀 Project Structure
- `/backend`: Core API implementation.
- `/compose.yml`: Multi-container orchestration.
- `pyproject.toml`: Unified project configuration and dependency definitions.

## 📜 License
This project is licensed under the MIT License.

---

### 2. The `backend/README.md`
This version contains the technical "Deep Dive" and your reorganized **Development Roadmap**.

# Backend Service Implementation

This directory contains the core logic of the Flask API, following a layered architecture pattern.

## 📂 Internal Structure

- `routes/`: Endpoint definitions (e.s., `/users`, `/tasks`).
- `services/`: Business logic implementation and orchestration.
- `models/`: SQLAlchemy models and database schema definitions.

## 🔐 Security Configuration

### Secret Key Setup
The application requires a secure SECRET_KEY to be set as an environment variable. For security reasons, the application will not start if the SECRET_KEY is not properly configured.

**For Development:**
1. Create a `.env` file in the `backend/` directory
2. Add your secret key: `SECRET_KEY=your-secure-secret-key-here`

**For Production:**
Set the SECRET_KEY as an environment variable in your deployment environment:
```bash
export SECRET_KEY=your-secure-secret-key-here
```

**Security Requirements:**
- The secret key must be at least 32 characters long
- Use a cryptographically secure random string
- Never commit the secret key to version control
- Rotate keys periodically for enhanced security
- The application will fail to start if SECRET_KEY is not set
- `validation/`: Pydantic models for request/response integrity.
- `alembic/`: Database migration scripts managed via Alembic.

## 🗄️ Database Migrations
We use **Alembic** to manage database schema changes. To generate and apply migrations:

### Local Development Migrations
1. **Create a new migration:**
   ```bash
   uv run alembic revision --autogenerate -m "description of change"
   ```

2. **Apply migrations:**
   ```bash
   uv run alembic upgrade head
   ```

### Docker Deployment Migrations
When deploying with Docker, database migrations are handled automatically:

1. **For local Docker deployment:**
   ```bash
   docker compose up -d
   ```

2. **To run migrations in the Docker container:**
   ```bash
   docker compose exec flaskapp uv run alembic upgrade head
   ```

3. **To create a new migration in Docker:**
   ```bash
   docker compose exec flaskapp uv run alembic revision --autogenerate -m "description of change"
   ```

### Migration Best Practices
- Always run `alembic revision --autogenerate` before making database schema changes.
- Migrations should be tested in a development environment before applying to production.
- When using Docker, ensure the database service is running before executing migration commands.

### Migration Configuration
The Alembic configuration is located at `alembic.ini` and uses the database URL from your environment variables. The Docker deployment automatically sets the correct `DATABASE_URL` environment variable for the Flask service.