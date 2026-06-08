---
name: social-card
description: >-
  Generate polished IG / LinkedIn social card image sets (carousels + single cards)
  from an article, notes, outline, or screenshots — a principle-driven design engine
  (Swiss + Editorial systems, fixed-ratio frames) that renders to exact-size PNG via
  agent-browser. USE THIS SKILL when the user wants Instagram carousel images, IG
  4:5 / 1:1 / 9:16 posts, LinkedIn document-carousel or square cards, or 「社群卡片」
  「IG 輪播圖」「貼文圖」「LinkedIn 卡片」. Targets IG (4:5 primary, 1:1, 9:16) and
  LinkedIn (1:1, 1.91:1); FB gets a single 1.91:1 card. Do NOT use to POST or schedule
  to social media (no account management), for 16:9 slide decks (use slide-deck), or
  for Xiaohongshu 3:4 / WeChat 21:9 covers.
license: MIT
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash(agent-browser:*)
---

# social-card — a principle-driven design engine for IG / LinkedIn cards

Most AI-made social cards fail the same way: text shrinks until it fits, every card is
a title plus three bullets, the palette is timid, and the set reads as "made by a
default template." This skill prevents that. **Quality comes from a rigorous design
system applied consistently — not from copying a template file.** That is also why the
repo ships no third-party template assets: design *principles* are free to reuse,
specific template *files* are copyrighted. We generate original cards instead.

The output is a set of **fixed-dimension card frames** in one HTML file, each rendered
to an **exact-size PNG** (e.g. IG 4:5 → exactly 1080×1350) via **agent-browser** — no
playwright, no chromium install. Posting/scheduling is out of scope; this produces the
images, you publish them.

## The non-negotiables (full reasoning in `references/principles.md`)

1. **One idea per card.** If a card carries more than one concept, split it. A longer
   carousel beats a crowded card.
2. **Shorten copy, never shrink type.** When content overflows the frame, cut words or
   add a card — *never* drop the font below the readable floor or crush line-height to
   cram. The QA gate enforces this.
3. **Respect the safe area.** IG Stories/Reels (9:16) reserve top/bottom bands for
   platform UI; keep titles, body, and CTAs inside the central safe band.
4. **Ship zero licensed assets.** Every template, palette, and background is original.

## Each run

1. **Read the input** — article, notes, outline, or screenshots — and the target
   platform(s). Default to IG 4:5 carousel unless told otherwise. See
   `references/platform-specs.md` for the exact pixel size and safe area of each ratio.
2. **Plan the card set** — pick page roles from `references/layouts.md` (cover →
   points → optional checklist/comparison/quote → summary) and a style family +
   palette from `references/style-system.md` (Swiss or Editorial).
3. **Build one HTML file** in a task folder, each card a fixed-dimension
   `<section class="card ig-45" id="ig-01">…</section>`. Start from
   `assets/template-swiss.html` or `assets/template-editorial.html`. Screenshots follow
   `references/screenshot-treatment.md` (object-fit by content type).
4. **Render + QA** per `references/render-qa.md`: agent-browser screenshots each frame
   to an exact-size PNG, then `agent-browser eval --stdin < scripts/qa-rules.js` checks
   overflow / font floor / title caps / safe area. Findings → fix by splitting or
   cutting copy, **never** by shrinking. Re-render until QA returns empty.

## References

- `references/platform-specs.md` — IG/LinkedIn/FB pixel sizes, safe areas, naming.
- `references/principles.md` — one idea per card, shorten-not-shrink, CJK line-height.
- `references/style-system.md` — Swiss vs Editorial, original palettes.
- `references/layouts.md` — the page-role catalog with character caps.
- `references/screenshot-treatment.md` — object-fit / framing rules.
- `references/render-qa.md` — the agent-browser render + eval QA pipeline.
- `references/attribution.md` — design principles adapted from guizang-social-card-skill.
