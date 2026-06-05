---
name: flask-conventions
description: Coding conventions and patterns for this Flask API project
---

# Flask Project Conventions

## Project Structure
- Routes live in `routes/` as Blueprints, registered in `app/__init__.py`
- Business logic goes in `services/`, never directly in routes
- SQLAlchemy models live in `models/`, one file per domain entity
- Shared utilities go in `utils/`

## Response Format
All API responses must follow this envelope:
```json
{ "data": ..., "error": null, "status": 200 }
```

## Error Handling
- Use the global `@app.errorhandler` in `app/errors.py`
- Never return raw exceptions — always wrap in the error envelope
- HTTP 422 for validation errors, 401 for auth, 404 for not found

## Database
- Always use SQLAlchemy ORM, no raw SQL
- Migrations via Flask-Migrate (`flask db migrate`)
- Use `db.session` context manager pattern

## Auth
- JWT via Flask-JWT-Extended
- Protect routes with `@jwt_required()` decorator
- User identity via `get_jwt_identity()`