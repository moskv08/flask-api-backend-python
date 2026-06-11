---
description: >
  Planning and design command for a Flask API backend.
  Usage:
    /plan feature <description>   → plan a new feature before writing code
    /plan refactor <description>  → plan a refactor or architecture change
---

# Flask API Planning

## Detect mode

- `/plan feature <description>` → run **Feature Plan**
- `/plan refactor <description>` → run **Refactor Plan**
- `/plan` with no argument → ask: "Feature or refactor? Describe what you have in mind."

The project stack: Flask · SQLAlchemy · Marshmallow · Flask-JWT-Extended · Alembic · uv · Docker Compose · PostgreSQL

Architecture to respect:
```
HTTP request
  → /routes       (thin: parse, validate, call service, return JSON)
  → /services     (business logic, orchestrate models)
  → /models       (SQLAlchemy ORM)
  → PostgreSQL
```

---

## Feature Plan

Given a feature description, produce a concrete plan before any code is written.

### Output structure

**1. Goal clarification**
- Restate the feature in one sentence
- Call out any ambiguity that needs a decision before starting

**2. API surface**
- Proposed endpoints (method + URL + purpose)
- Request shape (fields, types, validation rules)
- Response shape (fields, status codes)
- Auth requirements (`@jwt_required()`? public?)

**3. Stack touch-points**
List every file likely to need changes, grouped by layer:
- Routes: `routes/<resource>.py` — what changes
- Services: `services/<resource>_service.py` — new functions needed
- Models: `models/<resource>.py` — new fields or models
- Validation: `validation/<resource>_schema.py` — new Marshmallow schemas
- Migrations: what the Alembic migration will need to do

**4. Edge cases & gotchas**
- Things that could go wrong or need special handling
- SQLAlchemy session / relationship caveats
- JWT / auth edge cases
- Docker / environment considerations

**5. Open questions**
- Decisions that need to be made before writing code
- Keep this list short — only genuine blockers

**6. Suggested order of implementation**
A numbered list: what to build first, second, etc., and why.

---

## Refactor Plan

Given a description of what to change, produce a safe migration plan.

### Output structure

**1. Current state**
- What the code does now and why it's worth changing
- Which files / layers are affected

**2. Target state**
- What the code should look like after
- Concrete structural or behavioral differences

**3. Migration steps**
A numbered sequence of small, independently-committable steps.
Each step: what to do, which files to touch, how to verify it worked.

**4. Risks**
- What could break
- Anything that requires a DB migration
- Auth / session implications

**5. Rollback plan**
- What to undo if something goes wrong mid-refactor
- Whether a DB migration is reversible

**6. Test strategy**
- What to test before starting (to lock in current behavior)
- What to test after (to confirm the refactor is correct)
