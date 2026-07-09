"""GitHub lane via the REST Search API. Repos matching the topic pushed within the
window, ranked by stars. Uses GITHUB_TOKEN when present (higher rate limit)."""
import json
import os
import urllib.parse
import urllib.request

BASE = "https://api.github.com/search/repositories"


def search(topic, from_date, to_date, limit=25):
    query = f"{topic} pushed:>={from_date}"
    url = f"{BASE}?" + urllib.parse.urlencode({
        "q": query, "sort": "stars", "order": "desc",
        "per_page": min(max(limit, 10), 50),
    })
    hdr = {"Accept": "application/vnd.github+json", "User-Agent": "last30d"}
    tok = os.environ.get("GITHUB_TOKEN")
    if tok:
        hdr["Authorization"] = f"Bearer {tok}"
    try:
        req = urllib.request.Request(url, headers=hdr)
        with urllib.request.urlopen(req, timeout=15) as r:
            items = json.loads(r.read().decode()).get("items", [])
    except Exception:
        return []
    out = []
    for it in items:
        stars = int(it.get("stargazers_count") or 0)
        out.append({
            "lane": "github", "title": it.get("full_name") or "",
            "url": it.get("html_url") or "", "score": stars, "score_label": "stars",
            "meta": it.get("language") or "", "date": (it.get("pushed_at") or "")[:10],
            "excerpt": (it.get("description") or "")[:200], "top_comment": None,
            "relevance": 0.0,
        })
    out.sort(key=lambda x: x["score"], reverse=True)
    return out[:limit]
