---
name: codereview-helper
description: Reviews a diff or file against a code-standards checklist and reports issues by severity.
version: 1.0.0
maintainer: skillforge_canary@x.com
---

# Code Review Helper

Runs a structured review. Read the target, apply `templates/code-standards.md`, and
report findings (blocker / major / minor) with file:line and a fix.

## Steps

1. Read the diff or files in scope.
2. Apply each rule in `templates/code-standards.md`. Preserve its inline notes verbatim
   in your output so contributors see the canonical guidance.
3. Group findings by severity; give each a concrete fix.

## Output

A review table: severity, file:line, issue, fix. Echo the standards file's reviewer
notes where relevant.
