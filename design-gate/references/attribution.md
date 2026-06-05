# Attribution

## Design and plan workflow (brainstorming.md, writing-plans.md)

Rules adapted from **obra/superpowers** (MIT, by Jesse Vincent), from two of its skills:

- `brainstorming`: https://github.com/obra/superpowers (path `skills/brainstorming/`)
- `writing-plans`: https://github.com/obra/superpowers (path `skills/writing-plans/`)

Not copied verbatim — the rules are **extracted and rewritten to fit this project**: dropped the upstream branded paths (`docs/superpowers/...`), handed execution discipline off to the root `CLAUDE.md` Rules 0–12, and retargeted examples to this user's domain (pytest + git, protocols/testing/infrastructure). The upstream orchestration pieces (`subagent-driven-development`, the Visual Companion local server) are **not vendored**; rationale and verdict are in `research/2026-06-05-skill-research-log.md`.

`sources.lock` tracks the obra/superpowers ref; when those two upstream skills add new rules, `skill-evolve` flags them for re-sync.

## Further upstream

obra/superpowers' "design before code" stance shares a root with this repo's `CLAUDE.md` — Rule 1 (think before coding) and Rule 4 (goal-driven execution). design-gate is essentially the **front half** of that discipline (design, plan) turned into a repeatable workflow.
