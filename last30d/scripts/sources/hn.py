"""Hacker News lane via the public Algolia Search API (no key). Ranked by points."""
import json
import urllib.parse
import urllib.request
from datetime import datetime, timezone

BASE = "https://hn.algolia.com/api/v1/search_by_date"


def search(topic, from_date, to_date, limit=25):
    frm = int(datetime.fromisoformat(from_date).replace(tzinfo=timezone.utc).timestamp())
    to = int(datetime.fromisoformat(to_date).replace(tzinfo=timezone.utc).timestamp()) + 86400
    q = urllib.parse.urlencode({
        "query": topic, "tags": "story",
        "numericFilters": f"created_at_i>{frm},created_at_i<{to}",
        "hitsPerPage": max(limit * 2, 50),
    })
    try:
        with urllib.request.urlopen(f"{BASE}?{q}", timeout=15) as r:
            hits = json.loads(r.read().decode()).get("hits", [])
    except Exception:
        return []
    out = []
    for h in hits:
        pts = int(h.get("points") or 0)
        out.append({
            "lane": "hn",
            "title": (h.get("title") or "").strip(),
            "url": f"https://news.ycombinator.com/item?id={h.get('objectID')}",
            "score": pts, "score_label": "points",
            "meta": f"{h.get('num_comments') or 0} comments",
            "date": (h.get("created_at") or "")[:10],
            "excerpt": (h.get("story_text") or "")[:200], "top_comment": None,
            "relevance": 0.0,
        })
    out.sort(key=lambda x: x["score"], reverse=True)
    return out[:limit]
