# Attribution

This skill **vendors data** (not code). The SKILL.md workflow is original; the
knowledge under `data/` is curated material copied from four upstream projects.
Only data files were taken — no scripts, CLIs, or skill scaffolding were copied
or executed. Each source's full security review is in
`research/audits/2026-06-05-ui-ux-pro-max.md` and the day's research log.

## Sources

### 1. ui-ux-pro-max (the design-decision CSV pack) — MIT
- Repo: https://github.com/nextlevelbuilder/ui-ux-pro-max-skill (LICENSE file: MIT)
- Vendored: `.claude/skills/ui-ux-pro-max/data/*.csv` → `data/ui-ux-pro-max/`
  (12 domain CSVs + `stacks/` 22 framework files; originally taken from
  `src/ui-ux-pro-max/data/`, switched at v2.11.0 to the `.claude` copy — upstream
  fixed drift between its three internal data copies in #412 and the `.claude`
  copy is the canonical LF version).
- **Dropped:** `draft.csv` and `design.csv` (self-marked backup / not read by the
  upstream engine, Simplified-Chinese scratch; deleted upstream as of v2.11.0),
  `motion.csv` (GSAP snippet pack), and all scripts (`_sync_all.py`,
  `search.py`, `core.py`, `design_system.py` — we read the data directly instead).
- Re-synced 2026-07-20 at v2.11.0 (commit `b484e8338c25`): CSV-by-CSV diff;
  added the 6 desktop stacks (WPF/WinUI/UWP/Uno/Avalonia/JavaFX), re-vendored the
  rewritten `threejs.csv`, normalized line endings to upstream; scan clean.
- Note: upstream is a full skill with a CLI installer and image-generation scripts
  that read `~/.claude/.env`; **none of that is vendored** — only the pure-data
  CSVs. Star/commit anomaly (87k★ / ~134 commits) noted in the audit; irrelevant
  here because we took only inert data.

### 2. dictionary-of-colour-combinations (aesthetic palettes) — MIT
- Repo: https://github.com/mattdesl/dictionary-of-colour-combinations
  (LICENSE.md: MIT, © 2020 Matt DesLauriers)
- Vendored: `colors.json` → `data/color-combinations/colors.json` (348 historical
  combinations over 159 colours, from Sanzo Wada's *A Dictionary of Color
  Combinations*).
- Caveat: the underlying curation derives from a copyrighted print book; the
  colour **values** (hex/lab/cmyk) are facts and not copyrightable. Kept as an
  aesthetic layer the functional `colors.csv` lacks.

### 3. ux-ui-agent-skills (accessibility references) — MIT (LICENSE file added 2026-09-13)
- Repo: https://github.com/plugin87/ux-ui-agent-skills
- Vendored: `accessibility/wcag-checklist.md` + `accessibility/aria-patterns.md`
  → `data/accessibility/`.
- **Licensing:** the caveat is resolved — upstream added an MIT LICENSE file on
  2026-09-13. Until then only the README declared MIT (GitHub reported
  `license: null`), which is why the earlier notes flagged it as weaker.
  Its design-token / atomic-design / framework-code layers were
  **not** taken (different layer; overlaps `frontend-design`).
- **Re-vendored 2026-09-17:** `aria-patterns.md` had been stale since the initial
  release — sections 16–19 (Carousel, Grid/Calendar, Toolbar, Feed) landed upstream
  in June and two earlier re-syncs missed it, because they diffed old-pin against
  new-HEAD instead of against our local copy. Now at 19 patterns, 561 lines.
  `wcag-checklist.md` is unchanged and byte-identical to upstream.

### 4. SteveBarnett/Checklists (UX heuristics) — MIT
- Repo: https://github.com/SteveBarnett/Checklists (LICENSE file: MIT)
- Vendored: the heuristic/principle markdown files → `data/ux-heuristics/`
  (Nielsen's 10, Norman's principles, WCAG POUR, inclusive web design, cognitive
  load, defensive design, etc.). Skipped `README.md`.

## Principle adaptation (not vendored data)

`references/anti-default.md` adapts three **principles** from
**Leonxlnx/taste-skill** (MIT) — the "Design Read" one-line declaration, the
anti-default cliché list, and the three calibration dials (variance / motion /
density). **No files were copied**; the text is rewritten for this skill's
decision-brief workflow. taste-skill is a prompt-only frontend generator (37k★,
viral but solo, 4 months old as of 2026-06-08) we chose **not** to install or
vendor (overlaps this skill + `frontend-design`, off the user's core work — full
verdict in `research/audits/2026-06-08-taste-skill.md`); these three directives
were the parts worth keeping. Pinned in `sources.lock` so `skill-evolve` tracks
the upstream for better wording later.

`references/brand-assets.md` adapts the **brand-asset protocol** from
**alchaincyf/huashu-design** (MIT) — never write brand hex/logo rules from model
memory; fetch from official sources and pin the result — plus its framing of the
anti-slop argument ("default AI output is the average of all brands"). **No files
copied**; the ladder is restructured for this skill (offline-first: user-supplied
spec → WebFetch pin → ask; upstream's mandatory WebSearch step dropped), and the
pin format (`docs/design/brand/<brand>-spec.md`) is original. Full verdict:
`research/audits/2026-07-02-huashu-design.md` (🟦 build-your-own). Pinned in
`sources.lock` for `skill-evolve`. 2026-07-20: upstream 32cc5812 (2026-07-19)
hardened its direction gate — a brand name or style keyword no longer exempts
the 2–3-direction choice, it only narrows it; adopted as one sentence in
SKILL.md step 1. The §1.a brand-asset five-step protocol this file adapts is
unchanged at that commit.

## Re-sync

`sources.lock` pins each source at the commit vendored. When `skill-evolve` runs,
diff these sources for new/updated design data worth pulling. The aesthetic and
heuristic sources (2, 4) are stable/old and change rarely; the ui-ux-pro-max CSVs
(1) update more often and are the main thing to re-check.

## Customization layer

User-specific design preferences (brand colors, banned styles, house fonts) should
be added as a separate highest-priority file under `data/` rather than editing the
vendored files — keep upstream data clean so `skill-evolve` can still diff it.
