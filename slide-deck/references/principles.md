# Slide design principles

The design system behind every deck. These rules are distilled from four mature
slide projects (see `attribution.md`) and reconciled where they conflicted. They are
mostly judgment calls — but a few are mechanical and the bundled `check_deck.py`
enforces them. Read this before generating a deck; re-read when a slide feels off.

## Table of contents

1. One idea per slide
2. Split, never shrink
3. The type scale
4. The vertical-budget method (anti-overflow)
5. Layout & grid
6. Color discipline
7. Motion restraint
8. Anti-"AI slop" rules
9. Density modes
10. Deck rhythm (pacing)
11. Depth, emphasis & shadow
12. Visual self-review checklist
13. Chinese line-breaking (繁中換行)

---

## 1. One idea per slide

The root test of whether a deck is comfortable. A slide should make **one** point. If
you are tempted to put two, split into two slides — slides are free, attention is not.

- Heading **+** body, OR heading **+** ≤5 short bullets. Not both a paragraph *and* a
  long list on the same slide.
- A bullet should fit on **one line** at its font size. If it wraps, shorten it or give
  it its own slide.
- Hero/cover: title + one subtitle + maybe an eyebrow — nothing else.
- Section divider: the section title and almost nothing else.
- Heuristic: more than ~40 words (count each CJK glyph as a word) → split. `check_deck.py`
  warns past ~110 text units per slide.

Why: the audience reads a slide in 3 seconds while also listening to you. Two ideas means
they finish neither. Density is the enemy of comprehension, not the sign of substance.

## 2. Split, never shrink

**The most important rule.** When content does not fit, the instinct is to shrink the
font or tighten spacing. Never do this. Instead:

- Cut words (most slides have 30% that can go), or
- Split into a continuation slide.

Shrinking type below the scale, raising padding past the layout, or squeezing
line-height under 1.4 to make something fit are all the *same mistake* — they trade the
audience's comfort for your convenience. Splitting is always the right answer when the
budget is tight.

## 3. The type scale (1920×1080 canvas)

Use absolute pixels — the stage is a fixed canvas scaled by one transform, so px is
true and predictable. No `rem` / `vw` / `%` for type.

| Role | Size | Weight |
|------|------|--------|
| Hero / cover title | 140–200px | 800–900 |
| Section heading | 80–120px | 700 |
| Page heading | 56–80px | 700 |
| Body / bullets | 32–44px | 400–500 |
| Caption / label / page no. | 22–28px | 400–500 (often mono) |
| The one big number | 240–340px | 800 |

- **Never below 28px for body.** Under 28px is unreadable on a projector — the most
  common reason a deck looks unprofessional.
- Max 3 sizes per slide. One display font (titles/quotes) + one body font (scanning).
- Line-height: 1.1–1.2 for headings, 1.5–1.7 for body. For mixed CJK+Latin, lean toward
  the higher end and apply Pangu spacing (see the `chinese-typography` skill).
- **Webfont discipline (esp. CJK):** if the deck pulls a webfont, declare it once in
  `<head>`, list only the weights actually used, and subset CJK with Google Fonts' `&text=`
  (request just the glyphs on the slides). A full CJK family is megabytes; an unsubsetted,
  force-loaded one also hangs or crashes PDF export. Restrict-and-subset keeps the
  self-contained file light and printable.
- **兩軸字體（CJK 與 Latin 是兩個 face，不是一個）。** 雙語簡報用的是兩個字型家族，不是
  一個：一個 Latin face、一個 CJK face，組成一條**有序的** `font-family` 堆疊。
  - **Latin face 在前、CJK face 在後**：`font-family:"Switzer","Noto Sans TC",sans-serif`。
    逐字 fallback 於是讓 Latin 字母用 Latin face、Han 字落到 CJK face。**絕不把 CJK 家族
    排第一**——它的 Latin 字形通常扁平／等寬，會把整份簡報的西文拉低。
  - **挑 CJK face 去配 Latin face**：grotesque／sans 的 Latin 配 `Noto Sans TC` 一類黑體；
    serif／display 的 Latin 配 `Noto Serif TC` 一類明體。字重與調性對齊，讓兩個 face 讀起來
    是同一個聲音。
  - **依簡報主導語言決定載入**：先決定這份簡報是 Latin 主導還是 CJK 主導。Latin 主導、通篇
    無 Han 的簡報**不得**載入 CJK webfont——整套 CJK 家族是 MB 級，未 subset 的強制載入會
    拖慢／當掉 PDF 匯出（見上一條 Webfont discipline）。CJK 主導的簡報則仍要在堆疊裡保留一個
    真正的 Latin face，給內嵌的術語、數字、日期用。
  - 跨兩軸的**尺寸**已在 §13 處理（CJK 標題 −25–30%、混排行高偏高），此處不重複。
  - 這兩條會出錯的點（CJK 排第一、載入卻無 Han 字）由 `check_deck.py` 機械檢查（第 8 條）。

## 4. The vertical-budget method (the anti-overflow technique)

The canvas does **not** scroll. Anything below 1080px is silently cropped — the #1 cause
of broken AI slides. So compute the budget *before* writing the slide, not after.

```
usable_height = 1080 − top_padding − bottom_padding
element_height ≈ font_size × line_height × number_of_lines
(a wrapped bullet counts as 2+ lines; add a 32–64px gap before the next element)
```

Sum every element. If the total exceeds `usable_height`, split — do not raise padding or
shrink type (rule 2). And **never truncate with an ellipsis** to fake a fit: a `…` clip
hides content the slide was supposed to carry. Treat any length limit as advisory and the
box geometry as the real test — if the text doesn't fit, reflow, resize the block, or split
the slide; don't clip.

**Worked example** — a content slide, 120px padding top & bottom:

| Element | Calc | Height |
|---------|------|--------|
| usable height | 1080 − 240 | **840px** |
| heading (68px, lh 1.18, 1 line) | 68 × 1.18 | 80 |
| gap | | 48 |
| 4 bullets (36px, lh 1.55, 1 line each) | (36 × 1.55) × 4 | 224 |
| gaps between bullets (3 × 32) | | 96 |
| **total** | | **448 ≤ 840 ✓** |

448 of 840 — comfortable, ~47% filled, the rest breathing room (aim 40–60% content,
the rest whitespace; >80% filled reads as cramped). Add a fifth and sixth bullet and you
approach the limit — that is the signal to split, not to shrink.

The pixel budget answers "does it fit"; it does not answer "is it one idea". A slide can
clear the budget and still be too dense. So pair this with the **per-role content caps**
in `layouts.md` (Content ≤5 bullets, Big number = 1 stat + 1 caption, Quote ≤36 Han, …):
whichever limit you hit first — pixels or the role's cap — is the one that triggers a
split. The caps make density checkable mechanically, which is why `check_deck.py` enforces
the bullet cap by role.

## 5. Layout & grid

- **Content padding 100–160px from every edge.** Never let text touch the canvas edge.
- Pick one padding (e.g. 120px) and hold it across the deck.
- **Vertical-center by default.** Asymmetric top/bottom baselines: at most a couple of
  slides per deck, for deliberate effect.
- Left-aligned content reads editorial; centered reads ceremonial. Pick per deck, mostly
  one or the other.
- **No right-alignment of content** (titles, body, columns). Right-align is reserved for
  page numbers and numeric table columns.
- **Vary width.** Don't put every slide's content in the same fixed width — it reads
  monotonous. Strong single claims go narrow; timelines, tables, comparisons go wide.
- "Title + 3 columns" is **not** the default content slide. Use it only when the material
  genuinely has three parallel same-class items, and not on consecutive slides.

## 6. Color discipline

- One palette per deck: **1 background, 1 ink (primary text), 1 accent, 1 muted.** Define
  as CSS variables at the top; never improvise a color mid-deck.
- **Dark is not pure black, light is not dead white.** `#1a2332` ink over `#faf9f5` paper
  reads warmer and more designed than `#000` on `#fff`.
- **Dominant color + sharp accent beats a timid even palette.** Commit.
- **The accent appears at one spot per slide** — a kicker, OR a keyword, OR the number,
  OR the rule. Not everywhere. A few slides with *no* accent let it regain weight.
- A rough **60-30-10** split (dominant ground / secondary / accent) keeps proportion.
  **Accent overload** = more than ~2 accent colors spread across 3+ elements on one
  slide; it dilutes every highlight. Cap it.
- Contrast must clear WCAG AA: **≥4.5:1 for body text, ≥3:1 for large text (≥24px).** A
  beautiful palette no one can read fails.

## 7. Motion restraint

- The loudest "made in PowerPoint" signal is six different transitions in one deck. Pick
  **one** family and hold it.
- Duration 140–280ms (exit faster ~150, enter ~220). >350ms feels like video editing.
- Magnitude ceiling: **12px translate or 3% scale.** A full-width slide-in reads as "a
  different document."
- Opacity is always part of it. Ease-out for enter, ease-in for exit; **never `linear`.**
- Default to no transition (a clean cut) unless you have a reason. Respect
  `prefers-reduced-motion`.

## 8. Anti-"AI slop" rules

What makes a deck look auto-generated — avoid all of it:

- Generic fonts as display (Arial, Inter, Roboto, system stack). Use a distinctive
  pairing (see `style-presets.md`); load via Google Fonts / Fontshare.
- Purple-gradient-on-white, generic indigo `#6366f1`, everything-centered hero sections,
  identical card grids on every slide.
- Meaningless decoration: gratuitous glassmorphism, drop shadows without purpose, huge
  border-radius, decorative SVG icons that carry no information, fake chart data.
- The delete test: if removing an element still leaves the slide understandable, delete
  it. Whitespace is not wasted space.
- Images must earn their place (evidence, not filler). Never crop a face at the eyes;
  size by height, give it a caption if it makes a point.

## 9. Density modes

Two modes, chosen in Phase 1 — they change the limits, not the principles:

| | Speaker-led | Reading-first |
|--|------------|---------------|
| For | talks, keynotes, live | handouts, async, reports |
| Bullets/slide | 1–3 | 4–8 (or 4–6 cards) |
| Type | larger, more hierarchy | slightly tighter, still ≥28px |
| Slide count | more | fewer, more self-contained |
| Whitespace | generous | structured but not cramped |

Both obey rules 1–4. "Reading-first" raises the bullet ceiling; it never licenses
shrinking type or overflowing the canvas.

## 10. Deck rhythm (pacing)

A page-role catalog tells you *what* each slide is; rhythm tells you how they *sequence*.
Without deliberate pacing, every slide drifts toward the same medium-density card grid —
the canonical AI-generated look. So assign each slide a rhythm before generating:

- **anchor** — a high-impact moment: cover, a section divider, the one big number, the
  closing line. Maximal, immersive, little text.
- **dense** — a working slide that carries real content (bullets, a comparison, a table).
- **breathing** — a deliberate pause: a single sentence, a quote, a full-bleed image,
  generous whitespace. **Breathing slides forbid multi-card grids** — no 3-card row, no
  4-KPI grid, no 2×2 cards. Use naked text, a divider, or whitespace instead.

Alternate them. A run of `dense` slides with no `breathing` exhausts the audience; a deck
of all `anchor` slides says nothing. Aim for a wave: anchor → a few dense → breathing →
dense → anchor. This deck-level lever is what keeps a long deck from flattening into
sameness, and it survives even when per-slide detail is forgotten mid-generation.

## 11. Depth, emphasis & shadow

**Lift the key information.** A paragraph or bullet where every word is styled the same
reads as a wall of text. Within each line, emphasize (bold or accent) the load-bearing
parts — **numbers, results, before/after contrasts, and the one or two nouns the sentence
turns on**. Do **not** emphasize connectives, common verbs, every noun, or structural
text; highlighting everything highlights nothing. A content slide with substantial prose
and zero emphasized terms is a flag (the linter warns on it).

**Shadow is restraint, not default.** Depth is a tool to be spent, not a coat of paint:

- **At most two elevation tiers** on a slide (e.g. flat ground + one raised card).
- **Shadow budget ≤2–3 shadowed elements per slide.** More reads as Office-2007 clip-art.
- **Single light source:** every shadow's offset points the same direction.
- Opacity bands: resting `0.06–0.12`, raised up to `0.20`. Past `0.20` looks cheap.
- **Never stack visual-weight tools.** For any one container pick *one* of {shadow,
  border, gradient, tint}. Stacking two or more is an instant template look.

## 12. Visual self-review checklist

After generating (and ideally after glancing at the rendered slides), self-check the
things a source linter can't fully see. These thresholds are worth eyeballing per slide:

- **Overflow:** does any text cross its container or the 1080px floor? (rule 4 should
  have prevented it; verify.)
- **Centroid by role:** the visual center of mass shouldn't drift wildly from where the
  role wants it — covers can be off-center by design; content/data slides should sit near
  centered (offset under ~20% of canvas).
- **Emphasis matches intent:** the single most visually prominent element on the slide
  should be the one you *meant* to be primary — not an oversized caption or a stray accent.
- **Accent overload:** ≤2 accent colors, and not smeared across 3+ elements (§6).
- **Contrast:** body ≥4.5:1, large text ≥3:1 (§6).
- **Grid consistency:** cards in a row share spacing and baseline — uneven gaps (>~5%
  variance) or misaligned tops read as sloppy.
- **Rhythm:** did you actually alternate anchor / dense / breathing (§10), or did every
  slide become a card grid?

Fix by splitting or cutting (rule 2), never by shrinking.

## 13. Chinese line-breaking (繁中換行)

For Traditional-Chinese (and CJK) decks, a few line-break rules keep text from looking
wrong. The engine's CSS handles the mechanical ones; you handle the judgment ones.

**Handled by the engine's CSS (already on `.slide`):**

- **避頭尾 (`line-break: strict`)** — punctuation like `。，、！？」）` never falls at the
  *start* of a line, and `「（『` never at the *end*. The browser enforces it; you don't
  have to hand-place breaks to avoid it.
- **標點擠壓 (`text-spacing-trim: normal`)** — adjacent full-width punctuation (`」。`,
  `，「`) is kerned tighter so it doesn't read loose. (Chrome-stable; progressive.)
- **標點懸掛 (`hanging-punctuation: allow-end`)** — end-of-line punctuation hangs past the
  margin so the text edge stays straight. (Safari only; ignored elsewhere, harmless.)

All three are progressive enhancement — unsupported browsers ignore them and nothing
breaks.

**Your job (judgment — a script can't do this):**

- **Break headings at word/phrase boundaries.** When you put a manual `<br>` in a Chinese
  title, break *between* words, never inside one: `讓營運<br>永不中斷` ✓, not
  `讓營運永不中<br>斷` ✗ (which splits the word 中斷). There is no deterministic algorithm
  for this — Chinese segmentation (斷詞) is ambiguous — so read the phrase and break where
  the meaning joins.
- **No stranded glyph.** Don't let a lone character or a lone punctuation mark fall on the
  last line of a block; shorten the text or rebreak.
- **Keep terms and numbers whole.** Don't break inside `TXOne`, `IEC 62443-4-1`, or
  `3,600+`.

**Size CJK headlines down ~25–30% from the Latin scale.** The type scale in §3 is tuned
for Latin. Han characters are denser and carry more visual weight per glyph, so a Chinese
headline at a Latin hero size (176px) reads heavy and overflows width where the equivalent
English would breathe. For a CJK or CJK-majority headline, step the scale down: **hero
~120–140px** (not 176), **section ~80–90** (not 104), body unchanged (it's already ≥28 and
reads fine). The goal is equal *visual* presence, not equal pixels. (The bundled繁中 decks
already do this — e.g. `--t-hero:132px` for the TxOne deck; this just makes it a rule so
every CJK deck is consistent instead of hand-tuned each time.)

**One conflict to avoid (盤古之白 belongs to one layer).** Don't insert literal spaces for
CJK↔Latin spacing in the deck *and* also rely on CSS `text-autospace` — you'd double the
gap. The portable choice: space the text at the character level first (run it through the
`chinese-typography` skill / `normalize.py`), then let these CSS rules handle the rendered
line layout. That keeps `text-autospace` off and the normalizer as the single source of
the spacing.
