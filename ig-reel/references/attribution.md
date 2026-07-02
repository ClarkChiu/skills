# Attribution

**Original build.** All recipes, rules, and prose here were written for this skill;
no files were vendored from any upstream. What informed it:

- **Pipeline shape** (inventory → cut → reframe → subtitles → audio → assemble →
  batch): the common architecture of MoneyPrinterTurbo / ShortGPT, studied via this
  repo's research note `research/2026-06-21-video-editing-projects-for-ig.md` —
  **not** their code (never cloned or audited; their core value is fetching stock
  footage for users who have none, which this skill deliberately inverts: the
  footage is the user's, stage 2 scans their folder instead of Pexels). If their
  code is ever consulted directly, run `skill-auditor` first and pin them in
  `sources.lock` then.
- **Tooling choices** (ffmpeg core; auto-editor for silence-cutting; whisper for
  subtitles): the same research note's recommended route. These are tools this
  skill drives, not sources it copies.
- **Future extension route** (HTML timeline animation → Playwright capture →
  ffmpeg MP4/GIF, for card-style animated posts): `alchaincyf/huashu-design`
  (MIT), evaluated `research/audits/2026-07-02-huashu-design.md` — pinned in
  `sources.lock` so `skill-evolve` tracks it until that route is built.
- **Safe-area numbers** (9:16 top ~250px / bottom ~420px): same platform bands the
  sibling `social-card` skill uses; restated here because cross-skill pointers rot.

## Re-sync

On `skill-evolve`: check huashu-design's render-video chain for capture/export
improvements (ideas or, with a per-file audit, selective vendoring — MIT allows).
MoneyPrinterTurbo/ShortGPT are not pinned; revisit only if a direct code consult
becomes worth it.
