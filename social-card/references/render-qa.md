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

```bash
cd social-card-<slug>
agent-browser open "file://$(pwd)/index.html"
agent-browser wait --load networkidle          # let fonts/images settle
# one screenshot per frame, by element id → exact pixel size:
agent-browser screenshot "#ig45-01" output/ig45-01-cover.png
agent-browser screenshot "#ig45-02" output/ig45-02-point.png
agent-browser screenshot "#li191-cover" output/li191-cover.png
agent-browser close
```

- The **selector** form `screenshot "#<id>" <path>` is what guarantees exact dimensions —
  do not rely on viewport sizing.
- If a card uses a WebGL/canvas background, add `agent-browser wait 700` before its
  screenshot so the canvas has painted.
- Verify dimensions after export (a frame must match its spec in `platform-specs.md`):

```bash
python3 - <<'PY'
import struct, glob
for p in sorted(glob.glob("output/*.png")):
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
