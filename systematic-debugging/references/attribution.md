# Attribution

## Four-phase debugging method (SKILL.md)

Adapted from **obra/superpowers**' `systematic-debugging` skill (MIT, by Jesse Vincent):

- https://github.com/obra/superpowers (path `skills/systematic-debugging/`)

Not copied verbatim — the operating rule ("no fixes without root-cause investigation first"), the four phases, and the "≥3 failed fixes → question the architecture" escalation are kept faithful, but the skill is rewritten to fit this project: the phase-4 failing-test-first step ties to the root `CLAUDE.md` Rule 9 and TDD's red step, and the final verification hands off to `verify-before-done`.

`sources.lock` tracks the obra/superpowers ref; `skill-evolve` flags upstream rule changes for re-sync. The upstream orchestration pieces (subagent-driven-development, git worktrees, etc.) are not vendored — see `research/2026-06-05-skill-research-log.md`.
