# Page-role catalog & layout decision tree

A deck is a sequence of *roles*, not a stack of identical content slides. Reaching for
the right role per point is what gives a deck rhythm. The engine in `assets/template.html`
ships an archetype for each.

## The roles

| Role | When to use | Structure | Density |
|------|-------------|-----------|---------|
| **Cover** | first slide | eyebrow + title + 1 subtitle | almost empty |
| **Agenda** | optional, after cover | 3–6 numbered items, one line each | light |
| **Section divider** | start of a part | number + section title, little else | near-empty |
| **Content** | the workhorse | heading + body OR ≤5 one-line bullets | per density mode |
| **Big number** | a stat that matters | one number ~half the slide + caption | minimal |
| **Quote** | a voice / testimonial | quote ≤~36 Han chars (≤22 EN words) + attribution | minimal |
| **Comparison** | before/after, A/B, vs | 2 columns + gap, parallel structure | medium |
| **Timeline** | sequence, roadmap | horizontal axis + 3–5 nodes, wide width | medium |
| **Closing** | last slide | thanks / one line / contact | near-empty |

## Decision tree — content relationship → layout

- One strong claim or takeaway → **Content** (heading only, big) or **Big number**.
- One memorable sentence from a person → **Quote**.
- A single metric → **Big number** (never bury it in a bullet).
- Two things opposed or evolving → **Comparison**.
- Three genuinely parallel same-class items → 3-column **Content** (sparingly; not the
  default, not on consecutive slides).
- An ordered sequence over time → **Timeline** (use the wide width).
- A new part of the talk → **Section divider** before it.

## Rhythm rules

- Alternate dense and sparse. A Section divider or Big number after several Content
  slides lets the audience breathe and resets attention.
- Vary the container width across roles (claims narrow, timelines/tables wide) — uniform
  width is the root of a monotonous deck.
- Don't run two of the same role back-to-back unless they're an intentional series.
- Cover, Section divider, and Closing should feel **immersive** (minimal chrome); Content
  and Comparison can show page numbers and a running footer.

## When a slide doesn't fit a role

If a point needs more than a Content slide holds, it's two points — split it into two
roles (e.g. a Big number to state the stat, then a Content slide to explain it). Forcing
everything into one over-stuffed Content slide is the failure this catalog prevents.
