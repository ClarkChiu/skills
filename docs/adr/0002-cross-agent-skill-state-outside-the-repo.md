# 0002 — Cross-agent skill state lives outside the repo, under XDG data home

- Status: **Superseded (2026-08-05, same day) — kept for the analysis, not the decision**
- Date: 2026-08-05
- Context source: design doc `docs/specs/2026-08-05-relationship-counsel-design.md`

> **Why superseded:** the skill that motivated this ADR (`relationship-counsel`) dropped its
> memory layer in v3, so nothing in this repo currently needs cross-conversation state.
> A second review also found the decision unimplementable as written with the tool set it
> assumed: `Read/Write/Edit/Glob` **cannot delete a file** — which invalidates this ADR's
> central claim that "deleting or editing a file is a stronger guarantee than a script that
> promises deletion" (an agent can only blank the file; the filename, i.e. the person, stays
> on disk) — and with no `Bash` the skill cannot resolve `$HOME` to state the absolute path
> the consent flow required.
>
> **Kept, not deleted**, for two reasons: the option analysis below (XDG vs an agent's
> private tree vs an in-repo gitignored directory) is still the right analysis for any
> future skill that genuinely needs state, and the leak-path section records a live problem
> in `skill-evolve` that outlives this decision. Anyone reviving this must first solve the
> delete/path-resolution gap — most likely by adding `Bash`, which is its own trade-off.

## Context

`relationship-counsel` is the first self-built skill that needs to remember something
**between conversations** — who the user is talking about, what stage the relationship is
at, what was already tried. Two constraints were stated by the user:

1. The state must **never enter version control**.
2. It must work **across host agents**, not just Claude Code.

Three candidate locations were considered.

**A — Claude Code's per-project memory** (`~/.claude/projects/<slug>/memory/`).
Rejected: Claude-Code-specific. `opencode`, Hermes, Codex, and anything else that mounts
this repo's skills cannot see it. It is also a *shared* index — every session that opens
this project reads its index lines, so private material would surface in unrelated work.

**B — A directory inside the repo** (e.g. `state/`, gitignored).
Rejected, but **not** on the grounds that ignore rules are untrustworthy — this repo
already protects `research/*` exactly that way, and that arrangement is fine. The reason
is narrower: an in-repo path is still repo-bound, so it travels with the working copy, is
duplicated by every clone and worktree, and is visible to anything that scans the tree.
For material this private the store should not be *in* the artifact that gets cloned,
worktreed, and published at all. A gitignored directory is an adequate guard for audit
notes; it is the wrong shape for personal relationship data.

**C — The host agent's own workspace** (the `solo-think` precedent,
`~/.hermes/workspace/memory/`).
Rejected for this skill: it is exactly as agent-bound as A. It is the right answer for
`solo-think` — that skill *is* a Hermes agent — but wrong for a skill deployed to every
agent this repo targets.

## Decision

Cross-conversation state for skills in this repo lives **outside the repository, in the
XDG data directory**:

```
${XDG_DATA_HOME:-$HOME/.local/share}/<skill-name>/
```

as **plain Markdown files, written with the host agent's ordinary file tools** — no
database, no helper script, no new dependency.

Rationale, in the order the constraints were given:

- **Not in version control** — not by an ignore rule, but because the path is not inside
  any repository. There is nothing for git to ignore or accidentally stage.
- **Cross-agent** — XDG is an OS-level convention, not an agent's private tree. Any agent
  that can write a file can reach it, and they all reach the *same* file, so the profile
  does not fork per agent.
- **Plain Markdown, no script** — CLAUDE.md Rule 2: a database is not needed for a
  handful of short profile files, and a script would be one more thing to install on
  every machine. The user can read, edit, or delete the store with any text editor, which
  is a better revocation story than a `--confirm` subcommand.
- **Portable enough** — `~/.local/share` exists on this machine and `XDG_DATA_HOME` is
  unset, so the plain path applies. On macOS the native convention is
  `~/Library/Application Support`; `~/.local/share` is merely what many CLI tools use
  there, so this is a pragmatic choice rather than the platform-blessed one. On Windows
  the host agent runs under WSL here, so the Linux path applies.
  Note the skill has **no `Bash`**, so it cannot expand `$XDG_DATA_HOME` or read any
  environment variable: the spec is the fixed path `<HOME>/.local/share/<skill-name>/`,
  resolved by the agent from the home directory it already knows. Honouring an
  XDG override would require adding `Bash` — deliberately not done for one variable.

## Consequences

- The store does **not** travel with `git clone` + `apm install`. That is intended: the
  skill is portable, the private material is not. A new machine starts with no profile.
- No backup story is provided. If the user wants one, that is their own dotfile/backup
  arrangement — deliberately not this repo's business.
- No fine-grained lifecycle commands (pause / revoke-last-update / forget-one-object /
  purge) as in the upstream this skill was evaluated against; the equivalent is deleting
  or editing a file. Accepted: fewer moving parts, and direct file access is a stronger
  guarantee than a script that promises deletion.
- Any future self-built skill needing cross-conversation state should use the same
  location and shape rather than inventing a third convention.
- Consent gates **writing only**. Reading is not gated and cannot be: any agent or session
  with file permissions on this account can read
  `~/.local/share/relationship-counsel/`. "Cross-agent" is the feature and the exposure at
  the same time. Accepted, and stated here so it is not mistaken for a guarantee.
- The consent gate is a **prose rule, not a technical control**. Nothing in the runtime
  prevents a model from writing the file before asking. That is true of every rule in this
  repo, but it must not be described as though a real gate existed.

## The leak path this decision does NOT close

Keeping the store out of the repo protects the **store**. It does nothing for the
**conversation**, and there is a concrete path from one to the other:

`skill-evolve/scripts/mine_usage.py` defaults to `~/.claude/projects` and globs
`*/*.jsonl` — **every project on the machine, not just this repo**. It extracts the user's
literal prompts and clusters them, and one of its output categories is `MEMORY`:
"recurring preferences or facts not yet in CLAUDE.md" — i.e. **candidates for a file that
is version-controlled and published via APM**. Its `--redact` flag is opt-in and only
masks secret-shaped strings; it does nothing for "he cancelled on me again."

A second, smaller path: Claude Code's own per-project auto-memory. This ADR rejected it as
a *store*, but that does not stop an agent writing a relationship fact into its index
during an ordinary session — and every session that opens this project reads that index.

What actually happened to these:

- **The write side is closed, but by a different route than this ADR anticipated.** An
  earlier draft planned a hard skill rule ("never write relationship content to agent
  auto-memory / `CLAUDE.md` / handover documents"). That rule no longer exists, because
  the skill it was written for dropped its memory layer entirely and shipped with
  `allowed-tools: Read` — it has no ability to write anywhere. A structural property beat
  a prose rule. (Do not go looking for that rule in the design doc; its RFC numbering was
  rewritten and #7 is now the no-false-alarm rule.)
- **The read side is still open.** `mine_usage.py` needs a usable exclusion mechanism;
  "use it in a different directory" does not help when the glob already covers every
  project. **Not solved, and not solved by shipping `relationship-counsel` either** — the
  skill writes nothing, but the *conversation* is still in the transcript that
  `mine_usage.py` reads. Verified 2026-08-06: `mine_usage.py` is unchanged.
  Close this before scheduling `mine_usage.py` to run unattended.
