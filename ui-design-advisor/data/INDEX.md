# Data index — read this first, then open only what you need

This skill is **data read directly by the model** (no search engine, no scripts).
Routing rule: read THIS index → decide which 1–3 files the task needs → open only
those. Do **not** load every file. For keyword hits across files, use `Grep` on
`data/` (e.g. `grep -i "fintech" data/ui-ux-pro-max/*.csv`).

All files are plain CSV / JSON / Markdown. Formats are intentionally NOT uniform —
each source keeps its own shape; you read and reason over them directly.

## ui-ux-pro-max/ — design-decision tables (CSV, MIT)

| file | rows | what's in it | key columns | read when |
|---|---|---|---|---|
| `styles.csv` | 84 | UI style catalog (minimalism, glassmorphism, brutalism…) | Style Category, Keywords, Primary/Secondary Colors, Effects, Best For, Do Not Use For, Light/Dark, Performance, Accessibility | choosing the visual style |
| `ui-reasoning.csv` | 161 | the decision engine: per UI category → recommended pattern + priorities | UI_Category, Recommended_Pattern, Style_Priority, Color_Mood, Typography_Mood, Key_Effects, Decision_Rules, Anti_Patterns | **start here** to reason about a screen/component |
| `colors.csv` | 160 | functional palettes by product type (shadcn-style token set) | Product Type, Primary/Secondary/Accent, Background, Card, Muted, Border, Destructive (+ On- pairs) | picking a working palette / tokens |
| `typography.csv` | 73 | curated font pairings | Font Pairing Name, Heading Font, Body Font, Mood Keywords, Best For, Google Fonts URL, CSS Import, Tailwind Config | choosing fonts |
| `charts.csv` | 25 | chart-type selection | Data Type, Best Chart Type, When to Use / NOT, Data Volume, Color Guidance, Accessibility Grade | picking a chart/visualization |
| `products.csv` | 161 | per product-type recommendation bundle | Product Type, Primary/Secondary Style, Landing Pattern, Dashboard Style, Color Focus, Key Considerations | quick "what fits this kind of product" |
| `landing.csv` | 34 | landing-page section patterns | Pattern Name, Section Order, CTA Placement, Color Strategy, Effects, Conversion | designing a landing page |
| `icons.csv` | 104 | icon-library guidance | Category, Icon Name, Library, Import Code, Best For, Style | choosing icons |
| `ux-guidelines.csv` | 98 | UX do/don't rules with severity | Category, Issue, Platform, Do, Don't, Code Good/Bad, Severity | reviewing UX correctness |
| `app-interface.csv` | 29 | native/app-specific UI rules | (same shape as ux-guidelines) | mobile/app interfaces |
| `react-performance.csv` | 44 | React perf do/don't | (same shape as ux-guidelines) | React performance review |
| `google-fonts.csv` | 1923 | **large** raw Google Fonts catalog | font metadata | only for exhaustive font lookup — prefer `typography.csv` first |
| `stacks/<framework>.csv` | ~16 files | per-framework implementation guidelines | Category, Guideline, Do, Don't, Code Good/Bad, Severity, Docs URL | when implementing in react / nextjs / vue / svelte / astro / tailwind / shadcn / swiftui / flutter / angular / laravel / nuxt / jetpack-compose / threejs / react-native |

## color-combinations/ — curated aesthetic palettes (JSON, MIT)

| file | what's in it | read when |
|---|---|---|
| `colors.json` | 348 historical colour combinations over 159 named colours (Sanzo Wada), each with `name`, `combinations` (indices), `cmyk`, `lab`, `rgb`, `hex` | want a tasteful / editorial / heritage palette that the functional `colors.csv` lacks. Resolve a combination by its colour indices into the colour list. |

## accessibility/ — a11y references (Markdown)

| file | what's in it | read when |
|---|---|---|
| `wcag-checklist.md` | WCAG 2.2 checklist, P0/P1/P2 prioritized | accessibility audit / compliance pass |
| `aria-patterns.md` | 15+ WAI-ARIA interactive patterns | building accessible interactive components |

## ux-heuristics/ — classic UX/design principles (Markdown, MIT)

Small canonical references: Nielsen's 10 heuristics, Don Norman's principles, WCAG
POUR, inclusive-web-design principles, cognitive-load reduction, defensive design,
intuitive-UI steps, simplicity strategies, IxD checklist, common app-design
mistakes, usability scales, table design. Open the one whose filename matches the
question; they are short.

## Provenance / licensing
See `../references/attribution.md`. Sources: ui-ux-pro-max (MIT), dictionary-of-
colour-combinations (MIT), ux-ui-agent-skills a11y (MIT declared in README, no
LICENSE file), SteveBarnett/Checklists (MIT).
