---
name: issue-driven-dev
description: >
  A structured software development lifecycle for taking an identified issue (from code review,
  self-review, or a to-do) through to a safe, controlled implementation. Use this skill whenever
  the user says they want to work on a code review finding, fix a known issue, address technical
  debt, or refactor something in their project. Also trigger on phrases like "I want to work on",
  "I need to fix", "code review said", "I noticed a problem with", "let's tackle", or "how do I
  approach this change". Always produces a written plan for the user to review before any code is
  touched. Works hand-in-hand with the flask-project-guide skill for project-specific guidance.
  For Behavioral and Breaking changes, the tdd-enforcement skill is mandatory — strict
  red/green TDD applies to all new or modified functionality. No exceptions.
---

# Issue-Driven Development Lifecycle

A repeatable process for taking an identified problem → written plan → controlled implementation.
The plan is always produced and confirmed before touching any code.

---

## The Process

### Phase 1 — Confirm the Problem Statement

**Always start here.** Before anything else, reflect the issue back to the user in your own words
and ask them to confirm it is correctly understood. Do not skip this even if the issue seems obvious.

Present the restatement like this:

> **Problem as I understand it:**
> [Your restatement — what is wrong, where it lives, and why it matters]
>
> Does this match what you have in mind, or is there anything to adjust before we plan?

Wait for confirmation. Do not proceed to Phase 2 until the user says yes (or corrects you).

---

### Phase 2 — Scope & Classify

Once the problem statement is confirmed, determine:

**Change type** — pick one:
- 🎨 *Cosmetic* — renames, restructuring, no behavior change (e.g. URL pattern rename)
- ⚙️ *Behavioral* — logic changes, new/modified functionality → **TDD mandatory**
- 💥 *Breaking* — changes to the API contract, DB schema, or auth flow → **TDD mandatory**

> If the change type is ⚙️ or 💥, the tdd-enforcement skill activates. State this clearly
> when presenting the written plan. The test plan becomes part of Phase 3, and TDD Phases
> B–D replace the standard Phase 4 implementation flow.

**Scope** — list every layer of the stack that will be touched:
- Routes (`/routes`)
- Services (`/services`)
- Models + migrations (`/models`, Alembic)
- Validation schemas (`/validation`)
- Config / environment (`config.py`, Docker, `.env`)
- Tests (if they exist)
- Other (docs, scripts, etc.)

**Stack-specific risk flags** — check for any of these that apply:
- JWT-protected routes involved → token/auth behaviour must stay intact
- Alembic migration needed → must be generated, reviewed, and applied
- Docker rebuild required → image or config changes need `docker compose build`
- Public API contract change → external callers (Postman, frontend) break
- URL/blueprint registration in `app.py` → easy to miss

---

### Phase 3 — Written Plan

Produce a written plan the user will review before touching code. Structure it as follows:

---

**Plan: [Short title for this change]**

**Problem:** [One sentence restatement]

**Change type:** [Cosmetic / Behavioral / Breaking]

**What "done" looks like:**
- [Concrete checklist item]
- [Concrete checklist item]
- ...

**Files to change (in order of implementation):**

| Step | File | What changes |
|------|------|-------------|
| 1 | `path/to/file.py` | [What and why] |
| 2 | `path/to/file.py` | [What and why] |
| ... | | |

> Order: work bottom-up (models → services → routes) unless the change type
> dictates otherwise. Routes are the public surface — change them last.

**Risks & gotchas:**
- [Specific risk for this change, e.g. "blueprint prefix must also be updated in app.py"]
- [Any migration caveat, auth side-effect, Docker rebuild, etc.]

**Verification steps:**
- [ ] [Specific curl command or manual test]
- [ ] [Adjacent endpoint smoke test]
- [ ] Docker rebuild if needed: `docker compose up -d --build`
- [ ] Any migration: `docker compose exec flaskapp uv run alembic upgrade head`

**Out of scope / deferred:**
- [Anything explicitly not being done in this pass]

> **If change type is ⚙️ or 💥:** append a **Test plan** section here (see tdd-enforcement
> skill for the required table format). The test plan is reviewed and confirmed as part of
> this written plan — before any test or implementation code is written.

---

After presenting the plan, ask:

> Ready to start implementing, or would you like to adjust anything in the plan first?

Do not proceed until the user confirms the plan.

---

### Phase 4 — Implement

**🎨 Cosmetic changes:** work through the file list step by step. For each step:
1. Show the specific change (code snippet or diff-style)
2. Explain briefly why it's done this way in this stack
3. Flag if a follow-up step is now required (e.g. "next we update the blueprint registration")

**⚙️ Behavioral / 💥 Breaking changes:** hand off to the tdd-enforcement skill.
Follow TDD Phases B (red) → C (green) → D (refactor) in strict order.
Do not write any implementation code until the user confirms tests are red.

Use the flask-project-guide skill for any stack-specific patterns (auth, Alembic, uv commands, etc.)

---

### Phase 5 — Verify & Close

After all changes are made, run through the verification checklist from the plan.

Then produce a short closing summary:

**Change summary:** [2–3 sentences: what changed, why, and how it was verified]
**Deferred / follow-up:** [Anything punted to a later session, if applicable]

Then ask:

> Would you like a git commit message for this change?

If yes, produce a single ready-to-run command with a comprehensive message that covers:
- *What* changed (the concrete files/layers affected)
- *Why* (the problem it solves, referencing the issue if named)
- *How* (brief note on approach if non-obvious)

Example format:
```
git commit -m "refactor: remove 'flask' segment from API URL patterns

Routes previously used /api/flask/<resource> which was an unusual and
misleading naming pattern. Updated blueprint prefixes in app.py and all
route definitions in /routes to use /api/<resource> instead. No logic
changes — cosmetic refactor only."
```

Keep the subject line under 72 characters and follow conventional commit style
(`refactor:`, `fix:`, `feat:`, `chore:` etc.) where it fits naturally.

---

## Tone

This is a side project. Be direct and practical — no unnecessary ceremony. The plan should be
thorough enough to catch surprises, not so formal it becomes overhead. If a phase is trivially
short (e.g. a cosmetic rename touches only one file), say so and keep it brief.