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
    python3 check_deck.py --selftest      # self-check the font-axis rules (no file)

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
SLIDE_RE = re.compile(r'<section\b([^>]*class="[^"]*\bslide\b[^"]*"[^>]*)>(.*?)</section>',
                      re.IGNORECASE | re.DOTALL)
DATALABEL_RE = re.compile(r'data-label="([^"]*)"', re.IGNORECASE)
# Roles whose one-line-bullet density is deterministically cappable (layouts.md). A slide
# tagged with one of these via data-label gets its bullet count checked against the cap.
ROLE_CAPS = {"content": 5, "agenda": 6}
FONTSIZE_RE = re.compile(r"font-size\s*:\s*(\d+(?:\.\d+)?)px", re.IGNORECASE)
CJK_RE = re.compile(r"[㐀-鿿豈-﫿]")


# CJK font families (lowercased). Used two ways: to flag a CJK-first font stack
# (most CJK faces have weak Latin glyphs, so a CJK family before the Latin one drags
# the deck's Latin down), and to flag a CJK webfont loaded into a deck with no Han.
CJK_FAMILIES = (
    "noto sans tc", "noto serif tc", "noto sans sc", "noto serif sc",
    "noto sans jp", "noto serif jp", "noto sans hk", "source han",
    "pingfang", "microsoft yahei", "hiragino", "heiti", "songti",
    "ms mincho", "ms gothic", "simsun", "simhei",
)
# Generic CSS font keywords — never a "real" (Latin) named family.
GENERIC_FAMILIES = (
    "sans-serif", "serif", "monospace", "system-ui", "ui-sans-serif",
    "ui-serif", "ui-monospace", "cursive", "fantasy", "inherit", "initial",
)
# Any CSS declaration whose value is a font stack: standard font-family, OR this
# skill's preset custom properties (--font-display / --font-body / --font-mono),
# where the actual family names live (font-family itself usually holds var(...)).
FONTSTACK_RE = re.compile(r"(?:font-family|--font[\w-]*)\s*:\s*([^;}{]+)", re.IGNORECASE)


def visible_text(fragment: str) -> str:
    """Strip tags and decode entities to get on-screen text from an HTML fragment."""
    no_tags = TAG_RE.sub(" ", fragment)
    return _html.unescape(no_tags)


def count_units(text: str) -> int:
    """CJK glyphs count 1 each; runs of Latin/digits count as ~words."""
    cjk = len(CJK_RE.findall(text))
    latin_words = len(re.findall(r"[A-Za-z0-9][A-Za-z0-9'.\-]*", text))
    return cjk + latin_words


def _classify_family(token: str) -> str:
    """Classify one font-stack token: 'cjk' | 'generic' | 'var' | 'latin'."""
    t = token.strip().strip("\"'").strip().lower()
    if not t or t.startswith("var("):
        return "var"
    if any(fam in t for fam in CJK_FAMILIES):
        return "cjk"
    if t in GENERIC_FAMILIES:
        return "generic"
    return "latin"


def font_axis_warns(doc):
    """CJK/Latin two-axis font checks (principles.md §3). Pure: doc string in, warns out.

    (1) A CJK family before a real (named, non-generic) Latin family in a stack means the
        CJK face renders the Latin glyphs — order it Latin-first.
    (2) A CJK family is referenced but the deck has no Han glyphs — a megabyte CJK webfont
        loaded for nothing (and an unsubsetted force-load hangs PDF export).
    """
    warns = []
    order_bug = False
    for m in FONTSTACK_RE.finditer(doc):
        seen_cjk = False
        for kind in (_classify_family(tok) for tok in m.group(1).split(",")):
            if kind == "cjk":
                seen_cjk = True
            elif kind == "latin" and seen_cjk:
                order_bug = True
                break
        if order_bug:
            break
    if order_bug:
        warns.append("CJK font listed before the Latin family in a font stack — "
                     "Latin glyphs will render in the CJK face; put the Latin family first")
    if any(fam in doc.lower() for fam in CJK_FAMILIES):
        if not CJK_RE.search(visible_text(SCRIPT_STYLE_RE.sub("", doc))):
            warns.append("CJK webfont declared but the deck has no Han glyphs — "
                         "drop it to keep the file light and PDF-safe")
    return warns


def _selftest() -> int:
    """No-framework self-check for font_axis_warns (run via --selftest)."""
    ORDER, UNUSED = "before the Latin family", "no Han glyphs"
    a = ('<style>:root{--font-display:"Noto Sans TC","Switzer",sans-serif}</style>'
         '<section class="slide"><h1>測試標題</h1></section>')        # CJK-first, has Han
    b = ('<style>:root{--font-display:"Switzer","Noto Sans TC",sans-serif}</style>'
         '<section class="slide"><h1>測試標題</h1></section>')        # Latin-first, has Han
    c = ('<style>:root{--font-display:"Switzer","Noto Sans TC",sans-serif}</style>'
         '<section class="slide"><h1>Hello world</h1></section>')      # CJK declared, no Han
    wa, wb, wc = font_axis_warns(a), font_axis_warns(b), font_axis_warns(c)
    assert any(ORDER in w for w in wa), f"A: expected order-bug warn, got {wa}"
    assert not any(UNUSED in w for w in wa), f"A: unexpected unused warn, got {wa}"
    assert wb == [], f"B: expected no warns, got {wb}"
    assert any(UNUSED in w for w in wc), f"C: expected loaded-but-unused warn, got {wc}"
    assert not any(ORDER in w for w in wc), f"C: unexpected order warn, got {wc}"
    print("selftest OK")
    return 0


def main() -> int:
    if "--selftest" in sys.argv[1:]:
        return _selftest()
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
    for n, (attrs, frag) in enumerate(slides, 1):
        units = count_units(visible_text(frag))
        if units > MAX_VISIBLE_UNITS:
            warns.append(f"slide {n}: ~{units} text units (> {MAX_VISIBLE_UNITS}) — likely more than one idea, consider splitting")
        bullets = len(re.findall(r"<li\b", frag, re.IGNORECASE))
        if bullets > 6:
            warns.append(f"slide {n}: {bullets} bullets (> 6) — split into continuation slides, don't cram")
        m_lbl = DATALABEL_RE.search(attrs)
        role = m_lbl.group(1).strip().lower() if m_lbl else ""
        cap = ROLE_CAPS.get(role)
        if cap and bullets > cap:
            warns.append(f"slide {n}: role '{role}' has {bullets} bullets (cap {cap}) — split, don't cram")
        if units > MIN_UNITS_FOR_EMPHASIS and not EMPHASIS_RE.search(frag):
            warns.append(f"slide {n}: ~{units} text units and nothing emphasized — lift the key "
                         f"nouns/numbers (bold/accent), uniform text reads as a wall")

    # 5. Slide count vs hardcoded totals (page numbers should be derived, not typed).
    # Match the rendered "N / M" page-number form (spaces around the slash) so dates
    # like 7/31 or 8/17 aren't mistaken for a hardcoded page total.
    hard_total = re.findall(r"\d+\s+/\s+(\d+)\s*<", doc)
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

    # 8. CJK/Latin two-axis font discipline (principles.md §3).
    warns.extend(font_axis_warns(doc))

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
