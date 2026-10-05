# Attribution

`terse` is adapted from **mattpocock/skills** → `productivity/caveman` (MIT). The idea —
a toggled mode that cuts ~70% of tokens — is Matt's; this is an **original rewrite**, no
files copied. Full evaluation: `research/audits/2026-06-08-mattpocock-skills.md`
(verdict: 🟦 build-your-own).

## What changed vs upstream (and why)

Upstream `caveman` compresses by **mangling English grammar** ("respond terse like smart
caveman" — drop articles, telegraphic fragments). The user installed it and found it makes
**Chinese read as 怪腔怪調** — stilted, telegraphic, classical-sounding — because Chinese has
no articles to drop and is already compact, so grammar-mangling just breaks it.

The fix is the core redesign:
- **Cut CONTENT, not grammar** — remove preamble, hedging, restating, filler, repetition;
  keep the natural grammar of the response language.
- **Language-aware** — English may go clipped; **Chinese stays fluent Taiwan Traditional**.
- **Safety exception kept** — full text for security warnings and destructive-action
  confirmations (this part of caveman was sound).
- Positioned as a complement to the repo's `humanizer` (tone) vs `terse` (length).

## Second source: ayghri/i-have-adhd (2026-08-17)

**ayghri/i-have-adhd** (MIT) — an ADHD-friendly output-shaping skill. **Method only, no
files copied.** Full evaluation: `research/2026-08-17-skill-research-log.md` +
`research/audits/2026-08-17-i-have-adhd.md` (verdict: 🟦 build-your-own, don't install).

Seven of its ten rules were already covered here or by `CLAUDE.md` Rule 0/4/10/12, and its
headline rule (no preamble / no closer) is covered three times over. Four ideas were worth
taking, and they all sharpen what `terse` already claimed to do:

- **The first-line/last-line send check.** This skill had a cut-list but no acceptance
  test. Now it has one.
- **The hedging caveat** — cut hedging that carries no information, but keep a hedge that
  carries real uncertainty, because deleting it manufactures confidence. Previously the
  rule said cut hedging, full stop; that was a real hole against Rule 12.
- **End with the next step, not a pleasantry.** Previously sign-offs were cut wholesale,
  which also cut the useful kind. Added the report/verdict caveat (when the next move is
  the user's decision, ask for the decision — don't invent a task).
- **Rank-and-bucket a long list instead of capping it.** Upstream caps lists at 5; that
  was **deliberately not taken** — its own issue #96 shows models take the cap literally
  and truncate, and a hard cap contradicts CLAUDE.md Rule 0 ("as long and detailed as the
  problem genuinely requires"). Only the bucketing survives.

Its "when to break the rules" §5/§6 also generalized this skill's safety exception into
"the shape yields, the content wins" (task beats rule; harness and standing instructions
beat rule).

**Deliberately not taken**, and why — do not re-adopt these on a later re-sync:

- **Specific time estimates** ("about 15 minutes") — asks the model to invent a number
  where CLAUDE.md Rule 0 requires "never hallucinate" plus explicit confidence levels.
- **Numbered multi-step lists** and **restating state each turn** — CLAUDE.md Rule 4 and
  Rule 10 already do both, and Rule 10's three-state version (done / **verified** / left)
  is stricter.
- **Lead with an executable action as a general rule** — conflicts with Rule 1 (surface
  assumptions and competing interpretations first) and misfires on report-shaped output.
- The always-on `SessionStart` hook, the plugin packaging, and the five-language install
  docs — peripheral to a prose skill; audit found them clean but not worth the surface.

## Re-sync

`sources.lock` pins upstream. On `skill-evolve`, mine any new brevity ideas, but keep the
cut-content-not-grammar / language-aware rule — that is the whole point of the rewrite.
For `ayghri/i-have-adhd`, re-check the "deliberately not taken" list above before adopting
anything new; those four were rejected on conflicts that will not have changed.
