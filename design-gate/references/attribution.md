# Attribution

## Design and plan workflow (brainstorming.md, writing-plans.md)

Rules adapted from **obra/superpowers** (MIT, by Jesse Vincent), from two of its skills:

- `brainstorming`: https://github.com/obra/superpowers (path `skills/brainstorming/`)
- `writing-plans`: https://github.com/obra/superpowers (path `skills/writing-plans/`)

Not copied verbatim — the rules are **extracted and rewritten to fit this project**: dropped the upstream branded paths (`docs/superpowers/...`), handed execution discipline off to the root `CLAUDE.md` Rules 0–12, and retargeted examples to this user's domain (pytest + git, protocols/testing/infrastructure). The upstream orchestration pieces (`subagent-driven-development`, the Visual Companion local server) are **not vendored**; rationale and verdict are in `research/2026-06-05-skill-research-log.md`.

`sources.lock` tracks the obra/superpowers ref; when those two upstream skills add new rules, `skill-evolve` flags them for re-sync.

## Ubiquitous language + ADR capture (adr.md, the inline-capture step)

The Phase 1 step "sharpen terms and capture decisions as you go" + `references/adr.md`
adapt a **principle** from **mattpocock/skills** → `engineering/grill-with-docs` (MIT):
couple the plan-grilling interview to a living domain glossary and capture ADRs inline as
decisions crystallise (rather than batching docs at the end). The ADR format itself is the
standard Michael Nygard structure (public, not copyrightable). No files copied; pinned in
`sources.lock`. Full evaluation: `research/audits/2026-06-08-mattpocock-skills.md`.

## Spec conventions (spec-conventions.md)

`references/spec-conventions.md` is **original** to this repo. It draws only on public,
non-copyrightable standards — **RFC 2119** requirement keywords (IETF) and **Given/When/Then**
acceptance scenarios (Gherkin convention). No files copied, no GitHub upstream to track, so
nothing is added to `sources.lock`. Added 2026-06-30; rationale in
`research/2026-06-30-gentle-ai-borrowed-ideas.md`.

## Further upstream

obra/superpowers' "design before code" stance shares a root with this repo's `CLAUDE.md` — Rule 1 (think before coding) and Rule 4 (goal-driven execution). design-gate is essentially the **front half** of that discipline (design, plan) turned into a repeatable workflow.
