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
   the user or stated evidence. A value you had to assume is **grade D** (rule 2) and goes
   into the sensitivity check — D *is* the assumption label; don't invent a second one.
2. **Grade every input A/B/C/D and use the grade's own wording** (table in `SKILL.md`):
   A = measured record / official statistics / law / meta-analysis ("the record shows");
   B = one study or sourced benchmark ("one benchmark puts this at X — conditions differ");
   C = small sample / anecdote / impression ("as a working estimate");
   D = assumed ("assumed — the sensitivity check is the real answer").
   Then say whether the call survives the C and D inputs moving, and name the cheapest
   input that would upgrade to A or B.
3. **Compute with the scripts, not in your head.** Call the lens's script for every number.
4. **Close every brief with the exit rule** — watch window, stop condition, tripwire
   (see `SKILL.md`). Every lens file's brief structure ends with these three lines; they
   are not optional decoration.
5. **Output is a lean Markdown brief** (structure per the lens file). No HTML, no PDF, no
   export step. Output language follows the user's question (Traditional Chinese for a
   Chinese query — never Simplified).
