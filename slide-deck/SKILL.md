---
name: slide-deck
description: >-
  Build a polished, presentation-ready slide deck as a single self-contained HTML
  file (1920×1080, scales to any screen, prints to PDF). This is a principle-driven
  DESIGN ENGINE, not a template filler: it generates original decks from a bundled
  design system (type scale, layout grid, color discipline, motion restraint) and a
  library of original style presets — so the output looks custom-crafted, not like a
  default template, and ships with zero third-party/licensed assets in the repo.
  USE THIS SKILL whenever the user wants to make, build, design, or polish slides, a
  slide deck, a presentation, a 簡報, 投影片, a talk/keynote/pitch deck, lecture slides,
  or asks to turn notes / a document / an outline / a .pptx into slides — even if they
  just say「幫我做投影片」「做一份簡報」「slides for X」without naming a tool. Also use to
  improve an existing HTML deck, convert a PowerPoint into editable HTML, or match a
  brand/template style the user supplies. Do NOT use for a single static poster image,
  a PDF report with no slide structure, or editing a .pptx in place (this outputs HTML).
---

# Slide Deck — a principle-driven design engine

Most AI-made slides fail the same way: text shrinks until it fits, every slide is a
title-plus-three-columns, the palette is timid, and the whole thing reads as "made by
a default template." This skill exists to prevent that. **Quality comes from a rigorous
design system applied consistently — not from copying someone's template file.** That is
also why the repo ships no third-party template assets: design *principles* are free to
reuse, specific template *files* are copyrighted. We generate original decks instead.

The output is **one self-contained HTML file**: a fixed 1920×1080 canvas scaled as a
whole to any screen, keyboard/click navigation, and a print stylesheet so `Ctrl/Cmd-P →
Save as PDF` gives one slide per page. No framework, no build step, no dependencies.

## The non-negotiables (read `references/principles.md` for the full reasoning)

These are the rules that separate a clean deck from a cramped one. Internalize them;
they drive every decision below.

1. **One idea per slide.** If a slide carries more than ~40 words / one concept, split
   it. More slides is always better than a crowded slide.
2. **Split, never shrink.** When content overflows, cut text or split the slide —
   *never* drop the font below the scale or tighten line-height to cram. This is the
   single most important rule; it is what makes a deck feel comfortable.
3. **Big enough to read.** Body text 32–44px on the 1920×1080 canvas; never below 28px.
   Hero 140–200, section 80–120, page heading 56–80, caption 22–28.
4. **Do the vertical-budget math before writing a slide.** The canvas does not scroll;
   anything past 1080px is silently cropped. `usable = 1080 − 2×padding`; each element ≈
   `font-size × line-height × lines`, plus 32–64px gaps. Sum it; if it exceeds the
   budget, split. See `references/principles.md`.
5. **One coherent visual direction.** One palette (1 bg, 1 ink, 1 accent, 1 muted), one
   type pairing, one aesthetic — held across every slide. The accent appears at **one**
   spot per slide.
6. **Motion is restraint.** Pick one transition family (140–280ms, ≤12px / 3% magnitude,
   opacity always, never `linear`) or omit transitions entirely. Six different
   transitions is the loudest "made in PowerPoint" signal.

## Workflow

### Phase 0 — Mode

- **New deck** (default) → Phase 1.
- **From the user's PowerPoint / their own template** (path D) → `references/ingest.md`.
  Extract their content + style, then rejoin at Phase 3. We never redistribute their file.
- **Improve an existing HTML deck** → read it, apply the principles, lint, redeliver.

### Phase 1 — Content & intent (ask once, batched)

Gather in a single `AskUserQuestion` round — don't drip questions:

- **Purpose & audience** (pitch / teaching / report / keynote) — sets tone and density.
- **Length** (rough slide count).
- **Density mode** — the most load-bearing choice:
  - *Speaker-led* (talks): one idea per slide, large type, 1–3 bullets, more slides.
  - *Reading-first* (handouts/async): more self-contained slides, 4–8 bullets or 4–6
    cards, structured grids — still never cramped.
- **Motion** (static / subtle / rich).

If the user already pasted the content, infer answers and confirm rather than asking cold.

### Phase 2 — Style (pick the source — see the three legal paths)

The deck's look comes from a **style preset**: a self-contained recipe of palette + type
+ layout + motion. Three ways to source one, all repo-clean:

- **B — Built-in original presets (default).** Choose from `references/style-presets.md`
  (Swiss-minimal, editorial, brutalist, dark-neon, warm-paper, technical). These are our
  own CSS; pick one that fits the subject, or blend. Prefer this.
- **C — A commercial-OK licensed source.** Only if the user wants a specific external
  look. `references/licensed-sources.md` lists permissively-licensed template/font
  pools (reveal/Marp MIT, HTML5 UP & SlidesCarnival CC-BY, Google Fonts, Fontshare) and
  their attribution rules. Reference at runtime; **do not commit those files into this repo.**
- **D — The user's own template.** Match the style you extracted in Phase 0.

When the user is unsure, **show, don't tell**: generate 2–3 single-slide previews in
different presets, let them pick. People choose by seeing, not by adjective.

### Phase 3 — Plan the deck

Sketch page roles before writing any HTML: Cover · Agenda · Section divider · Content ·
Big number · Quote · Comparison · Closing (catalog + when-to-use in
`references/layouts.md`). Commit to the chosen preset's palette and type scale. For each
content slide, do the vertical-budget check (rule 4).

Also assign each slide a **rhythm** — `anchor` / `dense` / `breathing` — and lay them out
as a wave, not a flat run of dense slides (principles §10). This deck-level pacing is the
main defense against every slide collapsing into the same card grid. Breathing slides
forbid card grids.

### Phase 4 — Generate

Start from `assets/template.html` (the engine: fixed stage, scaler, nav, print CSS, and
the seven page archetypes). Replace the `:root` variables with the chosen preset; write
each `<section class="slide">` following the principles. Use absolute px for everything —
the scaler handles fit. Never hardcode page counts; the engine derives nav dots and page
numbers from the DOM.

**Re-anchor on long decks.** Before each slide, restate the locked constraints to
yourself — the 4 palette colors, the type scale, the chosen fonts, this slide's rhythm
tag — so slide 25 stays on the same palette as slide 1. Long generations drift off-style
when the original choices fall out of context; a one-line re-anchor per slide prevents it.

### Phase 5 — Lint & deliver

Run the bundled checker — it catches the mechanical failures (unreadable font sizes, a
slide too dense to be one idea, leftover placeholder/lorem, generic slop fonts, a deck
that would silently overflow):

```bash
python3 <skill>/scripts/check_deck.py deck.html
```

Fix every `ERROR`; weigh each `WARN`. Then open the file in a browser to eyeball it.
For PDF, either `Ctrl/Cmd-P → Save as PDF`, or run `scripts/export_pdf.py deck.html`
(needs Playwright — it renders each slide at 1920×1080).

**Links & QR.** Any URL the audience should reach must be a real
`<a href="…" target="_blank" rel="noopener">` — plain text isn't clickable, and the
engine's click-to-advance deliberately ignores `<a>` so links work. But a *projected*
deck can't be clicked at all, so for a call-to-action add a **QR code**: generate it
offline (Python `segno` → inline SVG) and embed it so the deck stays self-contained.

**Sharing.** The deck is one self-contained file — drop it on any static host. Fastest
zero-setup option: **Netlify Drop** (drag the file onto app.netlify.com/drop → instant
public URL, no account). Others: `surge` CLI, GitHub Pages, Cloudflare Pages, Vercel.

## On copying vs. originality (why no bundled templates)

Layout conventions, type scales, grid systems, and aesthetic *styles* (Swiss, editorial,
brutalist…) are ideas — not copyrightable, reuse freely. A specific template *file's*
exact expression (its graphics, image choices, arrangement) **is** copyrighted. So the
skill encodes the former (in `references/`) and generates original decks, rather than
shipping the latter. If a user points at a paid template (Tailwind UI, Canva Pro,
Envato), explain we can match its *style* but cannot redistribute its *files*.

## References

- `references/principles.md` — the full design system + the vertical-budget method. **Read first.**
- `references/style-presets.md` — the built-in original style library (path B).
- `references/layouts.md` — page-role catalog and the layout decision tree.
- `references/licensed-sources.md` — commercial-OK external sources + fonts (path C).
- `references/ingest.md` — converting the user's PowerPoint/template (path D).
- `references/output-formats.md` — HTML (this skill) vs native .pptx; when to reach for ppt-master instead.
- `references/attribution.md` — the projects this skill's principles are distilled from.
