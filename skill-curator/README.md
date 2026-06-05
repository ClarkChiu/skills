# skill-curator 🧭

An orchestration skill that decides whether an external agent skill is **worth using, and how**, and leaves a decision trail.

One line: hand it a skill (name / URL / a whole recommendation list) → run the full evaluation → get a verdict (🟩 install / 🟦 build-your-own / 🟨 vendor & customize / 🟥 skip) + a written record in the `research/` decision log.

## Role (no reinventing the wheel)

| Skill | Role |
|---|---|
| `skill-finder` | Discovery (skills.sh, read-only) |
| `skill-auditor` | Security verdict |
| **`skill-curator`** | **Relevance + install/build-your-own decision + record** (calls the two above) |
| `skill-evolve` | Tracks the upstream of self-built skills |

## Five-step pipeline

`relevance → duplication → security (skill-auditor) → provenance → verdict → record`

Full criteria and mantra in [`references/criteria.md`](./references/criteria.md) — that's this skill's brain. When judging duplication, also read [`references/skill-map.md`](./references/skill-map.md) (this project's existing skills and their boundaries).
Mantra: **engineering you can download, install; text you can write, write your own version of.**

## Output

- `research/<YYYY-MM-DD>-skill-research-log.md` — the day's work log, one row per evaluation (date/name/URL/author/duplicate/security/verdict).
- `research/audits/YYYY-MM-DD-<skill>.md` — full SKILL AUDIT REPORT.
- `research/skill-index.md` — public neutral index (kept in Chinese, the repo's index language).

## Notes

- **Discovery and decision, never install.** Research ≠ install.
- The security verdict always defers to `skill-auditor`; this skill must not override it.
- Verdict "install" → pin the commit, re-review the local copy after install.
- Needs local network access (fetch SKILL.md for static analysis).
