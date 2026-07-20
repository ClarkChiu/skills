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
- **Future extension route** (HTML timeline animation → headless capture →
  ffmpeg MP4/GIF, for card-style animated posts): `alchaincyf/huashu-design`
  (MIT), evaluated `research/audits/2026-07-02-huashu-design.md` — pinned in
  `sources.lock` so `skill-evolve` tracks it until that route is built. As of
  upstream 32cc5812 (2026-07-19) that route defaults to **HyperFrames** (HeyGen's
  open-source HTML→video framework, Apache-2.0; deterministic frame-seek
  rendering in a headless browser), demoting the old self-built
  Stage/render-video-seek.js to fallback — so if this extension is ever built,
  the starting point is evaluating HyperFrames, not the old route. Caveat:
  HyperFrames' init installs ~19 skills into `~/.claude/skills/`; it MUST go
  through `skill-auditor` before any trial.
- **Export verification ideas** (adopted 2026-07-20): the last three §6c checks
  in `pipeline.md` (leading/trailing black-frame detection, output-LUFS
  verification, duration tolerance) take the *ideas* of huashu-design's
  `verify-video.sh` at 32cc5812 — commands written here from scratch, zero new
  dependencies, no code copied.
- **Safe-area numbers** (9:16 top ~250px / bottom ~420px): same platform bands the
  sibling `social-card` skill uses; restated here because cross-skill pointers rot.

## Re-sync

On `skill-evolve`: check huashu-design's export verification and its HyperFrames
integration for capture/export improvements (ideas or, with a per-file audit,
selective vendoring — MIT allows).
MoneyPrinterTurbo/ShortGPT are not pinned; revisit only if a direct code consult
becomes worth it.
