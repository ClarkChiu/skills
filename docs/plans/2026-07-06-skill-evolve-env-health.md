# Plan — skill-evolve environment-health stream

Design: `docs/specs/2026-07-06-skill-evolve-env-health-design.md` (approved 2026-07-06).
Confirmed: curated `CLI_DEPS` map; two probe kinds (`cli` + `pymod`). Report-only. Do NOT touch `lint-skills.py`.

Task cycle: write failing test → confirm red → minimal impl → confirm green → commit.

## Task 1 — failing test `skill-evolve/scripts/test_env_health.py`

Create the assert-based self-check (no framework), mirroring `test_mine_usage.py`. Fake CLIs on a temp PATH. Load-bearing test: a shim on PATH that can't exec → `broken`, not `missing`.

(Full code in Task-1 code block below.)

**Verify (red):** `cd skill-evolve/scripts && python3 test_env_health.py` → expect `ModuleNotFoundError: No module named 'env_health'` (impl doesn't exist yet).

## Task 2 — implement `skill-evolve/scripts/env_health.py`

Deterministic, stdlib-only, read-only, stdout only. 5-state `cli` probe + `pymod` probe + curated `CLI_DEPS` + report/`--json`.

**Verify (green):** `python3 test_env_health.py` → `ALL <n> CHECKS PASSED`. Then live run `python3 env_health.py` prints an ENV HEALTH block for this machine.

**Commit:** `✨ feat(skill-evolve): env-health 證據流——探測各技能外部 CLI（broken≠missing）`

## Task 3 — wire into skill-evolve SKILL.md + evals

- SKILL.md: add optional workflow step "0.5 — environment health" pointing at `scripts/env_health.py`, and add the `ENV HEALTH` block to the report-format section; extend the description's two-evidence-streams line to mention env health.
- `evals/evals.json`: add one eval asserting the report distinguishes `broken` from `missing`.

**Verify:** `python3 scripts/lint-skills.py` → `✓ 25 個自建技能全部通過`.

**Commit:** `📝 docs(skill-evolve): 登錄 env-health 步驟＋報告區塊＋eval`

## Task 4 — final verification

`python3 skill-evolve/scripts/test_env_health.py` (green) + `python3 skill-evolve/scripts/test_mine_usage.py` (still green) + `python3 scripts/lint-skills.py` (25/25). Fresh-context review of the diff, then push.

---

### Task-1 code — `test_env_health.py`

See the file written to `skill-evolve/scripts/test_env_health.py` during execution (identical to what's committed). Key tests: `test_broken_not_missing` (the reason this exists over `which`), `test_missing`, `test_ok`, `test_error`, `test_timeout`, `test_pymod_ok`, `test_pymod_missing`, `test_report_dedup_and_used_by`, `test_deterministic`, `test_no_network_no_mutation`.

### Task-2 code — `env_health.py`

See the file written to `skill-evolve/scripts/env_health.py`. Curated `CLI_DEPS` (ig-reel→ffmpeg/ffprobe, p2pscout→go, social-card→agent-browser/convert, slide-deck→agent-browser, skill-auditor→skillspector, git-guardrails→rtk, chinese-typography→python3/opencc-pymod, translate/humanizer→opencc-pymod); `_probe_cli` (which→run --version→classify 126/127/timeout/error/ok), `_probe_pymod` (import), `build_report` (dedupe + used_by), `format_report` + `--json`.
