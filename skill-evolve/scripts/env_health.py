#!/usr/bin/env python3
"""Environment-health pre-pass for skill-evolve: probe each self-built skill's declared
external CLIs on THIS machine and report ok/missing/broken/timeout/error.

Deterministic, read-only, no network, no writes except stdout (mirrors mine_usage.py).
Borrows the taxonomy insight from Agent-Reach's probe.py: **broken != missing** — a shim
on PATH whose interpreter is gone (a stale pipx/uv venv after a Python upgrade) fails to
exec (FileNotFoundError, or exit 126/127) and gets a *reinstall* prescription, not a
"not installed" one. Report-only: it never installs, fixes, or modifies anything.

Deps live in agent-facing prose (not scripts), so they can't be auto-scanned reliably —
CLI_DEPS is a curated, human-judged map. Each dep is (name, kind): "cli" probes
`<name> --version`; "pymod" probes `python3 -c "import <name>"` (e.g. the opencc binding,
which is a Python package, not a CLI).
"""
import argparse, json, shutil, subprocess, sys

# Curated per-skill external dependency map, verified against each skill's source
# (fresh-context review, 2026-07-06). Skills with no external CLI are absent — e.g.
# html-diagram is self-contained; skill-curator only *describes* other skills' tools;
# translate delegates to chinese-typography and invokes nothing itself.
# Invariant: each CLI name uses a single kind across the map (see build_report).
CLI_DEPS = {
    "ig-reel":            [("ffmpeg", "cli"), ("ffprobe", "cli")],
    "p2pscout":           [("go", "cli"), ("aria2c", "cli")],       # downloads delegated to aria2c
    "social-card":        [("agent-browser", "cli"), ("convert", "cli")],
    "slide-deck":         [("playwright", "pymod"), ("pptx", "pymod")],  # export_pdf/extract_pptx
    "skill-auditor":      [("skillspector", "cli")],                # optional/best-effort; still informative
    "to-issues":          [("gh", "cli")],                          # gh issue create / auth
    "git-guardrails":     [("jq", "cli")],                          # hook parses tool_input.command with jq
    "chinese-typography": [("python3", "cli"), ("opencc", "pymod")],
    "humanizer":          [("opencc", "pymod")],                    # via chinese-typography normalize.py
}

# CLIs that don't accept --version; override the probe args here (verified on real tools).
_VERSION_ARGS = {
    "ffmpeg":  ["-version"],
    "ffprobe": ["-version"],
    "go":      ["version"],
}
_BROKEN_EXIT = {126, 127}   # shell: "found but not executable" / interpreter missing
TIMEOUT_S = 5


def _probe_cli(cmd):
    """Return (state, detail) for a binary CLI. broken != missing is the whole point."""
    if not shutil.which(cmd):
        return "missing", "not on PATH"
    args = [cmd] + _VERSION_ARGS.get(cmd, ["--version"])
    try:
        p = subprocess.run(args, capture_output=True, text=True, timeout=TIMEOUT_S)
    except FileNotFoundError:
        return "broken", "on PATH but exec failed (interpreter gone?)"
    except OSError as e:
        return "broken", f"exec error: {e}"
    except subprocess.TimeoutExpired:
        return "timeout", f">{TIMEOUT_S}s"
    if p.returncode in _BROKEN_EXIT:
        return "broken", f"exit {p.returncode} (found but not executable)"
    if p.returncode != 0:
        detail = " ".join((p.stderr or p.stdout or "").split())[:120]   # collapse to one line
        return "error", (detail or f"exit {p.returncode}")
    return "ok", ""


def _probe_pymod(mod):
    """Return (state, detail) for a Python module (e.g. the opencc binding)."""
    try:
        p = subprocess.run([sys.executable, "-c", f"import {mod}"],
                           capture_output=True, text=True, timeout=TIMEOUT_S)
    except subprocess.TimeoutExpired:
        return "timeout", f">{TIMEOUT_S}s"
    if p.returncode == 0:
        return "ok", ""
    return "missing", f"python module '{mod}' not importable"


def _probe(name, kind):
    return _probe_cli(name) if kind == "cli" else _probe_pymod(name)


def build_report(deps=None):
    deps = CLI_DEPS if deps is None else deps
    kinds = {}                                      # invariant: one kind per CLI name (tools is keyed by name)
    for items in deps.values():
        for name, kind in items:
            if kinds.setdefault(name, kind) != kind:
                raise ValueError(f"CLI '{name}' declared with two kinds: {kinds[name]} vs {kind}")
    results = {}                                    # (name, kind) -> (state, detail), one probe each
    for items in deps.values():
        for name, kind in items:
            results.setdefault((name, kind), None)
    results = {key: _probe(*key) for key in results}
    tools, per_skill = {}, {}
    for skill, items in deps.items():
        per_skill[skill] = {}
        for name, kind in items:
            state, detail = results[(name, kind)]
            per_skill[skill][name] = state
            t = tools.setdefault(name, {"state": state, "detail": detail, "used_by": []})
            t["used_by"].append(skill)
    for t in tools.values():
        t["used_by"] = sorted(set(t["used_by"]))
    return {"tools": tools, "skills": per_skill}


_ICON = {"ok": "✓", "missing": "✗", "broken": "⚠", "timeout": "⏱", "error": "✖"}
_HINT = {"broken": "stale shim; reinstall (uv tool install --force / pipx reinstall / repackage)"}
_ORDER = ["ok", "missing", "broken", "timeout", "error"]


def format_report(rep):
    lines = ["ENV HEALTH  (declared external CLIs · this machine)"]
    by_state = {s: [] for s in _ORDER}
    for name, t in sorted(rep["tools"].items()):
        by_state[t["state"]].append((name, t))
    for s in _ORDER:
        items = by_state[s]
        if s == "ok":
            lines.append(f"  {_ICON[s]} ok        {' '.join(n for n, _ in items) or '—'}")
            continue
        if not items:
            lines.append(f"  {_ICON[s]} {s:<9} —")
            continue
        for name, t in items:
            detail = f" ({t['detail']})" if t["detail"] else ""
            hint = f"   → {_HINT[s]}" if s in _HINT else ""
            lines.append(f"  {_ICON[s]} {s:<9} {name}{detail}  → used by: {', '.join(t['used_by'])}{hint}")
    return "\n".join(lines)


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="Probe self-built skills' declared external CLIs (read-only, no network).")
    ap.add_argument("--json", action="store_true", help="emit machine-readable JSON")
    a = ap.parse_args(argv)
    rep = build_report()
    if a.json:
        json.dump(rep, sys.stdout, ensure_ascii=False, indent=2)
        print()
    else:
        print(format_report(rep))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
