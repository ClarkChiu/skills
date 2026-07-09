"""Adapters over the vendored engines. Intent: reddit_lane backfills real scores by
post-id and attaches the top comment; x_lane degrades to []+skip without a key and maps
xai items to records when keyed. Vendored fns are mocked."""
import conftest  # noqa: F401
from sources import reddit_lane, x_lane


# ---- Reddit adapter ----
def test_reddit_lane_backfills_scores_and_top_comment(monkeypatch):
    rss_posts = [
        {"title": "A", "url": "https://www.reddit.com/r/rust/comments/aaa/x/",
         "subreddit": "rust", "score": 0, "num_comments": 0,
         "engagement": {"score": 0, "num_comments": 0}, "relevance": 0.9, "selftext": ""},
        {"title": "B", "url": "https://www.reddit.com/r/rust/comments/bbb/y/",
         "subreddit": "rust", "score": 0, "num_comments": 0,
         "engagement": {"score": 0, "num_comments": 0}, "relevance": 0.4, "selftext": ""},
    ]
    listing = [{"score": 500, "num_comments": 42, "metadata": {"post_id": "aaa"}}]
    monkeypatch.setattr(reddit_lane.reddit_rss, "search_rss", lambda *a, **k: rss_posts)
    monkeypatch.setattr(reddit_lane.reddit_listing, "fetch_listings", lambda *a, **k: listing)
    monkeypatch.setattr(reddit_lane.reddit_shreddit, "fetch_comments",
                        lambda url, **k: {"top_comments": [{"score": 99, "excerpt": "the real point"}],
                                          "num_comments": 42})
    out = reddit_lane.search("rust async", "2026-06-09", "2026-07-09", limit=25, enrich=2)
    a = next(r for r in out if r["title"] == "A")
    assert a["lane"] == "reddit" and a["score_label"] == "upvotes"
    assert a["score"] == 500, "score not backfilled from listing by post-id"
    assert a["top_comment"] == "(99↑) the real point"
    # A (relevance .9 + backfilled engagement) must outrank B.
    assert out[0]["title"] == "A"


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
