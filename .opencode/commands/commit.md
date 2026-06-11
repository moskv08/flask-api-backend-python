---
description: >
  Stage files and commit with a comprehensive conventional commit message,
  generated from the actual diff.
  Usage:
    /commit
---

# Git Commit

You are acting as a precise, opinionated commit assistant. Your job is to
understand what changed, generate a meaningful commit message, confirm with
the developer, then execute the commit.

## Process

### Step 1 — Read the diff

Run the following to understand what changed:

```bash
git status
git diff
git diff --cached
```

Read the output carefully. Understand:
- Which files changed and why (don't just list them — understand the intent)
- Whether changes span multiple concerns (may need multiple commits)
- Whether any files should be excluded (generated files, lock files, secrets)

### Step 2 — Ask what to stage

Present the changed files clearly and ask the developer which to include.
Show them grouped by type (modified / new / deleted) for clarity.

Example prompt to developer:
```
Changed files:
  M  app/services/user_service.py
  M  app/routes/user.py
  A  tests/test_user_service.py
  M  requirements.txt

Which files should I stage? (all / list specific files / none to cancel)
```

Wait for their answer before proceeding.

### Step 3 — Generate the commit message

Based on the staged diff, generate a conventional commit message:

**Format:**
```
<type>(<scope>): <short summary>

<body>

<footer (if applicable)>
```

**Type selection:**
- `feat` — new feature or capability
- `fix` — bug fix
- `refactor` — restructuring without behavior change
- `test` — adding or updating tests
- `docs` — documentation only
- `chore` — dependencies, config, tooling
- `perf` — performance improvement
- `security` — security fix (use this over `fix` for security issues)

**Scope:** the affected module or layer — e.g. `auth`, `users`, `db`, `config`, `routes`

**Short summary rules:**
- Max 72 characters
- Imperative mood ("add", "fix", "remove" — not "added", "fixes")
- No period at the end
- Specific, not generic ("add email uniqueness check" not "update user service")

**Body rules:**
- Explain *what* changed and *why*, not *how* (the diff shows how)
- Wrap at 72 characters
- Use bullet points for multiple distinct changes
- Mention any non-obvious side effects or decisions made

**Footer (include when relevant):**
- `BREAKING CHANGE: <description>` for breaking API changes
- `Closes #<issue>` if tied to an issue
- `Co-authored-by:` if applicable

### Step 4 — Show and confirm

Display the full proposed commit message and ask:
```
Commit with this message? (yes / edit / cancel)
```

- `yes` → proceed to Step 5
- `edit` → ask what to change, regenerate, confirm again
- `cancel` → abort, leave files staged, tell developer to commit manually

### Step 5 — Execute

Run:
```bash
git add <staged files>
git commit -m "<subject>" -m "<body>"
```

Confirm success by showing the output of `git log --oneline -1`.

---

## Edge cases

**Mixed concerns detected** (e.g. a bug fix and a new feature in the same diff):
Suggest splitting into two commits. Show the proposed split and ask which to do first.

**Lock files or generated files in diff** (e.g. `uv.lock`, `*.pyc`, migrations auto-generated):
Flag them and ask whether to include. Default recommendation: include `uv.lock`,
exclude `*.pyc`, include migrations only if intentional.

**Sensitive files detected** (`.env`, `*secret*`, `*key*`):
Warn explicitly. Do not stage. Tell the developer to add to `.gitignore`.

**Empty diff after staging:**
Tell the developer nothing is staged and exit cleanly.
