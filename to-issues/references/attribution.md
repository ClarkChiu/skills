# Attribution

`to-issues` is adapted from **mattpocock/skills** → `engineering/to-issues` (MIT). The
idea — break a plan into vertical, independently-grabbable issues — is Matt's; this is an
**original rewrite**, no files copied. Full evaluation:
`research/audits/2026-06-08-mattpocock-skills.md` (verdict: 🟦 build-your-own).

## What changed vs upstream

- **Positioned as the `design-gate` downstream.** design-gate emits a task plan →
  to-issues publishes it; the boundary (don't re-plan, that's design-gate) is explicit.
- **Confirm-before-publish gate.** The user chose "always show the full list and wait for
  approval before creating anything" — the skill creates no issue until approved, because
  it writes to a real tracker.
- **Uses the existing `gh`/`glab` session**, never reads or stores tokens; stops and defers
  `gh auth login` to the user if unauthenticated.
- Kept the vertical tracer-bullet slicing + dependency ordering (the genuinely good core).
  Dropped the upstream's tracker-config coupling (`setup-matt-pocock-skills`); this skill
  just uses whatever `gh`/`glab` is already set up.

## Re-sync

`sources.lock` pins upstream. On `skill-evolve`, mine slicing/ordering refinements; keep
the design-gate-downstream framing and the confirm-before-publish gate.
