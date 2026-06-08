---
name: to-issues
description: >-
  Turn a plan, spec, or PRD into independently-grabbable GitHub issues — vertical
  "tracer-bullet" slices in dependency order — and publish them with `gh` AFTER
  the user confirms the list. The natural downstream of `design-gate`: design-gate
  emits a task plan → to-issues files it as issues an engineer or agent can pick up.
  USE THIS SKILL when the user wants to break a plan into issues, file GitHub
  issues from a spec/PRD, says 「拆成 issue」「把計畫發成 GitHub issue」「開一批 issue」
  「to issues」. Always shows the full issue list for confirmation before creating
  anything. Do NOT use to plan/design (that's design-gate), or to manage an
  existing issue inbox (that would be a triage skill).
license: MIT
allowed-tools:
  - Read
  - Bash
---

# to-issues — a plan becomes grabbable GitHub issues

Takes a plan / spec / PRD and turns it into a set of GitHub issues, each a **vertical
slice** small enough for one person (or one agent) to grab and finish independently,
ordered by dependency. Publishing is gated: **you see the full list and approve it before
a single issue is created.**

This is the downstream of `design-gate` — design-gate settles the design and emits a task
plan; to-issues publishes that plan. It does not re-plan.

## The slicing rule — tracer-bullet vertical slices

- Each issue is a **thin end-to-end slice that delivers something testable**, not a
  horizontal layer ("all the DB", "all the UI"). A slice should be independently grabbable:
  someone can pick it up without first finishing three others.
- Name dependencies explicitly ("blocked by #N") and order the list so the earliest issues
  unblock the rest. Prefer a walking skeleton first (one thin slice that runs end to end),
  then widen.
- Keep each issue small — if it can't be described in a title + a few acceptance bullets,
  split it.

## Each run

1. **Read the source** — the plan/spec/PRD (or the current conversation if that's the
   plan). If it's vague, ask one or two questions; don't invent scope.
2. **Slice** into vertical issues. For each: a clear title, a 1-line goal, 2–5 acceptance
   criteria, and dependencies. Order by dependency.
3. **Confirm — show the FULL list first.** Present the issues (titles + slices +
   dependency order) as a preview and **ask the user to approve or adjust**. Create nothing
   yet.
4. **Publish** only after approval, with the user's already-authenticated CLI:
   ```bash
   gh issue create --title "<title>" --body "<goal + acceptance + blocked-by>" --label "ready-for-agent"
   ```
   Create in dependency order; capture each issue number so later issues can reference
   "blocked by #N". (Use `glab` instead for GitLab.)
5. **Report** the created issue numbers + URLs.

## Guardrails

- **Never create issues before the user approves the list** — this writes to a real
  tracker.
- The skill uses your existing `gh`/`glab` session; it does not read or store tokens.
- If `gh` isn't authenticated, stop and tell the user to run `gh auth login` themselves.
- Don't duplicate issues that already exist — check (`gh issue list`) if unsure.

## Boundary

| Need | Use |
|---|---|
| Settle the design + produce the task plan | `design-gate` (upstream) |
| Build a sliced task test-first | `tdd` |
