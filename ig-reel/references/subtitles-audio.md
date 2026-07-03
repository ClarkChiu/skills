# Subtitles & audio recipes

## Subtitles

### 1. Transcribe (whisper, optional tool)

```bash
whisper input.mp4 --model small --language zh --output_format srt --output_dir "$WORK"
```

No whisper → ask for an SRT or offer to skip. **Proofread before burning** — ASR
mangles names and jargon, and whisper's `zh` output is **often Simplified Chinese**:
check for 簡體 and convert with OpenCC `s2twp` (the `chinese-typography` skill's
engine) before burning. A wrong burned-in subtitle is permanent.

### 2. Burn (inside the safe area, above the type floor)

```bash
ffmpeg -y -i in.mp4 -vf "subtitles=subs.srt:force_style='FontName=Noto Sans TC,\
FontSize=14,Outline=2,Shadow=0,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,MarginV=70'" \
  -c:v libx264 -crf 20 -pix_fmt yuv420p -c:a copy out.mp4
```

Why these numbers: libass styles are in script units (default `PlayResY=288`), so on
the 1920-tall canvas —

- `FontSize=14` ≈ 93px rendered (floor: never below `FontSize=8` ≈ 53px).
- `MarginV=70` ≈ 467px from the bottom — clears the ~420px Reels bottom UI band.

White text + 2px black outline stays readable on any footage. Keep lines ≤ ~16 Han
characters; whisper's segmenting is usually fine after proofreading.

**After burning, extract one frame and look at it** (`-ss <t> -frames:v 1 check.jpg`) —
if the named font is missing, libass silently substitutes (or renders tofu boxes on a
machine with no CJK font at all), and the ffprobe verify step cannot catch that.

## Audio

### Music bed under speech (simple mix)

```bash
ffmpeg -y -i video.mp4 -i music.mp3 -filter_complex \
"[1:a]volume=0.25[m];[0:a][m]amix=inputs=2:duration=first[a]" \
-map 0:v -map "[a]" -c:v copy -c:a aac -b:a 192k out.mp4
```

### Ducking (music dips automatically when the voice speaks)

```bash
ffmpeg -y -i video.mp4 -i music.mp3 -filter_complex \
"[1:a][0:a]sidechaincompress=threshold=0.05:ratio=8:attack=5:release=300[duck];\
[0:a][duck]amix=inputs=2:duration=first[a]" \
-map 0:v -map "[a]" -c:v copy -c:a aac -b:a 192k out.mp4
```

(`sidechaincompress` order: `[music][voice]` — the voice is the trigger.)

### Loudness normalize (last audio step before export)

```bash
-af loudnorm=I=-16:TP=-1.5:LRA=11
```

`-af` **cannot** be combined with `-filter_complex` on the same stream — when the
pipeline runs as one `-filter_complex` pass (pipeline.md's "chain into one pass"),
append loudnorm to the chain tail instead:

```
…amix=inputs=2:duration=first[mix];[mix]loudnorm=I=-16:TP=-1.5:LRA=11[a]
```

Single-pass is fine for short reels; it prevents the "one reel blasts, the next
whispers" problem across a batch.

### Music licensing

Only use tracks the user has rights to. IG mutes or takes down videos over
unlicensed audio — warn if the user hands over a commercial track for an
account that isn't using IG's own music library at post time.
