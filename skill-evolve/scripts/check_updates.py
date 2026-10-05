#!/usr/bin/env python3
"""Check a skill's reference sources for updates against its sources.lock baseline.

Reads the GitHub repos a skill cites (via extract_sources), asks the GitHub API for each
repo's latest commit + release, and compares to the baseline recorded in the skill's
`sources.lock`. Reports what changed since you last looked. Deterministic: it gathers
facts only — judging whether a change is *worth adopting* is the agent's job, not this
script's (CLAUDE.md Rule 5).

Usage:
    python3 check_updates.py <skill-dir> [--json]
    python3 check_updates.py <skill-dir> --write-lock   # bump the baseline (see below)
    python3 check_updates.py --selftest                 # self-check merge_lock, no network

Set GITHUB_TOKEN in the environment to raise the API rate limit (recommended). By default
the lock file is NOT written — bumping the baseline is a deliberate step after you've
reviewed the report, so the diff stays meaningful next time. `--write-lock` does write,
and it **merges**: this script owns only `commit`/`release`/`date`, and every hand-written
field in an entry (`license`, `vendored`, `note`, `ref`, `url`, `::` sub-skill keys)
survives untouched, as does any source whose lookup errored this run. See `merge_lock`.

Exit: 0 normally (even with updates found); 2 on usage/IO error. Network/API errors are
reported loudly per-repo rather than failing silently (Rule 12).
"""
import sys
import os
import json
import datetime
import urllib.request
import urllib.error
import urllib.parse
import re

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


def _same_commit(a, b):
    """True if two commit SHAs refer to the same commit, tolerating short vs full.

    A lock may store an abbreviated SHA (e.g. '5e8b249') while the API returns a
    longer one ('5e8b2491651e'). A plain `!=` then false-flags an unchanged repo
    as UPDATED on every run. Compare by prefix on the shorter of the two instead.
    """
    if not a or not b:
        return a == b
    n = min(len(a), len(b))
    return a[:n].lower() == b[:n].lower()


def _latest_is_older(repo, base, latest):
    """True if `latest` is an ancestor of the `base` baseline — not an update.

    Happens when a path-scoped lookup returns the last commit touching that path while
    the lock stored the repo HEAD from an earlier run (handover's ace-fca.md and
    session-handoff, 2026-10-05). Any lookup failure answers False: report, don't hide.
    """
    try:
        cmp = _api(API.format(repo) + f"/compare/{base}...{latest}")
    except (urllib.error.URLError, ValueError):
        return False
    return cmp.get("status") == "behind"


def split_key(key):
    """Split a lock key into (repo, subpath). 'owner/repo :: a/b' → ('owner/repo', 'a/b').

    Sub-skill keys pin one directory inside a monorepo, so the check must be path-scoped:
    the repo's newest commit says nothing about whether *that* skill moved.
    """
    repo, _, sub = key.partition("::")
    return repo.strip(), sub.strip()


def is_repo_key(repo):
    """True if this looks like an owner/repo we can query. Article URLs recorded as
    sources (e.g. a blog post) are not repos and must be reported, not queried."""
    return repo.count("/") == 1 and all(repo.split("/")) and not re.search(r"[\s:]", repo)


def latest(repo, subpath=""):
    """Return {commit, commit_date, release} for a repo, or {error: ...} loudly.

    With `subpath`, the commit is the newest one touching that path (tried bare and under
    `skills/`, which is where these upstreams keep their sub-skills).
    """
    out = {}
    try:
        q = "/commits?per_page=1"
        if subpath:
            c = _api(API.format(repo) + q + "&path=" + urllib.parse.quote(subpath))
            if not c:
                c = _api(API.format(repo) + q + "&path=" + urllib.parse.quote("skills/" + subpath))
            if not c:
                return {"error": f"no commits touch path '{subpath}' (moved or removed upstream?)"}
        else:
            c = _api(API.format(repo) + q)
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


def merge_lock(lock, rows):
    """Fold freshly-checked commits into an existing lock. Pure: dicts in, dict out.

    This tool owns exactly three fields (commit/release/date). Everything else in an
    entry is hand-written provenance — `license`, `vendored`, `note`, `ref`, `url`, and
    sub-skill `::` keys — and some of it is load-bearing (e.g. a "PolyForm Noncommercial
    — ideas only, never vendor" restriction on a repo that this project redistributes
    publicly). Rebuilding from scratch deleted all of it silently, together with any
    source whose API call failed that run. So: keep what we did not check.
    """
    new = {k: dict(v) if isinstance(v, dict) else v for k, v in lock.items()}
    for r in rows:
        if r.get("error") or not r.get("latest"):
            continue                          # unverified: leave the old baseline alone
        entry = new.get(r["repo"])
        if not isinstance(entry, dict):       # absent, or a hand-mangled scalar
            entry = {}
        entry["commit"] = r["latest"]
        if r.get("latest_date"):
            entry["date"] = r["latest_date"]
        # A repo that no longer has a release must not keep the OLD tag pinned to a NEW
        # commit — that reads as "v1.2.0 is this commit", which is false. Drop it instead.
        rel = r.get("release")
        if rel and not str(rel).startswith("err "):
            entry["release"] = rel
        else:
            entry.pop("release", None)
        new[r["repo"]] = entry
    return new


def _selftest() -> int:
    """No-framework self-check for merge_lock + the lock-key parsing (run via --selftest)."""
    # Lock-key parsing: a sub-skill key must split into repo + path, an article-style key
    # must be refused rather than queried as a repo. Regression guard for the 2026-09-17
    # bug where nine skills' upstreams were silently skipped (docs cite bare owner/repo).
    assert split_key("owner/repo") == ("owner/repo", "")
    assert split_key("owner/repo :: productivity/grilling") == ("owner/repo", "productivity/grilling")
    assert split_key("owner/repo::a/b") == ("owner/repo", "a/b")
    assert is_repo_key("owner/repo")
    assert not is_repo_key("blocktempo/20-claude-prompts-productivity :: x")
    assert not is_repo_key("owner")
    assert not is_repo_key("owner/repo extra")
    assert not is_repo_key("")
    # merge_lock must not invent a `commit` on a vendored-files entry that tracks
    # per-file commits (last30d): it may update, but the hand-written fields stay.
    vend = {"acme/vendored": {"copied_from_commit": "1111aaaa", "vendored": "FILES", "note": "keep"}}
    got = merge_lock(vend, [{"repo": "acme/vendored", "latest": "2222bbbb",
                             "latest_date": "2026-09-01", "release": None, "error": None}])
    assert got["acme/vendored"]["copied_from_commit"] == "1111aaaa", got
    assert got["acme/vendored"]["vendored"] == "FILES" and got["acme/vendored"]["note"] == "keep"

    lock = {
        "acme/upstream": {"commit": "aaaa1111", "date": "2026-01-01",
                          "license": "PolyForm Noncommercial 1.0.0 — 僅取方法，永不收檔",
                          "vendored": "METHOD ONLY — no files", "note": "baseline note"},
        "acme/flaky": {"commit": "cccc3333", "note": "keep me"},
        "acme/upstream :: sub-skill": {"commit": "dddd4444", "note": "sub-skill baseline"},
    }
    rows = [
        {"repo": "acme/upstream", "latest": "bbbb2222", "latest_date": "2026-08-05",
         "release": "v2.0.0", "error": None},
        {"repo": "acme/flaky", "latest": None, "latest_date": None,
         "release": None, "error": "404"},
        {"repo": "acme/brand-new", "latest": "eeee5555", "latest_date": "2026-08-05",
         "release": None, "error": None},
    ]
    rows += [
        # errored AND not previously in the lock: must NOT be invented as a junk entry
        {"repo": "acme/never-seen", "latest": None, "latest_date": None,
         "release": None, "error": "timeout"},
        # release disappeared upstream: the old tag must not stay pinned to a new commit
        {"repo": "acme/detagged", "latest": "ffff6666", "latest_date": "2026-08-05",
         "release": None, "error": None},
        # a release lookup that failed yields an "err ..." string — not a tag
        {"repo": "acme/errtag", "latest": "9999aaaa", "latest_date": "2026-08-05",
         "release": "err 500", "error": None},
        # a hand-mangled scalar entry that IS being updated — must not crash
        {"repo": "acme/scalar", "latest": "7777bbbb", "latest_date": "2026-08-05",
         "release": None, "error": None},
    ]
    lock["acme/detagged"] = {"commit": "0000zzzz", "release": "v1.2.0", "note": "had a tag"}
    lock["acme/scalar"] = "hand-mangled"      # must not crash merge_lock
    out = merge_lock(lock, rows)
    up = out["acme/upstream"]
    assert up["commit"] == "bbbb2222" and up["date"] == "2026-08-05", f"A: bump failed: {up}"
    assert up["release"] == "v2.0.0", f"A: release not recorded: {up}"
    # B first, deliberately: this is the whole reason merge_lock exists, so a regression
    # that rebuilds from scratch should fail with a message naming the licence guardrail
    # rather than whichever unrelated assertion happens to sit earliest.
    assert up.get("license", "").startswith("PolyForm"), \
        f"B: hand-written licence guardrail was destroyed by a routine bump: {up}"
    assert up.get("vendored") == "METHOD ONLY — no files" and up.get("note") == "baseline note", \
        f"B: provenance fields lost: {up}"
    assert "acme/never-seen" not in out, \
        f"G: an errored, never-baselined source must not be invented: {out.get('acme/never-seen')}"
    assert "release" not in out["acme/detagged"], \
        f"H: stale release left pinned to a new commit: {out['acme/detagged']}"
    assert out["acme/detagged"]["note"] == "had a tag", "H: provenance lost while dropping release"
    assert "release" not in out["acme/errtag"], \
        f"I: an 'err ...' string was written as if it were a tag: {out['acme/errtag']}"
    assert out["acme/scalar"] == {"commit": "7777bbbb", "date": "2026-08-05"}, \
        f"J: a scalar lock value being updated must be replaced, not crash: {out['acme/scalar']}"
    assert out["acme/flaky"] == {"commit": "cccc3333", "note": "keep me"}, \
        f"C: a source whose check errored must keep its old baseline, got {out['acme/flaky']}"
    assert out["acme/upstream :: sub-skill"]["note"] == "sub-skill baseline", \
        "D: '::' sub-skill entries are not in rows and must survive"
    assert out["acme/brand-new"]["commit"] == "eeee5555", "E: new source not added"
    assert lock["acme/upstream"]["commit"] == "aaaa1111", "F: input lock was mutated"
    # K: a "latest" that is an ancestor of the baseline must not read as UPDATED, and a
    # failed compare must fall back to reporting (False), never to silently "unchanged".
    global _api
    real_api = _api
    try:
        _api = lambda path: {"status": "behind"}
        assert _latest_is_older("o/r", "base", "older"), "K: ancestor not recognised"
        _api = lambda path: {"status": "ahead"}
        assert not _latest_is_older("o/r", "base", "newer"), "K: a real update was hidden"

        def _boom(path):
            raise urllib.error.URLError("offline")
        _api = _boom
        assert not _latest_is_older("o/r", "base", "x"), "K: a failed compare hid an update"
    finally:
        _api = real_api
    print("selftest OK")
    return 0


def main():
    if "--selftest" in sys.argv[1:]:
        return _selftest()
    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    as_json = "--json" in sys.argv[1:]
    write_lock = "--write-lock" in sys.argv[1:]
    if not args:
        print("usage: check_updates.py <skill-dir> [--json] [--write-lock]", file=sys.stderr)
        return 2
    skill_dir = args[0]
    repos, _ = find_sources(skill_dir)
    lock_path = os.path.join(skill_dir, LOCK_NAME)
    lock, lock_comment = {}, None
    if os.path.exists(lock_path):
        try:
            payload = json.load(open(lock_path, encoding="utf-8"))
            lock = payload.get("sources", {})
            lock_comment = payload.get("_comment")
        except (ValueError, OSError) as e:
            print(f"WARNING: {lock_path} unreadable ({e}); treating every source as new.",
                  file=sys.stderr)

    # The docs are not the only place a source is recorded: attribution.md often cites an
    # upstream as bare `owner/repo` (no URL) or as `owner/repo :: sub-skill`, which the URL
    # scanner cannot see. The lock is the other half of the record, so check the union —
    # otherwise a skill with a full baseline silently reports "0 GitHub sources".
    keys = set(repos) | set(lock)
    lock_only = sorted(set(lock) - set(repos))
    if lock and not repos:
        print(f"WARNING: no source URL found in this skill's docs, but {len(lock)} "
              f"baseline(s) exist in {LOCK_NAME} — checking those. Cite them as full "
              f"https://github.com/owner/repo URLs so extraction stops depending on the lock.",
              file=sys.stderr)

    rows = []
    for key in sorted(keys):
        repo, sub = split_key(key)
        base = lock.get(key, {}) if isinstance(lock.get(key), dict) else {}
        # A non-GitHub `url` means the "source" is an article or page recorded under a
        # repo-shaped key; querying it as a repo just yields a confusing 404/401.
        url = str(base.get("url") or "")
        if not is_repo_key(repo) or (url and "github.com" not in url):
            rows.append({"repo": key, "status": "skipped", "baseline": base.get("commit"),
                         "latest": None, "latest_date": None, "release": None,
                         "error": f"not a GitHub repo ({url or 'no repo path'}) — re-read it by hand"})
            continue
        cur = latest(repo, sub)
        if cur.get("error"):
            status = "error"
        elif not base:
            status = "new-source"            # cited but never baselined
        elif _same_commit(cur.get("commit"),
                          base.get("commit") or base.get("copied_from_commit")):
            status = "unchanged"
        elif _latest_is_older(repo, base.get("commit") or base.get("copied_from_commit"),
                              cur.get("commit")):
            status = "unchanged"            # baseline is newer than the path's last commit
        else:
            status = "updated"
        rows.append({"repo": key, "status": status,
                     "baseline": base.get("commit") or base.get("copied_from_commit"),
                     "latest": cur.get("commit"),
                     "latest_date": cur.get("commit_date"), "release": cur.get("release"),
                     "error": cur.get("error")})

    if as_json:
        print(json.dumps(rows, ensure_ascii=False, indent=2))
        return 0

    order = {"updated": 0, "new-source": 1, "error": 2, "skipped": 3, "unchanged": 4}
    rows.sort(key=lambda r: order.get(r["status"], 9))
    extra = f" (+{len(lock_only)} from {LOCK_NAME})" if lock_only else ""
    print(f"# {os.path.basename(os.path.abspath(skill_dir))} — {len(keys)} sources"
          f"{extra}\n")
    for r in rows:
        tag = {"updated": "🔄 UPDATED", "new-source": "🆕 NEW (no baseline)",
               "error": "⚠️  ERROR", "skipped": "⏭️  SKIPPED",
               "unchanged": "✓  unchanged"}[r["status"]]
        line = f"{tag}  {r['repo']}"
        if r["status"] == "updated":
            line += f"  {r['baseline']} → {r['latest']} ({r['latest_date']})"
        elif r["status"] == "new-source":
            line += f"  latest {r['latest']} ({r['latest_date']})"
        elif r["status"] in ("error", "skipped"):
            line += f"  {r['error']}"
        if r.get("release"):
            line += f"  [release {r['release']}]"
        print(line)
    upd = sum(1 for r in rows if r["status"] in ("updated", "new-source"))
    print(f"\n{upd} source(s) need a look. Read the changelogs, judge relevance, then "
          f"discuss with the user before changing anything.")

    if write_lock:
        new = merge_lock(lock, rows)          # merge, never rebuild — see merge_lock()
        payload = {"_comment": lock_comment or
                   "由 skill-evolve 維護：各參考來源上次看到的版本，用來偵測更新。"
                   "檢視報告後才更新（--write-lock）。",
                   "checked_at": datetime.date.today().isoformat(), "sources": new}
        with open(lock_path, "w", encoding="utf-8") as fh:
            json.dump(payload, fh, ensure_ascii=False, indent=2)
            fh.write("\n")
        errs = sum(1 for r in rows if r.get("error"))
        bumped = sum(1 for r in rows if r["latest"] and not r.get("error"))
        # Report what was TOUCHED vs what the file holds — the old message printed the
        # whole merged lock as if every entry had just been re-checked.
        print(f"\n→ merged into {lock_path}  ({bumped} of {len(rows)} checked source(s) "
              f"updated; {len(new)} entries in the file"
              + (f"; {errs} left at their old baseline due to errors" if errs else "") + ")")
    return 0


if __name__ == "__main__":
    sys.exit(main())
