"""X lane — optional, over the vendored xai_x (first-party xAI Live Search).

No XAI_API_KEY -> [] + skip reason (Rule 12), so the rest of the run continues.
Maps xai_x items to the common record; ranks by likes.
"""
import os

from . import xai_x

SKIP = {"reason": None}


def search(topic, from_date, to_date, limit=25, depth="default"):
    SKIP["reason"] = None  # clear any stale reason from a prior in-process run
    key = os.environ.get("XAI_API_KEY")
    if not key:
        SKIP["reason"] = "no XAI_API_KEY"
        return []
    model = os.environ.get("XAI_MODEL", "grok-4")
    try:
        resp = xai_x.search_x(key, model, topic, from_date, to_date, depth=depth)
        items = xai_x.parse_x_response(resp)
    except Exception as e:
        SKIP["reason"] = f"xAI error: {type(e).__name__}"
        return []
    out = []
    for it in items:
        eng = it.get("engagement") or {}
        likes = int(eng.get("likes") or 0)
        handle = it.get("author_handle", "")
        out.append({
            "lane": "x", "title": (it.get("text") or "")[:120], "url": it.get("url", ""),
            "score": likes, "score_label": "likes",
            "meta": f'@{handle} · {eng.get("reposts") or 0} reposts',
            "date": it.get("date") or "", "excerpt": (it.get("text") or "")[:200],
            "top_comment": None, "relevance": it.get("relevance", 0.0) or 0.0,
        })
    out.sort(key=lambda x: x["score"], reverse=True)
    return out[:limit]
