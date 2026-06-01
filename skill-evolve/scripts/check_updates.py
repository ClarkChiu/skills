#!/usr/bin/env python3
"""Check a skill's reference sources for updates against its sources.lock baseline.

Reads the GitHub repos a skill cites (via extract_sources), asks the GitHub API for each
repo's latest commit + release, and compares to the baseline recorded in the skill's
`sources.lock`. Reports what changed since you last looked. Deterministic: it gathers
facts only — judging whether a change is *worth adopting* is the agent's job, not this
script's (CLAUDE.md Rule 5).

Usage:
    python3 check_updates.py <skill-dir> [--json]

Set GITHUB_TOKEN in the environment to raise the API rate limit (recommended). The lock
file is NOT written here — bumping the baseline is a deliberate step after you've reviewed
the report, so the diff stays meaningful next time.

Exit: 0 normally (even with updates found); 2 on usage/IO error. Network/API errors are
reported loudly per-repo rather than failing silently (Rule 12).
"""
import sys
import os
import json
import datetime
import urllib.request
import urllib.error

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from extract_sources import find_sources  # noqa: E402

LOCK_NAME = "sources.lock"
API = "https://api.github.com/repos/{}"


def _api(path):
    req = urllib.request.Request(path, headers={"Accept": "application/vnd.github+json",
                                                "User-Agent": "skill-evolve"})
    tok = os.environ.get("GITHUB_TOKEN")
    if tok:
        req.add_header("Authorization", f"Bearer {tok}")
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.load(r)


def latest(repo):
    """Return {commit, commit_date, release} for a repo, or {error: ...} loudly."""
    out = {}
    try:
        c = _api(API.format(repo) + "/commits?per_page=1")
        if c:
            out["commit"] = c[0]["sha"][:12]
            out["commit_date"] = c[0]["commit"]["committer"]["date"][:10]
    except urllib.error.HTTPError as e:
        return {"error": f"HTTP {e.code} (rate limit? set GITHUB_TOKEN)" if e.code == 403
                else f"HTTP {e.code}"}
    except (urllib.error.URLError, KeyError, ValueError) as e:
        return {"error": str(e)}
    try:
        rel = _api(API.format(repo) + "/releases/latest")
        out["release"] = rel.get("tag_name")
    except urllib.error.HTTPError as e:
        out["release"] = None if e.code == 404 else f"err {e.code}"
    except (urllib.error.URLError, ValueError):
        out["release"] = None
    return out


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    as_json = "--json" in sys.argv[1:]
    write_lock = "--write-lock" in sys.argv[1:]
    if not args:
        print("usage: check_updates.py <skill-dir> [--json] [--write-lock]", file=sys.stderr)
        return 2
    skill_dir = args[0]
    repos, _ = find_sources(skill_dir)
    lock_path = os.path.join(skill_dir, LOCK_NAME)
    lock = {}
    if os.path.exists(lock_path):
        try:
            lock = json.load(open(lock_path, encoding="utf-8")).get("sources", {})
        except (ValueError, OSError) as e:
            print(f"WARNING: {lock_path} unreadable ({e}); treating every source as new.",
                  file=sys.stderr)

    rows = []
    for repo in sorted(repos):
        cur = latest(repo)
        base = lock.get(repo, {})
        if cur.get("error"):
            status = "error"
        elif not base:
            status = "new-source"            # cited but never baselined
        elif cur.get("commit") != base.get("commit"):
            status = "updated"
        else:
            status = "unchanged"
        rows.append({"repo": repo, "status": status,
                     "baseline": base.get("commit"), "latest": cur.get("commit"),
                     "latest_date": cur.get("commit_date"), "release": cur.get("release"),
                     "error": cur.get("error")})

    if as_json:
        print(json.dumps(rows, ensure_ascii=False, indent=2))
        return 0

    order = {"updated": 0, "new-source": 1, "error": 2, "unchanged": 3}
    rows.sort(key=lambda r: order.get(r["status"], 9))
    print(f"# {os.path.basename(os.path.abspath(skill_dir))} — {len(repos)} GitHub sources\n")
    for r in rows:
        tag = {"updated": "🔄 UPDATED", "new-source": "🆕 NEW (no baseline)",
               "error": "⚠️  ERROR", "unchanged": "✓  unchanged"}[r["status"]]
        line = f"{tag}  {r['repo']}"
        if r["status"] == "updated":
            line += f"  {r['baseline']} → {r['latest']} ({r['latest_date']})"
        elif r["status"] == "new-source":
            line += f"  latest {r['latest']} ({r['latest_date']})"
        elif r["status"] == "error":
            line += f"  {r['error']}"
        if r.get("release"):
            line += f"  [release {r['release']}]"
        print(line)
    upd = sum(1 for r in rows if r["status"] in ("updated", "new-source"))
    print(f"\n{upd} source(s) need a look. Read the changelogs, judge relevance, then "
          f"discuss with the user before changing anything.")

    if write_lock:
        new = {r["repo"]: {k: v for k, v in (("commit", r["latest"]),
                                             ("release", r["release"]), ("date", r["latest_date"]))
                           if v} for r in rows if r["latest"] and not r.get("error")}
        payload = {"_comment": "由 skill-evolve 維護：各參考來源上次看到的版本，用來偵測更新。"
                               "檢視報告後才更新（--write-lock）。",
                   "checked_at": datetime.date.today().isoformat(), "sources": new}
        with open(lock_path, "w", encoding="utf-8") as fh:
            json.dump(payload, fh, ensure_ascii=False, indent=2)
            fh.write("\n")
        errs = sum(1 for r in rows if r.get("error"))
        print(f"\n→ wrote baseline {lock_path}  ({len(new)} sources"
              + (f", {errs} skipped due to errors" if errs else "") + ")")
    return 0


if __name__ == "__main__":
    sys.exit(main())
