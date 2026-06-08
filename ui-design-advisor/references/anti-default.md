# Anti-default taste — read the room, dodge the clichés, calibrate

Three habits that separate a considered design read from a default-template one.
Per-row `Anti_Patterns` in the CSVs catch *style-specific* mistakes; this file catches
the *universal LLM defaults* that fire regardless of style, plus a way to declare the
read and tune its intensity. Adapted from Leonxlnx/taste-skill (principles, not files —
see `attribution.md`).

## 1. The Design Read — declare it in one line before deciding

Most AI design is bad because the model jumps to a default aesthetic instead of reading
the room. Before choosing style/palette/fonts, state the read explicitly:

> **Reading this as: `<screen kind>` for `<audience>`, with a `<vibe>` language, leaning
> toward `<style / design system>`.**

Examples:
- *"B2B SaaS dashboard for technical operators, with a calm Linear-style language, leaning
  toward a restrained grotesque + functional palette + minimal motion."*
- *"OT-security marketing site for procurement buyers, with a trust-first language, leaning
  toward an authoritative Swiss system + the brand red as a single accent."*

The audience picks the aesthetic, not your taste. If the read genuinely diverges and you
cannot infer it, ask a clarifying question (sparingly, never a multi-question dump — same
budget as step 1) — otherwise declare the read and proceed.

## 2. Anti-default discipline — the LLM clichés to reach past

These are what every model defaults to. None is banned outright, but reaching for them
*by default* is the tell. Pick each one deliberately or not at all:

- **AI-purple / indigo gradients** (`#6366f1`, violet-on-white mesh) as the house color.
- **Centered hero over a dark mesh/aurora gradient** as the default first screen.
- **Three equal feature cards** in a row as the default "features" pattern.
- **Generic glassmorphism on everything** — blur + translucency as decoration, not meaning.
- **Inter / Roboto / system stack as the display face** — the default-font giveaway. Use a
  distinctive pairing from `typography.csv`.
- **slate-900 / zinc text on pure white** as the only contrast move.
- **Infinite-loop micro-animations everywhere**, drop shadows and huge border-radius with
  no purpose, decorative icons that carry no information.

When the data row you picked *is* one of these (e.g. a legitimately glassy style), keep it
— but say so in the brief's rationale, so it reads as a choice, not a default.

## 3. The three dials — turn "taste" into tunable parameters

Calibrate intensity along three axes, then let layout/motion/density decisions follow. State
the chosen values in the brief so they are reviewable, not implicit.

- **DESIGN_VARIANCE** (1 = perfect symmetry → 10 = artful asymmetry/chaos)
- **MOTION_INTENSITY** (1 = static → 10 = cinematic / physics-driven)
- **VISUAL_DENSITY** (1 = gallery / airy → 10 = cockpit / packed data)

Infer from the read:

| Signal | VARIANCE | MOTION | DENSITY |
|---|---|---|---|
| minimalist / clean / calm / editorial / Linear-style | 5–6 | 3–4 | 2–3 |
| premium consumer / Apple-y / luxury / brand | 7–8 | 5–7 | 3–4 |
| playful / experimental / agency / Awwwards | 9–10 | 8–10 | 3–4 |
| trust-first / public-sector / regulated / a11y-critical | 3–4 | 2–3 | 4–5 |
| data dashboard / admin / operator console | 4–6 | 2–4 | 7–9 |

Sensible default when nothing overrides: **6 / 4 / 4**. Overrides happen conversationally,
not by asking the user to edit a config.
