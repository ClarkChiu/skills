# Diagram style system — accents, SVG craft, CJK labels

A concrete styling layer for the hand-drawn SVG. The gallery examples show *how
good looks*; this file gives **reusable defaults and craft rules** so you don't
re-derive them each time. All of it obeys this skill's hard requirements —
notably **no web fonts, no CDN, no runtime network** (see the caution at the end).

Adapted principles, not vendored code (idea source in `attribution.md`).

## 1. Semantic accent palette (by component type)

Color nodes by **what the component is**, not arbitrarily — a reader learns the
key once and then reads the whole diagram faster. Fill is translucent (so a
subtle grid shows through); stroke is the solid accent. These are sensible
defaults, not law — adjust per diagram, but stay semantic.

| Component type | Fill (translucent) | Stroke (accent) |
|---|---|---|
| Frontend / client / UI | `rgba(20, 50, 62, 0.4)` | `#22d3ee` (cyan) |
| Backend / API / service | `rgba(18, 72, 55, 0.4)` | `#34d399` (emerald) |
| Database / store / cache | `rgba(72, 30, 100, 0.4)` | `#a78bfa` (violet) |
| Cloud / managed service | `rgba(110, 50, 18, 0.35)` | `#fbbf24` (amber) |
| Security / auth / crypto | `rgba(130, 25, 50, 0.4)` | `#fb7185` (rose) |
| Message queue / event bus | `rgba(251, 146, 60, 0.3)` | `#fb923c` (orange) |
| External / third-party | `rgba(38, 37, 30, 0.35)` | `#94a3b8` (slate) |
| AI / LLM / model | `rgba(80, 30, 120, 0.4)` | `#c084fc` (bright violet) |

**The key rule: accents stay constant across themes.** Theme only the
*substrate* — page background, card background, primary/secondary text, grid
lines, arrowheads, borders — through CSS variables. The **semantic accent
strokes and colored labels do NOT get themed**: keep them identical in light and
dark so the color→meaning mapping never shifts. (This is the one place hard-coded
`#hex` in the SVG is correct; everything else themes through classes as the hard
requirements demand.)

## 2. SVG craft rules (hand-drawn, solve real rendering problems)

- **Opaque mask behind a translucent box.** Because fills are semi-transparent,
  any arrow routed *behind* a node shows through it. To block it cleanly, draw an
  opaque themed rect first, then the translucent styled rect on top:
  ```svg
  <rect x="X" y="Y" width="W" height="H" rx="6" class="mask-bg"/>          <!-- opaque, themed -->
  <rect x="X" y="Y" width="W" height="H" rx="6" fill="FILL" stroke="ACCENT" stroke-width="1.5"/>
  ```
  `class="mask-bg"` is a themed variable (near-black in dark, ivory in light) so
  the mask follows the theme while the accent on top does not.
- **Arrow Z-order.** SVG paints in document order. Draw connector paths **early**
  (right after the grid), so component boxes drawn later render *over* them and
  the lines tuck under the nodes instead of crossing on top.
- **Spacing / no overlap.** Standard node height ~60px (services), 80–120px for
  larger blocks. Keep a **minimum 40px vertical gap** between stacked nodes; put
  inline connectors (a queue chip) *in the gap*, never overlapping a node.
- **Legend outside every boundary.** Compute the lowest boundary (`y + height`
  across all zone/cluster/security boxes) and place the legend ≥20px below it;
  extend the `viewBox` height if needed. A legend inside a boundary box reads as
  part of the system.

## 3. Boundary & flow encodings

- **Security group / trust boundary:** dashed stroke (`stroke-dasharray="4,4"`),
  transparent fill, rose (`#fb7185`).
- **Zone / region boundary:** larger dashes (`stroke-dasharray="8,4"`), amber,
  `rx="12"`.
- **Auth / security flow edges:** rose dashed (`#fb7185`) to set them apart from
  ordinary data-flow edges.
- **Boxes:** rounded rects, `rx="6"`–`8"`, 1.5px stroke. Grid pattern at 40px.

## 4. CJK labels (Traditional Chinese)

When labels are Chinese (this project's default per the repo convention):

- **Width:** a Han glyph is ~2× the width of a Latin one. Size node boxes to the
  text: **140–180px** for Chinese labels vs 110–140px for English. Center with
  `text-anchor="middle"`.
- **Spacing:** no space *between* Han characters; **one space between Han and
  Latin/number** runs (matches this repo's pangu spacing convention).
- **Keep technical proper nouns in Latin:** PostgreSQL, Kubernetes, OAuth 2.0,
  gRPC — don't translate identifiers. Prose/labels are Traditional Chinese; the
  API/tech names stay as-is.

## ⚠️ Constraint reminder — do NOT fetch a web font

The upstream this style was adapted from loads JetBrains Mono from
`fonts.googleapis.com`. **That violates this skill's zero-network hard
requirement.** Use a **system monospace stack** instead — no `<link>` to Google
Fonts, no `@import`, nothing fetched at runtime:

```css
font-family: ui-monospace, "SF Mono", "JetBrains Mono", "Cascadia Code",
             Menlo, Consolas, monospace;
```

The file must still open correctly fully offline.
