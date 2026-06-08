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

## Re-sync

`sources.lock` pins upstream. On `skill-evolve`, mine any new brevity ideas, but keep the
cut-content-not-grammar / language-aware rule — that is the whole point of the rewrite.
