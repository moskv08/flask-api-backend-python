---
name: testing-patterns
description: How tests are written in this project
---

# Testing Patterns

- Framework: pytest with pytest-flask
- Test files mirror source structure: `tests/routes/test_users.py`
- Use `conftest.py` fixtures for app, client, and db setup
- Mock external services with `unittest.mock.patch`
- Each test function tests one behaviour, named `test_<what>_<when>`
- Assert response status code AND response body shape