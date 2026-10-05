"""Reddit lane — thin ORIGINAL orchestrator over the vendored leaf fetchers.

Replaces upstream reddit_keyless (which balloons into keyed/rerank/arctic code we don't
use). The essential keyless flow, kept small:
  site-search discover (/svc/shreddit/search/ — each post arrives dated and scored)
  -> trim to the requested window -> rank by relevance+engagement
  -> enrich the top few with their single top comment.
Maps to the common record shape. Never raises (returns []).

Discovery used to be Reddit RSS (`reddit_rss`), which Reddit shuts off on 2026-11-13;
upstream replaced it with `reddit_search` (39a0adda954f, #1189) and so do we.
Reddit's `t=` buckets are rolling windows ending *now*, so `reddit_search` picks the
smallest bucket that reaches `from_date`, and this lane drops posts dated outside
`from_date`..`to_date` (undated posts are kept).
"""
import math

from . import reddit_search, reddit_shreddit


def _rank(p):
    eng = p.get("engagement", {})
    total = (eng.get("score", 0) or 0) + (eng.get("num_comments", 0) or 0)
    return (p.get("relevance") or 0.0) + min(0.25, math.log10(total + 1) / 20.0)


def _to_record(p):
    return {
        "lane": "reddit", "title": p.get("title", ""), "url": p.get("url", ""),
        "score": p.get("score", 0) or 0, "score_label": "upvotes",
        "meta": f'{p.get("num_comments", 0) or 0} comments · r/{p.get("subreddit", "")}',
        "date": p.get("date") or "", "excerpt": (p.get("selftext") or "")[:200],
        "top_comment": p.get("_top_comment"), "relevance": p.get("relevance", 0.0) or 0.0,
    }


def search(topic, from_date, to_date, limit=25, depth="default", enrich=3):
    posts = reddit_search.search(topic, depth=depth, from_date=from_date, to_date=to_date)
    posts = [p for p in posts if not p.get("date") or from_date <= p["date"] <= to_date]
    if not posts:
        return []
    posts.sort(key=_rank, reverse=True)
    posts = posts[:limit]
    # Enrich the top few with their single highest-scored comment (the substance).
    for p in posts[:enrich]:
        try:
            c = reddit_shreddit.fetch_comments(p.get("url", ""))
        except Exception:
            c = None
        if c and c.get("top_comments"):
            tc = c["top_comments"][0]
            p["_top_comment"] = f'({tc.get("score", 0)}↑) {tc.get("excerpt", "")}'
        if c and c.get("num_comments"):
            p["num_comments"] = c["num_comments"]
            p.setdefault("engagement", {})["num_comments"] = c["num_comments"]
    return [_to_record(p) for p in posts]
