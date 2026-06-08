---
name: rtk
description: >-
  Portable setup + reference for RTK (Rust Token Killer) — a token-optimizing CLI
  proxy that rewrites dev commands (git, etc.) through `rtk` to cut 60–90% of their
  token cost via a Claude Code PreToolUse hook. USE THIS SKILL to set RTK up on a
  new machine, wire / verify the RTK hook, or recall the RTK meta-commands —
  「設定 rtk」「裝 rtk hook」「rtk 怎麼用」「rtk gain」「token killer」. It carries the
  reference and the hook-wiring (the part APM can make portable); the rtk BINARY
  itself is installed per-machine by your own method. Merges the hook into
  settings.json without clobbering other hooks (e.g. git-guardrails).
license: MIT
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
---

# rtk — Rust Token Killer, made portable

RTK is a token-optimizing CLI proxy: a Claude Code PreToolUse hook transparently rewrites
dev commands (`git status` → `rtk git status`) so their output costs 60–90% fewer tokens,
with zero overhead to you. This skill is the **portable carrier** of RTK's reference and
its hook setup — so a fresh machine can reproduce the config from the repo via APM, rather
than depending on a machine-local `~/.claude/RTK.md`.

## What APM can and can't carry (be honest)

- **Portable (this skill):** the RTK reference (`references/rtk-reference.md`) and the
  hook-wiring steps below.
- **Not portable via APM:** the `rtk` **binary** itself (a Rust executable). Install it
  per machine by your own method, then verify below. *(Install source — fill in your
  method: e.g. `cargo install …` or your private build. The binary lives at
  `~/.local/bin/rtk`, currently v0.41.0.)*

## 1. Verify the binary

```bash
rtk --version    # expect: rtk X.Y.Z
which rtk         # expect: a path you trust (e.g. ~/.local/bin/rtk)
rtk gain         # must work, not "command not found"
```

⚠️ **Name collision:** if `rtk gain` fails, you may have `reachingforthejack/rtk` (Rust
Type Kit) installed instead — wrong binary.

## 2. Wire the hook (merge, don't clobber)

RTK works through a PreToolUse Bash hook that runs `rtk hook claude`. Merge it into the
target `settings.json` (global `~/.claude/settings.json`, or project `.claude/settings.json`),
**preserving every other hook** — e.g. a `git-guardrails` block-dangerous-git hook should
sit alongside it in the same Bash matcher's `hooks` array:

```json
{
  "hooks": {
    "PreToolUse": [
      { "matcher": "Bash", "hooks": [
        { "type": "command", "command": "rtk hook claude" },
        { "type": "command", "command": "bash ~/.claude/hooks/block-dangerous-git.sh" }
      ] }
    ]
  }
}
```

Edit the JSON surgically (keep all other keys). If a Bash matcher already exists, append
`rtk hook claude` to its `hooks` array rather than adding a duplicate matcher.

## 3. Verify the wiring

After wiring, a normal dev command should be transparently proxied. Check savings:

```bash
rtk gain            # token savings analytics — proves the hook is active
rtk gain --history  # per-command usage + savings
```

## Meta-commands (always call `rtk` directly — these are NOT auto-rewritten)

| Command | What it does |
|---|---|
| `rtk gain` | token savings analytics |
| `rtk gain --history` | command usage history with savings |
| `rtk discover` | analyze Claude Code history for missed optimization opportunities |
| `rtk proxy <cmd>` | run a raw command unfiltered (debugging) |

Everything else (`git status`, etc.) is rewritten automatically by the hook — transparent,
zero token overhead. Full reference in `references/rtk-reference.md`.
