# Attribution

`translate` is adapted from **JimLiu/baoyu-skills** → `skills/baoyu-translate` (MIT).
The load-bearing idea taken is the **separated critique discipline**: draft → critical
review that *diagnoses only* (never rewrites in the same step) → revision applying the
critique. This is an **original rewrite**, no files copied — the upstream glossary is
zh-CN-targeted and was not vendored; the term table here is built from scratch for
zh-TW. Full evaluation: `research/audits/2026-07-02-baoyu-skills.md` (verdict:
🟥 collection not installed + per-skill mining; baoyu-translate → 🟦 build-your-own).

## What changed vs upstream (and why)

- **Three modes → two.** Upstream's quick/normal/refined; the middle "normal"
  (analysis → translate) added a mode for marginal gain. Kept quick (快翻) + refined
  (精翻); normal's value survives as the "繼續精翻" upgrade path that reuses the quick
  output as the draft.
- **Target retargeted zh-CN → zh-TW, and made bidirectional.** Critique checklists are
  direction-specific: EN→zh-TW hunts Europeanized Chinese (歐化句/被動濫用/中國用語混入);
  zh-TW→EN hunts Chinglish (articles/tenses/collocations). Upstream has a single
  CJK-generic review step.
- **Glossary wired into this repo's word-preference stack** instead of upstream's
  EXTEND.md system: `user-dictionary.json` → `glossary.md` → `terms-en-zhtw.md` →
  general Taiwan convention. EXTEND.md solved multi-user preference persistence; this
  repo already solves that with CLAUDE.md + the chinese-typography data layer.
- **All engineering dropped** (bun/TS chunking scripts, parallel per-chunk subagents,
  EXTEND.md schema, image-language pass, URL fetching). Long documents are handled by
  whole-document analysis first (terminology table = cross-section consistency), then
  per-heading translation; ceiling noted in SKILL.md (revisit a Python chunker if
  multi-10k-word docs show seam inconsistency).
- **Boundary drawn vs `humanizer`**: translation-ese (source-language structure
  residue) belongs here; AI-tell removal belongs to humanizer. Neither copies the
  other's rules. Downstream suggestion chain: translate → humanizer → chinese-typography.

## Re-sync

`sources.lock` pins upstream. On `skill-evolve`, mine upstream's critique dimensions
(refined-workflow.md Step 4) and workflow refinements; keep the two-mode shape, the
zh-TW retargeting, the direction-specific checklists, and the glossary wiring.
