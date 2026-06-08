# Attribution

`decision-lens` is an **original rewrite**. The three decision *methods* it routes over
are adapted from the decision cluster of **yaojingang/yao-open-skills** (MIT); the math
itself is public-domain (Bayesian odds updating, Beta-Binomial conjugacy, the Kelly
criterion, weighted multi-criteria ranking) and not copyrightable. **No upstream files
were copied** — the scripts, references, and SKILL.md are written from scratch for this
project. Full evaluation of the source collection (including why it is never installed
wholesale) is in `research/audits/2026-06-08-yao-open-skills.md`.

## Sources (methods adapted, not files)

### 1. yao-bayesian-skill — MIT
- Repo: https://github.com/yaojingang/yao-open-skills → `skills/yao-bayesian-skill`
- Adapted: the evidence-to-action workflow — prior → likelihood-ratio grading → odds
  update → posterior → action threshold → sensitivity. Reimplemented in
  `scripts/bayes_update.py` (odds + Beta-Binomial) and `references/bayesian.md`.

### 2. yao-crux-skill — MIT
- Repo: https://github.com/yaojingang/yao-open-skills → `skills/yao-crux-skill`
- Adapted: primary/secondary problem diagnosis with three tests (decisiveness / leverage /
  stage) and a breakthrough action. **De-politicized** — the upstream's Mao-era
  "矛盾論" branding is dropped; only the analytical method is kept. Reimplemented in
  `scripts/crux_score.py` and `references/crux.md`.

### 3. yao-kelly-skill — MIT
- Repo: https://github.com/yaojingang/yao-open-skills → `skills/yao-kelly-skill`
- Adapted: Kelly sizing as a conservative allocation engine — binary f\* and multi-scenario
  log-growth maximization, fractional Kelly, caps, and the no-edge refusal. Reimplemented
  in `scripts/kelly_size.py` and `references/kelly.md`.

## What was deliberately NOT taken

- The upstream HTML/PDF/DOCX **export pipelines** (pandoc / weasyprint / headless-browser
  subprocess) — out of scope; the scripts here are pure calculators that print JSON.
- The **Simplified-Chinese default output** — this skill's output language follows the
  user's query (Traditional Chinese for a Chinese query).
- Any **frontmatter self-promotion / copyright-stamping** present elsewhere in the upstream
  collection (see the audit) — none of it is reproduced.

## Re-sync

`sources.lock` pins each of the three upstream skills at the commit reviewed. When
`skill-evolve` runs, diff them for a genuinely better method formulation worth folding in.
The math is stable; the prompts/protocols are the parts that may improve upstream.
