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
   come from the user or stated evidence. A value you had to assume is not forbidden —
   it is **grade D** (rule 4), and it must be marked as such and carried into the
   sensitivity check. "Assumption" is not a separate label; D *is* the assumption label.
   A confident posterior built on invented numbers is the failure mode this skill exists
   to prevent.
3. **Compute with the scripts.** Call the lens's script for every number; do not eyeball
   the arithmetic.
4. **Grade every input, and pin the wording to the grade.** See below.
5. **Every brief ends with a stop condition.** A decision with no exit rule is a decision
   you cannot be wrong about — which is worse than a wrong one. See below.
6. **Lean Markdown out.** Output a structured Markdown brief (per the lens file) — no HTML,
   no PDF, no export pipeline. **Output language follows the user's question** (Traditional
   Chinese for a Chinese query — never Simplified).

### Input grades (non-negotiable 4)

Rule 2 stops invented numbers. This stops *real* numbers of wildly different quality being
laundered into one confident posterior. Tag every input in the brief with its grade — and
say it in the grade's own words, so the strength of the evidence is visible **in the
sentence**, not just in the analyst's head:

| Grade | What it is | Say it like this |
|---|---|---|
| **A** | The user's own measured data or logs, official statistics, current law/contract terms, a meta-analysis | "the record shows", "the contract states" |
| **B** | A single study, a sourced industry benchmark, a comparable case with known conditions | "one benchmark puts this at X — conditions differ" |
| **C** | Small sample, anecdote, expert intuition, the user's impression | "as a working estimate", "this frames the question, it does not settle it" |
| **D** | Assumed so the model can run at all | "assumed — the sensitivity check below is the real answer" |

Then the check that makes grading worth doing: **if the recommendation flips when the C
and D inputs move within their plausible range, the decision is fragile — say so in one
line and name the cheapest input that would upgrade to A or B.** Often the honest output
is not the answer but "go measure this one thing first."

### Watch window & stop condition (non-negotiable 5)

Close every brief with three lines — concrete, not aspirational:

- **Watch window** — when this gets re-examined ("re-run after 3 sprints" / "at the
  next invoice"). A date or an event, never "periodically".
- **Stop condition** — the specific observation that means this call was wrong and the
  commitment should be cut. Written *before* any money or time is spent, because it will
  never be written honestly afterwards.
- **Tripwire** — the one signal worth interrupting for if it appears early.

Kelly briefs already size the bet; the stop condition is what keeps a sized bet from
becoming an unbounded one. Crux briefs get a stop condition on the *primary* problem: the
evidence that would say you picked the wrong crux and should re-rank.

## Each run

1. **Read the problem** and state the decision read:
   *"Reading this as: a `<belief | priority | allocation>` decision about `<subject>`,
   stake `<low | medium | high>`."*
2. **Route** via `references/routing.md`:
   - belief / "is X true given evidence" → **Bayesian** (`references/bayesian.md`)
   - "what do I tackle first" among tangled problems → **Crux** (`references/crux.md`)
   - "how much to commit" with an edge → **Kelly** (`references/kelly.md`)
   - missing a required input → ask **one** question; spanning two → chain them in order.
3. **Gather inputs** from the user / evidence. Assign each one a grade (A/B/C/D) and carry
   the grade's wording into the brief.
4. **Compute** by calling the lens's script under `scripts/`:
   - `bayes_update.py` — odds update + Beta-Binomial conjugate posterior.
   - `crux_score.py` — primary/secondary problem ranking on three tests.
   - `kelly_size.py` — Kelly f\* + log-growth scenarios + fractional sizing.
   Each reads a JSON request (`--json '…'` or stdin) and prints JSON. Pure stdlib — no
   network, no environment/keys, no file writes.
5. **Write the brief** in the lens's structure, embedding the computed numbers and the
   action threshold / breakthrough / sizing. Run the sensitivity or no-edge check and say
   plainly whether the decision is fragile — including whether it survives the C/D inputs
   moving. Close with the watch window, stop condition, and tripwire.

## References

- `references/routing.md` — signals → lens, the clarify / chain branches, hard rules.
- `references/bayesian.md` — prior → likelihood ratios → posterior → threshold → sensitivity.
- `references/crux.md` — primary/secondary problem scoring and breakthrough action.
- `references/kelly.md` — edge inputs → fractional Kelly sizing, no-edge refusal.
- `references/attribution.md` — methods adapted from yao-open-skills' decision cluster (MIT)
  and, for the input grades + stop condition, from goutoujunshi (MIT since 2026-08-17, non-commercial at adoption —
  **ideas only; none of its text enters this skill**).

## Boundaries

| Need | Use instead |
|---|---|
| Rehearse a negotiation / interview / hard conversation | `roleplay-coach` |
| Find the root cause of a bug | `systematic-debugging` |
| Design + plan before writing code | `design-gate` |
| Actually learn/understand a topic | `tutor` |
