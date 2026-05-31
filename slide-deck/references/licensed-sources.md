# Commercial-OK external sources (path C)

When the user wants a specific external look or asset, pull **only** from sources whose
license permits commercial use. **Reference these at runtime / fetch into the user's own
project — never commit their files into this skills repo.** Always keep required
attribution.

The default path is still B (our own presets). Use C only when the user asks for a
named external style or a specific asset our presets don't cover.

## Templates / theme CSS

| Source | License | Commercial | Notes |
|--------|---------|-----------|-------|
| reveal.js themes | MIT | ✅ | Liftable theme CSS as a starting point |
| Marp core themes | MIT | ✅ | Clean, minimal |
| Slidev themes | varies (mostly MIT) | check each | Verify the individual theme's license |
| HTML5 UP | CC BY 3.0 | ✅ | Must keep the credit link, or buy removal |
| SlidesCarnival | CC BY 4.0 | ✅ | Attribution required |

## Fonts (all commercial-OK)

| Source | License | How to load |
|--------|---------|-------------|
| Google Fonts | OFL / Apache 2.0 | `<link href="https://fonts.googleapis.com/css2?family=...">` |
| Fontshare | free commercial | `<link href="https://api.fontshare.com/v2/css?f[]=switzer@400,700&display=swap">` |

Avoid bundling font *files* in the repo; link the hosted CSS. Don't use a paid foundry
font without the user's own license.

## Icons (if genuinely needed — most slides need none)

| Source | License |
|--------|---------|
| Lucide | ISC ✅ |
| Heroicons | MIT ✅ |
| Tabler Icons | MIT ✅ |

## Images

| Source | License | Notes |
|--------|---------|-------|
| Unsplash | Unsplash License | ✅ free incl. commercial; no attribution required (courtesy appreciated) |
| Pexels | Pexels License | ✅ free incl. commercial |

Reference images by URL or have the user supply them; don't vendor large binaries into
the repo. An image must earn its place (rule 8 in `principles.md`).

## ❌ Do NOT redistribute (paid / buyer-locked)

These look great but their license is tied to the *purchaser* and forbids redistributing
the files. We can **match their style** with original CSS; we cannot ship their assets.

- Tailwind UI / Tailwind Plus
- Canva Pro templates
- Envato / ThemeForest / GraphicRiver
- Slidesgo & SlidesGo premium, most "premium PPT template" sites
- Any template whose terms say "personal/research use only" or "no redistribution"
  (this is exactly the GordenPPTSkill template situation — see `attribution.md`)

If the user points at one of these: explain we can reproduce the *look* (palette, type,
layout) as an original preset, but cannot copy or redistribute the file.
