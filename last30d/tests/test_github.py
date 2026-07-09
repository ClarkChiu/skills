"""GitHub lane: parse REST repo-search into records ranked by stars. Intent: map
full_name/stars/pushed_at, and attach the Authorization header when GITHUB_TOKEN is set
(higher rate limit). Network mocked; the mock captures the Request to check the header."""
import json
from contextlib import contextmanager

import conftest  # noqa: F401
from sources import github

CANNED = {"items": [
    {"full_name": "a/low", "html_url": "https://github.com/a/low", "stargazers_count": 90,
     "pushed_at": "2026-07-01T00:00:00Z", "description": "d1", "language": "Go"},
    {"full_name": "b/high", "html_url": "https://github.com/b/high", "stargazers_count": 800,
     "pushed_at": "2026-07-06T00:00:00Z", "description": "d2", "language": "Rust"},
]}


def _make_fake(captured):
    @contextmanager
    def _fake(req, *_a, **_k):
        captured["req"] = req
        class R:
            def read(self_inner):
                return json.dumps(CANNED).encode()
        yield R()
    return _fake


def test_github_ranks_by_stars_and_maps(monkeypatch):
    captured = {}
    monkeypatch.delenv("GITHUB_TOKEN", raising=False)
    monkeypatch.setattr(github.urllib.request, "urlopen", _make_fake(captured))
    out = github.search("cli", "2026-06-09", "2026-07-09", limit=25)
    assert [r["title"] for r in out] == ["b/high", "a/low"], "not ranked by stars desc"
    top = out[0]
    assert top["lane"] == "github" and top["score"] == 800 and top["score_label"] == "stars"
    assert top["url"] == "https://github.com/b/high" and top["date"] == "2026-07-06"


def test_github_sends_auth_header_when_token_set(monkeypatch):
    captured = {}
    monkeypatch.setenv("GITHUB_TOKEN", "ghp_test")
    monkeypatch.setattr(github.urllib.request, "urlopen", _make_fake(captured))
    github.search("cli", "2026-06-09", "2026-07-09")
    assert captured["req"].headers.get("Authorization") == "Bearer ghp_test"


def test_github_empty_on_error(monkeypatch):
    def boom(*_a, **_k):
        raise OSError("down")
    monkeypatch.setattr(github.urllib.request, "urlopen", boom)
    assert github.search("x", "2026-06-09", "2026-07-09") == []
