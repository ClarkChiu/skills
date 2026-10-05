# Narrative spine — settle the argument before the pages

A deck is an argument delivered on a clock, not a container for a document. The most
common failure in a generated deck happens *before* any design decision: the source
material gets chopped into pages in its original order, each page gets a title and some
bullets, and the audience leaves having seen a lot and concluded nothing.

`principles.md` governs how a slide *looks*. This file governs what the slides are
*for* — the order they argue in, and the one thing the audience must walk out with.
This is the classic **Minto pyramid / SCQA** discipline: answer first, evidence
underneath, order chosen by the argument rather than by the source document.

The failure mode this prevents has a shape: slide count high, information density high,
takeaway zero. More slides did not help. Better fonts did not help. The deck never
decided what it was claiming.

## 1. The claim (one sentence)

Before any structure, write one sentence: **if the audience forgets everything else,
what is the single thing they must remember?**

Rules that make it load-bearing rather than decorative:

- It is a **claim**, not a topic. "Q3 infrastructure review" is a topic. "We should
  stop provisioning per-team clusters and consolidate onto three regional ones" is a
  claim. A topic cannot be argued for, so a deck built on one has no spine.
- It is **one** sentence. Two claims means two decks, or one claim demoted to support.
- It is **falsifiable in the room** — the audience can disagree with it. If nobody
  could possibly object, it is a status update, and the deck should be a document.
- Every later page either **supports it, qualifies it, or moves toward it**. A page
  that does none of the three does not belong, however interesting it is.

If the user cannot state the claim, that is the finding — surface it before building.
A deck cannot fix an argument that has not been made.

## 2. The page table

Then a table, one row per page, before any HTML exists:

| # | Page job | Relation to previous | Evidence it carries | Spoken line |
|---|----------|---------------------|--------------------|-------------|
| 1 | Name the cost of the status quo | — (opening) | 2026 spend, 3 outages | "We are paying twice for the same reliability." |
| 2 | Show the cause is structural, not bad luck | **cause** | Per-team cluster count vs incident rate | "This is not operator error — it is the shape of the estate." |
| 3 | The consolidation proposal | **progression** | Three-region target diagram | "Three clusters, one on-call rotation." |
| 4 | The objection: latency for APAC | **turn** | p99 by region, before/after | "The obvious worry is APAC — here is what actually happens." |

Column by column:

- **Page job** — one verb phrase. What this page *does to the audience*, not what it
  contains. "Establish that the trend reversed" is a job; "Q3 chart" is a container.
  One job per page; this is the argument-layer twin of the "one idea per slide" rule
  in `principles.md`.
- **Relation to previous** — exactly one of **cause / progression / turn / contrast**.
  Exempt (mark `—`): the cover, the agenda, section dividers, and the closing. Every
  other page needs one. See §3.
- **Evidence it carries** — the specific number, quote, or diagram. "Some data" means
  the page has no evidence yet and will fill with prose at generation time.
- **Spoken line** — the one sentence said aloud while the page is up. Written now, not
  improvised later. It is the honesty test: **if you cannot say a useful sentence over
  the page, the page has no job.**

## 3. Relation vocabulary

Four relations, deliberately few. Adjacent pages must stand in one of them:

| Relation | Means | Typical use |
|----------|-------|-------------|
| **cause** | The previous page's fact *explains* or *produces* this one | Symptom → mechanism; decision → consequence |
| **progression** | Same thread, one step further along | Scope widening; timeline advancing; the next stage of a method |
| **turn** | Direction changes — objection, complication, reversal | "But here is what that misses"; the risk section |
| **contrast** | Two things set against each other to make a difference visible | Before/after; option A vs B; us vs the alternative |

If a page's relation is honestly "and also", the deck has stopped arguing and started
listing. Either merge it into the neighbour, cut it, or find the real relation. A run
of "and also" pages in the middle of a deck is the classic chopped-document signature.

The cover, agenda, section dividers, and the closing are structural furniture, not
argument steps — mark their relation `—` and move on. Everything else must carry one.

## 4. The gate

**Do not generate HTML until the table is complete and every non-exempt row has a
relation.** A blank relation cell means two adjacent pages have no argued connection —
that is precisely the defect this file exists to catch, and it is far cheaper to fix in
a table row than in a rendered slide.

This gate is a judgement check, not a lint rule: `check_deck.py` reads finished HTML
and cannot see an argument. Nothing downstream will catch a spine that was never built,
which is why the gate sits here rather than in the checker.

## 5. Length follows the argument

Slide count is an **output** of the table, not an input to it. Ask the user for a
ceiling ("we have 15 minutes" / "no more than 20 slides") and treat it as a constraint
to satisfy, not a quota to fill.

When the table exceeds the ceiling, cut by **argument rank**: drop the pages furthest
from the claim first. Do not compress by cramming — that violates
`principles.md` rule 2 (split, never shrink) and trades a clear short deck for a dense
long one. Cutting a page is a decision about the argument; shrinking type is a decision
to be unreadable.

## 6. Spoken lines in the HTML

Carry each row's spoken line into the generated deck as a hidden note inside its slide:

```html
<aside class="notes">We are paying twice for the same reliability.</aside>
```

Exactly that form. `assets/template.html` carries `aside.notes { display: none; }` and
`check_deck.py` strips exactly the same shape before counting on-screen density, so notes
never push a slide over the one-idea budget. The two are held in lockstep by the checker's
self-test, which asserts that for each attribute form the checker and the CSS agree:
`class="Notes"` (class selectors are case-sensitive), `data-class="notes"`, and
`speaker-notes` are **not** hidden, so they are **not** stripped — the mistake surfaces as
a density warning rather than silently printing your whole script on the slide.

**If the deck did not come from `assets/template.html`** — path C/D, or an existing deck
being improved — add the `aside.notes { display: none; }` rule yourself. `check_deck.py`
raises an ERROR when notes exist with no rule to hide them, so this cannot pass silently.

Two reasons this is worth doing: the speaker gets their own script back with the file,
and the note stays attached to the page it belongs to when the deck is revised months
later.

Notes are still checked for leftover placeholder text — a `TODO` in a note is a `TODO`
in the deliverable.
