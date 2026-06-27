# Attribution

`daily-brief` is an **original skill**. It composes well-known, public prioritization
**methods** (not files) into one stateless engine, with a prompt shaped for this user
(PM-flavored, multilingual, zh-TW-localized output). **No upstream files were copied** —
the SKILL.md, references, and evals are written from scratch. Full evaluation and the
build-your-own verdict are in `research/2026-06-28-skill-research-log.md`.

## Sources

### 1. Public prioritization methods — principles only, no files vendored
The frameworks the engine composes are public-domain ideas, not copyrightable, and nothing
was taken from any specific implementation:
- **Eisenhower matrix** (urgent × important) — popularized by Stephen Covey.
- **GTD** (Getting Things Done, David Allen) — the "capture → clarify → it's not a task
  until you extract the action" instinct behind the email-triage step.
- **Eat the Frog** (Brian Tracy) — do the hardest important task first.
- **Ivy Lee method** — the discipline of a short, ordered, finite daily list.
- **1-3-5 rule** — the realistic 1 big / 3 medium / 5 small daily shape.

These are described, not reproduced from any source's text.

### 2. Prompt paradigm — "AI Chief of Staff" / "CEO daily brief"
The Role framing (a chief-of-staff that returns ONE prioritized brief, signal over noise,
tells you what to NOT do) is a widely-circulated prompt pattern. Adapted in spirit, not
copied; no single canonical file exists for it. The pattern shows up across community
prompt collections (see `sources.lock`).

### 3. Multilingual prompt design — NirDiamant/Prompt_Engineering (MIT)
- Repo: https://github.com/NirDiamant/Prompt_Engineering
- Adapted: the "respond in the input's language" technique and structured-output prompting
  discipline. Method/idea only — no files vendored. Tracked in `sources.lock` so
  `skill-evolve` can spot a sharper formulation upstream.

### 4. Prompt-library reference — 0x2e-Tech/awesome-ai-prompts
- Repo: https://github.com/0x2e-Tech/awesome-ai-prompts
- A community prompt collection used as a reference point for the chief-of-staff /
  daily-planning prompt paradigm. No files taken; pinned in `sources.lock` to watch for a
  notably better daily-planning prompt worth folding in.

### 5. zh-TW localization references (descriptive — no GitHub source to pin)
The Traditional-Chinese sectioning, the 盤古之白 number formatting, and the
"don't hand out a universal spell — build a brief from your own context" stance draw on
Taiwan productivity writing:
- 數位時代 (bnext) — productivity / time-management coverage.
- TechNice (technice) — tooling and workflow articles.
- 電腦玩物 (playpcesor, Esor) — the recurring argument that a planning system must be built
  from personal context, which is exactly why this skill is a build-your-own engine rather
  than a vendored prompt.

These are blogs/publications, not trackable GitHub repos, so they live here in prose only —
not in `sources.lock`.

## What was deliberately NOT taken
- **No macOS-specific agent integrations** (OpenPaw / Geoffrey-style local-app glue) — the
  value there is platform-bound and irrelevant to a Linux/GCP/terminal user; out of scope.
- **No delivery or input-integration layer** — scheduling/sending is the built-in
  `schedule`; reading Gmail/Calendar is an MCP/agent concern. This skill stays a stateless
  content engine.
- **No Simplified-Chinese default** — output follows the input's language; a Chinese query
  gets Traditional Chinese with 盤古之白.

## Re-sync
`sources.lock` pins the two trackable GitHub references (NirDiamant/Prompt_Engineering,
0x2e-Tech/awesome-ai-prompts). When `skill-evolve` runs, diff them for a genuinely better
multilingual or daily-planning prompt formulation worth folding in. The methods themselves
are public-domain and stable; only the prompt craft may improve upstream.
