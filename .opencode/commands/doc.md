---
description: >
  Generate or update docstrings and README documentation for a module,
  service, or route file.
  Usage:
    /doc <file>                → docstrings for all public functions/classes
    /doc <file>:<function>     → docstring for one function
    /doc readme <module>       → README section describing the module
---

# Documentation Generator

Generate documentation that is actually useful — not just a restatement of the
function signature. Focus on *why* and *when*, not just *what*.

## Detect mode

- `/doc <file>` → **Docstrings** for all public functions and classes in the file
- `/doc <file>:<function>` → **Single docstring** for that function
- `/doc readme <module>` → **README section** describing the module for other developers

---

## Docstring mode

For each public function or class, generate a Google-style docstring:

```python
def create_user(email: str, password: str) -> User:
    """Create a new user and persist to the database.

    Hashes the password before storing. Raises ValidationError if the
    email is already registered.

    Args:
        email: The user's email address. Must be unique.
        password: Plain-text password. Will be hashed with bcrypt.

    Returns:
        The newly created User ORM instance.

    Raises:
        ValidationError: If a user with this email already exists.
    """
```

Rules:
- First line: one sentence, imperative mood ("Create", "Return", "Validate")
- Second paragraph: non-obvious behavior, side effects, exceptions raised
- Args: only document non-obvious parameters; skip self
- Returns: describe the shape, not just the type
- Raises: list every exception the caller might need to catch
- Skip docstrings for trivial getters/setters unless they have gotchas

Output the full updated file with docstrings inserted — not just the docstrings in isolation.

---

## README section mode

Produce a concise Markdown section (suitable for inclusion in the project README
or a `docs/` file) covering:

**Overview** — what this module is responsible for (2–3 sentences)

**Key functions / endpoints** — a small table or list of the most important
public interface, with one-line descriptions

**Usage example** — a short code snippet showing the most common usage pattern

**Notes** — anything a new developer needs to know before modifying this module
(auth requirements, session handling, ordering constraints, etc.)

---

## Tone

Write for a developer returning to this code after three months away.
Be specific. Avoid filler like "this function handles the logic for".
Say what it actually does.
