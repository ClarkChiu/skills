# Attribution

## Completion gate (SKILL.md)

Adapted from **obra/superpowers**' `verification-before-completion` skill (MIT, by Jesse Vincent):

- https://github.com/obra/superpowers (path `skills/verification-before-completion/`)

Not copied verbatim — the operating rule and the five-step gate are kept faithful, but the skill is rewritten to fit this project: tied to the root `CLAUDE.md` Rule 12 (fail loud), and deliberately scoped to **not** overlap the built-in `verify` skill (which launches the app to observe behavior) — this one is the lighter discipline gate for any test/lint/build/fix claim.

`sources.lock` tracks the obra/superpowers ref; `skill-evolve` flags upstream rule changes for re-sync. The upstream orchestration pieces (subagent-driven-development, git worktrees, etc.) are not vendored — see `research/2026-06-05-skill-research-log.md`.

## Second axis — intent drift (SKILL.md "Second axis: did it drift from intent?")

The idea that a completion gate must also check the work didn't silently drift from what the user *meant* — not just that the claim has evidence — is from **Geoffrey Litt**'s "Understanding is the new bottleneck" (his AI Engineer / AIE 2026 talk, July 2026; concrete mechanic: an AI-generated explainer with a quiz you must pass before shipping a change):

- Primary: https://www.geoffreylitt.com/2026/07/02/understanding-is-the-new-bottleneck.html
- Simon Willison's write-up ("Understand to participate"): https://simonwillison.net/2026/jul/2/understand-to-participate/

**Idea only — nothing vendored, and deliberately NOT in `sources.lock`**: a conference talk / tweet thread is not a diffable GitHub upstream, so there is nothing for `skill-evolve` to track. The "three checks / miss-a-constraint vs misread-the-goal / self-classify sure-fuzzy-blind" phrasing is an original reimplementation of the acceptance-by-understanding principle, re-aimed at the agent surfacing its own drift for the user (the note author's "five education practices" overlay was not adopted — most of it was already covered by design-gate / grill / tutor; see `research/2026-07-12-skill-research-log.md`).
