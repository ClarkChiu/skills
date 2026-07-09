"""Reddit lane — thin ORIGINAL orchestrator over the vendored leaf fetchers.

Replaces upstream reddit_keyless (which balloons into keyed/rerank/arctic code we don't
use). The essential keyless flow, kept small:
  RSS discover (no scores) -> listing partials backfill real upvote scores by post-id
  -> rank by relevance+engagement -> enrich the top few with their single top comment.
Maps to the common record shape. Never raises (returns []).
"""
import math
import re
from collections import Counter

from . import reddit_rss, reddit_listing, reddit_shreddit

_PID = re.compile(r"/comments/([A-Za-z0-9]+)")


def _pid(url):
    m = _PID.search(url or "")
    return m.group(1) if m else ""


def _rank(p):
    eng = p.get("engagement", {})
    total = (eng.get("score", 0) or 0) + (eng.get("num_comments", 0) or 0)
    return (p.get("relevance") or 0.0) + min(0.25, math.log10(total + 1) / 20.0)


def _to_record(p):
    return {
        "lane": "reddit", "title": p.get("title", ""), "url": p.get("url", ""),
        "score": p.get("score", 0) or 0, "score_label": "upvotes",
        "meta": f'{p.get("num_comments", 0) or 0} comments · r/{p.get("subreddit", "")}',
        "date": p.get("date", ""), "excerpt": (p.get("selftext") or "")[:200],
        "top_comment": p.get("_top_comment"), "relevance": p.get("relevance", 0.0) or 0.0,
    }


def search(topic, from_date, to_date, limit=25, depth="default", enrich=3):
    posts = reddit_rss.search_rss(topic, depth=depth)
    if not posts:
        return []
    # Backfill real upvote scores from the listing partials of the most common subs.
    subs = [s for s, _ in Counter(
        p.get("subreddit", "") for p in posts if p.get("subreddit")).most_common(5)]
    scored = reddit_listing.fetch_listings(subs, depth=depth, query=topic) if subs else []
    score_map = {}
    for p in scored:
        pid = p.get("metadata", {}).get("post_id", "")
        if pid:
            score_map[pid] = (p.get("score", 0), p.get("num_comments", 0))
    for p in posts:
        hit = score_map.get(_pid(p.get("url", "")))
        if hit:
            p["score"], p["num_comments"] = hit
            p.setdefault("engagement", {})["score"] = hit[0]
            p["engagement"]["num_comments"] = hit[1]
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
