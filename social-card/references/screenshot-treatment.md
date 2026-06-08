# Screenshot treatment

How to place a user-supplied screenshot or photo into a card without wrecking it. The
goal is clean evidence, not a redrawn mockup.

## object-fit by content type (the core rule)

| Content | `object-fit` | Why |
|---|---|---|
| UI screenshot, app window | `contain` | cropping hides controls/edges and misleads |
| Dense text, code, tables | `contain` | every line must stay readable |
| A photographed object, scene, portrait | `cover` (when crop is safe) | fills the frame; minor edge loss is fine |
| A chart/diagram | `contain` | axes and labels must survive |

Set `object-position` deliberately: `top` for long UI where the top matters, `center`
for objects, `35%–45%` vertical for portraits. Never pin an image to the canvas edge
unless the design intends a full bleed.

## Framing

- Build a clean target-ratio frame and place the screenshot inside with safe padding.
- Background behind the frame: plain white, refined grey, or paper. **Do not** add a
  page-wide grid/dot background unless the user explicitly wants a technical-blueprint look.
- If the capture is a floating window/card over unrelated UI, crop to the foreground
  subject before placing it.
- Preserve readable text. Do **not** redraw the screenshot unless the user asked for a redesign.
- Do **not** add perspective, skew, rotation, or mockup tilt unless the user explicitly
  asks for a scene mockup.

## Per-style finish

- **Swiss:** straight corners, no shadow by default; add a hairline only if the
  screenshot's own edge disappears into the background.
- **Editorial:** a small radius or a subtle shadow is allowed, but avoid SaaS
  marketing-card styling (no heavy rounded gradient cards).

## Sizing on a card

- On a Screenshot-frame layout, give the screenshot **55–70%** of the canvas.
- If it feels cramped, **reduce the surrounding copy**, do not shrink the screenshot.
- Keep text and the image out of each other's safe padding.

## Generated or missing visuals

If a visual is missing and the user wants one generated: generate only the **raw visual
asset** (keep text out of it), match the card's style and palette, save it into
`assets/`, and place it in the HTML. Generate only the 1–2 cards that need it — this
skill lays out and renders; it is not an image-generation tool.
