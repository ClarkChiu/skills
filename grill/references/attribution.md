# Attribution

`grill` is adapted from **mattpocock/skills** → `skills/productivity/grilling` (MIT),
with its sibling trigger `grill-me`. The core — interview relentlessly, one question
at a time, each with a recommended answer, look up facts but defer decisions, don't
enact until shared understanding — is Matt's. This is an **original rewrite**, no
files copied. Full evaluation: `research/audits/2026-07-08-grilling.md` (verdict:
🟦 build-your-own; discovered via the r/opencodeCLI "hmm" post, which named grilling
as its adversarial counterpart).

## What changed vs upstream

- **Standalone stress-tester, not a design flow.** Positioned as a lightweight,
  aim-at-anything "poke holes in this" mode for an idea/plan/PR that ALREADY exists —
  explicitly distinct from the self-built `design-gate` (which *produces* a design +
  task plan from a vague idea). The boundary is declared in SKILL.md and skill-map.
  This is the gap grilling fills that design-gate does not: adversarial temperament +
  standalone, mid-work usability.
- **Made the temperament explicit and tuned to this user.** Lead with the objection,
  no cushioning — matches CLAUDE.md's disagreement protocol (strongest counterargument
  first, no praise). Soft-spot targeting biased to this user's domain (protocol edge
  cases, concurrency/races, NAT/partition behavior, testability).
- **Added a handoff close.** Ends by summarizing survivors / changes / accepted risk,
  then hands off (design-gate / to-issues / build) rather than building — grill
  produces sharper thinking, not artifacts.
- **Language-aware trigger + reply** (English prose per the process-skill convention;
  responds in the conversation's language, Chinese stays natural Taiwan Traditional).

## Note on the upstream refactor (relevant to design-gate)

`grill-with-docs` still exists upstream at `skills/engineering/grill-with-docs`
(commit `658d53e`, 2026-05-31) but was **refactored into a thin composer** — its
SKILL.md is now just `Run a /grilling session, using the /domain-modeling skill.`
The pure interrogation was split out into `skills/productivity/grilling` (grill's
source), and the ADR / ubiquitous-language machinery moved into a **new**
`skills/engineering/domain-modeling` skill (`ADR-FORMAT.md` + `CONTEXT-FORMAT.md`,
commit `ee8bae4`, 2026-06-17). So the ADR/glossary content is **not gone — it
relocated**. `design-gate` pins `grill-with-docs` at `e3b90b5` (2026-05-28) for its
inline-ADR / ubiquitous-language phase; the real drift is minor (grill-with-docs →
2026-05-31) but the principle design-gate borrowed now actually lives in
`domain-modeling`. Flagged for the next `skill-evolve` pass: design-gate should
likely track `engineering/domain-modeling` too, since that's where ADR/glossary
refinements now land.

## Re-sync

`sources.lock` pins upstream at the grilling SKILL.md commit. On `skill-evolve`, mine
any refinement to the interrogation protocol; keep the standalone-vs-design-gate
framing, the explicit adversarial temperament, and the handoff-not-build close.
