"""Orchestrator CLI. Intent: only the requested --lanes run; --depth maps N; output goes
to stdout as markdown by default, JSON with --json, and to a file with --save. Lanes mocked."""
import json

import conftest  # noqa: F401
import last30d


def _rec(lane, score):
    return {"lane": lane, "title": f"{lane}-item", "url": f"https://{lane}", "score": score,
            "score_label": "x", "meta": "", "date": "2026-07-01", "excerpt": "",
            "top_comment": None, "relevance": 0.0}


def _patch_lanes(monkeypatch, calls):
    for name in last30d.ALL_LANES:
        mod = last30d._MOD[name]

        def make(n):
            def fake(topic, frm, to, limit=25, **kw):
                calls.append((n, limit))
                return [_rec(n, 100)]
            return fake
        monkeypatch.setattr(mod, "search", make(name))


def test_only_requested_lanes_run_and_depth_maps_N(monkeypatch, capsys):
    calls = []
    _patch_lanes(monkeypatch, calls)
    last30d.main(["Peter", "--depth", "quick", "--lanes", "hn,arxiv", "--as-of", "2026-07-09"])
    ran = {c[0] for c in calls}
    assert ran == {"hn", "arxiv"}, f"ran unexpected lanes: {ran}"
    assert all(c[1] == 10 for c in calls), "depth=quick did not map N=10"
    out = capsys.readouterr().out
    assert "## Hacker News" in out and "## arXiv" in out and "## Reddit" not in out


def test_json_flag_emits_valid_json(monkeypatch, capsys):
    _patch_lanes(monkeypatch, [])
    last30d.main(["Peter", "--lanes", "hn", "--json", "--as-of", "2026-07-09"])
    data = json.loads(capsys.readouterr().out)
    assert data["topic"] == "Peter" and data["lanes"]["hn"][0]["score"] == 100
    assert data["from"] == "2026-06-09" and data["to"] == "2026-07-09"


def test_save_writes_file(monkeypatch, tmp_path):
    _patch_lanes(monkeypatch, [])
    f = tmp_path / "out.md"
    last30d.main(["Peter", "--lanes", "hn", "--save", str(f), "--as-of", "2026-07-09"])
    assert f.exists() and "## Hacker News" in f.read_text()
