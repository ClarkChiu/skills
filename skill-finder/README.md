# skill-finder 🔎

Search the open agent-skills ecosystem **read-only** and route every candidate
to [`skill-auditor`](../skill-auditor/) before any install decision.

- Hits `skills.sh/api/search` + `raw.githubusercontent.com` directly — no
  `npx skills` CLI, no vendor code execution, no telemetry.
- Fetches a candidate `SKILL.md` for inspection; never installs.
- Hands findings to skill-auditor so evaluation always precedes trust.

Discovery and evaluation only. Install is the user's call, made elsewhere.
