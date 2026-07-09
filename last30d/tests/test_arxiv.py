"""arXiv lane: parse Atom into records. Intent: no engagement metric -> rank by recency
(date desc), filter to the window, map abs link. Network mocked."""
from contextlib import contextmanager

import conftest  # noqa: F401
from sources import arxiv

ATOM = """<?xml version="1.0"?>
<feed xmlns="http://www.w3.org/2005/Atom">
  <entry>
    <title>Older Paper</title>
    <published>2026-06-20T00:00:00Z</published>
    <summary>an older abstract</summary>
    <author><name>Alice</name></author>
    <link href="http://arxiv.org/abs/2606.11111" rel="alternate"/>
  </entry>
  <entry>
    <title>Newer Paper</title>
    <published>2026-07-05T00:00:00Z</published>
    <summary>a newer abstract</summary>
    <author><name>Bob</name></author>
    <link href="http://arxiv.org/abs/2607.22222" rel="alternate"/>
  </entry>
  <entry>
    <title>Out Of Window</title>
    <published>2026-01-01T00:00:00Z</published>
    <summary>too old</summary>
    <author><name>Carol</name></author>
    <link href="http://arxiv.org/abs/2601.33333" rel="alternate"/>
  </entry>
</feed>"""


@contextmanager
def _fake_urlopen(*_a, **_k):
    class R:
        def read(self_inner):
            return ATOM.encode()
    yield R()


def test_arxiv_ranks_recent_first_and_filters_window(monkeypatch):
    monkeypatch.setattr(arxiv.urllib.request, "urlopen", _fake_urlopen)
    out = arxiv.search("transformers", "2026-06-09", "2026-07-09", limit=25)
    assert [r["title"] for r in out] == ["Newer Paper", "Older Paper"], "not recency-ranked / window not applied"
    top = out[0]
    assert top["lane"] == "arxiv" and top["score_label"] == "arxiv"
    assert top["url"] == "http://arxiv.org/abs/2607.22222"
    assert top["date"] == "2026-07-05" and "Bob" in top["meta"]


def test_arxiv_empty_on_error(monkeypatch):
    def boom(*_a, **_k):
        raise OSError("down")
    monkeypatch.setattr(arxiv.urllib.request, "urlopen", boom)
    assert arxiv.search("x", "2026-06-09", "2026-07-09") == []
