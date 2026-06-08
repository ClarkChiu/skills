# Routing — pick the lens before you analyze

Read the problem, state a one-line **decision read** (what kind of decision is this, how
big is the stake), then route to exactly one lens — or clarify, or chain two.

## The decision read

Say it in one line before anything else:

> **Reading this as: a `<belief | priority | allocation>` decision about `<subject>`,
> stake `<low | medium | high>`.**

## Signals → lens

| If the problem is about… | Signals | Lens |
|---|---|---|
| **Whether to believe something** given evidence | "is X true?", "should I trust this signal?", a hypothesis + data, diagnosis, "how confident should I be?" | **Bayesian** → `bayesian.md` |
| **What to tackle first** among many tangled problems | "where do I start?", limited resources, several interlocking issues, "what's the real bottleneck?", triage | **Crux** → `crux.md` |
| **How much to commit** when you have an edge | "how much should I bet/invest/allocate?", sizing under uncertainty with a known-ish edge | **Kelly** → `kelly.md` |

## Two special branches

- **Clarify (ask ONE question).** If the lens is obvious but a *required input* is missing
  (no prior, no win-rate, no candidate list), ask exactly one targeted question, then
  proceed. Never silently invent the missing number — that defeats the whole point.
- **Chain (multiple lenses).** Some problems need two in sequence. The common chain:
  **Crux first** (which problem is primary) **→ Bayesian** on that primary problem
  (how confident are we in the leading explanation), or **→ Kelly** (how much to commit to
  the chosen bet). Say so explicitly and run them in order.

## Hard rules (all lenses)

1. **Never fabricate inputs.** Priors, likelihood ratios, win-rates, and scores come from
   the user or stated evidence. If you must assume, label it **assumption** and run a
   sensitivity check.
2. **Compute with the scripts, not in your head.** Call the lens's script for every number.
3. **Output is a lean Markdown brief** (structure per the lens file). No HTML, no PDF, no
   export step. Output language follows the user's question (Traditional Chinese for a
   Chinese query — never Simplified).
