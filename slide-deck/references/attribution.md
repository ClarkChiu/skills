# Attribution & sources

This skill's **principles** are distilled from four mature slide projects. We reused
their *ideas and conventions* (type scales, the vertical-budget method, density modes,
motion restraint, "one idea per slide") — which are not copyrightable — and wrote all
code, presets, and prose here from scratch. We did **not** copy any template files,
assets, or source code from them.

## Projects studied

| Project | URL | License | What we distilled |
|---------|-----|---------|-------------------|
| note-slides (gainubi) | https://github.com/gainubi/note-slides | MIT | One-idea-per-slide, 40–60% content / rest whitespace, source-anchor discipline, the single-file HTML deck + linter pattern |
| frontend-slides (zarazhangrui) | https://github.com/zarazhangrui/frontend-slides | MIT | Fixed 1920×1080 stage scaled by one transform, the two density modes, "show 3 previews — don't ask for taste in words", anti-AI-slop font/color rules. 2026-07-02: also its machine-readable selection metadata idea → the `best_for`/`avoid_for` selection table in `style-presets.md`, and its preview composition (1 safe + 1 bold + 1 wildcard, preview-authenticity rule) → SKILL.md Phase 2. Its 34-template pack and CDN-font approach were deliberately NOT adopted (conflicts with this skill's zero-third-party-assets stance) |
| open-slide (1weiho) | https://github.com/1weiho/open-slide | MIT | The type scale table, the **vertical-budget arithmetic**, the page-role catalog, the transition-restraint doctrine, the self-review checklist |
| GordenPPTSkill (GordenSun) | https://github.com/GordenSun/GordenPPTSkill | **Non-commercial; bundled templates third-party, no redistribution** | Methodology only: the capacity/overflow-enforcement idea and the "shorten text, never shrink font" rule. **We took no templates or assets** — its bundled .pptx files are exactly the kind of unlicensed material this skill deliberately avoids shipping |
| ppt-master (Hugo He) | https://github.com/hugohe3/ppt-master | MIT | An SVG→pptx engine (different medium). We distilled five *principles*: **deck rhythm** (anchor/dense/breathing pacing, breathing-forbids-card-grids), the **never-stack-visual-weight / shadow-budget** elevation discipline, the **lift-key-information** inline-emphasis rule, the **spec-lock anti-drift re-anchor** workflow step, and its **rendered-QC numeric thresholds** (now our visual self-review checklist). Conversely, our pre-computed **vertical-budget overflow math** is something ppt-master lacks — a two-way exchange, not a one-way copy. No code or assets taken |

## Why no bundled templates

GordenPPTSkill's templates are third-party designer work marked "personal/research use
only, no commercial use." Redistributing them would infringe. This skill instead encodes
design *principles* (free to reuse) and generates original decks — see the "On copying vs.
originality" section in `SKILL.md` and `licensed-sources.md`.

## Other references

- Two refinements surfaced by `skill-evolve` (principles only — no code taken):
  the **per-role density caps** in `layouts.md` (tie the overflow budget to a typed
  page-role contract) are sharpened from **proyecto26/slides-ai-plugin** (license
  unstated — verify before any code reuse); the **CJK-headline downscaling** rule in
  `principles.md` §13 is informed by **op7418/guizang-ppt-skill** (AGPL-3.0 — learn the
  idea, never vendor the code). 2026-07-02: the same project's **layout-lock** idea
  (register the allowed page roles, require `data-label` on every slide, have the
  checker flag unregistered/invented layouts — "constraints make AI-generated decks
  more reliable") was adapted into `layouts.md` + `check_deck.py`'s role-lock checks.
  Deliberate divergences: our checks are WARN-level (`--strict` escalates) instead of
  upstream's hard block, the registry is our own nine-role catalog (not S01–S22), and
  the checker code is entirely original — AGPL forbids vendoring any of its files.
  Evaluation: `research/audits/2026-07-02-guizang-ppt-skill.md`.
- W3C / design conventions for type scale, grid, and contrast (WCAG AA for body text).
- Public-domain design *movements* that inspired the presets in `style-presets.md` —
  Swiss/International Typographic Style, editorial/magazine layout, brutalism. Styles are
  ideas, not owned works.
- Fonts: Google Fonts (OFL/Apache), Fontshare (free commercial) — see `licensed-sources.md`.
- Chinese line-breaking (§13 of `principles.md`): the 避頭尾 / 標點擠壓 / 標點懸掛
  conventions and the choice of native CSS to express them are drawn from **W3C clreq**
  (Requirements for Chinese Text Layout, https://www.w3.org/TR/clreq/) and the reference
  designs **Han.css 漢字標準格式** (https://github.com/ethantw/Han, MIT) and **heti 赫蹏**
  (https://github.com/sivan/heti, MIT). We use the native CSS properties (`line-break`,
  `text-spacing-trim`, `hanging-punctuation`) rather than those libraries' code.
