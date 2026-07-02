# Built-in style presets (path B)

Six original aesthetic directions. Each is a self-contained recipe: a palette, a font
pairing, and a feel. **These are our own CSS, inspired by public-domain design
*movements* (Swiss, editorial, brutalist…) — not copied from any template file.** Reuse
freely; the design styles themselves are not copyrightable.

How to use: **check the selection table first**, then read only the chosen preset's
section; paste its `:root` block over the one in `assets/template.html`, load its fonts,
and follow its layout note. When the user is unsure, render one slide in 3 presets
(1 safe + 1 bold + 1 wildcard, see SKILL.md Phase 2) and let them choose by sight.

## Selection table (best_for / avoid_for)

| preset | best_for | avoid_for |
|---|---|---|
| Swiss | product, finance, anything precise & serious | warm narrative, kids' education |
| Editorial | storytelling, brand, narrative talks | dense data review, spec walkthroughs |
| Brutalist | launches, manifestos, opinionated stands | conservative clients, medical/finance compliance |
| Dark Neon | AI, developer, data, late-night product | print-first decks, bright-room projection |
| Warm Humanist | education, healthcare, community, onboarding | hard technical specs, financial reporting |
| Technical | specs, architecture, internal review | outward marketing, emotional narrative |

`avoid_for` is as load-bearing as `best_for` — a preset that fits the subject but
mismatches the room (projection, compliance, print) is still the wrong pick.

All fonts below are **commercial-OK**: Google Fonts (OFL/Apache) or Fontshare (free
commercial license). Load Google Fonts via `<link>`; Fontshare via its CSS API
(`https://api.fontshare.com/v2/css?f[]=...`). See `licensed-sources.md`.

---

## 1. Swiss — International Typographic

Clarity, grid, restraint. For product, finance, anything that wants to read precise and
serious. The accent is a single Swiss red, used once per slide.

```css
:root{
  --bg:#f4f3ee; --ink:#141414; --muted:#6e6e6e; --accent:#d6201f; --rule:#dad8cf;
  --font-display:"Switzer",sans-serif; --font-body:"Switzer",sans-serif;
  --font-mono:"Space Mono",monospace;
  --t-hero:168px; --t-section:104px; --t-head:64px; --t-body:34px; --t-caption:24px; --t-bignum:300px;
  --pad:150px;
}
```
Fonts: Switzer (Fontshare). Layout: strict left-align, generous margins, a thin top
rule on content slides, page numbers in mono bottom-right. Motion: none or a 150ms cut.

## 2. Editorial — Magazine

Warm, literary, confident. For storytelling, brand, talks with a narrative. Serif
display carries weight; body stays sans for scanning.

```css
:root{
  --bg:#faf7f1; --ink:#241f1a; --muted:#857c6f; --accent:#9c3024; --rule:#e7e0d4;
  --font-display:"Fraunces",Georgia,serif; --font-body:"Hanken Grotesk",sans-serif;
  --font-mono:"IBM Plex Mono",monospace;
  --t-hero:184px; --t-section:108px; --t-head:70px; --t-body:36px; --t-caption:26px; --t-bignum:300px;
  --pad:140px;
}
```
Fonts: Fraunces + Hanken Grotesk (Google). Layout: large serif heads, big quotes, wide
measure for pull-quotes, narrow for claims. Motion: gentle 220ms fade-rise.

## 3. Brutalist — Raw

Loud, structural, high-contrast. For launches, manifestos, anything that should feel
opinionated. Type is heavy; the accent is electric.

```css
:root{
  --bg:#ffffff; --ink:#0a0a0a; --muted:#5a5a5a; --accent:#2b34ff; --rule:#0a0a0a;
  --font-display:"Archivo",sans-serif; --font-body:"Archivo",sans-serif;
  --font-mono:"JetBrains Mono",monospace;
  --t-hero:200px; --t-section:120px; --t-head:76px; --t-body:36px; --t-caption:24px; --t-bignum:340px;
  --pad:110px;
}
```
Fonts: Archivo (use weight 900 for display) + JetBrains Mono (Google). Layout: thick
2–4px black rules, hard left baselines, oversized numbers, minimal color. Motion: snap
cuts only — no easing softness.

## 4. Dark Neon — Tech

Near-black stage, one luminous accent. For AI, data, developer, late-night-product
energy. Restraint keeps it from looking like a gamer skin.

```css
:root{
  --bg:#0d1015; --ink:#eef1f5; --muted:#8a93a3; --accent:#36e0c4; --rule:#1e2530;
  --font-display:"Clash Display",sans-serif; --font-body:"Switzer",sans-serif;
  --font-mono:"Space Mono",monospace;
  --t-hero:176px; --t-section:108px; --t-head:68px; --t-body:36px; --t-caption:24px; --t-bignum:320px;
  --pad:140px;
}
```
Fonts: Clash Display + Switzer (Fontshare). Layout: dark slides, accent on one keyword or
number, subtle hairline rules. Motion: 200ms fade with ≤12px rise. Keep glows subtle —
a faint accent underline beats a neon halo.

## 5. Warm Humanist — Approachable

Soft, friendly, human. For education, healthcare, community, onboarding. Rounded
humanist forms, sage accent, cream ground.

```css
:root{
  --bg:#f6f1e7; --ink:#2c2a26; --muted:#7d7868; --accent:#3f7d5f; --rule:#e4dccb;
  --font-display:"Bricolage Grotesque",sans-serif; --font-body:"Hanken Grotesk",sans-serif;
  --font-mono:"IBM Plex Mono",monospace;
  --t-hero:172px; --t-section:104px; --t-head:66px; --t-body:36px; --t-caption:26px; --t-bignum:300px;
  --pad:150px;
}
```
Fonts: Bricolage Grotesque + Hanken Grotesk (Google). Layout: centered or left, soft
generous whitespace, gentle accent on verbs/keywords. Motion: slow 240ms fade.

## 6. Technical — Documentation

Cool, even, engineered. For specs, architecture, internal review, dashboards-as-slides.
Looks like good docs, not marketing.

```css
:root{
  --bg:#fbfcfd; --ink:#1b2530; --muted:#647084; --accent:#2563c8; --rule:#e3e8ef;
  --font-display:"IBM Plex Sans",sans-serif; --font-body:"IBM Plex Sans",sans-serif;
  --font-mono:"IBM Plex Mono",monospace;
  --t-hero:160px; --t-section:100px; --t-head:60px; --t-body:34px; --t-caption:24px; --t-bignum:280px;
  --pad:140px;
}
```
Fonts: IBM Plex Sans + Mono (Google, OFL). Layout: tidy left-align, mono for labels/code,
restrained blue accent, clean tables. Motion: none.

---

## Picking & blending

- Match the preset to the **subject's temperature**: finance→Swiss/Technical,
  brand/story→Editorial/Humanist, launch→Brutalist, AI/dev→Dark Neon/Technical.
- Don't default every deck to the same one — variety is part of looking custom.
- Blending is fine: take Editorial's serif display over Swiss's grid, for instance. Keep
  it to one coherent result — change variables, not the principles.
- For CJK decks, pair with a Noto/source CJK face and apply Pangu spacing (the
  `chinese-typography` skill). 雙語簡報用**兩軸字體**：把 CJK face **接在 Latin face 之後**
  組成有序堆疊（`"<Latin>","Noto Sans TC",sans-serif`），**不可讓 CJK 家族排第一**（它的
  Latin 字形會拉低整份簡報的西文）。依簡報主導語言決定要不要載入 CJK webfont——純 Latin、
  無 Han 的簡報不載。完整規則見 `principles.md` §3「兩軸字體」；CJK 標題尺寸見 §13。
