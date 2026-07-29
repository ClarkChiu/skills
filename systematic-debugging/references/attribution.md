# Attribution

## Four-phase debugging method (SKILL.md)

Adapted from **obra/superpowers**' `systematic-debugging` skill (MIT, by Jesse Vincent):

- https://github.com/obra/superpowers (path `skills/systematic-debugging/`)

Not copied verbatim — the operating rule ("no fixes without root-cause investigation first"), the four phases, and the "≥3 failed fixes → question the architecture" escalation are kept faithful, but the skill is rewritten to fit this project: the phase-4 failing-test-first step ties to the root `CLAUDE.md` Rule 9 and TDD's red step, and the final verification hands off to `verify-before-done`.

## Evaluated and rejected: eliminated-hypothesis list (2026-07-29)

An "explicit eliminated list" rule was drafted for phase 3, adapted from **xieziyu/duetlens**' cross-round disposition protocol (`docs/design/rerun.md` @ `4abff67e6671`) — a restarted hunt should treat already-disproven theories as an input rather than re-deriving them, with the list living in `handover`'s "Dead ends & gotchas" past the session boundary.

**Measured, found redundant, reverted the same day.** Two A/B evals (with-skill vs no-skill, Sonnet):

- Eliminated list handed to the model in the prompt — both arms used it, neither re-tested the excluded theories, and the no-skill arm produced the better hypothesis list.
- Eliminated list *not* mentioned, hidden in a `.claude/handovers/` doc in the repo — **both arms went looking for it unprompted, found it, and respected its scope caveats.** The only delta was formatting (the skill arm labeled the section "Eliminated — do not re-test these").

Conclusion: producing the record is already `handover`'s job, and consuming it is default behavior — the rule bought nothing. Recorded here so the same idea isn't re-adopted from the same source later; the evidence is in `research/audits/2026-07-29-duetlens.md`. Nothing from Duetlens is used by this skill, so its GPL-3.0 has no bearing here.

`sources.lock` tracks the obra/superpowers ref; `skill-evolve` flags upstream rule changes for re-sync. The upstream orchestration pieces (subagent-driven-development, git worktrees, etc.) are not vendored — see `research/2026-06-05-skill-research-log.md`.
