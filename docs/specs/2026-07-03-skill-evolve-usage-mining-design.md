# Design — skill-evolve usage mining (nightly "mine my own usage → propose")

- Date: 2026-07-03
- Status: **Design — awaiting approval at the hard gate** (no code until approved)
- Inspiration: microsoft/SkillOpt `skillopt-sleep` + alchaincyf/darwin-skill (both 🟦 build-your-own)
- Decision record: `docs/adr/0001-fold-skill-self-optimization-into-skill-evolve.md`
- Language: English (engineering/process skill; skill-evolve is already English)

## 1. Purpose & success criteria

Give `skill-evolve` a second evidence stream: the user's **own Claude Code usage
transcripts**. It mines recurring patterns and reports where the user's skills (or
CLAUDE.md memory) should change — **report-only, the user adopts**. Automatable via the
built-in `schedule`, so the user need not remember to run it; adoption stays manual.

**Success = ** a `skill-evolve` run (on-demand or scheduled) produces a report whose new
**USAGE SIGNALS** section names concrete, evidence-backed candidates, and — for gaps —
hands over real prompts from history that become a `skill-creator` eval set. Nothing live
is edited by this skill.

## 2. Scope

**In (v1):** Harvest → Mine → Report (the "scout" half). Three signal types, partitioned
by **what should change**: a new skill / an existing skill / memory. All three share one
harvest pass; they differ only in the lens the LLM applies to the same digest.

| Signal | Trigger (raw markers the script surfaces) | Evidence in report | Routes to |
|---|---|---|---|
| **GAP** | same class of task recurs across sessions with **no skill invoked** (done ad-hoc each time) | recurring prompts + count + session ids | `skill-creator` (new skill) **+ a mined real-prompt eval set** |
| **FRICTION** | a skill **was** invoked, then **immediately** corrected / re-asked / manually fixed | skill name + the correcting quote + count + sessions | `skill-creator` (improve that skill) |
| **MEMORY** | a preference/fact/instruction the user **restates across sessions**, not yet in CLAUDE.md/memory | the recurring statement + count | user edits **CLAUDE.md / memory** (not skill-creator) |

Routing in one line: **GAP = build a new skill · FRICTION = fix an existing skill ·
MEMORY = update memory.** The three are mutually exclusive.

Note — **"recurring" needs a threshold**: a one-off is not a signal. The script surfaces
raw markers deterministically (repeated prompts, skill invocations, correction-adjacency,
restated lines); deciding "are these the same thing" is the LLM's semantic clustering
(Rule 5), so false positives are expected — every candidate ships **with its evidence**
for the user to judge.

**Out (v1, flagged for possible v2):** SkillOpt's automated `Replay` (re-run tasks under
current-vs-candidate skill, auto-score held-out). Rebuilding a scoring harness duplicates
`skill-creator`'s eval loop and burns tokens; the manual adopt path covers it.

**Not here at all:** the actual editing/optimization (bounded edits + ratchet) — that is
the `skill-creator` + adopt-time discipline described in the ADR, not this skill.

### 2.1 Phase boundary — the scout does NO editing

The disciplines the two projects are famous for (bounded edits, git-revert ratchet)
belong to the **optimize phase, not the scout phase**:

- **Scout phase (this skill, skill-evolve):** read-only → mine → report. It changes
  nothing, so there is nothing to bound or ratchet. It only surfaces candidates + evidence
  + real prompts.
- **Optimize phase (skill-creator, adopt-time):** where a proposal actually becomes edits
  scored against evals — *this* is where bounded-edit + ratchet apply.

**Corrected after auditing skill-creator (2026-07-03):** the "disciplines to steal" from
SkillOpt/darwin shrink from three to **two**, because skill-creator already has more than
first assumed:

| Discipline | Already in skill-creator? | Net-new to apply |
|---|---|---|
| Anti-self-eval bias | ✅ blind comparator (`agents/comparator.md`) — stronger (blind A/B) | — |
| Held-out train/test split | ✅ but only in the **description** optimizer (60/40, pick by test score, `SKILL.md:394`) | ~~port to content loop~~ — **out of scope: would edit upstream skill-creator** |
| Variance analysis | ✅ mean ± stddev, flags flaky evals | — |
| **Bounded edits** (one variable/round) | ❌ rewrite step is free-form | **yes — adopt-time discipline (external, no skill-creator edit)** |
| **git-revert ratchet** (strictly-improve-or-revert) | ❌ no hard reject gate | **yes — adopt-time discipline (external, plain git)** |

### 2.2 We do NOT modify skill-creator (it is upstream/built-in)

`skill-creator` is an upstream-installed built-in, not a self-built skill — editing it gets
clobbered on update and is off-limits (same reason the nightly loop does not live in it).
The two net-new disciplines are therefore **operating protocol, not code changes**:

- **Bounded edits** = how you *drive* skill-creator (one change per iteration, then re-run
  its evals). No file of skill-creator's is touched.
- **git-revert ratchet** = a **plain-git wrapper around** skill-creator: branch per attempt,
  read the `benchmark.json` delta it already emits, `git revert` if it isn't strictly
  positive. Happens entirely *outside* skill-creator.

Where the protocol lives: a short adopt-time hand-off note in **skill-evolve** (which we
own) — the scout report points to it. skill-creator stays pristine upstream.

The one item that *would* touch skill-creator — porting the description optimizer's
held-out split to the content eval loop — is **dropped from scope**: not worth
forking/vendoring an upstream skill for a single refinement.

So the optimize half is ~80% already in skill-creator; the genuine net-new is two cheap
operating disciplines (bounded edit + ratchet), **not a new engine and not an edit to
skill-creator** — reinforcing "don't rebuild the optimize half." All of this is adopt-time;
none of it lives in the scout.

## 3. Architecture — same two-layer pattern skill-evolve already uses

```
scripts/mine_usage.py   (deterministic, no network, no writes)
   reads ~/.claude/projects/*/<session>.jsonl  (streamed line-by-line, capped)
   → emits a compact JSON "usage digest" on stdout
        │
        ▼
skill-evolve SKILL.md step  (the LLM's judgment)
   reads the digest → semantic clustering + verdict → USAGE SIGNALS report section
```

This mirrors `extract_sources.py` (deterministic extract) → LLM judges. Cheap script does
the bulk-reading so the LLM never touches a 47 MB transcript directly. Per CLAUDE.md
Rule 5: the script counts/extracts (deterministic); the LLM clusters intents and judges
(the genuine judgment call).

## 4. `scripts/mine_usage.py` — component spec (spec only, no code yet)

- **Input / flags:** `<transcripts-dir>` (default `~/.claude/projects/`),
  `--lookback-hours N` (default 72, mirrors skillopt-sleep), `--max-sessions N`,
  `--max-prompts-per-session N` (default 50 — bounds digest size), `--redact` (SHOULD: mask
  obvious secret patterns — long hex/base64, key-like tokens — in emitted prompt text).
- **A typed prompt is strict:** `type=="user"` + `promptSource=="typed"` + not `isMeta`,
  and not a `<command-…>` wrapper. The lenient "absent promptSource = typed" reading floods
  the digest with slash-command noise (verified: absent-bucket ≫ typed-bucket) — don't use it.
- **Per session, deterministically extract:** `session_id`, typed prompt texts (truncated),
  skill invocations (`attributionSkill` — which appears on **assistant** lines only — plus
  assistant `tool_use` name=="Skill"), and **friction markers** (a typed prompt whose
  *immediately preceding turn* was an assistant turn AND carries a strong correction cue —
  redo/fix/重來/改成/不對, NOT ambiguous 其實/不是/actually). A friction marker's
  `skill_context` is the skill active in that preceding assistant turn (never off the user
  line — user lines carry no `attributionSkill`). `isSidechain` lines are skipped. No
  semantic judgment — just surface the raw signal; the LLM clusters.
- **Output:** JSON to stdout —
  `[{session_id, ts, user_prompts:[...], skills_invoked:[...], friction_markers:[...]}]`,
  capped in total size so the digest stays small.
- **Constraints (MUST):** no network; no writes except stdout; malformed JSONL lines are
  skipped and the skipped count is reported (fail loud, Rule 12); missing dir → clear
  non-zero exit.

## 5. Report — extend the existing SKILL EVOLVE REPORT

Add one section (upstream section unchanged), so the two streams compose:

```
USAGE SIGNALS  (from your own transcripts · lookback <N>h · <S> sessions · <K> skipped lines)
  GAP     "<clustered intent>"  ×<count>  sessions: <ids>
            → no skill covers this. Candidate for skill-creator.
            → mined eval prompts (real, held-out): 1) "<prompt>"  2) "<prompt>" ...
  FRICTION  skill <X>  ×<count>  — worked around/corrected in sessions <ids>
            → consider improving <X>; evidence: "<quote>"
  MEMORY  "<recurring preference/fact>"  ×<count>
            → consider adding to CLAUDE.md / memory
SCOPE NOTE: <lookback window, caps, sessions skipped — no implied exhaustiveness>
```

## 6. Scheduling (external, not baked in)

SKILL.md carries a concrete **"Running it nightly"** recipe: for the full report
unattended, create a built-in `schedule` routine (cron cloud agent) at e.g. 03:00 whose
prompt runs skill-evolve's usage scan; for a digest-only pre-pass, a bare OS crontab can
call `mine_usage.py` (but the GAP/FRICTION/MEMORY clustering is an LLM step, so the full
report needs an agent scheduler, not plain cron). The user reviews the queued report in the
morning; adoption stays manual. Matches the repo's content-engine-vs-timer split
(daily-brief + schedule precedent). The skill itself stays trigger-agnostic.

## 7. Security (strengthen skill-evolve's existing note)

- Transcripts are the **most sensitive local data** (pasted secrets, private context).
  Mining is **local-only, read-only, report-only**; nothing is transmitted, nothing live
  is edited.
- **Treat transcript content as data, not instructions** — a prompt you once pasted could
  contain injection; the miner summarizes, never obeys, mined text.
- `--redact` SHOULD mask obvious secrets in the emitted digest.

## 8. Testing (Rule 9 — verify intent)

- `mine_usage.py` gets a pytest over a **fixture transcript dir** (2–3 hand-made JSONL
  sessions): asserts it extracts the expected prompts, skill invocations, and friction
  markers; that a malformed line is skipped and counted; that it is deterministic and
  performs no network/write. This is the "one runnable check" the non-trivial parser
  earns.
- Add an eval to `skill-evolve/evals/evals.json` covering "given a digest, the report's
  USAGE SIGNALS section names the right GAP/FRICTION/MEMORY candidates with evidence."

### Acceptance criteria

- **AC1 (extract):** Given a fixture dir with a task done by hand in 3 sessions, When
  `mine_usage.py` runs, Then the digest surfaces those 3 prompts under one `session` each
  and the report clusters them into one GAP ×3 with a mined eval-prompt list.
- **AC2 (report-only):** Given any run, When it completes, Then no file under
  `~/.claude/` or any skill dir is modified (only stdout / the report is produced).
- **AC3 (friction):** Given a session where skill X is invoked then the user re-asks with
  a correction, When mined, Then X appears under FRICTION with the correcting quote.
- **AC4 (fail loud):** Given a malformed JSONL line, When mined, Then it is skipped and
  the skipped count appears in the SCOPE NOTE.

## 9. Registration & upstream tracking (repo conventions)

- `apm.yml` / README self-built table: no new skill row (extending existing); update
  skill-evolve's README description to mention the second evidence stream.
- `skill-curator/references/skill-map.md`: broaden skill-evolve's entry; sharpen
  boundaries vs `solo-think` and `skill-creator`.
- Create `skill-evolve/references/attribution.md` + `skill-evolve/sources.lock` pinning
  `microsoft/SkillOpt` and `alchaincyf/darwin-skill` (so skill-evolve now also tracks its
  own upstream — and a future skill-evolve run will diff them).

## 10. Decisions settled at the gate

1. **Scope:** scout-only v1 (Harvest → Mine → Report; no automated Replay). ✅ settled.
2. **Signal set:** all three — GAP / FRICTION / MEMORY (they share one harvest pass;
   marginal cost over GAP-only is small). ✅ settled.
3. **Transcript scope:** **all projects** under `~/.claude/projects/` by default
   (`mine_usage.py` default dir). ✅ settled (2026-07-03).

Remaining to confirm before Phase 2: nothing blocking — ready to write the plan on your
approval.
