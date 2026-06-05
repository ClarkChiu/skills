---
name: systematic-debugging
description: >-
  A disciplined four-phase debugging method that stops guess-and-check repair
  cycles: find the root cause before changing anything, compare broken against
  a working reference, test one hypothesis at a time, then fix only the cause
  with a failing test first. USE THIS SKILL when a bug is being chased,
  something is broken or flaky, an error/stack trace needs diagnosing, or fixes
  keep bouncing. Triggers on 「為什麼會壞」「這個 bug 怎麼修」「一直修不好」
  「找不到原因」「debug this」「why is this failing」「root cause」. Especially
  when two or more attempted fixes have already failed. Not for adding new
  features (that's design-gate) or for known one-line typo fixes.
allowed-tools: Read, Grep, Glob, Bash
---

# systematic-debugging

A method against thrashing. The operating rule:

> **No fixes without root-cause investigation first.**

Guess-and-check — changing something plausible and re-running — wastes time and quietly adds new bugs. Work the four phases in order.

## When to use, when not to

- **Use it** when chasing a bug, diagnosing an error or flaky behavior, or when fixes keep bouncing.
- **Skip it** for a known one-line typo, or for building new behavior (that's `design-gate`).
- **Escalation rule:** if **three or more** fixes have failed, STOP and question the architecture — the bug is probably not where you keep looking.

## The four phases

### 1. Root-cause investigation (before touching anything)

- Reproduce the problem consistently — an intermittent bug you can't trigger on demand isn't understood yet.
- Read the error message and stack trace in full. They often name the exact cause; don't skim past warnings.
- Check what changed recently (diff, recent commits) — most regressions have a culprit commit.
- Gather evidence across component boundaries; trace the data flow backward from the symptom to its source.

### 2. Pattern analysis

- Find a working example — a similar path that doesn't break, or the same code before it broke.
- Compare broken against working **completely**, not by eyeballing the obvious line.
- List every difference between the two. The cause is usually in that list.

### 3. Hypothesis and testing

- State an explicit theory of the root cause, in words, before changing code.
- Test it with the **smallest single-variable change** — change one thing, not five.
- Verify the result before moving on. If the theory was wrong, say so and form the next one; don't pile changes on top of a disproven guess.

### 4. Implementation

- Write a **failing test that reproduces the bug first** (this is the bug's regression test — watch it fail; the red-step rule lives in `design-gate`'s `references/writing-plans.md`, plus `CLAUDE.md` Rule 9).
- Implement the minimal fix that addresses **only the root cause** — not nearby code you think could be tidier.
- Verify no collateral damage: the new test passes, the rest of the suite still passes (gate this with `verify-before-done`).

## Why the order matters

Each phase exists to stop a specific failure mode: phase 1 stops fixing symptoms, phase 2 stops missing the real difference, phase 3 stops shotgun changes, phase 4 stops the bug coming back and stops the fix breaking something else. Skipping a phase reintroduces the failure mode it guards against.

## Boundary

Adapted from obra/superpowers' `systematic-debugging` (MIT); see `references/attribution.md`. Hands off to `verify-before-done` for the final "is it actually fixed" check, and shares the failing-test-first discipline with TDD.
