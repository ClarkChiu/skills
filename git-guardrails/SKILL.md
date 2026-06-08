---
name: git-guardrails
description: >-
  Install a Claude Code PreToolUse hook that blocks destructive git commands
  (force push, reset --hard, clean -f, branch -D, discard-all, delete remote
  branch) before they run. USE THIS SKILL when the user wants to guard against
  dangerous git operations, set up git safety rails, prevent accidental history
  loss, or says 「裝 git 防呆」「擋危險 git 指令」「git guardrails」「防止誤刪 git」.
  It MERGES into the existing settings.json without clobbering other hooks (e.g.
  an RTK hook), and can install at project scope (travels via git) or global
  scope (protects every project). Does NOT block pushing to main/master, and
  ALLOWS --force-with-lease (the safe force).
license: MIT
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
---

# git-guardrails — block destructive git before it runs

Claude Code can run `git` via Bash. One `git reset --hard` or `git push --force` at
the wrong moment loses work. This installs a **PreToolUse hook** that inspects every
Bash command and blocks the destructive git ones (exit 2) before they execute. The
hook is the portable artifact; this skill carries the hardened script and wires it in.

## What it blocks (and deliberately does not)

`scripts/block-dangerous-git.sh` blocks, anchored to a real command boundary so a git
command quoted in an echo or commit message is **not** falsely caught:

- `git push --force` / `-f` — **but allows `--force-with-lease`** (the safe force).
- `git reset --hard`, `git clean -f…`, `git branch -D`, `git checkout .` / `git restore .`
  (discard all), `git push --delete` / `git push :branch` (delete remote branch).

It does **not** block pushing to `main`/`master` (committing to master is a normal
workflow here). Tune the `DANGEROUS_PATTERNS` in the script if your needs differ.

## Why a hook, not just a prompt rule

A prompt rule is advisory; a PreToolUse hook is enforced by the harness — it fires even
if the agent "forgets." Hooks live in `settings.json` (machine-local), so this skill
makes the *script* portable (ships in the repo, travels via APM/git) and provides the
one-time wiring step per machine.

## Install

Ask the user **scope** first:

- **Project** → `<repo>/.claude/settings.json` + copy the script to `<repo>/.claude/hooks/`.
  Travels via git; active only inside that repo.
- **Global** → `~/.claude/settings.json` + copy the script to `~/.claude/hooks/`.
  Protects every project; re-run once per machine.

Then:

1. **Copy the script** to the chosen `hooks/` dir:
   `cp <this-skill>/scripts/block-dangerous-git.sh <target>/hooks/ && chmod +x <target>/hooks/block-dangerous-git.sh`
2. **Read** the target `settings.json` (create `{}` if absent).
3. **MERGE** — add a PreToolUse entry for the `Bash` matcher. **Do not overwrite existing
   hooks.** If a `PreToolUse` Bash matcher already exists (e.g. an RTK hook), append this
   command to that matcher's `hooks` array; otherwise add a new matcher object:
   ```json
   {
     "hooks": {
       "PreToolUse": [
         { "matcher": "Bash", "hooks": [
           { "type": "command", "command": "rtk hook claude" },
           { "type": "command", "command": "bash <target>/hooks/block-dangerous-git.sh" }
         ] }
       ]
     }
   }
   ```
   Edit the JSON surgically (preserve every other key). Use absolute paths.
4. **Verify**: `printf '%s' '{"tool_input":{"command":"git push --force"}}' | bash <target>/hooks/block-dangerous-git.sh; echo "exit=$?"` → prints a BLOCKED message and `exit=2`. Then a benign command (`git status`) → `exit=0`.

## Uninstall

Remove that one command object from the `Bash` matcher's `hooks` array in
`settings.json` (leave the others), and delete the copied script. Do not remove the RTK
or any other hook.

## Test

`bash scripts/test_block_dangerous_git.sh` runs 17 cases (9 must-block, 8 must-allow,
including the echo / commit-message false-positive guards).
