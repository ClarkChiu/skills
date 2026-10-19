"""YouTube lane (optional, yt-dlp). Intent: rank by views; parse yt-dlp --dump-json lines;
filter to window; and DEGRADE GRACEFULLY (Rule 12) when yt-dlp is absent -> [] + skip reason,
never a crash. subprocess & which are mocked."""
import json

import conftest  # noqa: F401
from sources import youtube


def _line(title, vid_url, views, likes, upload_date, desc="d"):
    return json.dumps({"title": title, "webpage_url": vid_url, "view_count": views,
                       "like_count": likes, "upload_date": upload_date, "description": desc})


class _Proc:
    def __init__(self, stdout, returncode=0, stderr=""):
        self.stdout, self.returncode, self.stderr = stdout, returncode, stderr


def test_youtube_ranks_by_views_and_filters_window(monkeypatch):
    monkeypatch.setattr(youtube.shutil, "which", lambda _n: "/usr/bin/yt-dlp")
    stdout = "\n".join([
        _line("Low", "https://youtu.be/1", 1000, 50, "20260702"),
        _line("High", "https://youtu.be/2", 90000, 4000, "20260705"),
        _line("TooOld", "https://youtu.be/3", 999999, 9, "20260101"),
    ])
    monkeypatch.setattr(youtube.subprocess, "run", lambda *a, **k: _Proc(stdout))
    out = youtube.search("ai agents", "2026-06-09", "2026-07-09", limit=25)
    assert [r["title"] for r in out] == ["High", "Low"], "not view-ranked / window not applied"
    top = out[0]
    assert top["lane"] == "youtube" and top["score"] == 90000 and top["score_label"] == "views"
    assert top["url"] == "https://youtu.be/2" and top["date"] == "2026-07-05"
    assert "4000 likes" in top["meta"]


def test_youtube_records_why_when_ytdlp_exits_nonzero(monkeypatch):
    # yt-dlp breaks often (YouTube changes, bot checks); a non-zero exit with no output
    # must say so instead of reading as "no videos about this topic".
    monkeypatch.setattr(youtube.shutil, "which", lambda _n: "/usr/bin/yt-dlp")
    err = "WARNING: slow\nERROR: Sign in to confirm you're not a bot\n"
    monkeypatch.setattr(youtube.subprocess, "run", lambda *a, **k: _Proc("", 1, err))
    monkeypatch.setitem(youtube.SKIP, "reason", None)
    assert youtube.search("x", "2026-06-09", "2026-07-09") == []
    assert youtube.SKIP["reason"] == "yt-dlp exit 1: ERROR: Sign in to confirm you're not a bot"


def test_youtube_skips_when_ytdlp_absent(monkeypatch):
    monkeypatch.setattr(youtube.shutil, "which", lambda _n: None)
    youtube.SKIP["reason"] = None
    out = youtube.search("x", "2026-06-09", "2026-07-09")
    assert out == [] and youtube.SKIP["reason"] == "yt-dlp not installed"
