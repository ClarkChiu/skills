---
name: handover
description: >-
  Package the current session into a handover document a fresh, zero-memory
  conversation can act on: elevator pitch, three-state progress (verified /
  unverified / not started), decisions with rationale, dead ends, one first
  action, dependency-ordered tasks with verifiable acceptance criteria.
  Reference-don't-copy (paths + commit hashes — the repo stays the source of
  truth), redact secrets, end with a user review gate. Two modes by RECEIVER:
  repo mode writes .claude/handovers/<date>-<slug>.md with fresh git metadata;
  chat mode (receiver can't read files — e.g. a claude.ai web conversation)
  emits one paste-ready Markdown block with the essentials inlined. USE THIS
  SKILL when the user wants to wrap a session for a fresh start — "handover",
  "handoff", "交接", 「做交接清單」「我要開新對話」「把這個對話打包」— or when
  context is visibly filling (~40–60%) at a phase boundary (suggest it, don't
  auto-run). Do NOT use for in-place compression (that's built-in /compact),
  for permanent cross-session facts (CLAUDE.md / memory), or to produce a
  design+plan that doesn't exist yet (that's design-gate).
license: MIT
allowed-tools:
  - Bash
  - Read
  - Grep
  - Glob
  - Write
---

# handover — package the session so a fresh conversation can continue

A clean baton pass beats recursive compression: summaries-of-summaries distort
earlier reasoning, which is why the field is moving from auto-compaction to
explicit handoffs. This skill packages the **resumable core** of the current
session — not a transcript — so a successor with zero memory can continue.

## When to fire

- The user asks for a handover.
- Proactively **suggest** one at a phase boundary when context is visibly
  filling (~40–60%). The worst handover is the one written at the death
  rattle — don't wait until the window is nearly full. Suggest; never auto-run.

## Two modes — decided by the RECEIVER, not the current environment

Ask if unclear: **can the next session read this repository/filesystem?**

- **Repo mode** (successor opens the same project — the normal Claude Code
  case): write `.claude/handovers/<YYYY-MM-DD>-<slug>.md`. A handover is a
  baton, not an artifact — make sure the directory is git-ignored (check
  `.gitignore`; if not covered, append to `.git/info/exclude` rather than
  editing the versioned `.gitignore`). Get git metadata **fresh** (`git
  branch --show-current`, `git log -1 --format='%h %ad'`, `git status`) — never
  from memory.
- **Chat mode** (successor cannot read files — a claude.ai web conversation,
  another machine, another person): emit **one paste-ready Markdown block** in
  the reply, nothing written to disk. Reference-don't-copy **inverts**: inline
  the few essential snippets (keep them small), and turn every other reference
  into "re-upload <file>" or "in the Project knowledge". Metadata becomes the
  date plus which attachments the old conversation had.

## The document

Write it in the language of the conversation (Traditional Chinese stays
natural Taiwan Traditional). Sections, in order:

```
# Handover — <topic> (<YYYY-MM-DD>)
<metadata: date · branch · last commit hash — chat mode: date · attachments>
<host assumptions: produced by <host, e.g. Claude Code / OpenCode> · assumes the
 successor loads <CLAUDE.md / AGENTS.md / none> · external deps the tasks need
 (e.g. gh, ffmpeg, an MCP server) — the successor verifies this line on arrival>

## 1. Background & goal      — elevator pitch, 3–5 sentences: where we are,
                               where we're going, why
## 2. Current state          — THE MOST IMPORTANT SECTION
     · Done & VERIFIED       — with the exact command/method that verified each
     · Done but UNVERIFIED   — and the risk it carries
     · In progress           — exactly where it stopped, what the next motion was
     · File map              — path + one line on each file's role
## 3. Decisions & rationale  — what was decided, why, which alternatives were
                               rejected and why
## 4. Dead ends & gotchas    — tried-and-failed approaches, traps, misleading
                               symptoms; the biggest time-saver in the document
## 5. First action           — ONE concrete step the successor takes on arrival,
                               before reading the task list
## 6. Remaining tasks        — dependency order; each task names its own
                               verification (which test, which output)
## 7. Acceptance criteria    — verifiable definition of done: tests that must
                               pass, files that must exist, commands that prove
                               it. Never "works fine".
## 8. Open questions         — undecided points awaiting the user; do NOT
                               resolve them silently
## 9. Suggested skills       — which skills the successor should invoke and
                               when (e.g. tdd for the build loop,
                               verify-before-done before any completion claim).
                               Cross-host: list only skills the RECEIVER has —
                               self-built skills travel (APM/symlinks), host
                               built-ins do not (/compact, Explore, code-review,
                               schedule are Claude Code's); name the receiver's
                               equivalent or say "no equivalent, do manually"
Chain: continues-from <path of the previous handover>   — only when chained
```

## Hard rules (load-bearing)

1. **Only what actually happened.** Nothing invented, nothing extrapolated.
   If you are unsure whether something was decided, it goes in Open questions.
2. **Three-state honesty.** Verified / unverified / not-started are different
   states; collapsing them is how successors ship false greens (Rule 12).
3. **Reference, don't copy** (repo mode). Code, designs, diffs → path or
   commit hash. The repository is the source of truth; the handover is a map.
   Chat mode inverts this — see above.
4. **Redact.** API keys, passwords, tokens, PII never enter the document.
5. **Forward-looking beats backward.** Completed work lives in git; decisions,
   dead ends, and next steps are what the successor can't recover on their own.
6. **Review gate.** Present the document to the user for review — a wrong
   handover is worse than none. Do not declare the handover done yourself.
7. **Host-aware baton** (when the successor is a different agent — OpenCode,
   Hermes, Codex…). Same repo still means repo mode and the same canonical
   `.claude/handovers/` path (it's just a path — one place to look beats
   host-neutral naming). But: fill the host-assumptions metadata line; restrict
   suggested skills per rule 9 above; and treat facts recalled from Claude
   Code's auto-memory like chat mode — the receiver can't read that memory, so
   anything the task depends on gets inlined, not pointed at.

## How the successor consumes it

- Repo mode opener: `讀 .claude/handovers/<file> 接手` (or "read <path> and
  continue"). If the document has a `Chain:` line, read the predecessor too.
- Chat mode: paste the block as the first message, then re-attach the files it
  lists.

## Boundaries

- **vs built-in `/compact`**: compaction compresses in place — lossy, and
  recursive on repeat. handover is a reviewed, selective baton for a *fresh*
  session.
- **vs CLAUDE.md / memory**: those are the permanent layer for slow-changing
  truths. A handover is one session's baton. If a fact should outlive this
  task, it belongs there — flag it, don't bury it in the handover.
- **vs `design-gate`**: a handover *reports* state; it never invents a plan.
  If no plan exists, say so and point the successor at design-gate.
- **vs `verify-before-done`**: any "done & verified" line must already satisfy
  its gate — no fresh evidence, no claim.
