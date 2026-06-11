---
description: >
  Explain a piece of code in plain language — what it does, why it's built
  that way, and what depends on it.
  Usage:
    /explain <file>
    /explain <file>:<function_or_class>
---

# Code Explanation

You are explaining code to the developer who wrote it — they know Flask and Python
but may have forgotten the details. Be precise, not patronizing.

## Output structure

**1. What it does**
One short paragraph. No jargon, no hedging. Just what this code actually does.

**2. Why it's structured this way**
Point out deliberate design decisions — patterns used, trade-offs made, things
that might look odd but have a reason. If something looks accidental or unclear,
flag it honestly.

**3. Dependencies & coupling**
- What does this code call or import?
- What calls or depends on *this* code?
- What would break if this were removed or renamed?

**4. Gotchas**
Anything non-obvious that would trip someone up when modifying this code.
SQLAlchemy session behavior, JWT context requirements, order-sensitive logic, etc.
Skip this section if there's nothing worth flagging.

**5. One-line summary**
End with a single sentence that could serve as a docstring for this code.

## Tone

Direct and concrete. Skip filler phrases like "this function is responsible for".
Just say what it does.
