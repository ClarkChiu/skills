#!/usr/bin/env bash
# Render each .card frame in an index.html to an exact-size PNG via agent-browser.
#
#   render-frames.sh <index.html> [output-dir]
#
# Why isolate + --full + crop (not a plain element screenshot):
#   agent-browser's headless viewport is ~1280×577 and the `viewport` command does
#   not resize the capture surface in this build. A plain `screenshot "#id"` returns
#   the element's exact box dimensions but does NOT paint content below the viewport
#   fold (tall cards come out half-blank). `screenshot --full` paints the whole
#   document but at viewport width. So: isolate one card at the origin, --full to
#   paint it completely, then crop to the card's exact width×height at (0,0).
set -euo pipefail

html="${1:?usage: render-frames.sh <index.html> [output-dir]}"
dir="$(cd "$(dirname "$html")" && pwd)"
url="file://$dir/$(basename "$html")"
outdir="${2:-$dir/output}"
mkdir -p "$outdir"

agent-browser open "$url" >/dev/null
agent-browser wait --load networkidle >/dev/null

# Collect "id width height" for every .card (one per line).
frames="$(printf '%s' \
  '(()=>[...document.querySelectorAll(".card")].map(c=>{const r=c.getBoundingClientRect();return c.id+" "+Math.round(r.width)+" "+Math.round(r.height)}).join("\n"))()' \
  | agent-browser eval --stdin --json \
  | python3 -c 'import sys,json; print(json.load(sys.stdin)["data"]["result"])')"

while read -r id w h; do
  [ -z "${id:-}" ] && continue
  # Isolate this frame at the origin: hide siblings, drop sheet padding, zero body margin.
  printf '%s' \
    "(()=>{document.querySelectorAll('.sheet').forEach(s=>s.style.cssText='padding:0;gap:0;display:block');document.querySelectorAll('.card').forEach(c=>c.style.display=(c.id==='$id')?'flex':'none');document.body.style.margin='0';return '$id';})()" \
    | agent-browser eval --stdin >/dev/null
  agent-browser screenshot --full "$outdir/_raw.png" >/dev/null
  convert "$outdir/_raw.png" -crop "${w}x${h}+0+0" +repage "$outdir/$id.png"
  echo "rendered $outdir/$id.png (${w}x${h})"
done <<< "$frames"

rm -f "$outdir/_raw.png"
agent-browser close >/dev/null
