#!/usr/bin/env python3
"""Deterministic linter for a single-file HTML slide deck.

The design principles in this skill are mostly judgment calls, but a handful
are mechanical and catch the ugliest, most common failures: text too small to
read on a projector, a slide so dense it breaks "one idea per page", leftover
placeholder/lorem text, generic AI-slop fonts, and a deck that silently overflows
its fixed canvas. A script checks these far more reliably than eyeballing, and
— per the skill's fail-loud principle — it should be run before delivery so you
never hand over a deck with a 14px caption or a `Lorem ipsum` still in it.

Usage:
    python3 check_deck.py deck.html [--strict]

Exit codes: 0 = clean (warnings allowed), 1 = errors found (or --strict + warnings),
2 = file unreadable. Stdlib only.
"""
import sys
import re
import html as _html

# Body text below this (in the 1920x1080 canvas) is unreadable on a projector.
MIN_BODY_PX = 24
# Captions/labels/page numbers are allowed to be smaller, down to this floor.
MIN_CAPTION_PX = 20
# A single slide carrying more than this much visible text usually means
# more than one idea — split it. Tuned to the "~40 words / one idea" rule,
# counting CJK chars individually (a CJK glyph ≈ a word).
MAX_VISIBLE_UNITS = 110
# A text-heavy slide with no emphasized terms reads as a flat wall of text — the
# load-bearing nouns/numbers should be lifted (bold/accent). Below this unit count we
# don't bother (covers, quotes, dividers are meant to be sparse).
MIN_UNITS_FOR_EMPHASIS = 50
EMPHASIS_RE = re.compile(r"<(?:strong|b|em|mark)\b|class=\"[^\"]*(?:accent|highlight|hl|key)",
                         re.IGNORECASE)
# Generic fonts that read as "default template / AI slop" when used for display.
SLOP_FONTS = ("arial", "roboto", "helvetica neue", "times new roman")
# Placeholder text that must never survive into a finished deck.
PLACEHOLDER_RE = re.compile(
    r"lorem ipsum|vivamus|\bTODO\b|\bFIXME\b|\bXXX\b|\[必填\]|\bplaceholder\b"
    r"|Your Title Here|Key Words Here|項目名稱|標題寫在這裡",
    re.IGNORECASE,
)

TAG_RE = re.compile(r"<[^>]+>")
COMMENT_RE = re.compile(r"<!--.*?-->", re.DOTALL)
SCRIPT_STYLE_RE = re.compile(r"<(script|style)\b.*?</\1>", re.IGNORECASE | re.DOTALL)
SLIDE_RE = re.compile(r'<section\b[^>]*class="[^"]*\bslide\b[^"]*"[^>]*>(.*?)</section>',
                      re.IGNORECASE | re.DOTALL)
FONTSIZE_RE = re.compile(r"font-size\s*:\s*(\d+(?:\.\d+)?)px", re.IGNORECASE)
CJK_RE = re.compile(r"[㐀-鿿豈-﫿]")


def visible_text(fragment: str) -> str:
    """Strip tags and decode entities to get on-screen text from an HTML fragment."""
    no_tags = TAG_RE.sub(" ", fragment)
    return _html.unescape(no_tags)


def count_units(text: str) -> int:
    """CJK glyphs count 1 each; runs of Latin/digits count as ~words."""
    cjk = len(CJK_RE.findall(text))
    latin_words = len(re.findall(r"[A-Za-z0-9][A-Za-z0-9'.\-]*", text))
    return cjk + latin_words


def main() -> int:
    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    strict = "--strict" in sys.argv[1:]
    if not args:
        print("usage: check_deck.py deck.html [--strict]", file=sys.stderr)
        return 2
    try:
        with open(args[0], encoding="utf-8") as fh:
            doc = fh.read()
    except OSError as e:
        print(f"cannot read {args[0]}: {e}", file=sys.stderr)
        return 2

    # Comments are authoring scaffold, not delivered content — and this skill's
    # own template documents <section class="slide"> inside a comment, which would
    # otherwise confuse the structural scans. Drop them before linting.
    doc = COMMENT_RE.sub("", doc)

    errors, warns = [], []

    # 1. Fixed 16:9 stage present?
    if "1920px" not in doc or "1080px" not in doc:
        warns.append("no 1920x1080 stage found — is this a fixed-canvas deck?")

    # 2. Font sizes: nothing below the readable floor.
    for m in FONTSIZE_RE.finditer(doc):
        px = float(m.group(1))
        if px < MIN_CAPTION_PX:
            errors.append(f"font-size {px:g}px is below the {MIN_CAPTION_PX}px floor — too small to read")

    # 3. Placeholder / lorem / TODO left in the visible deck.
    body = SCRIPT_STYLE_RE.sub("", doc)
    for m in PLACEHOLDER_RE.finditer(visible_text(body)):
        errors.append(f"placeholder text not replaced: {m.group(0)!r}")

    # 4. Per-slide density — one idea per slide.
    slides = SLIDE_RE.findall(doc)
    if not slides:
        warns.append("no <section class=\"slide\"> blocks found")
    nav_dots_dynamic = "createElement('button')" in doc or 'createElement("button")' in doc
    for n, frag in enumerate(slides, 1):
        units = count_units(visible_text(frag))
        if units > MAX_VISIBLE_UNITS:
            warns.append(f"slide {n}: ~{units} text units (> {MAX_VISIBLE_UNITS}) — likely more than one idea, consider splitting")
        bullets = len(re.findall(r"<li\b", frag, re.IGNORECASE))
        if bullets > 6:
            warns.append(f"slide {n}: {bullets} bullets (> 6) — split into continuation slides, don't cram")
        if units > MIN_UNITS_FOR_EMPHASIS and not EMPHASIS_RE.search(frag):
            warns.append(f"slide {n}: ~{units} text units and nothing emphasized — lift the key "
                         f"nouns/numbers (bold/accent), uniform text reads as a wall")

    # 5. Slide count vs hardcoded totals (page numbers should be derived, not typed).
    hard_total = re.findall(r"/\s*(\d+)\s*<", doc)
    if hard_total and slides:
        bad = {t for t in hard_total if t.isdigit() and int(t) != len(slides)}
        if bad:
            warns.append(f"page-number total(s) {sorted(bad)} != actual slide count {len(slides)} — derive counts from the DOM")

    # 6. Generic slop fonts used for display.
    low = doc.lower()
    for f in SLOP_FONTS:
        if f in low:
            warns.append(f"generic font '{f}' present — prefer a distinctive display/body pairing")

    # 7. No-reflow sanity: overflow:auto/scroll hides a too-tall slide instead of splitting.
    if re.search(r"overflow\s*:\s*(auto|scroll)", low):
        warns.append("overflow:auto/scroll found — the canvas must not scroll; split the slide instead")

    for w in warns:
        print(f"WARN  {w}")
    for e in errors:
        print(f"ERROR {e}")
    print(f"\n{len(slides)} slides · {len(errors)} errors · {len(warns)} warnings")

    if errors or (strict and warns):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
