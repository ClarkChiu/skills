# Attribution

## Design and plan workflow (brainstorming.md, writing-plans.md)

Rules adapted from **obra/superpowers** (MIT, by Jesse Vincent), from two of its skills:

- `brainstorming`: https://github.com/obra/superpowers (path `skills/brainstorming/`)
- `writing-plans`: https://github.com/obra/superpowers (path `skills/writing-plans/`)

Not copied verbatim — the rules are **extracted and rewritten to fit this project**: dropped the upstream branded paths (`docs/superpowers/...`), handed execution discipline off to the root `CLAUDE.md` Rules 0–12, and retargeted examples to this user's domain (pytest + git, protocols/testing/infrastructure). The upstream orchestration pieces (`subagent-driven-development`, the Visual Companion local server) are **not vendored**; rationale and verdict are in `research/2026-06-05-skill-research-log.md`.

`sources.lock` tracks the obra/superpowers ref; when those two upstream skills add new rules, `skill-evolve` flags them for re-sync.

2026-09-17 re-sync (v6.3.0, user decision): adopted the three-path classification (spike / bounded / architectural) with its rules (heavier path when unsure, paths only move up, bounded measures the repo, each task gets its own approval) into SKILL.md Step 0 and `brainstorming.md`, renamed the anti-pattern to "too simple to need approval", and added the `Spec:` pointer to the plan header in `writing-plans.md`. Rewritten, not copied.

2026-10-05 re-sync (v6.4.2, user decision): adopted the "write back your understanding" step (stated vs. assumed, invite correction) into Phase 1; staged approval (a yes covers only the stage presented; the user reviews the plan before execution) into the hard gate and handoff; the Review Focus plan-header list plus the Review Focus and Proportion self-review checks; and replaced the "complete code" rule with signature + test assertions + pinned values, a body only where tests don't determine the algorithm, and Interfaces-block references instead of repeated code. Not taken: the two-option execution menu (subagent-driven vs. native) — the non-vendored orchestration layer. Rewritten, not copied.

## Ubiquitous language + ADR capture (adr.md, the inline-capture step)

The Phase 1 step "sharpen terms and capture decisions as you go" + `references/adr.md`
adapt a **principle** from **mattpocock/skills** → `engineering/grill-with-docs` (MIT):
couple the plan-grilling interview to a living domain glossary and capture ADRs inline as
decisions crystallise (rather than batching docs at the end). The ADR format itself is the
standard Michael Nygard structure (public, not copyrightable). No files copied; pinned in
`sources.lock`. Full evaluation: `research/audits/2026-06-08-mattpocock-skills.md`.

## Spec conventions (spec-conventions.md)

`references/spec-conventions.md` is **original** to this repo. It draws only on public,
non-copyrightable standards — **RFC 2119** requirement keywords (IETF) and **Given/When/Then**
acceptance scenarios (Gherkin convention). No files copied, no GitHub upstream to track, so
nothing is added to `sources.lock`. Added 2026-06-30; rationale in
`research/2026-06-30-gentle-ai-borrowed-ideas.md`.

## Divergence pattern (brainstorming.md) — UditAkhourii/adhd, 2026-08-16

**UditAkhourii/adhd** (MIT) — parallel divergent ideation: fan out N isolated branches under
different cognitive frames, score, prune traps, deepen the survivors. **Method only, no files
copied.** Full evaluation: `research/2026-08-16-skill-research-log.md` +
`research/audits/2026-08-16-adhd.md` (verdict: 🟦 build-your-own, do not install, do not
create a new skill — the slot was already `design-gate`'s).

Three ideas landed in "Propose approaches", which was this skill's thinnest step — a single
pass in one context tends to return the three answers a senior engineer gives in thirty
seconds:

- **Strip the false constraints before diverging.** Upstream's `reframe` phase. The sharpest
  idea in the project, and a late addition there (2026-07-23), not part of its original design.
- **Widen before narrowing on a high-stakes fork** — independent explorations in separate
  contexts, one per lens, with the obvious answers ruled out explicitly. The lens list here is
  original and aimed at this user's domain (middlebox, loss, CI-vs-local, standards review,
  3am on-call, $0/hour); upstream's fifteen frames are generic lateral-thinking technique
  (inversion, naive user, red team, biomimicry) and were not taken.
- **A trigger gate** — escalate only when the fork is open *and* picking wrong is expensive.

**Deliberately not taken**, and why — do not re-adopt on a later re-sync:

- **The weighted scoring formula** (`novelty*0.35 + viability*0.40 + fit*0.25` over
  model-generated 0–10 scores). This is fabricated input dressed as arithmetic, which
  `decision-lens` explicitly forbids (never invent priors/odds; grade every input A–D and
  match the wording to the grade). Take the qualitative act — cluster, flag traps — not the
  number.
- **Fuzzy debugging as a trigger.** Generating 30 hypotheses and deepening the top three,
  with no loop that tests them one at a time, is the exact pattern `systematic-debugging`
  exists to stop. Debugging does not route here.
- **Its README's benchmark figures.** Do not cite them. n=6, single-trial, same-model-family
  judging, blinding defeated by output fingerprints, output 3.4–4.9× longer with no length
  control, and never re-run since 23 minutes after the repo was created despite three engine
  changes. The side-by-side on its front page is the one problem out of six that its own
  judge scored as a loss, with the losing dimension omitted.
- The npm package `adhd-agent` — the published 0.1.4 build sets `permissionMode:
  "bypassPermissions"` alongside `allowedTools: []`, and per the Agent SDK's own types
  `allowedTools` is an auto-approve list, not a restriction (restricting needs `tools`). The
  git source has since been fixed to `tools: []` but was never republished. Mitigating: SDK
  0.1.77 requires `allowDangerouslySkipPermissions: true`, which it does not set.

## Further upstream

obra/superpowers' "design before code" stance shares a root with this repo's `CLAUDE.md` — Rule 1 (think before coding) and Rule 4 (goal-driven execution). design-gate is essentially the **front half** of that discipline (design, plan) turned into a repeatable workflow.
