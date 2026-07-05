# Attribution

`skill-evolve`'s **usage-mining** evidence stream (the second stream beside upstream-drift
tracking) is adapted — **methodology only, no files vendored** — from two projects, both
evaluated 🟦 build-your-own (not installed). Full evaluations:
`research/audits/2026-07-03-skillopt.md` and `research/audits/2026-07-03-darwin-skill.md`.

- **microsoft/SkillOpt** (https://github.com/microsoft/SkillOpt) →
  `plugins/claude-code/skills/skillopt-sleep` (MIT). The
  load-bearing idea taken is the **harvest → mine → stage → report-only** shape of a
  nightly usage-mining cycle over your own transcripts, and the framing that **mined
  recurring tasks are real held-out eval cases**. Nothing vendored: SkillOpt ships a Python
  optimizer/replay framework (`pip install skillopt`) — that heavy "optimize" half stays in
  the built-in `skill-creator`; only the "scout" half is rebuilt here as a deterministic
  pre-pass (`scripts/mine_usage.py`) plus report prose.
- **alchaincyf/darwin-skill** (https://github.com/alchaincyf/darwin-skill) (MIT). The idea
  taken is the **git-revert ratchet**
  (strictly-improve-or-revert, never `git reset --hard`) and the **anti-pattern framing**,
  captured as an *adopt-time discipline* the user applies when driving `skill-creator` —
  NOT as code, and NOT as an edit to upstream `skill-creator`.

## What changed vs upstream (and why)

- **Split into scout vs optimize; only the scout is built here.** SkillOpt-Sleep's
  `Replay`/auto-scoring half duplicates `skill-creator`'s eval loop (which already has a
  blind comparator, variance analysis, and a held-out split in its description optimizer),
  so it is **out of scope** — see the design doc §2. The genuine net-new discipline shrank
  to two: bounded edits + git-revert ratchet.
- **Home = extend `skill-evolve`, not a new skill.** Usage mining is a second *evidence
  stream* feeding the same report and the same decision as upstream-drift tracking — one
  unified skill-health report. ADR: `docs/adr/0001-fold-skill-self-optimization-into-skill-evolve.md`.
- **Deterministic pre-pass, LLM judges.** `mine_usage.py` extracts raw markers (typed
  prompts, skill invocations via `attributionSkill`/`Skill` tool_use, correction-adjacency)
  from `~/.claude/projects/*/*.jsonl`; the semantic clustering into GAP/FRICTION/MEMORY is
  the LLM's job (this repo's Rule 5). No network, no writes, `--redact` for secrets.
- **Scheduling stays external** (built-in `schedule`/cron), matching the repo's
  content-engine-vs-timer split — the skill stays trigger-agnostic.

## Re-sync

`sources.lock` pins both upstream projects. On a future `skill-evolve` run, check SkillOpt
for a new release (the Sleep engine is evolving fast) and darwin-skill for changes to its
ratchet/anti-pattern framing; keep the scout-only scope and the "optimize half lives in
skill-creator" boundary unless the calculus changes.
