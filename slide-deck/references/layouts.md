# Page-role catalog & layout decision tree

A deck is a sequence of *roles*, not a stack of identical content slides. Reaching for
the right role per point is what gives a deck rhythm. The engine in `assets/template.html`
ships archetypes for seven of the nine roles; **Agenda** composes from the Content
archetype's numbered-list pattern, and **Timeline** from Content on the wide width with
a horizontal axis — both are still registered roles for `data-label`.

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

## Density caps per role (for splitting & linting)

The vertical-budget math (principles §4) checks whether content *fits in pixels*. But
fitting ≠ one idea — a slide can be under the 1080px budget and still be too dense. So
each role also carries a hard **content cap**. Exceed it → split (never shrink, rule 2).
These caps are what make density mechanically checkable, not just eyeballed.

| Role | Hard cap |
|------|----------|
| Cover | title + 1 subtitle + optional eyebrow · **0 bullets** |
| Agenda | **≤6** one-line items |
| Section divider | section title only (+ number/eyebrow) · **0 bullets** |
| Content | heading + body **OR ≤5** one-line bullets — not both |
| Big number | **1** number + **1** caption line |
| Quote | **≤36 Han / ≤22 EN words**, attribution only — no extra columns |
| Comparison | **2** columns × **≤3** items each |
| Timeline | **≤5** nodes |
| Closing | one line + contact · near-empty |

In *reading-first* density mode (principles §9) the Content/Comparison ceilings may rise
(≤8 bullets / 4–6 cards) — but the cap still exists, and overflowing it still means split,
not shrink.

**Role lock.** Every slide MUST carry a `data-label` naming a role from this catalog
(hyphen/case variants like `Big-Number` are accepted) — that label is the hook
`check_deck.py` uses for role checks: the Content/Agenda bullet caps, and a near-empty
density ceiling on the sparse roles (Cover / Section / Closing / Big number / Quote).
A label outside the catalog draws a warning: invented layouts are the main source of
unstable slides — constraints are what make generated decks reliable.

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
