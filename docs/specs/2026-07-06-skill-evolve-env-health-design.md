# Design — skill-evolve environment-health evidence stream

Date: 2026-07-06 · Status: **awaiting approval (hard gate)** · Scope: small, low-priority
Origin: distilled from the Agent-Reach `probe.py` study (2026-07-06 research log); Agent-Reach itself 🟥 skip, this borrows only the taxonomy pattern.

## 1. Purpose

Give `skill-evolve` a **third evidence stream** — *environment health*: which self-built skills' **declared external CLIs are actually runnable on THIS machine**. Today skill-evolve scouts two streams (upstream drift, usage mining); neither tells you that `ig-reel` is silently dead because `ffmpeg` isn't installed, or — worse — that a CLI's shim is on `PATH` but its interpreter is gone (a stale pipx/uv venv after a Python upgrade). **Report-only**, like the rest of skill-evolve.

## 2. Non-goals

- **No auto-fix / no install.** It reports; the user fixes. (Same discipline as the whole skill.)
- **Does NOT touch `lint-skills.py`.** That gate checks repo *form* (SKILL.md/evals/registration) and MUST stay portable and CI-safe — it has to pass on a box with none of these CLIs installed. Runtime CLI probing there would break its determinism. Explicitly out of scope.
- **No multi-backend selection.** Agent-Reach's "first-ok-wins among candidate backends" is dropped (YAGNI — each self-built skill wraps a single CLI, no fallback fan-out).
- Not a general system-health monitor; only the CLIs this repo's skills declare.

## 3. Chosen approach — curated dependency map (Option A)

A `CLI_DEPS` map (`skill → [cli, …]`) **curated by hand** inside the script. Rejected alternatives:

- **Per-skill frontmatter convention** (`external-cli:` field, auto-discovered): self-maintaining, but introduces a new repo-wide convention, touches every external-CLI skill, and needs lint/doc changes — over-engineering for ~10 skills.
- **Auto-scan skill files** for CLI mentions: demonstrably noisy. Evidence (2026-07-06 read-only pass): `skill-curator`'s SKILL.md name-drops ffmpeg/whisper/agent-browser/rtk/skillspector as *descriptions of other skills*, none its own deps — an auto-scan would falsely flag 6 phantom deps. The map needs human judgment.

**Decision (confirmed by user 2026-07-06):** curated map. Rationale: Simplicity First, ~10 skills, no new convention, matches the "small/low-priority" framing. Reinforced during exploration: external-CLI deps live in **agent-facing prose, not scripts**, so they aren't cleanly machine-extractable at all — a curated, human-judged map is the only reliable source.

**Probe kinds (confirmed by user 2026-07-06):** two kinds, because `opencc` in the Chinese skills is a **Python binding (`import opencc`), not a CLI** — probing an `opencc` binary would falsely report `missing`. So each dep is `(name, kind)`:
- `cli` → `shutil.which` + `<name> --version`, full 5-state taxonomy.
- `pymod` → `python3 -c "import <name>"`, exit 0 = `ok`, else `missing`.

> The exact map contents come from a per-skill judgment call verified against each skill's source (fresh-context review, 2026-07-06) — NOT the noisy grep. Final map: `ig-reel→[ffmpeg,ffprobe]`, `p2pscout→[go,aria2c]`, `social-card→[agent-browser,convert]`, `slide-deck→[playwright(pymod),pptx(pymod)]`, `skill-auditor→[skillspector]` (optional), `to-issues→[gh]`, `git-guardrails→[jq]` (hook parses tool_input with jq), `chinese-typography→[python3,opencc(pymod)]`, `humanizer→[opencc(pymod)]`. Excluded: `translate` (delegates to chinese-typography, invokes nothing); prose-only mentions. Corrections the review caught: slide-deck was wrongly `agent-browser` (copy-paste), git-guardrails wrongly `rtk` (only in comments — real dep is `jq`), p2pscout missing `aria2c`, `to-issues→gh` missing entirely.

## 4. Component

- `skill-evolve/scripts/env_health.py` — new, ~40–60 lines, stdlib only (`shutil`, `subprocess`, `dataclasses`). No network, no writes except stdout (mirrors `mine_usage.py`).
- `skill-evolve/scripts/test_env_health.py` — assert-based self-check, no framework (mirrors `test_mine_usage.py`).

## 5. The taxonomy (the borrowed insight)

Five states — the point is **broken ≠ missing**:

| state | detection | prescription |
|---|---|---|
| `missing` | `shutil.which(cmd)` falsy → return immediately, no exec | "not installed" |
| `broken` | which() finds a shim but it can't run: `FileNotFoundError`/`OSError` on exec, **or** returncode ∈ {126,127} | "stale/again shim — reinstall (`uv tool install --force` / `pipx reinstall` / repackage)" |
| `timeout` | `subprocess.TimeoutExpired` (bounded, default 5s) | "hangs — investigate" |
| `error` | ran, returncode ≠ 0 and not 126/127 (captures stderr) | show the tool's own error |
| `ok` | returncode 0 | — |

Probe command: `<cli> --version` by default, with a tiny per-CLI override for tools that use a different form (e.g. `-version`). Probes are side-effect-free (version checks only).

## 6. Data flow

`CLI_DEPS` → dedupe the distinct CLI set → probe each **once** → invert to `skill → {cli: state}` and `cli → [skills using it]` → emit ENV HEALTH block.

## 7. Report format (new block in skill-evolve's report)

```
ENV HEALTH  (declared external CLIs · this machine)
  ✓ ok        ffmpeg ffprobe go node opencc rtk agent-browser
  ✗ missing   whisper            → used by: ig-reel
  ⚠ broken    aria2c (exit 127)  → used by: p2pscout   → stale shim; reinstall
  ⏱ timeout   —
  ✖ error     —
```

Also `--json` for machine consumption (mirrors `mine_usage.py`'s digest ethos): `{cli: {state, detail}, skills: {skill: {cli: state}}}`.

## 8. Integration

- Standalone: `python3 scripts/env_health.py [--json]`. Deterministic, read-only, no network.
- `skill-evolve/SKILL.md`: add an **optional** workflow step (e.g. "0.5 — environment health") + document the ENV HEALTH block in the report format. Keep it optional/on-demand; not wired to any timer.
- `skill-evolve/evals/evals.json`: add one eval asserting the report distinguishes broken from missing.

## 9. Error handling

- A single CLI probe that throws is caught and recorded as `broken`/`error` — one bad CLI never aborts the run (fail-soft per-CLI, fail-loud overall).
- Unknown/typo CLI in the map → probes as `missing` (honest).
- The script's own bugs fail loud (non-zero exit on malformed invocation), like `mine_usage.py`.

## 10. Testing (Rule 9 — tests encode intent)

Assert-based self-check against a fixtures dir of **fake CLIs**:
- `fake_ok` (exit 0), `fake_error` (exit 1), `fake_broken` (a non-executable file / a script exiting 127), `fake_timeout` (sleeps past the bound), and a guaranteed-absent name.
- The load-bearing test: **the broken fixture classifies as `broken`, NOT `missing` and NOT `ok`** — that is the whole reason this exists over `which`.

## 11. Requirements (RFC 2119) & acceptance

- **MUST** classify a shim that exists on PATH but fails to exec (exit 126/127 or exec error) as `broken`, distinct from `missing`.
- **MUST** be report-only — no install, no file modification.
- **MUST NOT** modify `lint-skills.py` or add runtime CLI probing to the form-lint.
- **SHOULD** probe each distinct CLI at most once per run.
- **SHOULD** bound each probe with a timeout.

Given/When/Then:
- Given a CLI whose shim exists but interpreter is gone (exit 127), When probed, Then state=`broken` with a reinstall hint.
- Given a CLI absent from PATH, When probed, Then state=`missing`.
- Given a healthy CLI (`--version` exit 0), When probed, Then state=`ok`.

## 12. Size / priority

~40–60 LOC script + ~40 LOC test + small SKILL.md/evals edits. **Low priority** — a plain `which` loop covers ~80%; the earned value is the broken≠missing distinction for a pipx/uv-heavy, terminal-first setup. Ship only if that distinction is worth ~1–2 hours.
