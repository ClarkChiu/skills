# Attribution

This skill **vendors data** (not code). The SKILL.md workflow is original; the
knowledge under `data/` is curated material copied from four upstream projects.
Only data files were taken — no scripts, CLIs, or skill scaffolding were copied
or executed. Each source's full security review is in
`research/audits/2026-06-05-ui-ux-pro-max.md` and the day's research log.

## Sources

### 1. ui-ux-pro-max (the design-decision CSV pack) — MIT
- Repo: https://github.com/nextlevelbuilder/ui-ux-pro-max-skill (LICENSE file: MIT)
- Vendored: `src/ui-ux-pro-max/data/*.csv` → `data/ui-ux-pro-max/` (12 domain CSVs
  + `stacks/` 16 framework files).
- **Dropped:** `draft.csv` and `design.csv` (self-marked backup / not read by the
  upstream engine, Simplified-Chinese scratch), and all scripts (`_sync_all.py`,
  `search.py`, `core.py`, `design_system.py` — we read the data directly instead).
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

### 3. ux-ui-agent-skills (accessibility references) — MIT (declared, no LICENSE file)
- Repo: https://github.com/plugin87/ux-ui-agent-skills
- Vendored: `accessibility/wcag-checklist.md` + `accessibility/aria-patterns.md`
  → `data/accessibility/`.
- **Licensing caveat:** the README's License section states "MIT", but the repo
  ships **no LICENSE file** (GitHub reports `license: null`). Treated as an MIT
  grant per the author's stated intent; flagged here because it is weaker than a
  LICENSE-file MIT. Its design-token / atomic-design / framework-code layers were
  **not** taken (different layer; overlaps `frontend-design`). One-shot repo
  (created and last pushed the same 20-minute window, 2026-03-16).

### 4. SteveBarnett/Checklists (UX heuristics) — MIT
- Repo: https://github.com/SteveBarnett/Checklists (LICENSE file: MIT)
- Vendored: the heuristic/principle markdown files → `data/ux-heuristics/`
  (Nielsen's 10, Norman's principles, WCAG POUR, inclusive web design, cognitive
  load, defensive design, etc.). Skipped `README.md`.

## Re-sync

`sources.lock` pins each source at the commit vendored. When `skill-evolve` runs,
diff these sources for new/updated design data worth pulling. The aesthetic and
heuristic sources (2, 4) are stable/old and change rarely; the ui-ux-pro-max CSVs
(1) update more often and are the main thing to re-check.

## Customization layer

User-specific design preferences (brand colors, banned styles, house fonts) should
be added as a separate highest-priority file under `data/` rather than editing the
vendored files — keep upstream data clean so `skill-evolve` can still diff it.
