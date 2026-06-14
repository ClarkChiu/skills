# Skill Map

When evaluating the **duplication** of an external skill, check this map first — see which functional cluster the new skill lands in, and whether an existing skill already covers it. It's also the reference for avoiding internal rework when building/changing your own skills. **After adding or changing a self-built skill, come back and update this map.**

## Functional clusters

### A. External-skill governance (lifecycle pipeline)
- `skill-finder`: read-only search of skills.sh, fetch a candidate's SKILL.md. **Discovery only, never installs.**
- `skill-auditor`: security audit, produces a SKILL AUDIT REPORT. **Must run before installing any external skill.** Optional deterministic pre-pass via the external `skillspector` CLI (NVIDIA, see README external-CLI section) when installed — a clean scan never skips the manual protocol.
- `skill-curator`: orchestrates the two above + relevance + verdict + record. **Research/decision, never installs.**
- `skill-evolve`: tracks the upstream of self-built skills (reads each skill's `attribution.md` + `sources.lock`).

Pipeline: `skill-finder (discover) → skill-auditor (security) → skill-curator (verdict/record) → [build-your-own] skill-creator [built-in] drafts → skill-evolve (track upstream)`

### B. Chinese text (two-stage pipeline)
- `humanizer`: voice layer, removes AI-writing tells (bilingual EN + zh-TW). Also carries a "preserve-the-author" subtractive guardrail (don't flatten a real author's voice when editing their own draft) — principles from `orange2ai/renwei-writing` (2026-06-14, principles only, not vendored; custom license), tracked in humanizer's sources.lock.
- `chinese-typography`: typography layer — 盤古之白 / full-width punctuation / Simplified→Traditional / regional vocabulary / normalization.

Pipeline: `humanizer (voice) → chinese-typography (typography)`. Regional-vocabulary substitution belongs to the typography layer.

### C. Engineering discipline (around CLAUDE.md Rule 0–12)
- `design-gate`: **before** code — design → hard gate → plan. Phase 1 now also sharpens ubiquitous language + captures ADRs inline (`references/adr.md`, adapted from mattpocock grill-with-docs).
- `tdd`: **during** code — red-green-refactor build loop (one behaviour, fail-first, refactor only on green). pytest + protocol examples. Adapted from mattpocock/skills tdd.
- `systematic-debugging`: **when broken** — four-phase root-cause debugging.
- `verify-before-done`: **after** a completion claim — five-step verification gate.
- `to-issues`: **after the plan** — publishes a plan/PRD as vertical-slice GitHub issues via `gh`, confirm-before-create. Downstream of design-gate. Adapted from mattpocock/skills to-issues.

Order: `design-gate (before/plan) → to-issues (publish plan as issues) → tdd (build, test-first) → execution (CLAUDE discipline) → verify-before-done (after)`; `systematic-debugging` inserts when a bug appears, and its phase 4 hands back to `verify-before-done`. design-gate/tdd/verify share the "failing-test-first / red step" rule, whose **canonical statement lives in `design-gate/references/writing-plans.md`** — the others link to it rather than restating (tdd executes that loop in depth).

### Standalone tools
- `slide-deck`: produces a single-file HTML slide deck.
- `p2pscout`: BitTorrent resource search + downloadability ranking (Go tool).
- `ui-design-advisor`: the UI **decision** layer — picks style / palette / fonts / charts / a11y for a screen from a vendored design-data library, outputs a design brief, then hands to `frontend-design` to build. Data vendored (data only, MIT) from ui-ux-pro-max + dictionary-of-colour-combinations + ux-ui-agent-skills (a11y) + SteveBarnett/Checklists. Pipeline: `ui-design-advisor (decide look) → frontend-design (implement)`.
- `solo-think`: autonomous **inward** reflection for a Hermes Agent — a heartbeat-triggered loop (dream reflection + thinking queue) that writes thoughts to memory and **never acts outward**. Inward-only is structurally enforced (heartbeat `--toolsets file` + skill `allowed-tools` Read/Write/Edit); reflection is grounded by a user-set `focus`, bounded by `active_hours`, and paced by heartbeat frequency (no agent-side token tally). Rewritten in Taiwan Traditional Chinese from `loryoncloud/Heartbeat-Like-A-Man` (MIT) with all outward actions (autonomous exploration, community patrol) stripped and ported OpenClaw→Hermes. Standalone — does NOT collect intelligence or notify (that outward/inbound-collection track lives in the separate `tg-intelligence-hub` project, not here).
- `tutor`: interactive tutoring protocols — Feynman (zero knowledge: explain → comprehension-check → only advance on a demonstrated concept) + Socratic (existing beliefs: questions only, never gives the answer). Load-bearing value = the pinned hard rules that stop lecture-mode drift; session ends with the LEARNER explaining the topic back. Adapted from prompts #18/#20 of the @AnatoliKopadze 20-prompt roundup (via BlockTempo translation; #9/#10/#12 became `roleplay-coach`, the other 15 skipped — see `research/skill-index.md`). Boundary: tutor = the user learns through dialogue; built-in explanations / `deep-research` = the model produces the answer.
- `roleplay-coach`: rehearsal for high-stakes conversations — salary negotiation, mock interview, difficult-conversation (playbook first, rehearsal second). Core = realistic resistance (counterpart doesn't cave), one-turn-at-a-time (never simulates both sides), honesty gate on unrealistic goals BEFORE the roleplay, mandatory break-character debrief naming what the user left on the table. Rehearses in the language of the real conversation. Adapted from prompts #9/#10/#12 of the same roundup. Boundary: roleplay-coach = the user practices speaking; doc-coauthoring / drafting = the model writes the artifact.
- `social-card`: principle-driven IG/LinkedIn social-card image generator — turns an article/notes/screenshots into fixed-ratio card frames rendered to exact-size PNG via **agent-browser** (IG 4:5/1:1/9:16, LinkedIn 1:1/1.91:1; FB single). Two original style families (Swiss/Editorial) + palettes + 7 page roles; load-bearing rules one-idea-per-card + shorten-not-shrink, enforced by `scripts/qa-rules.js` over `agent-browser eval`. Generates images only — NOT posting/scheduling (that outward 'manage' track is a separate Meta Graph API project, not a skill). Adapted from `op7418/guizang-social-card-skill` (principles only, no files vendored — AGPL/ISC license inconsistency; platforms retargeted CN→IG/LinkedIn; render playwright→agent-browser). Boundary vs `slide-deck`: slide-deck = 16:9 presentation HTML that scales on-screen → PDF; social-card = fixed-ratio social images → PNG. Both: principle-driven, one-idea-per-frame, shorten-not-shrink, zero licensed assets.
- `decision-lens`: a **decision-support router** over three lenses — **Bayesian** (belief under evidence: prior → likelihood ratios → posterior → action threshold → sensitivity), **Crux** (prioritization among tangled problems: primary vs secondary scored on decisiveness/leverage/stage), **Kelly** (allocation with an edge: fractional Kelly sizing, no-edge refusal). The math runs in three pure-stdlib calculators (`bayes_update.py`/`crux_score.py`/`kelly_size.py` — print JSON, no net/keys/subprocess), output is a lean Markdown brief, language follows the query (Traditional Chinese, never Simplified). Load-bearing rule: never fabricate priors/win-rates (ask or label assumptions + sensitivity). Adapted from `yaojingang/yao-open-skills` decision cluster (methods only, no files; math is public-domain; Crux de-politicized; MIT). Boundaries: vs `roleplay-coach` = decide vs rehearse a conversation; vs `systematic-debugging` = decide which hypothesis the evidence supports vs chase a bug to root cause; vs `design-gate` = a general decision vs a pre-code engineering design+plan.
- `git-guardrails`: a portable safety **hook** (not a prose skill) — installs a Claude Code PreToolUse hook (`scripts/block-dangerous-git.sh`) that blocks destructive git (force push, reset --hard, clean -f, branch -D, discard-all, delete remote) before it runs. Hardened over upstream: anchored patterns (no echo/commit-message false-positives), allows `--force-with-lease`, does NOT block push-to-master (user's normal workflow). Merge-not-clobber install (preserves the RTK hook); project or global scope. Adapted from mattpocock/skills git-guardrails (hardened rewrite, MIT). The script is portable via APM/git; the one-line settings.json wiring is per-machine (where all hooks live).
- `html-diagram`: produces a single self-contained HTML file whose whole purpose is one high-quality SVG diagram (architecture / stack / sequence & request-flow / flowchart) — full-screen, diagram-first, hand-rolled dark mode, zero dependencies; nodes clickable, sequences animatable. Load-bearing rules: get the topology right first (ask, don't invent edges), theme the SVG via CSS classes (no hard-coded hex), viewBox scaling, interactivity only when it earns its keep. **Vendor & customize** from `ThariqS/html-effectiveness` (Apache-2.0, Thariq Shihipar) — only the diagram-relevant subset of the 20-file gallery (05/07/08/10/13 + LICENSE/README) + the finished `architecture-example.html` from `plannotator/effective-html` (MIT); SKILL.md written from scratch and narrowed to diagrams. Verified self-contained (no external script/CDN/fetch). Boundary: vs `slide-deck` = one diagram vs a 16:9 multi-slide deck; vs built-in `web-artifacts-builder` = diagram-only vs general HTML report/explainer/prototype (the omitted gallery files cover that, intentionally left out); vs `social-card` = HTML/SVG diagram vs fixed-ratio raster card; vs `frontend-design` = artifact vs shippable app UI.
- `terse`: a manually-toggled token-economy mode — shorten by cutting filler/preamble/hedging, NOT by mangling grammar; language-aware (English may go clipped, Chinese stays natural Taiwan Traditional). Fixes the upstream caveman's Chinese 怪腔怪調. Safety exception (security/destructive confirmations stay full). Adapted from mattpocock/skills caveman (MIT). Complements `humanizer`: humanizer = tone (sound human), terse = length (save tokens); both refuse to break grammar.

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
| `decision-lens` | `roleplay-coach` / `systematic-debugging` | decision-lens = pick a method + do the math for a real decision; roleplay-coach = rehearse a conversation; systematic-debugging = chase a bug to root cause |
| `tdd` | `verify-before-done` / `systematic-debugging` | tdd = test-first BUILD loop (during coding); verify-before-done = completion gate (after a claim); systematic-debugging = root-cause a bug (when broken) |
| `to-issues` | `design-gate` | to-issues = publish a settled plan as GitHub issues (downstream); design-gate = produce the design+plan (upstream) — don't re-plan in to-issues |
| `terse` | `humanizer` | terse = remove length / save tokens (live mode); humanizer = remove AI tone (post-edit). Both keep grammar intact |
| `git-guardrails` | (none — it's a hook) | a PreToolUse safety hook, not a prose skill; no built-in equivalent. Merges alongside the RTK hook (and must run before it, or tolerate an `rtk ` prefix, since rtk rewrites commands) |

## Quick judgment for a new external skill

1. Which cluster does it fall in — A / B / C / tools?
2. Which self-built or built-in does it collide with? → usually "extend the existing one" or "build-your-own", rarely install.
3. Only a genuine gap warrants 🟦 build-your-own / 🟨 vendor & customize (criteria in `criteria.md`).
