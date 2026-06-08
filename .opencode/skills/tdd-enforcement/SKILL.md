---
name: tdd-enforcement
description: >
  Enforces strict test-driven development (red/green cycle) for any new functionality
  in the Flask project. This skill is NOT standalone — it is invoked automatically by
  the issue-driven-dev skill whenever Phase 2 classifies a change as Behavioral or Breaking.
  Do not invoke this skill for Cosmetic changes (renames, restructuring with no logic change).
  The strict cycle is: write the test first → confirm it fails (red) → implement the feature
  → confirm the test passes (green). Implementation MUST NOT begin before the red step is
  confirmed by the user. Assumes pytest infrastructure is already in place.
---

# TDD Enforcement — Strict Red/Green Cycle

Applies to all **Behavioral** and **Breaking** changes in the issue-driven-dev lifecycle.
Replaces Phase 4 (Implement) for those change types. Cosmetic changes skip this entirely.

---

## When This Activates

In Phase 2 of issue-driven-dev, if change type is ⚙️ Behavioral or 💥 Breaking, state:

> This change introduces new or modified functionality, so we'll follow a strict TDD cycle.
> Implementation won't start until we have a failing test in place.

Then proceed with the phases below instead of the standard Phase 4.

---

## TDD Phase A — Design the Tests

Before writing any test code, produce a **test plan** as part of the written plan (Phase 3
of issue-driven-dev). Add a dedicated section:

---

**Test plan:**

| # | Test name | What it asserts | Layer |
|---|-----------|----------------|-------|
| 1 | `test_<name>` | [Expected behaviour in plain English] | unit / integration |
| 2 | `test_<name>` | [Expected behaviour in plain English] | unit / integration |
| ... | | | |

**Test file(s):** `tests/[test_routes_x.py / test_services_x.py / ...]`

> Layer guidance for this stack:
> - **Unit** → test services in isolation (mock DB / dependencies)
> - **Integration** → test routes end-to-end via Flask test client (hits real service + DB)
> - When in doubt, prefer integration tests for new endpoints; unit tests for complex service logic

---

This test plan is part of the written plan the user confirms before any code is touched.

---

## TDD Phase B — Write the Tests (Red)

Write all test stubs and assertions first. No implementation code yet.

For each test in the plan:
1. Show the complete test function
2. Identify exactly what it will fail on (missing route, missing service method, wrong response shape, etc.)

Then instruct the user to run the tests:

```
docker compose exec flaskapp uv run pytest tests/<test_file>.py -v
```

Then ask:

> Please run the tests above and confirm they all fail (red). Share the output or
> just confirm before we move to implementation.

**Do not proceed to TDD Phase C until the user confirms the tests are red.**
This is a hard gate — do not skip it even if failure seems obvious.

---

## TDD Phase C — Implement (Green)

Only after red is confirmed: implement the feature, working through the file list
from the issue-driven-dev written plan (bottom-up: models → services → routes).

For each implementation step:
1. Show the code change
2. Note which test(s) it is intended to make pass
3. Flag any follow-on steps required

After all implementation steps are done, instruct the user to run the tests again:

```
docker compose exec flaskapp uv run pytest tests/<test_file>.py -v
```

Then ask:

> Please confirm the tests are now passing (green).

**Do not proceed to Phase 5 (Verify & Close) of issue-driven-dev until green is confirmed.**

---

## TDD Phase D — Refactor (if needed)

Once green, briefly assess whether the implementation needs cleanup:
- Any duplication introduced?
- Any shortcuts taken to get to green that should be tidied?
- Any edge cases the tests don't yet cover that are worth adding?

If nothing needs attention, say so explicitly and move on. Keep this short — it is a
check, not a full review.

---

## Test Writing Guidelines for This Stack

**Use Flask test client for route tests:**
```python
def test_create_todo(client, auth_headers):
    response = client.post("/api/todos", json={...}, headers=auth_headers)
    assert response.status_code == 201
    assert response.json["title"] == "..."
```

**Mock at the service boundary for unit tests:**
```python
def test_todo_service_create(mocha, db_session):
    # test service logic in isolation from routes
```

**JWT-protected routes** — always include auth headers in integration tests;
failure to do so should return 401, which is itself worth a test case.

**Naming convention:** `test_<verb>_<resource>_<condition>`
e.g. `test_create_todo_returns_201`, `test_get_user_not_found_returns_404`

---

## Non-Negotiable Rules

1. **No implementation before red is confirmed.** Always.
2. **Tests live in** `tests/` and mirror the layer they test
   (`test_routes_todos.py`, `test_services_todos.py`, etc.)
3. **Each new endpoint gets at least:** a happy-path test and a notable failure case
   (e.g. 404, 401, 422 validation error)
4. **The test plan is part of the written plan** — it is reviewed and confirmed
   alongside the file table before anything is written