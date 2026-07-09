"""arXiv lane via the public arXiv API (Atom, no key).

arXiv carries no engagement metric, so this lane ranks by recency (published desc)
within the window. score stays 0; score_label is 'arxiv' so the digest shows recency.
"""
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

ATOM = "{http://www.w3.org/2005/Atom}"
BASE = "http://export.arxiv.org/api/query"


def search(topic, from_date, to_date, limit=25):
    q = urllib.parse.urlencode({
        "search_query": f"all:{topic}", "sortBy": "submittedDate",
        "sortOrder": "descending", "max_results": max(limit * 2, 40),
    })
    try:
        with urllib.request.urlopen(f"{BASE}?{q}", timeout=20) as r:
            root = ET.fromstring(r.read().decode())
    except Exception:
        return []
    out = []
    for e in root.iter(f"{ATOM}entry"):
        pub = (e.findtext(f"{ATOM}published") or "")[:10]
        if pub and (pub < from_date or pub > to_date):
            continue
        title = " ".join((e.findtext(f"{ATOM}title") or "").split())
        link = ""
        for l in e.iter(f"{ATOM}link"):
            if l.get("rel") == "alternate":
                link = l.get("href", "")
        authors = [a.findtext(f"{ATOM}name") or "" for a in e.iter(f"{ATOM}author")]
        out.append({
            "lane": "arxiv", "title": title, "url": link, "score": 0,
            "score_label": "arxiv", "meta": ", ".join(a for a in authors[:3] if a),
            "date": pub,
            "excerpt": " ".join((e.findtext(f"{ATOM}summary") or "").split())[:200],
            "top_comment": None, "relevance": 0.0,
        })
    out.sort(key=lambda x: x["date"], reverse=True)
    return out[:limit]
