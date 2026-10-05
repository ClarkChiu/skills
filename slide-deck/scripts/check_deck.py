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
    python3 check_deck.py --selftest      # self-check the checker itself (no file needed):
                                          # font-axis rules, page-role lock, and the
                                          # speaker-notes/CSS lockstep end-to-end

Exit codes: 0 = clean (warnings allowed), 1 = errors found (or --strict + warnings),
2 = file unreadable. Stdlib only.
"""
import sys
import re
import html as _html
import io
import os
import contextlib
import tempfile

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
# Speaker notes (narrative.md §6) live inside the slide but never render. They must not
# count toward the one-idea density budget, the bullet cap, or the emphasis check —
# otherwise a well-noted slide looks overfull. They ARE still placeholder-checked.
# `notes` must be a whole class token (so `speaker-notes` / `notes-draft` do NOT match)
# and the element must be <aside> — this mirrors the template's `aside.notes` CSS rule
# exactly. The two must agree: anything the checker ignores but CSS still renders is a
# silent hole, and anything CSS hides but the checker counts is a bogus warning.
# Ceiling: a nested <aside> inside a note ends the match early (non-greedy), and an
# unclosed <aside> is not stripped at all. Both are authoring errors, not worth an HTML
# parser here; the deck's own rendering makes them obvious.
# `notes` is matched CASE-SENSITIVELY via (?-i:…): HTML class selectors are
# case-sensitive in standards mode, so `class="Notes"` is NOT hidden by `aside.notes`
# and must therefore not be stripped either. `(?<![-\w])` keeps `data-class="notes"`
# from counting as a class attribute. Whitespace around `=` and unquoted values are
# legal HTML and CSS hides them, so the checker must strip them too.
NOTES_RE = re.compile(
    r'<aside\b[^>]*?(?<![-\w])class\s*=\s*'
    r'(?:(["\'])(?:[^"\']*\s)?(?-i:notes)(?:\s[^"\']*)?\1'
    r'|(?-i:notes)(?=[\s>]))'
    r'[^>]*>.*?</aside>',
    re.IGNORECASE | re.DOTALL)
# A deck may declare the hiding rule as `aside.notes`, `.slide aside.notes`, etc. What
# matters is that SOME rule hides it; without one the whole speaker script renders.
NOTES_CSS_RE = re.compile(r'aside\.notes\b[^{]*\{[^}]*display\s*:\s*none', re.IGNORECASE)
COMMENT_RE = re.compile(r"<!--.*?-->", re.DOTALL)
SCRIPT_STYLE_RE = re.compile(r"<(script|style)\b.*?</\1>", re.IGNORECASE | re.DOTALL)
SLIDE_RE = re.compile(r'<section\b([^>]*class="[^"]*\bslide\b[^"]*"[^>]*)>(.*?)</section>',
                      re.IGNORECASE | re.DOTALL)
DATALABEL_RE = re.compile(r'data-label=(["\'])([^"\']*)\1', re.IGNORECASE)
# Roles whose one-line-bullet density is deterministically cappable (layouts.md). A slide
# tagged with one of these via data-label gets its bullet count checked against the cap.
ROLE_CAPS = {"content": 5, "agenda": 6}
# Registered page roles (layouts.md). data-label is the hook that makes role checks
# possible; an unregistered label usually means an invented layout — the main source
# of unstable slides (constraints make generated decks more reliable).
ROLE_ALIASES = {"big-number": "bignumber", "section-divider": "section", "divider": "section"}
KNOWN_ROLES = {"cover", "agenda", "section", "content", "bignumber", "quote",
               "comparison", "timeline", "closing"}
# Near-empty roles (layouts.md density table): prose beyond this belongs on a Content slide.
SPARSE_ROLES = {"cover", "section", "closing", "bignumber", "quote"}
MAX_SPARSE_UNITS = 50
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


def strip_notes(fragment: str) -> str:
    """Drop <aside class="notes"> blocks — spoken script, never rendered."""
    return NOTES_RE.sub(" ", fragment)


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


def slide_role_warns(attrs: str, frag: str, n: int):
    """Role-lock checks against the layouts.md registry. Pure: attrs+fragment in, warns out.

    Every slide should declare its page role via data-label; that hook is what makes
    role-level checks (bullet caps, near-empty density) possible at all. An unregistered
    label is usually an invented layout, which is where unstable pages come from.
    """
    warns = []
    units = count_units(visible_text(frag))
    bullets = len(re.findall(r"<li\b", frag, re.IGNORECASE))
    m_lbl = DATALABEL_RE.search(attrs)
    role = m_lbl.group(2).strip().lower() if m_lbl else ""
    role = re.sub(r"[\s_]+", "-", role)   # catalog display names use spaces ("Big number")
    role = ROLE_ALIASES.get(role, role)
    if not role:
        warns.append(f"slide {n}: no data-label — tag its registered role "
                     f"({', '.join(sorted(KNOWN_ROLES))}) so role checks can apply")
    elif role not in KNOWN_ROLES:
        warns.append(f"slide {n}: data-label '{role}' is not a registered role "
                     f"({', '.join(sorted(KNOWN_ROLES))}) — invented layouts are the "
                     f"main source of unstable slides; pick from the catalog")
    cap = ROLE_CAPS.get(role)
    if cap and bullets > cap:
        warns.append(f"slide {n}: role '{role}' has {bullets} bullets (cap {cap}) — split, don't cram")
    if role in SPARSE_ROLES and units > MAX_SPARSE_UNITS:
        warns.append(f"slide {n}: role '{role}' is a near-empty role but carries ~{units} "
                     f"text units (> {MAX_SPARSE_UNITS}) — move the prose to a Content slide")
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
    # role-lock checks (slide_role_warns)
    R_MISS, R_UNREG, R_SPARSE = "no data-label", "not a registered role", "near-empty role"
    wd = slide_role_warns('class="slide"', "<h1>Hi</h1>", 1)
    assert any(R_MISS in w for w in wd), f"D: expected missing-label warn, got {wd}"
    we = slide_role_warns('class="slide" data-label="hero-mega"', "<h1>Hi</h1>", 2)
    assert any(R_UNREG in w for w in we), f"E: expected unregistered-role warn, got {we}"
    wf = slide_role_warns('class="slide" data-label="Quote"', "<p>" + "字" * 60 + "</p>", 3)
    assert any(R_SPARSE in w for w in wf), f"F: expected sparse-density warn, got {wf}"
    wg = slide_role_warns('class="slide" data-label="Big-Number"', "<h1>42</h1>", 4)
    assert wg == [], f"G: alias Big-Number should be registered and clean, got {wg}"
    wh = slide_role_warns("class=\"slide\" data-label='cover'", "<h1>Hi</h1>", 5)
    assert wh == [], f"H: single-quoted data-label should parse, got {wh}"
    wi = slide_role_warns('class="slide" data-label="Section divider"', "<h1>Part 2</h1>", 6)
    assert wi == [], f"I: space variant 'Section divider' should normalize, got {wi}"
    # Speaker notes (narrative.md §6) — end-to-end through main(), because the thing
    # that can break is the WIRING, not the regex. An assertion that hand-feeds an
    # already-stripped fragment to slide_role_warns still passes when main() forgets to
    # strip at all; these run the real file path under --strict, where a warning fails.
    def _lint(body: str, notes_css: bool = True) -> int:
        """Run the real checker over a minimal deck; return its exit code."""
        hide = "aside.notes{display:none}" if notes_css else ""
        deck = ('<style>:root{--font-display:"Switzer",sans-serif}'
                f'{hide}.slide{{font-size:40px}}</style>'
                '<div id="stage" style="width:1920px;height:1080px">'
                f'<section class="slide" data-label="Cover">{body}</section></div>')
        fd, path = tempfile.mkstemp(suffix=".html")
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as fh:
                fh.write(deck)
            argv, sys.argv = sys.argv, ["check_deck.py", path, "--strict"]
            try:
                with contextlib.redirect_stdout(io.StringIO()):
                    return main()
            finally:
                sys.argv = argv
        finally:
            os.unlink(path)

    prose = "字" * 80          # well over MAX_SPARSE_UNITS for a Cover slide
    # L: the control — this much prose ON SCREEN must fail, or the test proves nothing.
    assert _lint(f"<h1>標題</h1><p>{prose}</p>") == 1, \
        "L: sparse-role control should fail; the notes cases below would be vacuous"
    # M: the same text as notes must NOT count — this fails if main() stops stripping.
    assert _lint(f'<h1>標題</h1><aside class="notes">{prose}</aside>') == 0, \
        "M: notes must not count toward on-screen density"
    assert _lint(f"<h1>標題</h1><aside class='notes'>{prose}</aside>") == 0, \
        "M: single-quoted class='notes' must strip too (CSS hides it)"
    # N: near-miss class names are NOT hidden by `aside.notes` CSS, so they must count.
    assert _lint(f'<h1>標題</h1><aside class="speaker-notes">{prose}</aside>') == 1, \
        "N: 'speaker-notes' renders on screen — the checker must not ignore it"
    assert _lint(f'<h1>標題</h1><div class="notes">{prose}</div>') == 1, \
        "N: only <aside class=notes> is the canonical hidden form"
    # O: notes are still scanned for leftover placeholder text.
    assert _lint('<h1>標題</h1><aside class="notes">TODO write this</aside>') == 1, \
        "O: a TODO inside a note is a TODO in the deliverable"
    # P: notes with NO hiding rule must be an ERROR, not a clean deck. Without this the
    # strip silently turns "forgot the CSS" into "whole speaker script on the slide,
    # 0 warnings" — the worst outcome the notes feature can produce.
    assert _lint(f'<h1>標題</h1><aside class="notes">{prose}</aside>', notes_css=False) == 1, \
        "P: notes without an aside.notes display:none rule must fail"
    # Q: checker and CSS must agree on EXACT attribute forms. Class selectors are
    # case-sensitive in standards mode, `data-class` is not a class, and whitespace
    # around `=` / unquoted values are legal HTML that CSS does hide.
    for attr, hidden_by_css in (('class="Notes"', False),      # CSS: case-sensitive → visible
                                ('data-class="notes"', False),  # not a class attribute
                                ('class = "notes"', True),      # legal HTML, CSS hides it
                                ('class=notes', True)):         # unquoted, CSS hides it
        code = _lint(f'<h1>標題</h1><aside {attr}>{prose}</aside>')
        want = 0 if hidden_by_css else 1
        assert code == want, \
            f"Q: <aside {attr}> — CSS hides={hidden_by_css}, checker disagreed (exit {code})"
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

    # 3b. Speaker notes present but nothing hides them (narrative.md §6). The checker
    # strips notes from the density budget, so without this check a deck that forgot the
    # CSS rule prints the entire spoken script on the slides and still lints clean —
    # exactly the silent failure the strip introduced. Decks built on paths C/D or an
    # existing deck being improved do not inherit the rule from assets/template.html.
    if NOTES_RE.search(doc) and not NOTES_CSS_RE.search(doc):
        errors.append("<aside class=\"notes\"> present but no `aside.notes { display: none }` "
                      "rule — the speaker script will render on the slides")

    # 4. Per-slide density — one idea per slide.
    slides = SLIDE_RE.findall(doc)
    if not slides:
        warns.append("no <section class=\"slide\"> blocks found")
    nav_dots_dynamic = "createElement('button')" in doc or 'createElement("button")' in doc
    for n, (attrs, frag) in enumerate(slides, 1):
        frag = strip_notes(frag)      # spoken script is not on-screen content
        units = count_units(visible_text(frag))
        if units > MAX_VISIBLE_UNITS:
            warns.append(f"slide {n}: ~{units} text units (> {MAX_VISIBLE_UNITS}) — likely more than one idea, consider splitting")
        bullets = len(re.findall(r"<li\b", frag, re.IGNORECASE))
        if bullets > 6:
            warns.append(f"slide {n}: {bullets} bullets (> 6) — split into continuation slides, don't cram")
        warns.extend(slide_role_warns(attrs, frag, n))
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
