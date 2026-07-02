# Brand assets — never guess a brand's colors

Triggered from Workflow step 1: the Design Read involves a **recognizable brand**
(a company, product, or open-source project with an established identity).

## Why this is a hard rule

Model memory holds an *average* of every era of a brand's identity — old rebrands,
fan recreations, compressed screenshots. A hex written from memory is almost always
slightly wrong, and slightly-wrong brand color is worse than none: it reads as
counterfeit to anyone who knows the brand. This is the brand-level case of the
generic-AI problem: **default AI output is the average of all brands, so no brand is
recognizable in it.** Therefore: **MUST NOT write a brand hex, logo rule, or
typeface claim from memory.** Get it from a source or don't state it.

## Source ladder (stop at the first rung that answers)

1. **User-supplied / existing spec.** Assets the user handed over, or a previously
   pinned `docs/design/brand/<brand>-spec.md` in this repo. If a spec exists,
   reuse it — do not re-fetch, do not re-ask.
2. **Fetch and pin (only when WebFetch is available this session).** Official
   sources, in order of authority: the brand's own design/brand-guidelines page →
   the brand site's rendered CSS (buttons, header) → standing logo/hex databases
   (`svgl.app`, `simpleicons.org`). Record the source URL and fetch date next to
   every value.
3. **Ask.** No network, or the fetch is inconclusive → `AskUserQuestion` for the
   hex values / an asset file. A one-question pause beats a counterfeit palette.

No rung permits falling back to memory. If the user explicitly says "just
approximate it", record that instruction in the brief and mark the values
`(approximate, user-waived)`.

## Pin it: `docs/design/brand/<brand>-spec.md`

After rung 2 or 3 succeeds, persist the result so the ladder starts at rung 1
next time:

```markdown
# <Brand> — brand spec
- Primary: #RRGGBB   (source: <url>, fetched YYYY-MM-DD)
- Secondary / accent: #RRGGBB (source: …)
- On-dark / on-light usage notes: <constraints, e.g. "logo never on gradient">
- Typeface (if official): <name> (source: …)
```

Keep it values-and-URLs only — do **not** save logo image files into the repo.

## Override rule

A brand-spec **overrides** palette rows from `data/`: the vendored data picks the
*style* (layout language, type pairing, effects); the brand assets pin the
*colors*. When both speak, brand wins on color, data wins on style. This is the
disciplined version of SKILL.md's "Your preferences win".
