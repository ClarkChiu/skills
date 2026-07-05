#!/usr/bin/env python3
"""Assert-based self-check for mine_usage.py (no framework). Run: python3 test_mine_usage.py"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import mine_usage as mu

FIX = os.path.join(HERE, "fixtures", "usage")


def test_extract_and_skip():
    d = mu.build_digest(FIX, lookback_hours=0, max_sessions=0, cap_prompt=500, redact=False)
    assert d["session_count"] == 2, d["session_count"]
    assert d["skipped_lines"] >= 1, "malformed line must be counted"
    ids = {s["session_id"] for s in d["sessions"]}
    assert ids == {"sess1", "sess2"}, ids


def test_tool_result_excluded():
    d = mu.build_digest(FIX, 0, 0, 500, False)
    s1 = next(s for s in d["sessions"] if s["session_id"] == "sess1")
    # 2 typed prompts (pcap + 日誌偏好); the tool_result user line must NOT appear
    assert len(s1["prompts"]) == 2, s1["prompts"]
    assert all("output" not in p["text"] for p in s1["prompts"])


def test_friction_and_skill_context():
    d = mu.build_digest(FIX, 0, 0, 500, False)
    fric = [p for s in d["sessions"] for p in s["prompts"] if p["friction"]]
    assert any(p["skill_context"] == "chinese-typography" for p in fric), fric


def test_skill_invoked():
    d = mu.build_digest(FIX, 0, 0, 500, False)
    s2 = next(s for s in d["sessions"] if s["session_id"] == "sess2")
    assert "chinese-typography" in s2["skills_invoked"], s2["skills_invoked"]


def test_gap_recurs_across_sessions():
    d = mu.build_digest(FIX, 0, 0, 500, False)
    hits = sum(1 for s in d["sessions"]
               if any("NAT binding" in p["text"] for p in s["prompts"]))
    assert hits >= 2, hits


def test_redact():
    dr = mu.build_digest(FIX, 0, 0, 500, redact=True)
    texts = [p["text"] for s in dr["sessions"] for p in s["prompts"]]
    assert any("«redacted»" in t for t in texts), "secret must be masked"
    assert not any("FAKEtestSECRETforREDACTIONcheck000000000" in t for t in texts), "raw secret leaked"


def test_deterministic():
    a = mu.build_digest(FIX, 0, 0, 500, False)
    b = mu.build_digest(FIX, 0, 0, 500, False)
    assert a == b


def test_no_network_imports():
    src = open(os.path.join(HERE, "mine_usage.py"), encoding="utf-8").read()
    for bad in ("import socket", "import requests", "urllib.request", "http.client", "urlopen"):
        assert bad not in src, f"network surface present: {bad}"


if __name__ == "__main__":
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for fn in fns:
        fn(); print("ok:", fn.__name__)
    print(f"ALL {len(fns)} CHECKS PASSED")
