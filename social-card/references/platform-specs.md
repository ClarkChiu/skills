# Platform specs — IG / LinkedIn / FB

Export at the exact pixel sizes below (already high-res; the user can downsample). Each
ratio maps to a CSS class with a fixed `width`/`height` and `box-sizing: border-box;
overflow: hidden`. Frame IDs drive the per-frame screenshot (`agent-browser screenshot
"#<id>" output/<name>.png`).

## The ratio table

| Platform / ratio | CSS class | Pixels | Use | Frame ID prefix |
|---|---|---|---|---|
| **IG portrait 4:5** ⭐ | `.ig-45` | 1080×1350 | Primary: carousel + feed | `ig45-` |
| IG square 1:1 | `.ig-11` | 1080×1080 | Single post / cover | `ig11-` |
| IG story/reel 9:16 | `.ig-916` | 1080×1920 | Stories / Reels cover | `ig916-` |
| LinkedIn square 1:1 | `.li-11` | 1080×1080 | Document carousel / feed | `li11-` |
| LinkedIn landscape 1.91:1 | `.li-191` | 1200×627 | Link / share card | `li191-` |
| FB single 1.91:1 🔻 | `.fb-191` | 1200×630 | One link image only — reuses the LinkedIn landscape geometry; **do not build a full FB set** | `fb191-` |

IG 4:5 is the default. FB is deliberately a single card, not a carousel — FB feed does
not reward card carousels, so one 1.91:1 link image is enough.

## Safe areas

Keep all titles, body, and key objects inside the safe area; platform UI or cropping
eats anything outside it.

| Frame | Side | Top | Bottom | Note |
|---|---|---|---|---|
| `.ig-45`, `.ig-11` | 64–96px | 64–96px | 64–96px | Feed crops are minimal; margins are for breathing room |
| `.ig-916` | 64–96px | **~250px** | **~340px** | Top band = profile/close UI; bottom band = caption/CTA/Reels controls. Body must sit in the central safe band |
| `.li-11` | 80–112px | 80–112px | 80–112px | Document-carousel pages read close-up; keep generous margins |
| `.li-191`, `.fb-191` | 72–96px | 64–88px | 64–88px | Keep the title in a clear band, center-left; avoid a hollow middle |

## Fixed-dimension CSS (canonical)

```css
.card { box-sizing: border-box; overflow: hidden; position: relative; }
.ig-45  { width: 1080px; height: 1350px; }
.ig-11  { width: 1080px; height: 1080px; }
.ig-916 { width: 1080px; height: 1920px; }
.li-11  { width: 1080px; height: 1080px; }
.li-191 { width: 1200px; height: 627px;  }
.fb-191 { width: 1200px; height: 630px;  }
```

## Naming and output

```text
social-card-<slug>/output/
  ig45-01-cover.png
  ig45-02-point.png
  ig45-03-checklist.png
  ...
  li191-cover.png
  fb191-cover.png
```

Cover first, then content pages in reading order, then any single cards. Use a
`-cover` / `-point` / `-list` / `-quote` / `-summary` suffix matching the layout role.
