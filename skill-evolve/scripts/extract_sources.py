#!/usr/bin/env python3
"""Extract the reference sources a skill cites, from its own docs.

A well-kept skill records where its ideas came from (this repo's convention:
`references/attribution.md`). This script reads a skill's Markdown and pulls out the
upstream sources — GitHub repos especially — so the rest of skill-evolve can check them
for updates. It is deterministic: it only reads and classifies text, makes no network
calls, and never modifies the skill.

Usage:
    python3 extract_sources.py <skill-dir>        # one skill
    python3 extract_sources.py --all <repo-root>  # every */SKILL.md under a repo

Output: JSON on stdout — {skill, github_repos:[owner/repo...], other_urls:[...]}.
"""
import sys
import os
import re
import json

# GitHub repo URLs → normalize to owner/repo (strip .git, trailing slash, sub-paths).
# Exclude api.github.com by requiring the host to be a www/bare github.com (negative
# lookbehind on "api.").
_GH = re.compile(r"(?<!api\.)github\.com/([A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?)/([A-Za-z0-9._-]+)")
# Owners that are really GitHub API/route prefixes, not real accounts.
_SKIP_OWNER = {"repos", "sponsors", "apps", "orgs", "users", "search", "OWNER"}
_URL = re.compile(r"https?://[A-Za-z0-9./?#%&=:_~+-]+")


def find_sources(skill_dir):
    """Return (github_repos:set, other_urls:set) cited anywhere in the skill's docs."""
    texts = []
    # Sources can be cited in SKILL.md, the README (e.g. p2pscout records its inspiration
    # there), or any reference doc — scan all of them.
    for top in ("SKILL.md", "README.md"):
        p = os.path.join(skill_dir, top)
        if os.path.exists(p):
            texts.append(_read(p))
    refs = os.path.join(skill_dir, "references")
    if os.path.isdir(refs):
        for name in sorted(os.listdir(refs)):
            if name.endswith(".md"):
                texts.append(_read(os.path.join(refs, name)))
    blob = "\n".join(texts)

    repos = set()
    for m in _GH.finditer(blob):
        owner, repo = m.group(1), m.group(2).removesuffix(".git")
        # Skip obvious non-repo paths (e.g. github.com/owner with no repo, or anchors).
        if owner not in _SKIP_OWNER and repo and repo not in ("", "blob", "tree", "issues", "pull"):
            repos.add(f"{owner}/{repo}")
    other = set()
    for m in _URL.finditer(blob):
        url = m.group(0).rstrip(".,);")
        if "github.com" not in url:
            other.add(url)
    return repos, other


def _read(path):
    try:
        with open(path, encoding="utf-8") as fh:
            return fh.read()
    except OSError:
        return ""


def _one(skill_dir):
    repos, other = find_sources(skill_dir)
    return {
        "skill": os.path.basename(os.path.abspath(skill_dir)),
        "github_repos": sorted(repos),
        "other_urls": sorted(other),
    }


def main():
    args = sys.argv[1:]
    if not args:
        print("usage: extract_sources.py <skill-dir> | --all <repo-root>", file=sys.stderr)
        return 2
    if args[0] == "--all":
        root = args[1] if len(args) > 1 else "."
        out = []
        for name in sorted(os.listdir(root)):
            d = os.path.join(root, name)
            if os.path.exists(os.path.join(d, "SKILL.md")):
                out.append(_one(d))
        print(json.dumps(out, ensure_ascii=False, indent=2))
    else:
        print(json.dumps(_one(args[0]), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
