"""YouTube lane via yt-dlp (optional external CLI). Ranked by view count.

yt-dlp is user-supplied (like ffmpeg for ig-reel) — never auto-installed. Absent yt-dlp
-> [] + a skip reason (Rule 12 graceful degrade), so the rest of the run continues.
Full extraction (no --flat-playlist) is used deliberately: flat mode omits view/like/date,
which are exactly this lane's engagement signal.
"""
import json
import shutil
import subprocess

SKIP = {"reason": None}


def available():
    return shutil.which("yt-dlp") is not None


def search(topic, from_date, to_date, limit=25):
    SKIP["reason"] = None  # clear any stale reason from a prior in-process run
    if not available():
        SKIP["reason"] = "yt-dlp not installed"
        return []
    try:
        p = subprocess.run(
            ["yt-dlp", f"ytsearch{max(limit, 10)}:{topic}", "--dump-json", "--no-warnings"],
            capture_output=True, text=True, timeout=120,
        )
    except Exception:
        SKIP["reason"] = "yt-dlp failed"
        return []
    out = []
    for line in (p.stdout or "").splitlines():
        try:
            v = json.loads(line)
        except ValueError:
            continue
        up = v.get("upload_date") or ""
        date = f"{up[:4]}-{up[4:6]}-{up[6:8]}" if len(up) == 8 else ""
        if date and (date < from_date or date > to_date):
            continue
        views = int(v.get("view_count") or 0)
        out.append({
            "lane": "youtube", "title": v.get("title") or "",
            "url": v.get("webpage_url") or v.get("url") or "",
            "score": views, "score_label": "views",
            "meta": f"{v.get('like_count') or 0} likes", "date": date,
            "excerpt": (v.get("description") or "")[:200], "top_comment": None,
            "relevance": 0.0,
        })
    out.sort(key=lambda x: x["score"], reverse=True)
    return out[:limit]
