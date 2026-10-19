"""Lane failures must say why (Rule 12). A failed lane still returns [] so the run goes on,
but a bare "0" reads as "nobody talked about it" — a wrong answer, not a missing one. So
each keyless lane records the reason in its SKIP dict, as the X and YouTube lanes do.
Network mocked."""
from contextlib import contextmanager

import pytest

import conftest  # noqa: F401
from sources import arxiv, github, hn

LANES = [hn, github, arxiv]
# A valid answer with no results, per lane.
EMPTY = {hn: b'{"hits": []}', github: b'{"items": []}',
         arxiv: b'<feed xmlns="http://www.w3.org/2005/Atom"></feed>'}
_ids = lambda m: m.__name__.split(".")[-1]  # noqa: E731


@pytest.mark.parametrize("mod", LANES, ids=_ids)
def test_failed_lane_records_why(monkeypatch, mod):
    monkeypatch.setitem(getattr(mod, "SKIP", {}), "reason", None)  # restored after the test
    def refused(*_a, **_k):
        raise OSError("connection refused")
    monkeypatch.setattr(mod.urllib.request, "urlopen", refused)
    assert mod.search("x", "2026-06-09", "2026-07-09") == []
    assert getattr(mod, "SKIP", {}).get("reason") == "OSError: connection refused"


@pytest.mark.parametrize("mod", LANES, ids=_ids)
def test_next_run_clears_an_old_reason(monkeypatch, mod):
    # A failure from an earlier run in the same process must not be blamed on a later run
    # that worked but found nothing.
    monkeypatch.setitem(mod.SKIP, "reason", "OSError: connection refused")

    @contextmanager
    def ok(*_a, **_k):
        class R:
            def read(self_inner):
                return EMPTY[mod]
        yield R()
    monkeypatch.setattr(mod.urllib.request, "urlopen", ok)
    assert mod.search("x", "2026-06-09", "2026-07-09") == []
    assert mod.SKIP["reason"] is None
