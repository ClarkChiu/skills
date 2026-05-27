---
name: skill-finder
description: |
  Search the existing open agent-skills ecosystem (skills.sh) READ-ONLY — no
  install, no third-party code execution, no telemetry — and route every
  candidate to skill-auditor before any install decision. Use this whenever the
  user wants to find, discover, search, browse, look up, compare, or evaluate
  existing skills ("is there a skill for X", "find a skill that...", "what
  skills exist for...", "search skills", "show me skills about..."), or wants to
  inspect a published skill's SKILL.md before trusting it. Always prefer this
  over `npx skills find` or any CLI that downloads/executes vendor code: this
  skill only issues read-only HTTPS GETs to skills.sh and raw.githubusercontent.com.
  Discovery and evaluation ONLY — never install through this skill.
version: 1.0.0
permissions:
  file-read: false
  file-write: false
  network: true
  shell: true
---

# Skill Finder

Search what already exists in the open agent-skills ecosystem, fetch a
candidate's `SKILL.md` for inspection, and hand it to **skill-auditor** — all
without installing anything or running any vendor code.

The point is to keep the *trust* step (install) separate from the *discovery*
step (search). Discovery here is nothing but read-only HTTP GETs, so you can
look at any skill, audit it, and only then decide whether to install it through
whatever channel you trust. That ordering is the whole value: evaluate before
you trust, never the other way round.

## When to use

- The user wants to find/search/discover an existing skill for some task
- The user wants to see what skills exist in a domain, or compare popular ones
- The user wants to read a published skill's `SKILL.md` before installing it
- Any time you'd otherwise reach for `npx skills find` — use this instead

## What this skill must NOT do — and why

- **Never install.** No `npx skills add`, no `cp`/`ln -s` into a skills dir, no
  writing into `~/.claude/skills/`, `.agents/skills/`, etc. Installing a skill
  loads its `SKILL.md` into the agent prompt — the attack lands before any tool
  runs. So install is a trust decision the user makes *after* seeing an audit.
- **Never execute vendor code.** `npx skills find` downloads and runs Vercel's
  CLI and pings its telemetry endpoint with the query string. This skill avoids
  that entirely by hitting the public search API directly.
- **Never recommend on install-count alone.** Installs measure popularity, not
  safety. A 100k-install skill still gets audited before you suggest it.

## Endpoints — the only network this skill touches

| Host | Method | Purpose |
| --- | --- | --- |
| `skills.sh/api/search` | GET | search the registry |
| `raw.githubusercontent.com` | GET | fetch a candidate's raw `SKILL.md` |
| `api.github.com` | GET | (fallback) locate `SKILL.md` path / default branch |

All read-only, all HTTPS. No POST, no auth, no data sent beyond the search query.

## Step 1 — Search

The registry exposes a read-only JSON search endpoint. URL-encode the query.

```bash
q="react performance"
curl -fsSL "https://skills.sh/api/search?q=$(printf '%s' "$q" | jq -sRr @uri)" \
  | jq -r '.skills[] | "\(.installs)\t\(.source)@\(.skillId)"' \
  | sort -rn | head -25
```

Response shape (up to 100 results, semantic + fuzzy ranked):

```json
{ "query": "...", "searchType": "semantic",
  "skills": [ { "id": "owner/repo/skillId", "skillId": "...",
               "name": "...", "installs": 430213, "source": "owner/repo" } ] }
```

`source` is `owner/repo`; `id` is `source/skillId`. Present the top results to
the user as `installs · source@skillId` so they can pick.

## Step 2 — Fetch a candidate's SKILL.md (read-only)

Repo layouts vary, so try the common paths in order. This fetches text only —
it never executes anything.

```bash
# usage: fetch_skill owner/repo skillId
fetch_skill() {
  local src="$1" id="$2" b
  for b in main master; do
    for p in "skills/$id/SKILL.md" "$id/SKILL.md" "SKILL.md" ".claude/skills/$id/SKILL.md"; do
      if curl -fsSL "https://raw.githubusercontent.com/$src/$b/$p" 2>/dev/null; then return 0; fi
    done
  done
  echo "SKILL.md not found via common paths — locate it with the GitHub tree API:" >&2
  echo "  curl -s 'https://api.github.com/repos/$src/git/trees/HEAD?recursive=1' | jq -r '.tree[].path | select(endswith(\"SKILL.md\"))'" >&2
  return 1
}
```

If the common paths miss, fall back to the GitHub tree API line printed above to
find the real path, then re-fetch.

## Step 3 — Audit before recommending — always

Once you have the raw `SKILL.md` (and ideally the rest of the skill's files),
**invoke the `skill-auditor` skill on it.** Do not summarize the skill as "safe"
or suggest installing it until the audit produces a verdict.

Then present to the user:
1. What the skill does + its source + install count
2. The **skill-auditor verdict** (SAFE / SUSPICIOUS / DANGEROUS / BLOCK)
3. If they still want it, the install is *their* call, made *outside* this skill

For a deeper look, fetch every file in the skill dir, not just `SKILL.md` —
prompt injection and exfil patterns hide in references/ and scripts/ too. List
the tree with the GitHub API:

```bash
curl -s "https://api.github.com/repos/$src/git/trees/HEAD?recursive=1" \
  | jq -r '.tree[].path | select(startswith("skills/'"$id"'/"))'
```

## Example

**User:** "is there a skill for reviewing PRs? I want to vet it before I install."

1. Search → `npx skills`-free:
   `curl -fsSL "https://skills.sh/api/search?q=pr%20review" | jq ...`
2. Show top hits, e.g. `1156 · pytorch/pytorch@pr-review`.
3. `fetch_skill pytorch/pytorch pr-review` → raw `SKILL.md`.
4. Run **skill-auditor** on it → report verdict.
5. "Here's the audit. Verdict: ⚠️ SUSPICIOUS — telemetry endpoint found. Want
   the details, or shall I look at a cleaner alternative?"

The user never installed anything to find this out. That's the design.
