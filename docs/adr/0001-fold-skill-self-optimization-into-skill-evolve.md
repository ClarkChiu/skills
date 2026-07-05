# 0001 — Fold skill self-optimization (SkillOpt / darwin-skill) into skill-evolve

- Status: Proposed (awaiting user approval at the design gate)
- Date: 2026-07-03
- Context source: `research/audits/2026-07-03-{darwin-skill,skillopt}.md`, design doc `docs/specs/2026-07-03-skill-evolve-usage-mining-design.md`

## Context

The user is interested in the "nightly mine my own usage → propose skill improvements"
loop from microsoft/SkillOpt (specifically its `skillopt-sleep` plugin) and
alchaincyf/darwin-skill. Both were evaluated 🟦 build-your-own (not install): their
value is methodology, not downloadable engineering tied to a trustworthy-enough upstream
to depend on.

Two candidate homes were considered:

1. **Extend `skill-evolve`** — add "your own usage transcripts" as a second evidence
   stream beside its existing "upstream source drift".
2. **New self-built skill** (e.g. `usage-miner`).

An initial lean toward a new skill rested on skill-evolve's SKILL.md line "on-demand
only; scheduling is not built in" conflicting with a nightly-scheduled capability. The
user clarified that scope line is not a hard constraint, dissolving the objection.

## Decision

**Extend `skill-evolve`.** Its single job is "produce a report of what should change
about your skills, and let you decide." Today that report's evidence is upstream drift;
adding "your own usage" is a second evidence stream feeding the *same* report and the
*same* decision — a richer input, not scope creep. The two signals compose into one
unified skill-health report.

**Scope v1 = the scout half only** (proceeded on this after the user stepped away;
revisit at the gate). Split the two projects into two loops:

- **Scout loop (build here):** Harvest → Mine → Report. Surface recurring hand-done
  tasks (gap), worked-around skills (friction), and recurring facts/preferences
  (memory), each with evidence. Report-only.
- **Optimize loop (do NOT rebuild):** bounded edits + held-out validation + git-revert
  ratchet + anti-pattern checklist. This is already the built-in `skill-creator`'s job;
  the scout's output is shaped to feed it. (Audit 2026-07-03: skill-creator already has
  the blind comparator, variance analysis, and a held-out split in the *description*
  optimizer; the genuine net-new is just **bounded edits + git-revert ratchet**, both
  adopt-time disciplines — the scout itself does no editing.)

The load-bearing synthesis: **mined recurring tasks are real held-out eval cases.** The
scout emits, for each gap, a list of real prompts from the user's own history — a
non-invented eval set that `skill-creator` optimizes against.

Automated `Replay`/scoring (SkillOpt's heavy half) is explicitly out of scope for v1.

## Consequences

- One skill, one report, one decision surface — the user need not remember two skills.
- `skill-evolve` gains: a sibling script `scripts/mine_usage.py` (deterministic pre-pass,
  same pattern as `extract_sources.py`); a broadened identity line ("on-demand or
  scheduled"); a stronger security section (transcripts = most-sensitive local data);
  `references/attribution.md` + `sources.lock` pinning SkillOpt + darwin-skill (so it now
  tracks its own upstream — pleasant recursion).
- Boundary sharpened: vs `solo-think` (inward reflection → memory) this produces an
  outward proposal from usage evidence; vs `skill-creator` this decides *what/why* to
  change, creator does the *how*.
- Scheduling stays external (built-in `schedule`/cron), matching the repo's
  content-engine-vs-timer split (daily-brief precedent).
- Risk accepted: transcript mining is a heavier privacy surface than reading upstream
  READMEs; mitigated by local-only, read-only, report-only, treat-content-as-data, and a
  SHOULD-level secret redaction pass in the digest.
