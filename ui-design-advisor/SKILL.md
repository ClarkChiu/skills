---
name: ui-design-advisor
description: >-
  Decide what a UI should look like BEFORE building it. Given a product, screen,
  or feature, this skill picks a coherent visual design language — style,
  color palette (with hex), font pairing, chart types, key effects, and
  accessibility notes — each justified against a vendored library of curated
  design-decision data (UI styles, palettes-by-product, font pairings, chart
  selection, UX heuristics, WCAG/ARIA). It produces a short DESIGN BRIEF and
  then hands off to the built-in `frontend-design` skill for implementation.
  USE THIS SKILL when the user wants a design direction, asks 「這個 UI 該長怎樣」
  「幫我定設計風格」「選配色」「挑字體」「該用什麼圖表」, or says "design direction",
  "what should this look like", "pick a style/palette/fonts", "design system for
  X" — especially before writing any frontend code for a dashboard, landing page,
  web app, or mobile screen. It is the DECISION layer (what it should look like);
  `frontend-design` is the IMPLEMENTATION layer (build the UI). Do NOT use for
  writing the actual component code (that's frontend-design), for HTML slide
  decks (that's slide-deck), or for pre-code engineering design+plan of
  non-visual logic (that's design-gate).
allowed-tools: Read, Grep, Glob, Write, AskUserQuestion, WebFetch
---

# UI Design Advisor

Turn a vague "make it look good" into a **defensible design brief**, grounded in
a vendored data library rather than generic taste. Decide; then hand to
`frontend-design` to build.

## What this is / is not

- **Is:** the *decision* layer — which style, palette, fonts, charts, effects,
  and a11y rules fit THIS product, and why.
- **Is not:** the implementation layer. Once the brief is agreed, tell the user
  to use the built-in **`frontend-design`** skill to write the UI (pass it the
  brief). For an HTML slide deck use `slide-deck`; for pre-code engineering
  design of non-visual logic use `design-gate`.

## Data — read only what you need

All knowledge lives under `data/`. **Read `data/INDEX.md` first**, then open only
the 1–3 files the task needs. Never load every file. Use `Grep` over `data/` for
keyword hits (e.g. `grep -i "saas dashboard" data/ui-ux-pro-max/*.csv`).

Sources (see `references/attribution.md`): a UI-decision CSV pack (styles,
`ui-reasoning`, palettes, fonts, charts, products, landing, stacks), a curated
aesthetic-palette JSON, and accessibility + UX-heuristic markdown.

## Workflow

1. **Scope the request.** Identify: product type / domain (fintech, SaaS,
   e-commerce, healthcare, creative…), platform (web / mobile / desktop),
   the specific screen (landing, dashboard, form, marketing site), audience, and
   any brand or stack constraints. If two or more of these are unknown and they
   change the answer, ask **one or two** clarifying questions (AskUserQuestion) —
   do not guess silently. Then **state a one-line Design Read** before deciding
   anything (`references/anti-default.md` §1): *"Reading this as: \<screen> for
   \<audience>, with a \<vibe> language, leaning toward \<style>."* The audience
   picks the aesthetic, not your taste. If the request involves a **recognizable
   brand**, open `references/brand-assets.md` and follow its source ladder —
   never write brand hex/logo rules from memory.

2. **Route, then read.** Open `data/INDEX.md`. Start from
   `ui-ux-pro-max/ui-reasoning.csv` (the per-category decision rules), then pull
   only the relevant tables: `styles.csv` for the style, `colors.csv` for a
   functional palette / tokens (or `color-combinations/colors.json` for a
   tasteful editorial palette), `typography.csv` for fonts, `charts.csv` if there
   is data viz, `products.csv` / `landing.csv` for the product/page pattern, and
   `stacks/<framework>.csv` if the implementation framework is known. For
   accessibility or UX correctness, read `accessibility/` and `ux-heuristics/`.

3. **Decide a coherent language.** Choose ONE direction (not a menu) where the
   pieces reinforce each other. Resolve concrete values: palette as hex,
   named font pairing, specific chart types, named effects. Check it against the
   chosen rows' `Do Not Use For` / `Anti_Patterns` / severity columns, **and**
   against the universal LLM clichés in `references/anti-default.md` §2 (AI-purple
   gradients, centered hero on dark mesh, three equal cards, blanket
   glassmorphism, Inter/Roboto display, slate-on-white) — the row anti-patterns
   are style-specific; the anti-default list fires regardless of style. Set the
   three dials (`anti-default.md` §3) — **DESIGN_VARIANCE / MOTION_INTENSITY /
   VISUAL_DENSITY** — from the Design Read. Note light vs dark and the
   accessibility grade.

4. **Write the DESIGN BRIEF** (concise, structured):
   - **Design Read** — the one-line read from step 1 (screen / audience / vibe).
   - **Calibration** — the three dials (`variance / motion / density`, e.g. `6 / 4 / 4`).
   - **Product & screen** — one line of what this is for.
   - **Style** — name + why (cite the style row's reasoning), light/dark stance.
   - **Palette** — roles with hex (primary / accent / background / surface /
     muted / border / destructive), or a `colors.json` combination if editorial.
     Brand case: cite the brand-spec (`references/brand-assets.md`) — its values
     override palette rows on color; the data still picks the style.
   - **Typography** — heading + body pairing, with the Google Fonts / Tailwind
     hookup from `typography.csv`.
   - **Charts** (if any) — type per data shape, with accessibility note.
   - **Key effects & motion** — restrained, from the style row.
   - **Accessibility** — the P0 items from `wcag-checklist.md` that apply.
   - **Anti-patterns to avoid** — from the rows you used, plus any universal
     default you deliberately kept and why (`references/anti-default.md`).
   Optionally `Write` the brief to `docs/design/<screen>-brief.md` if the user
   wants it persisted.

5. **Hand off.** End by telling the user: implement with the **`frontend-design`**
   skill, passing this brief (and the relevant `stacks/<framework>.csv` rules).

## Example

`examples/txone-website-redesign.md` is a full worked brief (redesigning an
OT-security company's marketing site) showing the routing → data-cited decisions →
brief → handoff flow end to end.

## Your preferences win

The vendored CSV/JSON encode someone else's taste and may age. If the user states
a preference (a brand color, a banned style, a house font), it **overrides** the
data. Durable preferences belong in a user file under `data/` (highest priority),
not hard-coded into this prompt — keep the data as the source of truth.

## Boundaries (don't reinvent)

| Need | Use | Not this skill because |
|---|---|---|
| Build the actual UI code | `frontend-design` | this only decides the look |
| HTML slide deck | `slide-deck` | different output format |
| Pre-code design+plan of non-visual logic | `design-gate` | that's engineering design, not visual |
| Decide whether to adopt an external skill | `skill-curator` | unrelated |
