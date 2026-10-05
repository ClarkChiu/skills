# Attribution

`decision-lens` is an **original rewrite** drawing on two upstreams: the three decision
*methods* from **yaojingang/yao-open-skills** (MIT), and — added 2026-08-05 — the input
grades and the stop condition from **powerycy/goutoujunshi** (MIT since 2026-08-17;
PolyForm Noncommercial at the version we adopted from; §4 below, ideas only). The math
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

### 4. goutoujunshi (狗頭軍師) — MIT since 2026-08-17 (was PolyForm Noncommercial 1.0.0) — **ideas only, never vendor**

- Repo: https://github.com/powerycy/goutoujunshi
- A Chinese-language relationship-advisor skill; the domain is irrelevant here, two of its
  *disciplines* are not. Adopted 2026-08-05, both reimplemented from scratch:
  - **Evidence grading with the wording pinned to the grade.** The four-tier shape itself
    is long-standing prior art (GRADE, levels-of-evidence hierarchies) and upstream's A/B/C
    tiers are a conventional rendering of it — ours are close because both descend from the
    same convention, not because ours is novel. **What we actually took from upstream is
    the second half: fixing which phrasing each tier may use** ("綜合證據較一致" vs
    "一項研究發現" vs "可作為提問框架"), so weak evidence cannot be narrated in strong
    language. Our contribution is retargeting the tiers from *research claims* to *decision
    inputs* (D repurposed as the assumption label), writing our own "Say it like this"
    column, and wiring the result into the pre-existing sensitivity check —
    fragile-if-C-and-D-move.
  - **The stop condition.** Upstream closes every piece of advice with an action, a watch
    window, and an explicit stop condition. `decision-lens` already produced action
    thresholds but let the user walk away with no exit rule; the closing three lines
    (watch window / stop condition / tripwire) come from that.
- **No upstream text enters the skill itself** — `SKILL.md`, the scripts, and the rest of
  `references/` are written from scratch. At adoption (2026-08-05) the license was
  non-commercial, and this repo is publicly redistributed via APM, so that was a hard
  restriction. Upstream switched to MIT on 2026-08-17 (commit 8d30c86), which removes the
  license reason; the method-only rewrite stands for the remaining reasons in the audit
  (PRC-law context, gendered defaults, MBTI scoring, maintenance churn). The three quoted Chinese phrases above are
  confined to this attribution file, where recording *what* was adopted is the whole
  point and brief quotation for that purpose is fair. Methods and ideas are not
  copyrightable; its prose is. Evaluation: `research/audits/2026-08-05-goutoujunshi.md`.

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
