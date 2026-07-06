#!/usr/bin/env python3
"""Assert-based self-check for env_health.py (no framework). Run: python3 test_env_health.py

Fixtures are fake CLIs on a temp PATH. The load-bearing test: a shim that exists on
PATH but can't exec classifies as `broken`, NOT `missing` and NOT `ok` — the whole
reason this exists over a plain `which` check.
"""
import os, stat, sys, tempfile
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import env_health as eh

# --- fake CLIs on a temp PATH (module-level setup) ---
_D = tempfile.mkdtemp(prefix="envhealth-")


def _make(name, content):
    p = os.path.join(_D, name)
    with open(p, "w") as f:
        f.write(content)
    os.chmod(p, os.stat(p).st_mode | 0o111)


_make("fake_ok",       "#!/bin/sh\necho v1\n")
_make("fake_error",    "#!/bin/sh\necho boom 1>&2; exit 1\n")
_make("fake_multiline", "#!/bin/sh\nprintf 'line1\\nline2\\nline3\\n' 1>&2; exit 2\n")
_make("fake_broken",   "#!/nonexistent/interp\nx\n")   # on PATH + executable, but interp gone
_make("fake_timeout",  "#!/bin/sh\nsleep 3\n")
os.environ["PATH"] = _D + os.pathsep + os.environ["PATH"]
eh.TIMEOUT_S = 1   # keep the timeout test fast


def test_ok():
    st, _ = eh._probe_cli("fake_ok")
    assert st == "ok", st


def test_missing():
    st, _ = eh._probe_cli("definitely_not_a_real_cli_xyz")
    assert st == "missing", st


def test_broken_not_missing():
    # THE reason this exists over `which`: shim on PATH but exec fails → broken.
    st, detail = eh._probe_cli("fake_broken")
    assert st == "broken", (st, detail)


def test_error():
    st, _ = eh._probe_cli("fake_error")
    assert st == "error", st


def test_error_detail_is_one_line():
    # multi-line tool output must collapse to one line so the report stays readable.
    st, detail = eh._probe_cli("fake_multiline")
    assert st == "error", st
    assert "\n" not in detail and "line1" in detail, repr(detail)


def test_timeout():
    st, _ = eh._probe_cli("fake_timeout")
    assert st == "timeout", st


def test_pymod_ok():
    st, _ = eh._probe_pymod("json")   # always importable
    assert st == "ok", st


def test_pymod_missing():
    st, _ = eh._probe_pymod("no_such_module_zzz")
    assert st == "missing", st


def test_report_dedup_and_used_by():
    deps = {"skillA": [("fake_ok", "cli"), ("fake_broken", "cli")],
            "skillB": [("fake_ok", "cli")]}          # fake_ok shared → one probe, two users
    rep = eh.build_report(deps)
    assert rep["tools"]["fake_ok"]["state"] == "ok"
    assert set(rep["tools"]["fake_ok"]["used_by"]) == {"skillA", "skillB"}
    assert rep["tools"]["fake_broken"]["state"] == "broken"
    assert rep["skills"]["skillA"]["fake_broken"] == "broken"


def test_deterministic():
    deps = {"s": [("fake_ok", "cli"), ("json", "pymod")]}
    assert eh.build_report(deps) == eh.build_report(deps)


def test_cli_deps_wellformed():
    # every real map entry uses a valid kind, and no CLI name is declared with two kinds
    # (the build_report invariant — tools is keyed by name alone).
    kinds = {}
    for items in eh.CLI_DEPS.values():
        for name, kind in items:
            assert kind in ("cli", "pymod"), (name, kind)
            assert kinds.setdefault(name, kind) == kind, f"{name} declared with two kinds"


def test_build_report_rejects_mixed_kind():
    bad = {"a": [("x", "cli")], "b": [("x", "pymod")]}   # same name, two kinds → must fail loud
    try:
        eh.build_report(bad)
    except ValueError:
        return
    assert False, "build_report must reject a CLI name with two kinds"


def test_no_network_no_mutation():
    src = open(os.path.join(HERE, "env_health.py"), encoding="utf-8").read()
    for bad in ("import socket", "import requests", "urllib.request", "http.client", "urlopen"):
        assert bad not in src, f"network surface: {bad}"
    for bad in ("shutil.rmtree", "os.remove", "os.unlink", "os.rmdir"):
        assert bad not in src, f"mutation surface: {bad}"


if __name__ == "__main__":
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for fn in fns:
        fn(); print("ok:", fn.__name__)
    print(f"ALL {len(fns)} CHECKS PASSED")
