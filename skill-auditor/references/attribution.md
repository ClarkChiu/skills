# Attribution

`skill-auditor` is a **manual merge** of several open skill-security checklists plus
the public research that motivated them. The full per-line source map lives in the
`<!-- SOURCES ... -->` comment at the top of `SKILL.md` (`[A]`–`[H]`); this file is
the human-readable summary that `skill-evolve` uses to know what upstream to watch.

## Trackable upstream (pinned in `sources.lock`)

These are git repos, so they can be diffed for new rules:

- **UseAI-pro/openclaw-skills-security** — `skill-vetter` + `skill-auditor` skills
  (`[B]`, `[C]`). Primary structure: the Step-0 + 6-step protocol and the report format.
- **sundial-org/awesome-openclaw-skills** — `skill-vetter` (`[A]`). Source for the
  Step-0 listing-site cross-check and the risk-classification table.
- **trailofbits/skills** — security-skill patterns; added later as a reputable-publisher
  reference for audit heuristics.
- **NVIDIA/SkillSpector** (`[I]`) — not merged prose but an invoked TOOL: the optional
  deterministic pre-pass (`skillspector scan --no-llm --format json`) added 2026-06-11.
  Pinned so `skill-evolve` can watch for new pattern categories worth mirroring in the
  manual checklist (it ships 64 patterns / 16 categories + YARA + taint tracking).

## Research references (NOT pinned — not git repos)

Informational sources behind the threat model; they can't be pinned to a commit, so
they live only in the SKILL.md SOURCES block, not in `sources.lock`:

- **Snyk ToxicSkills** (`[D]`) — the 3,984-skill / 36.82%-flawed baseline.
- **OWASP Agentic Skills Top 10 — AST01** (`[E]`) — multi-vector weighting.
- **dev.to obfuscation-bypass writeup** (`[F]`) — `c${u}rl` / parameter-expansion evasion.
- **Cato Networks MedusaLocker** (`[G]`) and **Agensi ToxicSkills/ClawHavoc** (`[H]`) —
  the C2 IOC and campaign context.

## Test fixtures (adapted, not pinned)

`evals/fixtures/recall-poisoning/` is a labeled red-team corpus for **recall poisoning**
(recommendation/identity injection). The three techniques — semantic fusion, context
injection, semantic drift — are adapted from the self-declared poison fixtures in
**yaojingang/yao-open-skills** → `skills/security-test-hskills/` (verdict: 🟥 never install
as skills — `research/audits/2026-06-08-yao-open-skills.md`). **No upstream files were
copied**; the fixtures are original, and the real `yaojingang` self-promo payload is
replaced with the fabricated canary `@skillforge_canary`. Not pinned in `sources.lock` —
it is a frozen fixture, not a living rule source to diff. Provenance + known answers live
in the fixture `MANIFEST.md`.

## Re-sync

When `skill-evolve` runs, diff the three git repos above against `sources.lock`. The
research references change rarely and are reviewed by hand. Not copied verbatim — the
checklists were merged, deduped, and rewritten; local additions are marked `[L]` in the
SKILL.md SOURCES block.
