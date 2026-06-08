#!/usr/bin/env bash
# Test the guardrail: feed each command as PreToolUse JSON, assert exit code.
# exit 2 = blocked, 0 = allowed. Run: bash test_block_dangerous_git.sh
set -uo pipefail
HOOK="$(dirname "$0")/block-dangerous-git.sh"
fail=0

check() {  # check <expect:block|allow> <command>
  local expect="$1" cmd="$2" code
  printf '{"tool_input":{"command":%s}}' "$(printf '%s' "$cmd" | jq -R -s .)" \
    | bash "$HOOK" >/dev/null 2>&1
  code=$?
  local got="allow"; [ "$code" -eq 2 ] && got="block"
  if [ "$got" = "$expect" ]; then
    echo "ok   [$expect] $cmd"
  else
    echo "FAIL [want $expect, got $got] $cmd"; fail=1
  fi
}

# must BLOCK
check block 'git push --force'
check block 'git push -f origin main'
check block 'git reset --hard HEAD~1'
check block 'git clean -fd'
check block 'git branch -D feature'
check block 'git checkout .'
check block 'git restore .'
check block 'git push origin --delete feature'
check block 'cd /tmp && git reset --hard'

# NOTE: an `rtk `-prefixed form (e.g. `rtk git reset --hard`) is intentionally NOT blocked.
# The agent types plain `git reset --hard` (rtk rewrites transparently), and both hooks see
# that original command — so it is caught directly. Anchoring is kept so quoted text like
# the line below is NOT a false positive:
check allow 'printf "%s" "rtk git push --force"'

# must ALLOW
check allow 'git push'
check allow 'git push --force-with-lease'
check allow 'git status'
check allow 'git reset HEAD~1'
check allow 'git checkout feature-branch'
check allow 'git commit -m "fix: document git push --force pitfalls"'
check allow 'echo "git push --force is dangerous"'
check allow 'git clean -n'

[ "$fail" -eq 0 ] && echo "ALL PASS" || { echo "SOME FAILED"; exit 1; }
