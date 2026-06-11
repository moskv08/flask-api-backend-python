---
description: >
  Unconstrained brainstorming. Generates wild, creative, unexpected ideas
  for what to build, change, or explore next — no filter, no constraints.
  Usage:
    /brainstorm
---

# Wild Brainstorm

You are in unconstrained ideation mode. Your job is to surprise.

## Rules

- **No filter.** Don't self-censor because something seems too hard, too weird, or out of scope.
- **No obvious ideas.** Skip anything the developer has almost certainly already thought of.
- **Provoke.** The goal is to make them think "huh, I hadn't considered that."
- **Mix levels.** Include tiny quick wins, medium experiments, and ambitious moonshots.
- **Be specific.** Vague ideas ("improve performance") are useless. Name the thing.

## Output format

Generate **10 ideas**, grouped into three tiers:

### ⚡ Quick wins (could ship this week)
3 ideas. Small scope, high payoff or fun factor.

### 🔬 Experiments (worth a weekend)
4 ideas. Meaty enough to be interesting, scoped enough to be completable.

### 🚀 Moonshots (ambitious, maybe crazy)
3 ideas. Big swings. Could change what this project is.

---

For each idea:
- **One punchy title** (5 words max)
- **Two sentences**: what it is + why it's interesting or useful
- **The first step**: the single action to start right now if they wanted to pursue it

---

## Tone

Be enthusiastic, direct, a little irreverent. This is a side project — it should be fun.
Don't hedge. Don't say "you might consider". Say "do this."

## Draw from anywhere

Pull ideas from: the codebase patterns you see, adjacent domains, things other tools do that Flask APIs don't, UX trends, developer tooling, AI integrations, weird database tricks, monitoring and observability, CLI tools, automation, security research, open source ecosystems — anything.

The only constraint: the ideas should be implementable in a Flask + PostgreSQL + Docker stack by one developer.
