---
name: skill-curator
description: >-
  External-skill research & decision orchestrator. Given an external agent skill
  — by name, GitHub/skills.sh URL, or a whole curated list — this runs the full
  evaluation pipeline and returns a verdict: relevance (does it help THIS user) →
  duplication (does it duplicate built-ins/existing skills) → security (delegates
  to skill-auditor) → provenance → verdict (install / build-your-own / vendor /
  skip) → record (writes research/<date>-skill-research-log.md + audits/). USE
  THIS SKILL whenever the user wants to research, evaluate, vet, or decide on an
  external skill — phrases like 「研究這個 skill」「這個 skill 該不該裝」「評估一下」
  「值不值得裝」「幫我看看這個 skill」「install or build my own」, or pastes a list
  of recommended skills to assess. It ORCHESTRATES skill-finder (discovery) and
  skill-auditor (security) — it does not re-implement them. Discovery/decision
  only; never installs.
---

# skill-curator — external-skill research & decision

Decide whether an external skill is **worth using, and how**, and leave a decision trail. You are the curator: the question is never "is this skill good?" but **"is it useful for THIS user's work/life, and should we install it or build our own?"**

This is the **orchestration layer**; it explicitly **does not re-implement** the existing tools:

| Existing skill | Role | How this skill uses it |
|---|---|---|
| `skill-finder` | Discovery (skills.sh, read-only) | find the canonical source, fetch the `SKILL.md` |
| `skill-auditor` | Security verdict | get the SAFE/⚠️/❌ verdict and safe-run plan |
| `skill-evolve` | Tracks upstream of self-built skills | after build/vendor, record the upstream in attribution |

Full decision criteria live in **`references/criteria.md`** — read it before acting; it's this skill's brain. When judging duplication, also read **`references/skill-map.md`** (this project's existing skills: clusters, pipelines, boundaries vs built-ins); **after adding or changing a self-built skill, update that map** so future evaluations don't redo the work.

## Start from the user profile

First read the **"使用者定位 (User Profile)" section of the repo-root `CLAUDE.md`** (the portable source of truth, auto-loaded across machines via git/APM; the machine-local `user-profile` memory is just a local cache, don't depend on it when moving machines). Every evaluation starts from "is it useful for **this person's** context", not from generic good/bad. With no profile available, ask the user first: what's the main work, what problem should the skill solve.

## Recall first, then the five-step pipeline

**[R] Recall — always the first move, before any fetching or auditing.** The user
forgets what's already been evaluated; that's your job. Scan
**`research/skill-index.md`** (the committed, portable index — its `來源` column
holds the original URL, plus name / author / duplicate? / verdict) and match the
candidate by name OR URL. If present locally, also skim the day logs
`research/<date>-skill-research-log.md` + `research/audits/` for fuller reasoning —
but those are gitignored/local-only, so `skill-index.md` is the source of truth that
survives a fresh `git clone`. If the skill was already evaluated: **surface the prior
verdict and date, and stop** unless the user wants a re-evaluation (e.g. upstream
changed, or the prior call was thin). Don't silently re-run a decision already made.

Run the pipeline once per skill. For several skills (or a list), run each and summarize into one table.

```
[R] Recall      → already in research/skill-index.md (by name/URL)? Surface prior verdict + date, stop unless re-eval wanted.
[0] Relevance   → useful for the user's context (dev/systems/PM/writing/research/life)? No → "skip", stop.
[1] Duplication → duplicates a built-in or existing skill? Check references/skill-map.md first.
                  Yes → suggest using/extending the existing one, not a new install.
[2] Security    → run skill-auditor (static, no execution). Not SAFE → stop or sandbox-only.
[3] Provenance  → author trustworthy? maintained? or a low-star solo fork / inconsistent repo / no frontmatter?
[4] Verdict     → use the table in references/criteria.md: install / build-your-own / vendor & customize / skip.
[5] Record      → local detail (gitignored): research/audits/<date>-<skill>.md + the day's work log;
                  public: append one neutral row to research/skill-index.md (date/skill/url/author/dup/verdict).
```

### Step detail

- **[R] recall is cheapest of all**: one read of `research/skill-index.md` can end the task ("already evaluated 2026-06-05 → 🟥 skip"). Saves a full fetch+audit. Do it before anything else.
- **[0]+[1] first, they're cheap**: use existing knowledge + `skill-finder` to fetch the description, judge relevance and duplication. Irrelevant or pure duplicates don't need a full audit — mark them, state the reason (saves tokens).
- **[2] security goes to skill-auditor**: don't re-implement audit logic here. Drop the auditor's SKILL AUDIT REPORT verbatim into `audits/`. If the auditor says not-SAFE, this skill's verdict must not override it.
- **[3] provenance signals**: star counts without API auth misread/inflate → mark "unverified", don't treat as fact. High stars + few commits + short history = the SEO-sprint pattern, low trust.
- **[4] verdict**: see `references/criteria.md`. One mantra — **engineering you can download, install; text you can write, write your own version of.**
- **[5] record**: research ≠ install. Leave a trail on every evaluation so research isn't repeated and install/no-install stays traceable.

## Handling a multi-source list

Users often paste a third-party recommendation list. Note:

- **One bullet ≠ one skill** (`minimax-docx、pdf、xlsx` on one line is actually 3) → expand before counting.
- **List sources are low-trust**: they mix authors and quality levels.
- **Same name, different thing**: cross-check against the canonical repo, don't trust the listing's pairing.
- When researching several in parallel, dispatch subagents to gather evidence (fetch files + scan), but **make the verdict yourself**.

## Output format

Researching one skill → one SKILL AUDIT REPORT (auditor format) + a verdict and reasoning.
Researching a list → each item first, then one summary table:

```
| Skill | Relevant | Duplicates built-in? | Security | Provenance | Verdict | One-line reason |
```

Verdict is one of four: **🟩 install** / **🟦 build-your-own** / **🟨 vendor & customize** / **🟥 skip**. Each needs a "why this verdict" (tied back to the criteria signals).

## Landing the decision

Recording has two layers (everything under `research/` except `skill-index.md` is gitignored, never pushed to the public repo):

- **Local detail (private)**: for each skill deep-reviewed, write `research/audits/YYYY-MM-DD-<skill>.md` (full SKILL AUDIT REPORT) + **that day's** work log `research/<YYYY-MM-DD>-skill-research-log.md` (reasoning, third-party security detail, wording all stay here). A new day starts a new file.
- **Public index**: sync one **neutral** row to `research/skill-index.md` (committed) — only date / skill / url / author / duplicates-built-in? / verdict, **no** security detail, vulnerability disclosure, or commentary on the third party. Reason: a public repo shouldn't name-and-shame someone else's skill; the verdict is framed as "fit for this project", not a quality judgment. The index is kept in Chinese (the repo's index language); map the verdicts to its labels: install→直接裝, build-your-own→參考自製, vendor & customize→收錄＋客製, skip→跳過.
- Verdict "install" → remind: pin the commit, **re-review the local copy after install** (v1.0 safe ≠ the version you fetched).
- Verdict "build-your-own / vendor" → you can then use `skill-creator` to draft, and record the upstream in the new skill's `references/attribution.md` (which `skill-evolve` will later track).
