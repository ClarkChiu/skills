"""HN lane: parse Algolia results into ranked common-records. Intent: rank by points desc,
map to the HN item URL, tag lane/score_label. Network is mocked — deterministic."""
import json
import urllib.parse
from contextlib import contextmanager

import conftest  # noqa: F401  (puts scripts/ on path)
from sources import hn

CANNED = {
    "hits": [
        {"title": "Low", "objectID": "111", "points": 50, "num_comments": 4,
         "created_at": "2026-07-02T10:00:00Z", "created_at_i": 1782000000, "url": None},
        {"title": "High", "objectID": "222", "points": 300, "num_comments": 90,
         "created_at": "2026-07-05T10:00:00Z", "created_at_i": 1782200000, "url": None},
    ]
}


@contextmanager
def _fake_urlopen(*_a, **_k):
    class R:
        def read(self_inner):
            return json.dumps(CANNED).encode()
    yield R()


def _capturing(captured):
    @contextmanager
    def _fake(url, *_a, **_k):
        captured["url"] = url
        class R:
            def read(self_inner):
                return json.dumps(CANNED).encode()
        yield R()
    return _fake


def _query(url):
    return urllib.parse.parse_qs(urllib.parse.urlsplit(url).query)


def test_hn_query_is_limited_to_the_window(monkeypatch):
    # Algolia ranks all-time results unless filtered, so the window must stay in the query:
    # from 2026-06-09 00:00Z up to the end of to_date (2026-07-10 00:00Z, exclusive).
    captured = {}
    monkeypatch.setattr(hn.urllib.request, "urlopen", _capturing(captured))
    hn.search("x", "2026-06-09", "2026-07-09")
    assert _query(captured["url"])["numericFilters"] == [
        "created_at_i>1780963200,created_at_i<1783641600"]


def test_hn_asks_for_the_top_of_the_window_not_the_newest(monkeypatch):
    # search_by_date returns newest first, so the 50 hits we fetch cover only the last few
    # days of a hot topic. Measured 2026-10-19, "claude", 30-day window, 885 stories:
    # search_by_date → 10-16..10-19, best 1051 points; search → 09-20..10-18, best 1806.
    # /search ranks by relevance then points, so its top hits span the whole window.
    captured = {}
    monkeypatch.setattr(hn.urllib.request, "urlopen", _capturing(captured))
    hn.search("x", "2026-06-09", "2026-07-09")
    assert urllib.parse.urlsplit(captured["url"]).path == "/api/v1/search"


def test_hn_ranks_by_points_and_maps_records(monkeypatch):
    monkeypatch.setattr(hn.urllib.request, "urlopen", _fake_urlopen)
    out = hn.search("anything", "2026-06-09", "2026-07-09", limit=25)
    assert [r["title"] for r in out] == ["High", "Low"], "not ranked by points desc"
    top = out[0]
    assert top["lane"] == "hn"
    assert top["score"] == 300 and top["score_label"] == "points"
    assert top["url"] == "https://news.ycombinator.com/item?id=222"
    assert "90 comments" in top["meta"]


def test_hn_returns_empty_on_network_error(monkeypatch):
    def boom(*_a, **_k):
        raise OSError("down")
    monkeypatch.setattr(hn.urllib.request, "urlopen", boom)
    assert hn.search("x", "2026-06-09", "2026-07-09") == []
