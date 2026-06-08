---
name: decision-lens
description: >-
  Pick the right decision method for a problem, then run the real math and return a lean
  Markdown decision brief. Routes to one of three lenses — Bayesian (should I believe X
  given this evidence? — priors, likelihood ratios, posterior, action thresholds), Crux
  (which tangled problem do I tackle first? — primary vs secondary, scored on
  decisiveness/leverage/stage), or Kelly (how much should I commit when I have an edge? —
  fractional Kelly sizing). USE THIS SKILL when the user faces a real decision and wants it
  reasoned, not just answered — "幫我決策", "該不該", "先打哪個 / 先解哪個", "投入多少 / 要押多少",
  "決策分析", "help me decide", "how confident should I be", "what should I prioritize",
  "how much should I allocate". Do NOT use to rehearse a conversation (roleplay-coach), to
  debug code (systematic-debugging), to design+plan before coding (design-gate), or to
  teach a topic (tutor).
license: MIT
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
---

# decision-lens — route a decision to the right method, then do the real math

Most "help me decide" answers are vibes dressed as analysis. This skill does the opposite:
it picks the *right* decision method for the problem, runs the actual computation with a
small auditable script, and hands back a lean decision brief grounded in numbers you can
check — never invented ones.

It is a **router over three lenses**. The whole reason these beat "just ask the model" is
the real math, so the math runs in `scripts/`, not in your head.

## The non-negotiables

1. **Route first.** State a one-line decision read, then pick exactly one lens (or clarify,
   or chain two). See `references/routing.md`.
2. **Never fabricate inputs.** Priors, likelihood ratios, win-rates, and problem scores
   come from the user or stated evidence. If you must assume a value, label it an
   **assumption** and run a sensitivity check. A confident posterior built on invented
   numbers is the failure mode this skill exists to prevent.
3. **Compute with the scripts.** Call the lens's script for every number; do not eyeball
   the arithmetic.
4. **Lean Markdown out.** Output a structured Markdown brief (per the lens file) — no HTML,
   no PDF, no export pipeline. **Output language follows the user's question** (Traditional
   Chinese for a Chinese query — never Simplified).

## Each run

1. **Read the problem** and state the decision read:
   *"Reading this as: a `<belief | priority | allocation>` decision about `<subject>`,
   stake `<low | medium | high>`."*
2. **Route** via `references/routing.md`:
   - belief / "is X true given evidence" → **Bayesian** (`references/bayesian.md`)
   - "what do I tackle first" among tangled problems → **Crux** (`references/crux.md`)
   - "how much to commit" with an edge → **Kelly** (`references/kelly.md`)
   - missing a required input → ask **one** question; spanning two → chain them in order.
3. **Gather inputs** from the user / evidence. Label any assumption.
4. **Compute** by calling the lens's script under `scripts/`:
   - `bayes_update.py` — odds update + Beta-Binomial conjugate posterior.
   - `crux_score.py` — primary/secondary problem ranking on three tests.
   - `kelly_size.py` — Kelly f\* + log-growth scenarios + fractional sizing.
   Each reads a JSON request (`--json '…'` or stdin) and prints JSON. Pure stdlib — no
   network, no environment/keys, no file writes.
5. **Write the brief** in the lens's structure, embedding the computed numbers and the
   action threshold / breakthrough / sizing. Run the sensitivity or no-edge check and say
   plainly whether the decision is fragile.

## References

- `references/routing.md` — signals → lens, the clarify / chain branches, hard rules.
- `references/bayesian.md` — prior → likelihood ratios → posterior → threshold → sensitivity.
- `references/crux.md` — primary/secondary problem scoring and breakthrough action.
- `references/kelly.md` — edge inputs → fractional Kelly sizing, no-edge refusal.
- `references/attribution.md` — methods adapted from yao-open-skills' decision cluster.

## Boundaries

| Need | Use instead |
|---|---|
| Rehearse a negotiation / interview / hard conversation | `roleplay-coach` |
| Find the root cause of a bug | `systematic-debugging` |
| Design + plan before writing code | `design-gate` |
| Actually learn/understand a topic | `tutor` |
