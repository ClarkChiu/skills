"""Digest renderer. Intent: per-lane sections (never a merged table), Reddit rows show
the top-comment line, skipped lanes are VISIBLE (Rule 12), the header carries per-lane
counts, and --json emits the same data as valid JSON."""
import json

import conftest  # noqa: F401
from sources import digest

RESULTS = {
    "reddit": [{"lane": "reddit", "title": "Hero or insufferable?", "url": "https://r/x",
                "score": 569, "score_label": "upvotes", "meta": "210 comments · r/ClaudeCode",
                "date": "2026-06-24", "excerpt": "", "top_comment": "(312↑) he nailed it",
                "relevance": 0.9}],
    "hn": [{"lane": "hn", "title": "Show HN: thing", "url": "https://news.yc/1",
            "score": 300, "score_label": "points", "meta": "90 comments", "date": "2026-07-05",
            "excerpt": "", "top_comment": None, "relevance": 0.0}],
}
SKIPS = {"x": "no XAI_API_KEY", "youtube": "yt-dlp not installed"}


def test_markdown_has_per_lane_sections_and_visible_skips():
    md = digest.render_markdown("Peter", "2026-06-09", "2026-07-09", RESULTS, SKIPS)
    assert "## Reddit" in md and "## Hacker News" in md
    assert "Hero or insufferable?" in md and "569" in md
    assert "↳ top comment (312↑) he nailed it" in md, "reddit top-comment line missing"
    # skipped lanes must be visible, not hidden
    assert "skipped: no XAI_API_KEY" in md and "skipped: yt-dlp not installed" in md
    # header shows per-lane counts
    assert "reddit 1" in md and "hn 1" in md


def test_json_roundtrips_same_data():
    js = digest.render_json("Peter", "2026-06-09", "2026-07-09", RESULTS, SKIPS)
    data = json.loads(js)
    assert data["topic"] == "Peter"
    assert data["lanes"]["reddit"][0]["score"] == 569
    assert data["skipped"]["x"] == "no XAI_API_KEY"
