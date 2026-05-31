#!/usr/bin/env python3
"""Render a single-file HTML deck to PDF, one slide per page, at 1920×1080.

The deck already has a print stylesheet (Ctrl/Cmd-P → Save as PDF works by hand). This
script automates it for batch/headless use via Playwright, which drives the same print
path so the output matches what the browser would produce.

Usage:
    python3 export_pdf.py deck.html [out.pdf]

Needs Playwright: `pip install playwright && playwright install chromium`. If it's
absent the script says so loudly (exit 2) rather than silently producing nothing.
"""
import sys
import os


def main() -> int:
    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    if not args:
        print("usage: export_pdf.py deck.html [out.pdf]", file=sys.stderr)
        return 2
    src = args[0]
    out = args[1] if len(args) > 1 else os.path.splitext(src)[0] + ".pdf"
    if not os.path.exists(src):
        print(f"no such file: {src}", file=sys.stderr)
        return 2

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("ERROR: Playwright not installed. Run:\n"
              "  pip install playwright && playwright install chromium\n"
              "Or just open the deck and use Ctrl/Cmd-P → Save as PDF.",
              file=sys.stderr)
        return 2

    url = "file://" + os.path.abspath(src)
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(url, wait_until="networkidle")
        # The deck's @media print rules lay every .slide out one-per-page at 1920×1080;
        # preferCSSPageSize honors the @page size declared there.
        page.pdf(path=out, prefer_css_page_size=True, print_background=True)
        browser.close()
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
