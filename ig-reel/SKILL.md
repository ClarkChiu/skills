---
name: ig-reel
description: >-
  Turn the user's OWN video/photo stockpile into Instagram vertical short videos
  (Reels, 9:16, 1080×1920, ≤60s) with an ffmpeg-first, terminal-first pipeline:
  inventory → rough cut → 9:16 reframe (subject-centered crop or blur-pad) →
  subtitles (whisper, optional) → music/ducking → verified export, batchable.
  USE THIS SKILL when the user wants to 「把素材剪成 IG 影片」「做 Reel／限動影片」
  「直式短片」「9:16 影片」「批次出片」, or says "make a reel from my footage",
  "cut my clips into an IG video", "vertical video from my stock". Do NOT use to
  generate videos from nothing (no stock-footage downloading, no AI topic
  invention — the footage and the idea are the user's), to POST or schedule to
  Instagram (no account actions), for social card IMAGES (that's social-card),
  or for presentations (that's slide-deck).
allowed-tools: Read, Write, Edit, Bash, Glob, AskUserQuestion
---

# ig-reel — your stockpile → an Instagram Reel, verified

The one-click generators (MoneyPrinterTurbo, ShortGPT) exist to conjure videos from
nothing — they fetch stock footage and invent topics. This user has the opposite
problem: **plenty of real footage, no pipeline**. So this skill is a disciplined
editing pipeline over the user's own material, driven by ffmpeg commands the user
can read, re-run, and batch.

Output: 1080×1920 (9:16) H.264 MP4, `yuv420p`, `+faststart`, 30fps, aiming ≤60s
(warn past it, don't hard-block). Files go where the user says; scratch work goes
to the system temp area; nothing lands in a git repo.

## Tools (never auto-install anything)

| Tool | Status | Role |
|---|---|---|
| `ffmpeg` / `ffprobe` | **required** | every stage; check `ffmpeg -version` first |
| `auto-editor` | optional | stage-2 silence/dead-air cutting; degrade to manual in/out points |
| `whisper` (openai-whisper) | optional | stage-4 subtitle transcription; degrade to user-supplied SRT or skip |

If an optional tool is missing, say so and offer the degraded path — do **not**
`pip install` / `npm install` on the user's behalf.

## The pipeline (recipes in `references/pipeline.md`)

1. **Inventory** — `ffprobe` the source folder into a table (duration, resolution,
   orientation, audio). Confirm clip selection and narrative order with the user.
   Never guess a clip's content from its filename — extract a frame or ask.
2. **Rough cut** — `auto-editor` if present, else `-ss`/`-to` in/out points.
   Stream-copy (`-c copy`) whenever no filter is needed.
3. **Reframe to 9:16** — per-clip decision, not a blanket rule: vertical source →
   scale; horizontal source → subject-centered **crop** or **blur-pad** (see
   `references/reframe.md`). Never silently crop a subject away.
4. **Subtitles** — whisper → SRT → proofread → burn inside the safe area with the
   readable floor (`references/subtitles-audio.md`). Subtitles are the engagement
   workhorse on IG — default to recommending them.
5. **Audio** — music bed, duck under speech, `loudnorm` before export.
6. **Assemble & verify** — concat, export, then **ffprobe-verify every output**
   (1080×1920, H.264, has audio, duration). Batch mode reports success/failure
   per item and exits non-zero on any failure — never silently skip.

## The non-negotiables

1. **The footage is the user's.** No stock-site downloads, no invented filler
   shots, no AI-generated B-roll — if a shot is missing, say so.
2. **Fail loud.** An output that fails the ffprobe check is not delivered.
   "Batch done" with silent failures is a lie (CLAUDE.md Rule 12).
3. **Safe area + type floor.** Burned text stays inside the Reels UI bands
   (top ~250px / bottom ~420px on the 1920 canvas) and never below ~48px.
4. **Re-encode once.** Cuts stream-copy; the single filter pass does the one
   re-encode. Every extra generation costs quality.
5. **No posting.** Publishing/scheduling is out of scope (same boundary as
   `social-card`); this produces files.

## References

- `references/pipeline.md` — all six stages as runnable ffmpeg recipes + the batch loop + the verify step.
- `references/reframe.md` — the 9:16 decision table, crop vs blur-pad recipes, safe-area numbers.
- `references/subtitles-audio.md` — whisper→SRT→burn styling; music/ducking/loudness recipes.
- `references/attribution.md` — what informed this build (original; no files vendored).

## Boundaries

- vs `social-card`: images vs video — together they are the "圖＋影" pair for IG.
- vs `slide-deck`: a deck is a presentation; this is footage editing.
- Future extension (deliberately not built yet): the HTML-animation→MP4 route
  (huashu-design render chain, pinned in `sources.lock`) for card-style animated
  posts — revisit when the user wants animated text posts rather than footage.
