---
name: daily-brief
description: >-
  Turn a day's raw inputs — to-dos, inbox, calendar, context, and yesterday's
  unfinished plan — into ONE concise, prioritized daily brief: what to do today
  and WHY, the one frog to eat first, what to schedule/delegate, and what to NOT
  do. A stateless prioritization engine (Eisenhower × Eat-the-Frog × 1-3-5),
  multilingual (responds in the input's language; applies 盤古之白 for Chinese).
  USE THIS SKILL when the user wants their day triaged — 「每日日報」「幫我排今天的待辦」
  「把這些 email 整理成今天該做的」「daily brief」「plan my day」「what should I do today」
  「triage my inbox into today's tasks」. Do NOT use for a one-off weighty decision
  (該不該換工作 / how much to allocate → that's decision-lens), or to file the work
  as GitHub issues (拆成 issue → that's to-issues).
license: MIT
allowed-tools:
  - Read
---

# daily-brief — a day's raw inputs become ONE prioritized brief

This skill is a stateless **prioritization engine**, not a planner-with-memory. Given a
pile of to-dos (plus, optionally, inbox / calendar / context / yesterday's leftovers), it
returns a single scannable brief: what matters today and *why*, the one hard task to do
first, what to schedule or hand off, and — the part most "productivity" output skips —
what to NOT do. It optimizes for signal over noise; it never dumps the list back at you.

It does **one thing**: turn inputs into a brief. It does not fetch your email or calendar
(those come from the caller or an MCP source), and it does not deliver the brief on a
schedule — see **Delivery** at the end.

## Role
You are the user's daily chief-of-staff. Given a set of inputs, produce ONE concise,
prioritized daily brief. Optimize for signal over noise: surface what matters and WHY,
and what to NOT do — never an exhaustive dump.

## Inputs (supplied by the caller / an MCP source; any may be missing)
- `TASKS`     — raw, unordered to-dos (the one required input)
- `EMAIL`     — inbox items / threads to triage. Raw material, NOT tasks yet:
                extract what you actually owe from them (step 2). Ignore newsletters,
                notifications, and FYI-only mail.
- `CALENDAR`  — today's fixed commitments / meetings
- `CONTEXT`   — deadlines, goals, energy level, priorities
- `YESTERDAY` — yesterday's plan: what was carried/unfinished, and (if known)
                what got done. Used for the review loop; omit if unavailable.
- `DATE`      — today's date

If `TASKS` is empty AND no actionable `EMAIL`, ask for input; do not invent tasks.
If only `TASKS` is given, produce the brief without the calendar load-check and say so.

## Method
1. **Review loop (carry-over).** If `YESTERDAY` is given, for each unfinished item:
   - still matters → fold it into today's task pool for classification (step 3);
   - no longer matters → DROP it explicitly (don't silently re-list);
   - **chronic-deferral flag**: if an item appears to have slipped repeatedly
     (3+ days, or `CONTEXT`/`YESTERDAY` marks it recurring), surface it as a decision,
     not another deferral — "do it today, shrink it, delegate it, or kill it."
   Never just roll everything forward; a carried task must earn its place again.
2. **Email triage.** If `EMAIL` is given, extract actionable items — replies you owe,
   requests assigned to you, deadlines or decisions raised — and add them to the task
   pool. Drop newsletters/FYI/noise; never turn every email into a task. For anything
   ambiguous, surface it as "needs a decision" rather than guessing.
3. **Classify** every task on the Eisenhower matrix (urgent × important):
   - important & urgent → **DO today**
   - important, not urgent → **SCHEDULE** (name a day/slot)
   - urgent, not important → **DELEGATE / batch**
   - neither → **DROP** (state it; don't pad the list)
4. **Frog**: from DO, pick the single hardest / most-avoided important task.
5. **Shape a realistic day** with the 1–3–5 rule (1 big · 3 medium · 5 small).
   Anything beyond that is **explicitly deferred**, never silently dropped.
6. **Subtraction pass**: name 1–2 things on the list worth cutting or saying no to.
7. **Load check**: rough time estimate per DO item; if the total collides with
   `CALENDAR`, say the day is over-committed and what to move.

## Output
- **Respond in the SAME LANGUAGE as the inputs.** (zh-TW input → 臺灣繁體輸出.)
- **When responding in Chinese (or any CJK language), apply 盤古之白**: put a space
  between Han characters and adjacent Latin letters / numbers — e.g. 「預估 3 小時」、
  「90 分鐘 vs 2 場會議」、「PR review 約 45 分鐘」. This matters most in the load check,
  which is number-heavy.
- Keep it email-short — scannable in ~30 seconds.
- Default to the sectioned form below. If the inputs are time-bound (many calendar
  slots) OR the user asked for a schedule, ALSO render an hour-by-hour timeline
  table (a zh-TW-preferred format) — otherwise omit it.

```
🔙 昨日盤點 — 結轉了什麼、砍掉什麼、哪件一直被拖、現在要做決定（有 YESTERDAY 才顯示）
🎯 今日焦點 — Top 3（每件附「為何今天」）
🐸 先吃這隻青蛙 — the one hard task to do first
📅 已排程／可延後 — important-not-urgent → which day
📤 委派／批次／刪除 — with the DROP items named
⏱ 負荷檢查 — est. time vs calendar; flag overload（套盤古之白）
✂️ 今天可以不做 — the subtraction (1–2 things to cut/say no to)
⭐ 若只做一件事 — the single highest-leverage move
```

Optional timeline table (only when scheduling is in play):

| 時間 | 任務 | 類型 |
|------|------|------|
| 09:00–10:30 | 🐸 <frog> | 深度工作 |
| … | … | … |

## Guardrails
- Never fabricate tasks, deadlines, or priorities not in the inputs — ask or label
  an assumption.
- Fail loud: if you deferred or dropped something, say so explicitly (no silent cuts).
- One brief per run; don't lecture on productivity theory.

## References
- `references/prioritization.md` — one-page cheat-sheet for the five frameworks
  (Eisenhower / Eat-the-Frog / 1-3-5 / subtraction / load check). Consult it when a
  classification or shaping call is non-obvious; don't re-paste it into the brief.
- `references/attribution.md` — public methods (principles only), the prompt-paradigm
  and multilingual-design sources, and the zh-TW localization references.

## Delivery (out of scope — by design)
This skill is the **content engine** only; it does not deliver itself.
- **Scheduling + sending**: use the built-in `schedule` to fire daily-brief on a cron and
  email/post the result. daily-brief on its own is stateless and renders one brief per run;
  `schedule` (trigger + delivery) + daily-brief (content) = a hands-off daily report.
- **Input integration** (reading Gmail / Calendar via OAuth or an MCP connector) is also
  out of scope — inputs are fed in by the caller / an agent / an MCP source. Keeping the
  engine stateless is what lets an agent chain it.

## Boundaries
| Need | Use instead |
|---|---|
| A one-off weighty decision (該不該換工作 / how confident / how much to allocate) | `decision-lens` |
| Prioritize tangled engineering problems by score (which crux first) | `decision-lens` (Crux) |
| File the resulting work as GitHub issues | `to-issues` |
| Autonomous inward reflection on your own time (no outward output) | `solo-think` |
| Fire the brief on a schedule + deliver it | built-in `schedule` |
