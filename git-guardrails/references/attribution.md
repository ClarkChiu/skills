# Attribution

`git-guardrails` is adapted from **mattpocock/skills** →
`misc/git-guardrails-claude-code` (MIT). The idea — a PreToolUse hook that blocks
destructive git — is Matt's; the script here is an **original, hardened rewrite**, no
files copied. Full evaluation of the source collection is in
`research/audits/2026-06-08-mattpocock-skills.md` (verdict: 🟨 vendor & customize).

## What changed vs upstream

- **Anchored patterns.** Upstream substring-greps the raw command (`"git push"` etc.),
  which false-positives on a commit message / echo that merely mentions a git command,
  and is trivially bypassable. This rewrite anchors each pattern to a real command
  boundary (line start or after `;` `&&` `||` `|` `(`).
- **Allows `--force-with-lease`.** Upstream blocks all force pushes; this blocks only the
  raw `--force` / `-f` and lets `--force-with-lease` through (the safe force — it fails if
  the remote moved). Blocking it would push the user toward the more dangerous raw force.
- **Does not block push to main/master.** This user commits to master as normal workflow;
  blocking it would break their day-to-day.
- **Merge-not-clobber install.** The SKILL.md install step merges into the existing
  `settings.json` PreToolUse Bash matcher, explicitly preserving other hooks (e.g. the
  user's RTK hook) — rather than assuming a fresh hooks block.
- **Bundled test** (`scripts/test_block_dangerous_git.sh`, 17 cases) — upstream ships none.

## Re-sync

`sources.lock` pins the upstream at the reviewed commit. On `skill-evolve`, diff for new
dangerous-pattern ideas worth folding in; keep the local hardening (anchoring,
force-with-lease, no-master-block).
