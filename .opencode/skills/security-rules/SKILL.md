---
name: security-rules
description: Security requirements to enforce in all code
---

# Security Non-Negotiables

- Never log request bodies that may contain passwords or tokens
- Always validate and sanitize user input before DB operations
- Never expose internal error messages to API consumers
- Secrets only via environment variables — never hardcoded
- CORS must be explicitly configured, never `*` in production