---
name: python-style
description: Python code style rules for this project
---

# Python Style Rules

- PEP 8 strictly — max line length 88 (Black formatter)
- Type hints required on all function signatures
- Docstrings on all public functions (Google style)
- No wildcard imports (`from module import *`)
- f-strings preferred over `.format()` or `%`
- Prefer `pathlib` over `os.path`