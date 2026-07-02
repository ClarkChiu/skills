# Reframe to 9:16 — decision first, filter second

The reframe choice is **per clip**, decided by looking at the content (pull a frame)
or asking — never a blanket rule, and never a silent center-crop that beheads the
subject.

| Source | Content | Recipe |
|---|---|---|
| Vertical (H>W) | any | **scale** (A) |
| Horizontal | one clear subject (person, product) | **subject-centered crop** (B) |
| Horizontal | can't crop: landscape, group, on-screen text | **blur-pad** (C) |

## A. Vertical source → scale

```bash
ffmpeg -y -i in.mp4 -vf "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920" \
  -c:v libx264 -crf 20 -pix_fmt yuv420p -c:a copy out.mp4
```

## B. Horizontal → subject-centered crop

Crop a 9:16 window at full source height, then scale. Center by default; shift the
window when the subject is off-center (`x` is the crop's left edge):

```bash
# centered
ffmpeg -y -i in.mp4 -vf "crop=ih*9/16:ih:(iw-ih*9/16)/2:0,scale=1080:1920" \
  -c:v libx264 -crf 20 -pix_fmt yuv420p -c:a copy out.mp4
# subject on the left third: x = (iw-ih*9/16)*0.25   (0 = far left, *0.5 = center)
```

Check a frame after cropping (`-frames:v 1`) before committing the full render.

## C. Horizontal → blur-pad (full frame kept, blurred self as background)

```bash
ffmpeg -y -i in.mp4 -filter_complex \
"[0:v]split=2[bg][fg];\
[bg]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=20:2[b];\
[fg]scale=1080:-2[f];\
[b][f]overlay=(W-w)/2:(H-h)/2" \
  -c:v libx264 -crf 20 -pix_fmt yuv420p -c:a copy out.mp4
```

## Safe areas (1080×1920 canvas)

Same bands social-card uses for 9:16 stories/reels (platform UI covers them):

- **Top ~250px**: username, camera icon.
- **Bottom ~420px**: caption, actions, music tag.

Burned subtitles, titles, and CTAs stay inside the central band
(y ≈ 250–1500). The subtitle `MarginV` recipe in `subtitles-audio.md` already
clears the bottom band — don't lower it.
