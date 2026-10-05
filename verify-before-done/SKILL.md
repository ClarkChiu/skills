---
name: verify-before-done
description: >-
  A completion gate: never claim something is done, working, passing, or fixed
  without first running the verification fresh and reading its full output.
  Turns "fail loud" from a principle into a five-step gate. USE THIS SKILL
  before stating that tests pass, a build succeeds, a bug is fixed, a migration
  completed, or a feature works — and when reviewing whether such a claim is
  actually backed by evidence. Triggers on 「跑過了嗎」「確認一下有沒有過」
  「真的好了嗎」「verify before done」「is it actually passing」, or any moment
  you're about to report success. Gates two axes: that a claim is backed by
  fresh evidence (false green), and — on delegated or non-trivial work — that
  the result didn't silently drift from what the user meant (a true green on
  the wrong thing). Does NOT replace the built-in `verify` skill
  (which launches the app to observe behavior) — this is the lighter discipline
  gate that applies to any test/lint/build/fix claim. Not for exploratory work
  with nothing to claim yet.
allowed-tools: Read, Grep, Glob, Bash
---

# verify-before-done

A gate against false "done". The operating rule:

> **No completion claim without fresh verification evidence.**

This is `CLAUDE.md` Rule 12 (fail loud) turned into a concrete gate. "It passes", "it's fixed", "the build is green", "the migration completed" — every one of those is a claim, and a claim needs evidence you just produced, not assumed. That's the first axis. A claim can also be green and still solve the wrong thing — correct code aimed at the wrong target; the second axis (below) catches that on delegated work.

## When to use, when not to

- **Use it** right before you report that something passes / works / is fixed / completed.
- **Skip it** for exploratory work where there's nothing to claim yet.
- This is **not** the built-in `verify` skill (which launches the app and watches behavior). This one is the lightweight discipline gate for any test / lint / build / fix claim. They compose: use this gate, and reach for `verify` when the right evidence is "run the app and observe".

## The five-step gate

Before making any completion claim:

1. **Identify** the exact command whose output would prove the claim (the test, the linter, the build, the repro).
2. **Run it fresh, in full** — not a remembered result from earlier, not a subset.
3. **Read the entire output and the exit code** — not just the last line, not a proxy like "no errors scrolled past".
4. **Check the output actually confirms the claim** — the failure count is zero, the specific test named in the claim passed, the repro no longer reproduces.
5. **Only then** state the result, with the evidence attached.

Skipping any step is a violation of the gate.

## What counts as a real claim

Treat paraphrases and implications the same as the literal word "done":

- "Tests pass" is a claim — even if you say "should pass" or "looks green".
- "Fixed the bug" is a claim — even if you only changed code that looks related.
- "Migration completed" is a claim — and it's wrong if any record was skipped silently.

If you can't attach fresh output that confirms it, don't claim it. Say what you actually know: what you ran, what it showed, what's still unverified.

## Common false-green traps

- Reporting a remembered pass from before your last change.
- Reading "0 failed" but missing "12 skipped" or "3 errored".
- A test that passed because it asserts nothing (a test you never watched fail proves nothing — see the red-step rule in `design-gate`).
- "The linter passed" when you actually only ran it on one file.
- Running only the test file your task touched instead of the project's whole suite — or leaving a failure out of the report because you didn't cause it. Name every failure the run shows, pre-existing ones included.
- Exit code 0 from a wrapper script that swallowed an inner failure.

## Second axis: did it drift from intent?

The five-step gate catches a **false green** — a claim with no evidence behind it. It does not catch a **true green on the wrong thing**: tests pass, build is clean, and the work still solves a problem you weren't asked to solve, on a silent wrong assumption. Fresh output proves the code does what the *code* says — never that it does what the user *meant*.

So on delegated or non-trivial work, add a cheap drift check before "done" — surface the drift yourself, don't wait to be caught:

1. **Name the top two or three checks.** "To confirm I didn't drift from what you meant, check these" — aimed at the riskiest decisions, not trivia: the assumption you're least sure of, a constraint you only inferred, a path you never tested against the actual goal.
2. **Call the likelier failure mode:** did you **miss a constraint** (something true about their world you never saw) or **misread the goal** (constraints understood, wrong target)? Bet on one.
3. **List the silent assumptions** the work stands on, so a wrong one is visible instead of buried.

Then it's the user's move — self-classify each part as sure / fuzzy / only-trusting-you-here, and probe the fuzzy. Don't classify for them; make it possible by doing 1–3.

The payoff of surfacing 1–3: if the work later breaks, the user can localize it fast — reasoning drifted, or a constraint was missed — instead of diagnosing from zero.

## Boundary

Adapted from obra/superpowers' `verification-before-completion` (MIT); the intent-drift second axis is from Geoffrey Litt's "Understanding is the new bottleneck" (the code-quiz thesis; idea only, not a tracked repo) — see `references/attribution.md`. This skill only gates claims — it doesn't decide what the right verification is for a given task; that's your judgment (and for "run the app and observe", the built-in `verify` skill).
