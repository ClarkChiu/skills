#!/usr/bin/env python3
"""Assert-based self-check for mine_usage.py (no framework). Run: python3 test_mine_usage.py

Fixtures mirror REAL transcript shapes (verified against ~/.claude/projects):
attributionSkill appears only on ASSISTANT lines; slash-command lines lack
promptSource=="typed". Tests encode intent, not the implementation's convenience.
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import mine_usage as mu

FIX = os.path.join(HERE, "fixtures", "usage")


def _friction(d):
    return [p for s in d["sessions"] for p in s["prompts"] if p["friction"]]


def test_extract_and_skip():
    d = mu.build_digest(FIX, lookback_hours=0, max_sessions=0, cap_prompt=500, redact=False)
    assert d["session_count"] == 2, d["session_count"]
    assert d["skipped_lines"] >= 1, "malformed line must be counted"
    assert {s["session_id"] for s in d["sessions"]} == {"sess1", "sess2"}


def test_tool_result_excluded():
    d = mu.build_digest(FIX, 0, 0, 500, False)
    s1 = next(s for s in d["sessions"] if s["session_id"] == "sess1")
    assert len(s1["prompts"]) == 2, s1["prompts"]  # pcap + 日誌偏好; tool_result excluded
    assert all("output" not in p["text"] for p in s1["prompts"])


def test_slash_command_noise_excluded():
    # A non-typed user line (slash-command expansion) must NOT become a prompt.
    d = mu.build_digest(FIX, 0, 0, 500, False)
    assert all("<command-name>" not in p["text"]
               for s in d["sessions"] for p in s["prompts"]), "slash-command noise leaked"


def test_friction_skill_context_from_preceding_assistant():
    # #1: skill_context must come from the ASSISTANT turn (user lines carry no attributionSkill).
    d = mu.build_digest(FIX, 0, 0, 500, False)
    fric = _friction(d)
    assert len(fric) == 1, [p["text"] for p in fric]          # only the 不對…重來 line
    assert "不對" in fric[0]["text"]
    assert fric[0]["skill_context"] == "chinese-typography", fric[0]["skill_context"]


def test_friction_requires_immediate_adjacency():
    # #3: a correction cue NOT immediately after an assistant turn is NOT friction.
    d = mu.build_digest(FIX, 0, 0, 500, False)
    s2 = next(s for s in d["sessions"] if s["session_id"] == "sess2")
    lone = [p for p in s2["prompts"] if p["text"] == "重來"]
    assert lone and lone[0]["friction"] is False, "non-adjacent cue must not be friction"


def test_correction_cues_tightened():
    # #3: ambiguous words are no longer correction cues; strong ones still are.
    assert not mu.CORRECTION_RE.search("我其實很好奇這個")
    assert not mu.CORRECTION_RE.search("這不是上游安裝的嗎")
    assert mu.CORRECTION_RE.search("不對，重來")


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
    assert mu.build_digest(FIX, 0, 0, 500, False) == mu.build_digest(FIX, 0, 0, 500, False)


def test_no_network_imports():
    src = open(os.path.join(HERE, "mine_usage.py"), encoding="utf-8").read()
    for bad in ("import socket", "import requests", "urllib.request", "http.client", "urlopen"):
        assert bad not in src, f"network surface present: {bad}"


if __name__ == "__main__":
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for fn in fns:
        fn(); print("ok:", fn.__name__)
    print(f"ALL {len(fns)} CHECKS PASSED")
