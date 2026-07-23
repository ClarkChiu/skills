# Attribution

`handover` is an **original rewrite** — no files copied — that composes methods
from three diffable upstreams (pinned in `sources.lock`) plus several prose
sources (not diffable, recorded here only). Evaluated 2026-07-23; verdicts in
`research/2026-07-23-skill-research-log.md`.

## Method sources (pinned in sources.lock)

- **mattpocock/skills → `skills/productivity/handoff`** (MIT). Upstream is a
  ~15-line skill; what we adopted is its three sharpest rules: **reference,
  don't duplicate** (point at specs/plans/commits by path or hash instead of
  copying), a **suggested-skills** section directing the successor's first
  invocations, and **redact sensitive information**. Rejected: writing to the
  OS temp directory (WSL2 `/tmp` does not survive a reboot; we use
  `.claude/handovers/`, git-ignored).
- **softaworks/agent-toolkit → `skills/session-handoff`** (MIT). Adopted the
  **section skeleton** (current state / important context / decisions *with
  rationale* / immediate next steps / gotchas), **handover chaining**
  (`continues-from` breadcrumbs), and the spirit of its validation gate (no
  `[TODO]` placeholders, secrets block completion) — reimplemented as prose
  rules, not scripts. Rejected: the Python scripting/scoring machinery — this
  stays a pure-prompt skill.
- **humanlayer/advanced-context-engineering-for-coding-agents → `ace-fca.md`**
  (no license file; ideas only, nothing copied). Adopted the **timing rule**
  (hand over deliberately at ~40–60% context, at a phase boundary — never at
  the death rattle) and **human review at the high-leverage point** (a bad
  line in a handover cascades like a bad line in a plan → the review gate).

## Prose sources (not in sources.lock — blogs/news aren't diffable repos)

- **jdhodges.com, "Claude Handoff Prompt"**
  (https://www.jdhodges.com/blog/ai-session-handoffs-keep-context-across-conversations/)
  — the 8-section prompt template;
  source of **"what to avoid" (dead ends) as a first-class section** and the
  insistence on concrete values (commands run, test results) over vague
  summaries.
- **tessl.io on Amp retiring compaction**
  (https://tessl.io/blog/amp-retires-compaction-for-a-cleaner-handoff-in-the-coding-agent-context-race/)
  — the *why* of the whole skill:
  recursive summaries distort earlier reasoning (OpenAI's compaction report),
  so a reviewed, selective handoff to a fresh session beats in-place
  compression. Also the source of the "let go cleanly" framing.
- **Sonovore/claude-code-handoff** (github.com/Sonovore/claude-code-handoff) —
  evaluated and mostly rejected: its hook machinery (SessionStart auto-load,
  per-message live-handoff injection, four modes) is too invasive next to the
  existing RTK hook. Its one retained idea — **forward-looking (decisions +
  next steps) beats backward (completed work)** — survives as Hard rule 5.
  Idea-only, so no sources.lock pin (same treatment as ACE-FCA).
- **Cline Memory Bank** (https://docs.cline.bot/best-practices/memory-bank)
  — evaluated and **not** adopted as
  structure: its layered persistent files (projectbrief → activeContext) solve
  the *permanent memory* problem, which CLAUDE.md + auto-memory already cover
  here. Its influence survives as the boundary rule: slow-changing truths go
  to CLAUDE.md/memory, not into the baton.

## What's ours

The three-state progress discipline (verified / unverified / not started, tied
to CLAUDE.md Rule 12), the receiver-decides-the-mode split (repo mode vs chat
mode with the reference-rule inversion for web conversations), the single
"first action" ahead of the task list, verifiable acceptance criteria wording,
the fresh-git-facts rule, and the boundary map to `/compact` / CLAUDE.md /
`design-gate` / `verify-before-done`. The chat-mode thin-prompt twin lives at
`prompts/handover.md` for claude.ai web conversations where skills don't load.
