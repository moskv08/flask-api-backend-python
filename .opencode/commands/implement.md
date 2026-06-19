---
description: >
  Implement a feature or task by working through the Flask stack layer by layer,
  checking its own work at each step.
  Usage:
    /implement <description or reference to a /plan output>
---

# Implement

You are implementing a feature in a Flask + SQLAlchemy + Marshmallow + JWT project.
Work carefully, layer by layer. Check your own output before moving to the next layer.
Never skip steps to go faster — correctness over speed.

## Stack layering (always respect this order)

```
model → migration → validation schema → service → route → tests
```

Never write a route before the service exists. Never write a service before the model is correct.

## Process

### Step 1 — Clarify before touching code

Read the description or linked plan. If anything is ambiguous, ask now — not mid-implementation.

Specifically confirm:
- Does this require a DB change? (new model, new column, new relationship)
- Does this require auth? (`@jwt_required()`? Which roles?)
- Is there an existing service/route file to extend, or are we creating new files?
- Are there any known edge cases or constraints to handle?

If the description is clear, state your implementation plan in a short numbered list before starting. Wait for a thumbs-up or correction.

### Step 2 — Model (if DB change needed)

Edit the relevant file in `/models/`.

Rules:
- Use SQLAlchemy declarative base consistent with existing models
- Add `__tablename__` explicitly
- Use `db.relationship()` with explicit `back_populates` (not `backref`)
- Add indexes for any column used in `filter_by()` or `join()`
- Never put business logic in models — just schema and basic DB operations

After writing: read the model back and verify column types, nullability, and relationships make sense.

### Step 3 — Migration

Generate and review the migration:

```bash
uv run alembic revision --autogenerate -m "<description>"
```

Then read the generated file in `alembic/versions/`. Check for:
- ⚠️ Missing constraints (unique, check) — autogenerate often misses these
- ⚠️ Destructive operations (column drops, type changes) — flag these explicitly
- ⚠️ Missing index creation for new foreign keys

Fix the migration file manually if needed. Do not apply it yet.

Show the migration to the developer and confirm before proceeding.

### Step 4 — Validation schema

Create or update the Marshmallow schema in `/validation/`.

Rules:
- Separate request schema (input) from response schema (output)
- Use `@validates` for field-level business validation
- Use `Meta.unknown = EXCLUDE` on request schemas to ignore extra fields
- Required fields must be explicit — don't rely on model defaults for validation
- Response schemas should never expose password hashes, internal IDs unless needed, or sensitive fields

### Step 5 — Service

Create or update the service in `/services/<resource>_service.py`.

Rules:
- All business logic lives here — routes call services, services call models
- One function per operation (create, get, update, delete, list)
- Handle DB errors explicitly — catch `IntegrityError` for unique violations
- Always commit or rollback within the service, not in the route
- Return ORM objects or plain dicts — never return HTTP responses from a service

After writing each function: trace through it mentally and check for:
- SQLAlchemy session handling (commit, rollback, detached instance risks)
- Edge cases (not found, duplicate, empty result)
- Missing error handling

### Step 6 — Route

Create or update the route in `/routes/<resource>.py`.

Rules:
- Routes are thin: validate input → call service → return JSON
- Use the Marshmallow schema to validate request data before calling the service
- Return consistent response envelopes (match existing patterns in the project)
- Use correct HTTP status codes:
  - `200` for successful GET/PUT
  - `201` for successful POST (resource created)
  - `204` for successful DELETE (no body)
  - `400` for validation errors
  - `401` for missing/invalid auth
  - `403` for unauthorized action
  - `404` for not found
  - `409` for conflict (duplicate)
  - `422` for unprocessable entity
- Register blueprint in `app.py` if this is a new route file

### Step 7 — Tests

Generate tests for the new code using the same rules as `/test`:
- Happy path
- Validation errors
- Auth failures (if route is protected)
- Edge cases (not found, duplicate, empty)

### Step 8 — Self-review

Before declaring done, run through this checklist:

- [ ] Model changes have a migration
- [ ] Migration reviewed for destructive ops and missing constraints
- [ ] Request schema validates all required fields
- [ ] Response schema excludes sensitive fields
- [ ] Service handles not-found and duplicate cases
- [ ] Route uses correct HTTP status codes
- [ ] Blueprint registered if new file
- [ ] Tests cover happy path and at least 2 error cases
- [ ] No business logic leaked into the route
- [ ] No raw SQL queries (use SQLAlchemy ORM)

Report the checklist result to the developer. Flag any items that are incomplete and why.

### Step 9 — Apply migration

Only after the developer confirms the implementation looks good:

```bash
docker compose exec flaskapp uv run alembic upgrade head
```

Confirm with:
```bash
docker compose exec flaskapp uv run alembic current
```

---

## Tone

Be methodical, not hasty. If something doesn't feel right mid-implementation, stop and say so.
It's better to pause and ask than to build three layers on a wrong assumption.