# Pipeline recipes — six stages, all runnable

Every command here targets ffmpeg ≥4.4. `$SRC` = the user's footage folder,
`$WORK` = scratch dir (system temp), `$OUT` = the user's delivery dir.

## 1. Inventory

```bash
for f in "$SRC"/*.{mp4,mov,MP4,MOV} ; do [ -e "$f" ] || continue
  ffprobe -v error -select_streams v:0 \
    -show_entries stream=width,height,avg_frame_rate:format=duration \
    -of default=noprint_wrappers=1 "$f" | tr '\n' ' ' ; echo "  <- $f"
done
```

Build a table: file / duration / WxH / orientation (H>W = vertical) / has-audio
(`-select_streams a` returns a stream or not). Confirm the clip list and order with
the user. To see what a clip actually contains, pull a frame — never trust filenames:

```bash
ffmpeg -y -ss 3 -i clip.mp4 -frames:v 1 "$WORK/peek.jpg"
```

## 2. Rough cut

With `auto-editor` (if installed) — strips silence/dead air, keeps 0.2s margins:

```bash
auto-editor clip.mp4 --margin 0.2s --no-open -o "$WORK/cut-01.mp4"
```

Without — manual in/out. Fast keyframe cut (stream copy, cut lands on the nearest
keyframe, fine for rough trims):

```bash
ffmpeg -y -ss 00:00:12 -to 00:00:31 -i clip.mp4 -c copy "$WORK/cut-01.mp4"
```

Frame-accurate cut (re-encodes — use only when the extra precision matters, and
remember rule 4: this spends the one re-encode budget early):

```bash
ffmpeg -y -i clip.mp4 -ss 00:00:12.40 -to 00:00:31.15 -c:v libx264 -crf 18 -c:a aac "$WORK/cut-01.mp4"
```

## 3–5. Reframe / subtitles / audio

See `reframe.md` and `subtitles-audio.md`. Chain the filters into **one** pass when
possible (reframe + burn + audio mix in a single `-filter_complex`) so the whole
pipeline re-encodes exactly once.

## 6a. Assemble (concat)

Segments must share codec/resolution/fps for copy-concat:

```bash
printf "file '%s'\n" "$WORK"/seg-*.mp4 > "$WORK/list.txt"
ffmpeg -y -f concat -safe 0 -i "$WORK/list.txt" -c copy "$WORK/joined.mp4"
```

Mismatched segments → re-encode concat with the export parameters below instead.

## 6b. Export parameters (the canonical tail)

```bash
-c:v libx264 -profile:v high -crf 20 -pix_fmt yuv420p -r 30 \
-c:a aac -b:a 192k -movflags +faststart
```

Target ≤60s for a Reel — warn past 60s (and past 90s repeat the warning louder),
but the user decides.

## 6c. Verify — every output, no exceptions

```bash
ffprobe -v error -select_streams v:0 \
  -show_entries stream=width,height,codec_name,pix_fmt -of csv=p=0 out.mp4
# expected: h264,1080,1920,yuv420p   (ffprobe prints fields in stream order, codec first)
ffprobe -v error -select_streams a:0 -show_entries stream=codec_name -of csv=p=0 out.mp4
# expected: aac   (empty output = NO AUDIO — fail)
ffprobe -v error -show_entries format=duration -of csv=p=0 out.mp4
# sanity-check against the planned length
```

An output failing any line is **not delivered** — fix and re-run.

## Batch

Manifest = one TSV line per reel: `source-clips<TAB>in-out points<TAB>srt<TAB>music<TAB>outname`.
Loop it; **collect failures instead of stopping or hiding them**:

```bash
fail=0
while IFS=$'\t' read -r srcs cuts srt music out; do
  build_one "$srcs" "$cuts" "$srt" "$music" "$OUT/$out" || { echo "FAIL: $out"; fail=1; }
done < manifest.tsv
exit $fail
```

End-of-batch report: N succeeded / M failed with reasons. "Batch done" with silent
failures is a lie (Rule 12).
