# ADR — Architecture Decision Record

An ADR captures **one significant decision**: the context that forced it, the decision
made, and the consequences accepted. The point is to preserve the *why* — six months later
the code shows what, never why. (Format after Michael Nygard.)

## When to write one (ADR-worthy?)

Write an ADR when a decision is **significant and not obvious from the code**:

- A choice between real alternatives with trade-offs (protocol A vs B, sync vs async,
  library X vs rolling your own, a data model, a boundary).
- Something a future reader would otherwise re-litigate ("why didn't we just use…?").
- A constraint you're accepting on purpose (a limit, a non-goal, a deferred concern).

Do **not** ADR trivia (naming, formatting, a one-line fix) — that's noise.

## Where + naming

One decision per file, in `docs/adr/`, zero-padded sequential:
`docs/adr/0001-use-pseudo-tcp-for-nat-traversal.md`. Files are **append-only**: don't edit
a decided ADR — if it changes, write a new ADR and mark the old one **Superseded by
ADR-NNNN**.

## Format

```markdown
# ADR-0001: <short decision title>

- **Status:** Proposed | Accepted | Superseded by ADR-NNNN
- **Date:** YYYY-MM-DD

## Context
What forced this decision — the constraints, the forces in tension, what we know and don't.

## Decision
The choice, stated plainly. "We will …".

## Consequences
What this buys and what it costs — the good, the bad, and the new constraints it creates.
Include the alternatives considered and why they lost.
```

## In the design-gate flow

Capture ADRs **inline** during Phase 1, the moment a significant choice is settled — not
batched at the end. The design doc (`docs/specs/…`) holds the whole design; ADRs are the
lighter, decision-focused records that outlive it and travel with the codebase. A glossary
line in `CONTEXT.md` does the same for *terms* (ubiquitous language) the way an ADR does
for *decisions*.
