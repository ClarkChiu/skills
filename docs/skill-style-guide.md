# Self-built skill style guide

Conventions every self-built skill in this repo must follow. The machine-checkable
subset is enforced by `scripts/lint-skills.py` (run it before committing a new or
changed skill). The judgment items are not linted — they are for the author and for
`skill-evolve` to keep honest.

Provenance: distilled from the README "新增一個自建技能" checklist and CLAUDE.md;
the lint idea is adapted from Gentle-AI's `skill-improver`
(github.com/Gentleman-Programming/gentle-ai). We deliberately drop its body
token budget — skills here are intentionally rich (e.g. chinese-typography,
slide-deck carry large `references/`), so a word cap would be wrong.

## Machine-checkable (lint enforces, fails loud)

1. `SKILL.md` exists.
2. `evals/evals.json` exists and is valid JSON.
3. Frontmatter parses and has both `name:` and `description:`.
4. `name:` equals the directory name.
5. **Pairing rule**: `references/attribution.md` and `sources.lock` are both
   present or both absent — never one without the other. Present means the skill
   was adapted from an upstream source; absent means it is pure-original.
6. Registered in `apm.yml` dependencies (`./<name>/`).
7. Symlinked into both `.claude/skills` and `.agents/skills` (opencode consumes
   the `.agents/skills` cross-agent standard; there is no repo-level `.opencode/skills`).
8. Mentioned in the README self-built table.

## Judgment (not linted — author + skill-evolve)

- `description` leads with what the skill does, lists trigger words, and states
  USE THIS / Do NOT boundaries.
- Language follows the CLAUDE.md two-layer rule: a skill's language matches its
  topic; Chinese content is Taiwan Traditional, no Chinese-English mixing.
- Body is not padded. No hard word budget — flag only egregious bloat by eye.

## Usage

```bash
python3 scripts/lint-skills.py   # exit 1 on any violation
```
