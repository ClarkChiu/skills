# Principles — what makes a card read as designed, not templated

These drive every layout and copy decision. Internalize them; the QA gate
(`scripts/qa-rules.js`) enforces the load-bearing ones automatically.

## 1. One idea per card

A card carries one concept. If you find yourself writing a second heading or a third
bullet cluster, that is a second card. A 7-card carousel that each land one point beats
a 4-card carousel where every card is crowded.

**Why:** social cards are read at thumb-speed on a phone. A card with one clear idea is
grasped in the half-second before the thumb moves; a dense card is skipped.

## 2. Shorten copy, never shrink type (the highest rule)

When content overflows a fixed frame, the fix is to **cut words or split the card** —
never to drop the font below the readable floor or crush line-height to cram. There is
no "make it fit" by shrinking.

**Why:** the frame is fixed and the floor is the floor. Shrinking to fit produces the
exact cramped, unreadable look this skill exists to prevent. `qa-rules.js` fails any
card with `scrollHeight > clientHeight` (R1) or body type below the floor (R3), and the
fix is always copy/structure, never font size.

- Readable floor: **body text ≥ 28px** on a 1080-wide canvas (≈ 32px is safer).
- Title hard cap: **≤ 4 display lines** per card; if it needs more, the title is too long.

## 3. Respect the safe area

IG Stories/Reels (9:16) reserve a top band (~250px, profile/close UI) and a bottom band
(~340px, caption/CTA/Reels controls). Titles, body, and CTAs must sit in the central
safe band. Feed ratios (4:5, 1:1) need only breathing margins.

**Why:** anything in the UI bands is covered at view time — the viewer never sees it.

## 4. CJK + Latin line-height and spacing

- Big display titles: line-height **1.08–1.22**.
- Body / lead / caption: line-height **1.35–1.55** so Chinese characters breathe.
- Do **not** use negative letter-spacing on Chinese body text.
- Mixed CJK + Latin follows 盤古之白 (a space between Han and Latin/digits) — if the
  user wants the copy normalized, hand it to `chinese-typography` first; this skill
  lays out, it does not rewrite text.

**Why:** Chinese glyphs are dense; tight leading that looks fine in Latin turns a CJK
paragraph into a gray wall.

## 5. Contrast and text-over-image

- Strong contrast for all text. Never place long text over a busy photo.
- If text must sit over an image, use a solid ink/paper block or a high-contrast strip
  behind it — not a soft blur blob.

**Why:** a phone screen in daylight loses every low-contrast edge; the blur-blob trick
reads as low-effort and still fails legibility.

## 6. Cover earns the tap, content pays it off

The cover card carries the hook (a sharp title + one strong visual + an optional 3–5
point strip). Content cards each pay off one promise from the cover. A hollow center on
the cover (empty middle) is a fail — enlarge the title, the image, or add a bottom
strip.
