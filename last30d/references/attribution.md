# Attribution

`last30d` **vendors** the hard-to-reproduce, endpoint-fragile fetchers from
**mvanhorn/last30days-skill** (MIT) and wraps them in an original, narrowed skill.
Full evaluation & security audit: `research/audits/2026-07-08-last30days.md`
(skill-curator verdict: 🟨 vendor & customize). Design: `docs/specs/2026-07-08-social-pulse-design.md`.

## Vendored verbatim (upstream `skills/last30days/scripts/lib/`, copied into `scripts/sources/`)

The **Reddit keyless leaf fetchers/parsers** and the **X first-party client** — the parts
that carry undocumented-endpoint knowledge and rot when the platforms change:

- `reddit_rss.py`, `reddit_listing.py`, `reddit_shreddit.py`, `reddit_enrich.py`
- `xai_x.py`
- shared deps pulled by the above: `http.py`, `relevance.py`, `cjk.py`, `dates.py`, `log.py`

Copied verbatim (no edits) so a re-sync is a clean re-pull, not a hand-port.

## Deliberately NOT vendored

The upstream `reddit_keyless.py` orchestrator was **not** vendored — it balloons the
closure into `reddit_arctic`→`rerank` (708L) and `reddit_enrich`→ lazy `reddit.py` (keyed
path, 731L) → `providers/query/schema/signals`: ~1700 lines of keyed-path + rerank
machinery this skill never uses. The hard IP is only in the leaf parsers above. So the
**orchestration is original** (`scripts/sources/reddit_lane.py`): RSS discover → listing
score-backfill → shreddit comment enrich → rank. Also dropped: the bird/cookie X path,
web-only fallback, plugin/MCP/wizard, author npm CLIs, SessionStart hook, hosted mode,
and every other platform (design §11 register).

## Original (not from upstream)

`hn.py` (HN Algolia), `arxiv.py` (arXiv API), `github.py` (GitHub REST), `youtube.py`
(yt-dlp), `reddit_lane.py`, `x_lane.py`, `digest.py`, `scripts/last30d.py`, all tests.
These lanes use clean official APIs — no vendoring needed (CLAUDE.md Rule 2).

## Re-sync rule (for skill-evolve)

`sources.lock` pins the upstream commit the vendored files were copied from. On drift:
**re-pull the changed leaf file verbatim** (don't hand-merge) — especially when a Reddit
`/svc/shreddit/...` endpoint or the xAI `x_search` contract changes upstream. The parser
regression tests (`tests/test_reddit_parsers.py`) guard that a re-pull didn't break parsing.
The original `reddit_lane.py` orchestration is ours and does not track upstream.
