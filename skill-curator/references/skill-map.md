# Skill Map

When evaluating the **duplication** of an external skill, check this map first — see which functional cluster the new skill lands in, and whether an existing skill already covers it. It's also the reference for avoiding internal rework when building/changing your own skills. **After adding or changing a self-built skill, come back and update this map.**

## Functional clusters

### A. External-skill governance (lifecycle pipeline)
- `skill-finder`: read-only search of skills.sh, fetch a candidate's SKILL.md. **Discovery only, never installs.**
- `skill-auditor`: security audit, produces a SKILL AUDIT REPORT. **Must run before installing any external skill.**
- `skill-curator`: orchestrates the two above + relevance + verdict + record. **Research/decision, never installs.**
- `skill-evolve`: tracks the upstream of self-built skills (reads each skill's `attribution.md` + `sources.lock`).

Pipeline: `skill-finder (discover) → skill-auditor (security) → skill-curator (verdict/record) → [build-your-own] skill-creator [built-in] drafts → skill-evolve (track upstream)`

### B. Chinese text (two-stage pipeline)
- `humanizer`: voice layer, removes AI-writing tells (bilingual EN + zh-TW).
- `chinese-typography`: typography layer — 盤古之白 / full-width punctuation / Simplified→Traditional / regional vocabulary / normalization.

Pipeline: `humanizer (voice) → chinese-typography (typography)`. Regional-vocabulary substitution belongs to the typography layer.

### C. Engineering discipline (around CLAUDE.md Rule 0–12)
- `design-gate`: **before** code — design → hard gate → plan.
- `systematic-debugging`: **when broken** — four-phase root-cause debugging.
- `verify-before-done`: **after** a completion claim — five-step verification gate.

Order: `design-gate (before) → execution (CLAUDE discipline) → verify-before-done (after)`; `systematic-debugging` inserts when a bug appears, and its phase 4 hands back to `verify-before-done`. The three share the "failing-test-first / red step" rule, whose **canonical statement lives in `design-gate/references/writing-plans.md`** — the other two link to it rather than restating.

### Standalone tools
- `slide-deck`: produces a single-file HTML slide deck.
- `p2pscout`: BitTorrent resource search + downloadability ranking (Go tool).
- `ui-design-advisor`: the UI **decision** layer — picks style / palette / fonts / charts / a11y for a screen from a vendored design-data library, outputs a design brief, then hands to `frontend-design` to build. Data vendored (data only, MIT) from ui-ux-pro-max + dictionary-of-colour-combinations + ux-ui-agent-skills (a11y) + SteveBarnett/Checklists. Pipeline: `ui-design-advisor (decide look) → frontend-design (implement)`.
- `solo-think`: autonomous **inward** reflection for a Hermes Agent — a heartbeat-triggered loop (dream reflection + thinking queue) that writes thoughts to memory and **never acts outward**. Inward-only is structurally enforced (heartbeat `--toolsets file` + skill `allowed-tools` Read/Write/Edit); reflection is grounded by a user-set `focus`, bounded by `active_hours`, and paced by heartbeat frequency (no agent-side token tally). Rewritten in Taiwan Traditional Chinese from `loryoncloud/Heartbeat-Like-A-Man` (MIT) with all outward actions (autonomous exploration, community patrol) stripped and ported OpenClaw→Hermes. Standalone — does NOT collect intelligence or notify (that outward/inbound-collection track lives in the separate `tg-intelligence-hub` project, not here).

## Boundaries vs built-in skills (the easiest collisions when evaluating externals)

| Self-built / need | Built-in neighbor | Boundary |
|---|---|---|
| `design-gate` | `doc-coauthoring` | design-gate = pre-code design+plan gate; doc-coauthoring = general docs/proposals |
| `verify-before-done` | `verify` | former = discipline gate for test/lint/build/fix claims; latter = run the app and observe |
| `systematic-debugging` | `code-review` | former = chase one bug to root cause; latter = review a diff for issues |
| `slide-deck` | `pptx` / `frontend-design` | slide-deck = HTML deck; pptx = .pptx (use ppt-master); frontend-design = web UI |
| `ui-design-advisor` | `frontend-design` | advisor = decide the look (style/palette/fonts/charts/a11y brief); frontend-design = implement the UI code. Upstream → downstream |
| `humanizer` | (none) | de-AI writing voice |
| `skill-curator` | `skill-creator` | curator = decide whether to use; creator = actually build a skill |

## Quick judgment for a new external skill

1. Which cluster does it fall in — A / B / C / tools?
2. Which self-built or built-in does it collide with? → usually "extend the existing one" or "build-your-own", rarely install.
3. Only a genuine gap warrants 🟦 build-your-own / 🟨 vendor & customize (criteria in `criteria.md`).
