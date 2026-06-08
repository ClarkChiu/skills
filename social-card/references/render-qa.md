# Render + QA — the agent-browser pipeline

No playwright, no chromium install. Rendering and QA both run through **agent-browser**,
which the host already has. The render method is pinned: a per-frame element-selector
screenshot captures each card at its **exact CSS pixel size** (verified: a 1080×1350
`.card` exports as exactly 1080×1350).

## Task folder

```text
social-card-<slug>/
  index.html          # all card frames in one file
  assets/             # user screenshots / generated visuals
  output/             # exported PNGs
```

`index.html` holds every frame as a fixed-dimension section with a stable id:

```html
<main class="sheet">
  <section class="card ig-45" id="ig45-01">…</section>
  <section class="card ig-45" id="ig45-02">…</section>
  <section class="card li-191" id="li191-cover">…</section>
</main>
```

## Render — one exact-size PNG per frame

Use the bundled helper; it renders every `.card` in the HTML to an exact-size PNG:

```bash
bash <skill>/scripts/render-frames.sh social-card-<slug>/index.html social-card-<slug>/output
# → output/ig45-01-cover.png (1080x1350), output/ig45-02-point.png (1080x1350), …
```

**The frame's `id` becomes the output filename**, so give each `.card` a descriptive id
by role: `id="ig45-01-cover"`, `id="ig45-02-point"`, `id="li191-cover"`. The helper
reads every `.card`, so the ids you choose are exactly the PNG names you get.

**Why a helper, not a plain `screenshot "#id"`** (verified the hard way, 2026-06-08):
agent-browser's headless viewport is ~1280×577 and the `viewport` command does **not**
resize the capture surface in this build. A plain `screenshot "#id"` returns the
element's exact box *dimensions* but does **not** paint content below the viewport fold —
a tall card (e.g. 1080×1350) comes out cream on top and blank/grey below. `screenshot
--full` paints the whole document but at viewport width. So the helper does, per frame:

1. **isolate** the card at the origin — hide siblings (`display:none`), zero the
   `.sheet` padding/gap, `body { margin:0 }` — via `agent-browser eval`;
2. **`screenshot --full`** so the whole card is painted (full document height);
3. **`convert _raw.png -crop {w}x{h}+0+0 +repage out/<id>.png`** to the card's exact
   width×height (read live from `getBoundingClientRect`).

Requires `convert` (ImageMagick). If a card uses a WebGL/canvas background, add a short
wait before its screenshot so the canvas has painted (edit the helper, or render that
card separately with `agent-browser wait 700`).

Verify dimensions after export (each must match its spec in `platform-specs.md`):

```bash
python3 - <<'PY'
import struct, glob
for p in sorted(glob.glob("social-card-*/output/*.png")):
    with open(p,'rb') as f:
        f.read(16); w,h=struct.unpack('>II', f.read(8))
    print(f"{p}: {w}x{h}")
PY
```

## QA — DOM checks on the rendered page

With the page still open (run QA before `close`, or re-open), pipe the rule script into
`eval`:

```bash
agent-browser open "file://$(pwd)/index.html"
agent-browser wait --load networkidle
agent-browser eval --stdin < <skill>/scripts/qa-rules.js
agent-browser close
```

The script returns a JSON array of findings; **empty array = pass**. Each finding is
`{card, rule, …, fix}`:

| rule | meaning | fix |
|---|---|---|
| `R1-overflow` | content taller than the frame | split the card or cut copy — **never shrink the font** |
| `R3-font-floor` | body type below 28px | cut copy or split; raise the font back to the floor |
| `title-cap` | title > 4 display lines | shorten the title |
| `safe-area` | text enters the Stories/Reels UI band | pull content into the central safe band |

## The loop

Render → QA → if findings, **fix by cutting/splitting copy or adjusting layout, never by
shrinking type** → re-render → repeat until QA returns `[]`. Only then are the PNGs in
`output/` final. Surface the QA result to the user; do not claim the set is done while
findings remain (CLAUDE.md Rule 12).
