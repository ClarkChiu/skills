# Attribution

## Completion gate (SKILL.md)

Adapted from **obra/superpowers**' `verification-before-completion` skill (MIT, by Jesse Vincent):

- https://github.com/obra/superpowers (path `skills/verification-before-completion/`)

Not copied verbatim — the operating rule and the five-step gate are kept faithful, but the skill is rewritten to fit this project: tied to the root `CLAUDE.md` Rule 12 (fail loud), and deliberately scoped to **not** overlap the built-in `verify` skill (which launches the app to observe behavior) — this one is the lighter discipline gate for any test/lint/build/fix claim.

`sources.lock` tracks the obra/superpowers ref; `skill-evolve` flags upstream rule changes for re-sync. The upstream orchestration pieces (subagent-driven-development, git worktrees, etc.) are not vendored — see `research/2026-06-05-skill-research-log.md`.
