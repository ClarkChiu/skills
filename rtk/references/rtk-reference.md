# RTK reference — Rust Token Killer

Token-optimized CLI proxy (60–90% savings on dev operations). This is the portable copy of
the machine-local `~/.claude/RTK.md`, carried in the repo so it travels via APM/git.

## Meta-commands (always use `rtk` directly)

```bash
rtk gain              # Show token savings analytics
rtk gain --history    # Show command usage history with savings
rtk discover          # Analyze Claude Code history for missed opportunities
rtk proxy <cmd>       # Execute raw command without filtering (for debugging)
```

## Installation verification

```bash
rtk --version         # Should show: rtk X.Y.Z
rtk gain              # Should work (not "command not found")
which rtk             # Verify correct binary
```

⚠️ **Name collision:** if `rtk gain` fails, you may have `reachingforthejack/rtk`
(Rust Type Kit) installed instead.

## Hook-based usage

All other commands are automatically rewritten by the Claude Code PreToolUse hook
(`rtk hook claude`). Example: `git status` → `rtk git status` (transparent, 0 token
overhead). The hook coexists with other PreToolUse Bash hooks (e.g. `git-guardrails`) —
keep both in the matcher's `hooks` array.

## Binary install (per machine — not carried by APM)

The `rtk` binary is a Rust executable installed outside APM. Record your install method
here so a fresh machine is reproducible (e.g. `cargo install <…>`, or a private build),
then run the verification block above.
