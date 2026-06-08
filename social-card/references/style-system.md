# Style system — Swiss and Editorial, with original palettes

Two style families, three original palettes. Everything here is original — no third-party
template, font file, or background asset is shipped or required. Palettes are driven by
CSS variables so a card set switches theme by changing the variable block, not the markup.

## Choosing a family

| Pick **Swiss** when… | Pick **Editorial** when… |
|---|---|
| Technical, product, data, how-to, dev/infra content | Essay, story, opinion, travel, lifestyle, brand voice |
| The content is structured (lists, comparisons, steps) | The content is narrative and wants atmosphere |
| You want maximum clarity and authority | You want warmth, texture, and a magazine feel |

Default to **Swiss** for this user's typical technical/PM/writing content. Use Editorial
when the piece is a personal essay or wants a softer, magazine register.

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
```

Add a fourth on demand, but keep the set small — three well-tuned palettes beat ten
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
