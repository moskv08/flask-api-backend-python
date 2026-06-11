---
description: >
  Generate pytest tests for a route, service function, or model method.
  Fixtures included, edge cases covered.
  Usage:
    /test <file>
    /test <file>:<function_or_class>
---

# Test Generator

Generate production-quality pytest tests for the target code. Don't generate
tests that just confirm the happy path — cover what can go wrong.

## Before generating tests

Read:
- The target file and function/class
- Existing tests in `tests/` to match conventions (fixtures, naming, structure)
- Related schemas (Marshmallow) for request/response shapes
- Auth decorators to know if JWT is required

## Output structure

**1. Fixtures needed**
List any fixtures required that don't already exist. Show the code for each.
Reuse existing fixtures where possible — don't duplicate `test_client`, `db_session`, etc.

**2. Test cases**
Generate the full pytest code. Group tests in a class if testing one resource.

Cover in this order:
- ✅ Happy path (valid input, expected response)
- ⚠️ Validation errors (missing fields, wrong types, constraint violations)
- 🔒 Auth failures (missing token, expired token, wrong role if applicable)
- 🔴 Edge cases (empty results, duplicate data, boundary values)
- 💥 Error paths (DB failure if mockable, downstream service errors)

**3. What's not covered**
Be honest. List test scenarios that would be valuable but are omitted
(e.g. require complex setup, external services, or are out of scope for unit tests).

## Conventions to follow

- Use `pytest` and `pytest-flask`
- Mock external calls with `unittest.mock.patch` or `pytest-mock`
- Use `factory_boy` or direct model creation for test data if the project uses it
- Assert on status code first, then response body shape, then specific values
- Test function names: `test_<action>_<condition>_<expected_result>`
  e.g. `test_create_user_missing_email_returns_422`

## Tone

Output only code and brief inline comments. No prose explanations unless
something genuinely needs a note to the developer.
