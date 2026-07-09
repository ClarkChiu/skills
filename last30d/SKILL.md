---
name: last30d
description: >-
  Fetch the last ~30 days of discussion about a topic or person across Reddit, X,
  Hacker News, GitHub, arXiv, and YouTube, rank each lane by its own engagement metric
  (upvotes / likes / points / stars / recency / views), and print a per-lane structured
  digest. This is a FETCH-AND-SCORE tool, not a report writer — hand the digest to the
  session model or `deep-research` for synthesis. USE THIS SKILL when the user wants the
  recent social signal on something — "what are people saying about X lately", "last 30
  days on <topic/person>", 「最近 30 天大家在討論什麼」「某某人最近的動態」「社群風向」.
  Do NOT use it for a web-verified cited report (that's `deep-research`) or generic web
  search (that's built-in WebSearch).
license: MIT
allowed-tools:
  - Bash
  - Read
---

# last30d — last-30-days social-signal fetcher

Given a topic or person, pull recent discussion from six lanes, rank each by its own
engagement metric, and emit a per-lane digest. **It fetches and scores; it does not
synthesize.** Read the digest, then let the session model (or `deep-research`) turn it
into prose. Per-lane, never a merged score — cross-platform engagement scales aren't
comparable.

## Run it

```bash
python3 last30d/scripts/last30d.py "<topic>" [--depth quick|default|deep] \
    [--lanes reddit,x,hn,github,arxiv,youtube] [--json] [--save PATH]
```

- `--depth` sets per-lane top-N: quick=10, default=25, deep=50.
- `--lanes` runs a subset (default: all six).
- `--json` emits structured JSON instead of Markdown; `--save PATH` writes to a file.

Read the printed digest and synthesize from it, or pass the `--json` output to
`deep-research` for a fuller, cited write-up.

## Lanes

**Four always-on (keyless / free):**
- **Reddit** — RSS discovery + shreddit listing partials for real upvote scores + top
  comment per post. No key.
- **Hacker News** — Algolia Search API. No key.
- **GitHub** — REST Search (repos matching the topic, ranked by stars). Uses `GITHUB_TOKEN`
  if set (higher rate limit).
- **arXiv** — arXiv API; no engagement metric, so ranked by recency.

**Two optional (degrade visibly if unavailable — the run continues):**
- **X** — via the **xAI** first-party API (`XAI_API_KEY`; xAI owns X). No key →
  `skipped: no XAI_API_KEY`. Cost when enabled ≈ $0.5–1.5/run (Live Search per-source).
  Optional `XAI_MODEL` (default `grok-4`).
- **YouTube** — via **`yt-dlp`** (external CLI, user-installed like `ffmpeg`; never
  auto-installed). Absent → `skipped: yt-dlp not installed`.

The digest header lists per-lane counts, so a lane that failed or returned nothing is
visible, not silently hidden.

## Boundaries

- **vs `deep-research`** — last30d is the *social-signal fetcher* (engagement-scored
  platform data, a structured digest); `deep-research` is the *web-verified cited report*.
  Natural pipeline: `last30d --json` → feed to `deep-research` for synthesis.
- **vs built-in `WebSearch`** — platform-native engagement data vs generic web search.
- Fetch-only: it never posts, never writes to any account, and reads only your own
  `XAI_API_KEY` / `GITHUB_TOKEN` from the environment.

## Provenance

The Reddit keyless engine and the X (`xai_x`) client are **vendored verbatim** from
`mvanhorn/last30days-skill` (MIT) — see `references/attribution.md` and `sources.lock`.
HN / GitHub / arXiv / YouTube lanes, the orchestrator, and the digest are original. External
CLIs (`yt-dlp`) and keys (`XAI_API_KEY`) are user-supplied.
