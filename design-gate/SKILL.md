---
name: design-gate
description: >-
  Design gate before coding: turn a vague idea into an agreed design, then a
  task-by-task plan an engineer can execute independently. Two phases — first
  DESIGN (converge requirements one question at a time, propose 2–3 approaches,
  write a design doc, self-review), then a HARD GATE (no code, no scaffolding,
  no implementation until the user approves the design), then PLAN (break work
  into 2–5 minute tasks, each with exact file paths, complete code, verification
  commands, and a commit). USE THIS SKILL when the user wants to plan a feature
  or change before writing code, or says 「先設計」「幫我規劃」「寫個計畫」
  「動手前先想清楚」「design first」「write a plan」「plan this before coding」.
  Especially for multi-step work where jumping straight to code risks rework.
  Do NOT use for trivial one-line changes, or when a design/plan already exists
  and the user just wants it executed.
allowed-tools: Read, Grep, Glob, Write, Edit, AskUserQuestion
---

# design-gate

Two gates before code: **pin down the requirements (design), then break them into steps anyone can follow (plan).** The most expensive anti-pattern is "this is too simple to need a design" — *"'simple' projects are where unexamined assumptions cause the most wasted work."* The design can be short (a few sentences for a truly simple change), but you MUST present it and get approval.

This skill only owns the **front half**: design and plan. The discipline for actually writing and testing code is already in this repo's root `CLAUDE.md` — Rule 1 (think before coding), Rule 2 (simplicity first), Rule 4 (goal-driven execution), Rule 9 (tests verify intent), Rule 12 (fail loud). This skill does not repeat those; it **feeds into** them: once the design and plan are settled, execution follows your existing rules.

Rules adapted from obra/superpowers' `brainstorming` and `writing-plans` (MIT), rewritten to fit this project. Details in `references/`.

## When to use, when not to

- **Use it** for a multi-step feature or change where you want the design and steps pinned down before touching code.
- **Skip it** for a one-line change, or when a design/plan already exists and you just want it executed.

## Flow: two phases, one hard gate between them

```
[DESIGN] explore context → converge (one Q at a time) → propose 2–3 approaches
         → present in sections, approve each → write design doc → self-review
   │
   ▼  ←─── HARD GATE: until the user approves the design, do NOT write code,
   │                  scaffold a project, or invoke any implementation skill
[PLAN] break into 2–5 min tasks (exact paths + complete code + verify + commit)
       → hand off to execution
```

### Phase 1 — Design (details in `references/brainstorming.md`)

1. **Explore context**: read the relevant code, docs, and existing design first — including any project **glossary / `CONTEXT.md`** and existing **ADRs** (`docs/adr/`) — so questions build on the current state and the project's own vocabulary instead of asking what's already written.
2. **Converge, one question at a time**: *only one question per message.* Prefer multiple-choice over open-ended. Focus on purpose, constraints, and success criteria.
3. **Propose 2–3 approaches** with trade-offs — don't just build the first idea.
4. **Present the design in sections** (architecture, components, data flow, error handling, testing) and get approval after each section before moving on.
5. **Flag oversized scope on the spot**: if one request really spans several independent subsystems, say so and split it into sub-projects.
6. **Sharpen terms and capture decisions as you go.** Use the project's words; when a term is fuzzy, pin it down and record it (a glossary line / `CONTEXT.md`). When a *significant* architectural choice is settled, write a short **ADR** to `docs/adr/NNNN-<topic>.md` right then — don't batch them. Format and "what counts as ADR-worthy" in `references/adr.md`.
7. **Write the design doc** to `docs/specs/YYYY-MM-DD-<topic>-design.md`.
8. **Self-review** before handing off (placeholder scan, internal consistency, scope, ambiguity — see the reference).

### The hard gate

Until the user has explicitly approved the design doc, do **NOT**: write any code, scaffold any project, or invoke any implementation skill. This gate is the whole point of the skill — don't skip it to "get moving."

### Phase 2 — Plan (details in `references/writing-plans.md`)

Break the approved design into a task list that meets one bar: **a skilled engineer who knows almost nothing about this codebase can execute it independently, without coming back to ask.**

- Each task is **one action, 2–5 minutes**.
- Each task carries: **exact file paths** (create/modify/test), **complete runnable code** (no pseudocode, no `TODO`), **verification commands with expected output**, and a **commit**.
- Tuned to your domain: the task cycle is **write a failing test → run it to confirm it fails → minimal implementation → run tests to confirm pass → commit** (pytest + git).
- Write the plan to `docs/plans/YYYY-MM-DD-<topic>.md`.

### Handoff to execution

Once the plan is written and saved, hand back to execution. Default: **execute the plan task-by-task in the current session**, following this repo's `CLAUDE.md` discipline (Rule 4 goal-driven, Rule 9 tests verify intent, Rule 12 fail loud).

> Optional (advanced): if you later want Claude to run autonomously for a long stretch, dispatching a fresh subagent per task with review between tasks, that's superpowers' `subagent-driven-development` orchestration — **not vendored here** (rationale in `research/2026-06-05-skill-research-log.md`). Evaluate vendoring it if you actually want that.

## Artifacts and paths

| Phase | Artifact | Path |
|---|---|---|
| Design | design doc | `docs/specs/YYYY-MM-DD-<topic>-design.md` |
| Design | ADR (per significant decision) | `docs/adr/NNNN-<topic>.md` (see `references/adr.md`) |
| Plan | task plan | `docs/plans/YYYY-MM-DD-<topic>.md` |

(Paths are configurable; the defaults carry no upstream branding.)

## Boundaries

- Produces only the design and plan documents — **no implementation code** (that comes after the gate, after handoff).
- For general docs, proposals, or decision records (not a pre-code design+plan), use the built-in `doc-coauthoring` skill instead — design-gate is specifically the gate that runs *before writing code*.
- No shell, no network. Context exploration is read-only (Read/Grep/Glob); ask the user for git history if you need it.
- Commit messages follow this repo's convention: gitmoji + Conventional, no `Co-Authored-By` trailer.
