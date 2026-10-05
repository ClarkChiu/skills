"""Adapters over the vendored engines. Intent: reddit_lane ranks site-search posts by
relevance+engagement, keeps only the requested window, and attaches the top comment; x_lane degrades to []+skip without a key and maps
xai items to records when keyed. Vendored fns are mocked."""
import conftest  # noqa: F401
from sources import reddit_lane, x_lane


# ---- Reddit adapter ----
def test_reddit_lane_ranks_trims_window_and_adds_top_comment(monkeypatch):
    def post(title, pid, score, rel, date):
        return {"title": title, "url": f"https://www.reddit.com/r/rust/comments/{pid}/x/",
                "subreddit": "rust", "score": score, "num_comments": 3,
                "engagement": {"score": score, "num_comments": 3}, "relevance": rel,
                "selftext": "", "date": date}
    found = [post("B", "bbb", 2, 0.4, "2026-07-01"), post("A", "aaa", 500, 0.9, "2026-07-02"),
             post("Old", "ooo", 9000, 1.0, "2026-05-01"),  # outside the window -> dropped
             post("Undated", "uuu", 1, 0.1, None)]          # no date -> kept, not guessed
    seen = {}

    def fake_search(topic, **kw):
        seen.update(kw)
        return found
    monkeypatch.setattr(reddit_lane.reddit_search, "search", fake_search)
    monkeypatch.setattr(reddit_lane.reddit_shreddit, "fetch_comments",
                        lambda url, **k: {"top_comments": [{"score": 99, "excerpt": "the real point"}],
                                          "num_comments": 42})
    out = reddit_lane.search("rust async", "2026-06-09", "2026-07-09", limit=25, enrich=1)
    # The window must reach the engine, or reddit_search falls back to t=month regardless.
    assert seen["from_date"] == "2026-06-09" and seen["to_date"] == "2026-07-09"
    assert [r["title"] for r in out] == ["A", "B", "Undated"], "rank or window trim wrong"
    a = out[0]
    assert a["lane"] == "reddit" and a["score_label"] == "upvotes" and a["score"] == 500
    assert a["top_comment"] == "(99↑) the real point" and "42 comments" in a["meta"]


# ---- X adapter ----
def test_x_lane_skips_without_key(monkeypatch):
    monkeypatch.delenv("XAI_API_KEY", raising=False)
    x_lane.SKIP["reason"] = None
    out = x_lane.search("topic", "2026-06-09", "2026-07-09")
    assert out == [] and x_lane.SKIP["reason"] == "no XAI_API_KEY"


def test_x_lane_maps_items_when_keyed(monkeypatch):
    x_lane.SKIP["reason"] = "no XAI_API_KEY"  # stale reason from a prior keyless run
    monkeypatch.setenv("XAI_API_KEY", "xai-test")
    items = [
        {"text": "small", "url": "https://x.com/u/1", "author_handle": "u",
         "engagement": {"likes": 10, "reposts": 1}, "date": "2026-07-01", "relevance": 0.5},
        {"text": "big one", "url": "https://x.com/u/2", "author_handle": "v",
         "engagement": {"likes": 900, "reposts": 100}, "date": "2026-07-06", "relevance": 0.8},
    ]
    monkeypatch.setattr(x_lane.xai_x, "search_x", lambda *a, **k: {"raw": True})
    monkeypatch.setattr(x_lane.xai_x, "parse_x_response", lambda resp: items)
    out = x_lane.search("topic", "2026-06-09", "2026-07-09", limit=25)
    assert [r["title"] for r in out] == ["big one", "small"], "not ranked by likes"
    assert out[0]["lane"] == "x" and out[0]["score"] == 900 and out[0]["score_label"] == "likes"
    assert "@v" in out[0]["meta"]
    assert x_lane.SKIP["reason"] is None, "a successful keyed run must clear the stale skip reason"
