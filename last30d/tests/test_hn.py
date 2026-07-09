"""HN lane: parse Algolia results into ranked common-records. Intent: rank by points desc,
map to the HN item URL, tag lane/score_label. Network is mocked — deterministic."""
import json
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
