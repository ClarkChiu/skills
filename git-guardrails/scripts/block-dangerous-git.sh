#!/usr/bin/env bash
# PreToolUse Bash hook for Claude Code: block destructive git commands.
#
#   exit 2  -> block the tool call (message on stderr is shown to the agent)
#   exit 0  -> allow
#
# Hardened over a naive substring grep:
#  - patterns are anchored to a COMMAND BOUNDARY (start, or after ; && || | ( )
#    so a git command quoted inside an echo or a commit message is NOT blocked;
#  - `--force-with-lease` is ALLOWED (it is the safe force — it fails if the
#    remote moved), only the raw `--force` / `-f` is blocked;
#  - pushing to main/master is NOT blocked (this user commits to master).
#
# Reads the hook JSON on stdin, inspects .tool_input.command. Needs `jq`.
set -euo pipefail

INPUT="$(cat)"
COMMAND="$(printf '%s' "$INPUT" | jq -r '.tool_input.command // empty' 2>/dev/null || true)"
[ -z "$COMMAND" ] && exit 0

# command boundary: line start, or just after a shell separator
B='(^|[;&|(]|&&|\|\|)[[:space:]]*'

block() {
  printf "BLOCKED: '%s' matches a destructive git pattern (%s). The user's git-guardrails hook prevented this. If it is truly intended, ask the user to run it manually.\n" "$COMMAND" "$1" >&2
  exit 2
}

has() { printf '%s' "$COMMAND" | grep -Eq -- "$1"; }

# force push — but allow --force-with-lease
if has "${B}git[[:space:]]+push\b" \
   && has '(--force([[:space:]]|=|$)|(^|[[:space:]])-f([[:space:]]|=|$))' \
   && ! has '--force-with-lease'; then
  block "force push"
fi

has "${B}git[[:space:]]+reset\b[^;&|]*--hard"            && block "reset --hard"
has "${B}git[[:space:]]+clean\b[^;&|]*(-[a-zA-Z]*f|--force)" && block "clean -f"
has "${B}git[[:space:]]+branch\b[^;&|]*(-[a-zA-Z]*D)"    && block "branch -D (force delete)"
has "${B}git[[:space:]]+(checkout|restore)\b[^;&|]*([[:space:]]\.([[:space:]]|$)|--[[:space:]]+\.)" && block "discard all working changes"
has "${B}git[[:space:]]+push\b[^;&|]*(--delete|[[:space:]]:[A-Za-z])" && block "delete remote branch"

exit 0
