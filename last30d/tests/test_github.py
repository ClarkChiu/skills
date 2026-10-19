"""GitHub lane: parse REST repo-search into records ranked by stars. Intent: map
full_name/stars/pushed_at, and attach the Authorization header when GITHUB_TOKEN is set
(higher rate limit) — but never let it follow a redirect to another host. Network mocked;
the mock captures the Request to check the header. The redirect test uses real loopback
servers instead, so it exercises urllib's actual redirect handling."""
import http.server
import json
import threading
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
    assert captured["req"].get_header("Authorization") == "Bearer ghp_test"


def _serve(handler_cls):
    srv = http.server.HTTPServer(("127.0.0.1", 0), handler_cls)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv


def test_github_token_not_forwarded_on_cross_host_redirect(monkeypatch):
    # The token can carry repo/workflow scope: a redirect must never hand it to another
    # host. 127.0.0.1 redirects to localhost (a different host); the target records what
    # it received. Expecting exactly one hit also proves the redirect was really followed.
    seen = []

    class Target(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            seen.append(self.headers.get("Authorization"))
            body = json.dumps(CANNED).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def log_message(self, *_a):
            pass

    target = _serve(Target)

    class Redirector(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(302)
            self.send_header("Location", f"http://localhost:{target.server_port}/search")
            self.send_header("Content-Length", "0")
            self.end_headers()

        def log_message(self, *_a):
            pass

    redirector = _serve(Redirector)
    monkeypatch.setenv("GITHUB_TOKEN", "ghp_test")
    monkeypatch.setenv("no_proxy", "*")  # a proxy env var must not reroute loopback
    monkeypatch.setattr(github, "BASE", f"http://127.0.0.1:{redirector.server_port}/search")
    try:
        github.search("cli", "2026-06-09", "2026-07-09")
    finally:
        for srv in (redirector, target):
            srv.shutdown()
            srv.server_close()
    assert seen == [None], f"redirect target received Authorization: {seen}"


def test_github_empty_on_error(monkeypatch):
    def boom(*_a, **_k):
        raise OSError("down")
    monkeypatch.setattr(github.urllib.request, "urlopen", boom)
    assert github.search("x", "2026-06-09", "2026-07-09") == []
