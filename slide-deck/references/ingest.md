# Ingesting the user's own PowerPoint / template (path D)

When the user supplies their own deck or brand template, extract its **content** and
**style**, then regenerate as an HTML deck. The user owns that file's license; we use it
for them and **do not redistribute it** into this repo.

## From a .pptx

Use the optional helper (needs `python-pptx`):

```bash
python3 <skill>/scripts/extract_pptx.py theirs.pptx > extracted.json
```

It emits per-slide: title, body text, bullet structure, speaker notes, image count, and
the dominant theme colors/fonts it can read. If `python-pptx` is absent, the script says
so (fail loud) — either `pip install python-pptx` or have the user paste the outline.

Then:
1. **Content** → feed the extracted outline into Phase 1/3 of the main workflow. Preserve
   their order, text, and per-slide notes (carry notes as HTML comments).
2. **Style** → read the extracted palette and fonts. Build a matching preset: map their
   primary/accent into `--ink`/`--accent`, pick the nearest commercial-OK font (see
   `licensed-sources.md`) if their font isn't web-available. Don't copy their slide
   master; reproduce the *look* with our engine.
3. Generate, lint (`check_deck.py`), deliver — same as a new deck.

## From an HTML deck or a screenshot

- HTML: read it directly, extract palette/type from its CSS, apply the principles, and
  rebuild on our engine.
- Screenshot/image of a brand slide: sample the colors and identify the type style by
  eye, then express it as an original preset. You're matching a *style*, not copying a
  file — which is fine.

## Boundaries

- Keep their file out of the repo and out of any commit.
- If their template is a paid/locked asset, you can still match its style for them, but
  say plainly that the original file can't be redistributed.
- If brand guidelines specify exact hex/fonts, honor them exactly — that's the one case
  where you don't substitute your own taste.
