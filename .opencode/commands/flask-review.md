---
description: Full code review for a Flask API backend
---

# Flask API Code Review

Perform a thorough code review of this Flask API backend. Analyze the entire project and produce a structured Markdown report covering:

## 1. Architecture & Structure
- Project layout and separation of concerns (blueprints, models, services, routes)
- Adherence to Flask best practices and application factory pattern
- Configuration management (dev/prod/test environments, secrets handling)

## 2. API Design
- REST conventions (HTTP methods, status codes, URL naming)
- Request validation and input sanitization
- Response consistency and error response format

## 3. Security
- Authentication and authorization checks (JWT, sessions, API keys)
- Protection against common vulnerabilities: SQL injection, XSS, CSRF
- Sensitive data exposure (secrets in code, verbose error messages)

## 4. Database & ORM Usage
- SQLAlchemy model design and relationships
- Query efficiency (N+1 queries, missing indexes)
- Migration strategy (Flask-Migrate / Alembic)

## 5. Error Handling & Logging
- Global error handlers registered via `@app.errorhandler`
- Meaningful log messages and appropriate log levels
- No bare `except` clauses swallowing exceptions silently

## 6. Code Quality
- PEP 8 compliance and naming conventions
- Dead code, commented-out blocks, or TODO items
- Repeated logic that should be refactored into utilities or decorators

## 7. Testing
- Test coverage of routes and edge cases
- Use of fixtures and mocking external dependencies
- Missing test scenarios

## 8. Dependencies
- `requirements.txt` / `pyproject.toml` pinned versions
- Unused or outdated packages
- Known vulnerable packages (flag any you recognize)

For each section, list:
- ✅ What is done well
- ⚠️ What needs improvement
- 🔴 Critical issues that should be fixed before production

End with a prioritized action list of the top 5 things to fix first.