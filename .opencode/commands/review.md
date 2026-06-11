---
description: >
  Full or focused code review for a Flask API backend.
  Usage:
    /review              → full review across all areas
    /review security     → authentication, vulnerabilities, secrets
    /review api          → REST design, validation, response format
    /review db           → SQLAlchemy models, queries, migrations
    /review quality      → PEP8, dead code, naming, refactor candidates
    /review tests        → coverage, fixtures, missing scenarios
    /review arch         → structure, blueprints, config, app factory
    /review deps         → requirements, pinning, vulnerable packages
    /review errors       → error handlers, logging, bare excepts
---

# Flask API Code Review

## Detect mode

Look at the invocation:
- If called as `/review` with no argument → run **Full Review** (all sections below)
- If called as `/review <area>` → run **Focused Review** for that area only

---

## Full Review

Analyze the entire project and produce a structured Markdown report:

### 1. Architecture & Structure (`arch`)
- Project layout and separation of concerns (blueprints, models, services, routes)
- Adherence to Flask best practices and application factory pattern
- Configuration management (dev/prod/test environments, secrets handling)

### 2. API Design (`api`)
- REST conventions (HTTP methods, status codes, URL naming)
- Request validation and input sanitization
- Response consistency and error response format

### 3. Security (`security`)
- Authentication and authorization checks (JWT, sessions, API keys)
- Protection against common vulnerabilities: SQL injection, XSS, CSRF
- Sensitive data exposure (secrets in code, verbose error messages)

### 4. Database & ORM Usage (`db`)
- SQLAlchemy model design and relationships
- Query efficiency (N+1 queries, missing indexes)
- Migration strategy (Flask-Migrate / Alembic)

### 5. Error Handling & Logging (`errors`)
- Global error handlers registered via `@app.errorhandler`
- Meaningful log messages and appropriate log levels
- No bare `except` clauses swallowing exceptions silently

### 6. Code Quality (`quality`)
- PEP 8 compliance and naming conventions
- Dead code, commented-out blocks, or TODO items
- Repeated logic that should be refactored into utilities or decorators

### 7. Testing (`tests`)
- Test coverage of routes and edge cases
- Use of fixtures and mocking external dependencies
- Missing test scenarios

### 8. Dependencies (`deps`)
- `requirements.txt` / `pyproject.toml` pinned versions
- Unused or outdated packages
- Known vulnerable packages (flag any you recognize)

For each section, list:
- ✅ What is done well
- ⚠️ What needs improvement
- 🔴 Critical issues that should be fixed before production

End with a **prioritized action list of the top 5 things to fix first**, each with a one-line rationale.

---

## Focused Review

When called with a specific area (e.g. `/review security`), do the following:

1. **Read only the relevant files** for that area — don't scan the whole project
2. Go deep rather than broad
3. Output **at most 5 findings**, ranked by severity (🔴 critical first, then ⚠️, then ✅)
4. Each finding must include:
   - What the issue is
   - Where exactly it is (file + line if possible)
   - A concrete fix or code snippet
5. End with **one next action** — the single most important thing to do right now

### Area focus guides

**`arch`** — `app.py`, blueprint registration, `config.py`, project folder structure  
**`api`** — route files, Marshmallow schemas, HTTP status codes, response shapes  
**`security`** — JWT decorators, input handling, `.env` / config files, error messages  
**`db`** — SQLAlchemy models, service-layer queries, Alembic migration files  
**`errors`** — error handlers, logging calls, `try/except` blocks  
**`quality`** — any Python file; look for duplication, naming, dead code, TODOs  
**`tests`** — `tests/` folder, fixture setup, coverage gaps  
**`deps`** — `pyproject.toml`, `uv.lock`, installed packages  
