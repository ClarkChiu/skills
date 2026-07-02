# Style system — Swiss, Editorial, and Sweet, with original palettes

Three style families, five original palettes. Everything here is original — no third-party
template, font file, or background asset is shipped or required. Palettes are driven by
CSS variables so a card set switches theme by changing the variable block, not the markup.

## Choosing a family

| Pick **Swiss** when… | Pick **Editorial** when… | Pick **Sweet** when… |
|---|---|---|
| Technical, product, data, how-to, dev/infra content | Essay, story, opinion, brand voice | Travel, food, lifestyle, personal shares, light topics |
| The content is structured (lists, comparisons, steps) | The content is narrative and wants atmosphere | The content wants to feel friendly, soft, handmade |
| You want maximum clarity and authority | You want warmth, texture, and a magazine feel | You want playfulness without losing the discipline |

Default to **Swiss** for this user's typical technical/PM/writing content. Use Editorial
when the piece is a personal essay or wants a softer, magazine register. Use Sweet for
travel/food/lifestyle/personal posts (e.g. travel notes) — it never takes the default
away from technical content.

## Swiss family — grid, hairlines, type hierarchy

- **Grid:** a strict column grid (8 columns on 4:5, 6 on square). Align everything to it.
- **Type:** one geometric/grotesque sans across the set. Hierarchy by **size and weight**,
  not by color. Display titles heavy (700–800); body regular (400–500).
- **Rules:** hairline dividers (1–2px), not boxes. Generous whitespace.
- **No shadow, straight corners.** Flatness is the point.
- **Accent:** one accent color used sparingly (a number, a keyword, a rule), never as fill.

## Editorial family — magazine, asymmetry, texture

- **Asymmetry:** off-center titles, an editorial sidebar column, intentional negative space.
- **Type:** a display serif (or a high-contrast sans) for titles + a clean sans for body.
  Allow a drop-cap or an oversized issue number.
- **Texture:** a subtle paper grain or a single ink-wash accent — kept low-opacity on
  content pages, stronger on covers, dividers, and pull-quotes.
- **Rules:** thin accent rules and a small radius / subtle shadow are allowed — but avoid
  SaaS marketing-card styling (no big rounded gradient cards).

## Sweet family — macaron pastels, sticker outlines, restrained doodles

The sweet register without the kitsch: rounded and warm, but the skill's discipline
(one idea per card, type floor, whitespace) stays fully in force.

- **Shape:** big radius (24–32px on panels — clearly rounder than Editorial's subtle
  radius). Sticker-style elements get a thick white outline (`border: 6px solid #fff`)
  and a soft drop for the cut-out feel.
- **Photos:** the polaroid frame is this family's variant of screenshot/photo treatment
  (white padding, slight rotation ≤2°) — object-fit rules in
  `screenshot-treatment.md` still apply inside the frame.
- **Type:** rounded sans stack (`ui-rounded`, Hiragino Maru Gothic fallbacks) — same
  type scale and floors as the other families; do NOT invent a new scale.
- **Doodles:** hand-drawn-feel hearts / stars / wavy lines as original inline SVG or
  CSS, colored `--deco`, low visual weight (small, ~80% opacity), placed in whitespace.
  **At most 3 decorations per card (每卡裝飾最多 3 個), and a decoration MUST NOT
  overlap text.** More sweetness comes from color and shape, not from more stickers.

### Family × page-role fit

| Page role | Swiss | Editorial | Sweet |
|---|---|---|---|
| cover | ✓ | ✓ | ✓ (decorations may go up to the cap of 3) |
| points | ✓ | ✓ | ✓ |
| checklist | ✓ | ✓ | ✓ (check marks may be hand-drawn style) |
| comparison | ✓ | ✓ | △ (use rounded panels instead of table rules) |
| quote | ✓ | ✓ | ✓ |
| stat | ✓ | △ | △ (big number in `--accent`; no doodles on stat cards) |
| summary/CTA | ✓ | ✓ | ✓ |

## Original palettes (CSS variables)

Each palette defines `--ink` (primary text), `--paper` (background), `--accent`, and
`--muted` (secondary text/rules). Contrast of ink-on-paper meets a comfortable margin.

```css
/* paper-ink — default Swiss; calm, authoritative */
.theme-paper-ink   { --paper:#f5f2ea; --ink:#1a1a1a; --muted:#6b6862; --accent:#c4452f; }

/* mono-signal — high-contrast mono with one signal color; best for data/dev */
.theme-mono-signal { --paper:#ffffff; --ink:#111418; --muted:#5b6470; --accent:#1f6feb; }

/* dusk-editorial — warm Editorial; essays, story, lifestyle */
.theme-dusk        { --paper:#1d1a26; --ink:#f3ece2; --muted:#a99fb3; --accent:#e0a458; }

/* macaron — Sweet; pastel strawberry — travel, lifestyle */
.theme-macaron     { --paper:#fff5f7; --ink:#46323d; --muted:#a38a95; --accent:#e0507e; --deco:#8fd0c5; }

/* cream-mint — Sweet; creamy mint — food, fresh topics */
.theme-mint        { --paper:#f4faf5; --ink:#2e4137; --muted:#7c988a; --accent:#e8933a; --deco:#f2b8c6; }
```

Sweet palettes add one extra variable, `--deco`, used only for decorations (doodles,
sticker accents) — never for text.

Add more on demand, but keep the set small — a few well-tuned palettes beat ten
noisy ones. A card set uses **one** palette throughout unless the cover deliberately
inverts (dark cover, light content) for emphasis.

## Type scale (reference, 1080-wide canvas)

| Token | Size | Use |
|---|---|---|
| `--h-hero` | 120–160px | Cover display title |
| `--h-xl` | 84–108px | Content-card title |
| `--lead` | 44–56px | Lead sentence under a title |
| `--body` | 32–40px | Body text (floor: 28px) |
| `--caption` | 26–30px | Captions, meta, labels |

Scale up proportionally for 9:16 (taller canvas), down slightly for 1.91:1 (shorter).
