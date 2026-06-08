---
name: tdd
description: >-
  Build a feature or fix a bug test-first, with a strict red-green-refactor loop:
  one failing test that pins one behaviour → run it to confirm it FAILS for the
  right reason → minimal code to pass → run to confirm green → refactor only on
  green → commit. USE THIS SKILL when the user wants to build or change behaviour
  test-first, says 「用 TDD」「測試先行」「red-green-refactor」「先寫測試」, or wants tests that
  actually pin the behaviour. Language-agnostic discipline with pytest / network-
  protocol integration examples. It is the BUILD-loop middle of the pipeline:
  `design-gate` (plan) → tdd (build) → `verify-before-done` (final gate). Do NOT
  use to plan before coding (design-gate), to chase an existing bug to root cause
  (systematic-debugging), or to merely claim something passes (verify-before-done).
license: MIT
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
---

# tdd — red-green-refactor, one behaviour at a time

Test-first done properly drives the design, not just checks it. The loop is small and
non-negotiable; the value is that each test pins **one** behaviour and would fail if the
business logic regressed (CLAUDE.md Rule 9 — tests verify intent, not just behaviour).

This is the **build** phase. Plan with `design-gate` first; gate the final claim with
`verify-before-done`. design-gate's `writing-plans` already states the canonical
"failing-test-first / red step"; this skill executes that loop in depth.

## The loop (never skip a step)

1. **Pick one behaviour.** The smallest slice that's worth a test. If you can't name it in
   one sentence, it's too big — split it.
2. **RED — write ONE failing test** that asserts that one behaviour. Run it. **Confirm it
   fails, and fails for the right reason** (asserting the real thing, not a typo / import
   error). A test that passes immediately, or errors instead of failing, is not a red.
3. **GREEN — minimal code to pass.** The least code that makes the test green — not the
   general solution, not the next feature. Run the test. Confirm green.
4. **REFACTOR — only on green.** Clean up names, duplication, structure with the test green
   the whole time. **Never refactor while red.** Re-run to confirm still green.
5. **Commit** the green state, then take the next behaviour.

## Hard rules

- **One test, one behaviour, one reason to fail.** No test that asserts five things.
- **Never write code with no failing test demanding it.** If nothing is red, stop and write
  the test first.
- **Never refactor on red.** Red means "make it pass," not "improve it."
- **The test must be able to fail when the logic is wrong.** `assert get_name() == "John"`
  is worthless if the function hardcodes "John". Pin the behaviour, not a constant.
- **Don't delete or weaken a test to get green** — that inverts the whole method.

## Test design & mocking

- What to test and what not to: `references/test-design.md`.
- When to mock vs use the real thing — especially for **network/protocol** code where a
  real socket on loopback beats a mock that encodes your assumptions:
  `references/mocking.md`.

## Examples

`references/test-design.md` and `references/mocking.md` use **pytest**, including a
**network-protocol integration** example (a real loopback socket round-trip). The loop and
rules are language-agnostic; the commands shown are pytest + git.

## Boundary

| Need | Use |
|---|---|
| Settle the design + task plan before coding | `design-gate` |
| Diagnose an existing bug's root cause | `systematic-debugging` |
| Final gate before claiming done/passing | `verify-before-done` |
