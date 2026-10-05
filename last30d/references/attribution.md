# Attribution

`last30d` **vendors** the hard-to-reproduce, endpoint-fragile fetchers from
**mvanhorn/last30days-skill** (MIT) and wraps them in an original, narrowed skill.
Full evaluation & security audit: `research/audits/2026-07-08-last30days.md`
(skill-curator verdict: 🟨 vendor & customize). Design: `docs/specs/2026-07-08-last30d-design.md`.

## Vendored verbatim (upstream `skills/last30days/scripts/lib/`, copied into `scripts/sources/`)

The **Reddit keyless leaf fetchers/parsers** and the **X first-party client** — the parts
that carry undocumented-endpoint knowledge and rot when the platforms change:

- `reddit_search.py`, `reddit_listing.py`, `reddit_shreddit.py`, `reddit_enrich.py`
- `xai_x.py`
- shared deps pulled by the above: `http.py`, `health.py`, `relevance.py`, `cjk.py`, `dates.py`, `log.py`
- `reddit.py` — **extract only**: the two pure date helpers `_days_to_reddit_bucket` and
  `_window_to_time_filter`, copied verbatim from upstream's keyed `reddit.py`, because
  `reddit_search.py` lazily imports `_window_to_time_filter` on its hot path (and would turn a
  missing import into a silent empty lane). The rest of upstream `reddit.py` is not vendored.

Copied verbatim (no edits) so a re-sync is a clean re-pull, not a hand-port.

## Deliberately NOT vendored

The upstream `reddit_keyless.py` orchestrator was **not** vendored — it balloons the
closure into `reddit_arctic`→`rerank` (708L) and `reddit_enrich`→ lazy `reddit.py` (keyed
path, 731L) → `providers/query/schema/signals`: ~1700 lines of keyed-path + rerank
machinery this skill never uses. The hard IP is only in the leaf parsers above. So the
**orchestration is original** (`scripts/sources/reddit_lane.py`): site-search discover
(dated and scored) → window trim → rank → shreddit comment enrich. Also dropped: the bird/cookie X path,
web-only fallback, plugin/MCP/wizard, author npm CLIs, SessionStart hook, hosted mode,
and every other platform (design §11 register).

## Original (not from upstream)

`hn.py` (HN Algolia), `arxiv.py` (arXiv API), `github.py` (GitHub REST), `youtube.py`
(yt-dlp), `reddit_lane.py`, `x_lane.py`, `digest.py`, `scripts/last30d.py`, all tests.
These lanes use clean official APIs — no vendoring needed (CLAUDE.md Rule 2).

## Re-pull log

**2026-07-20** — verbatim re-pull of three leaves (upstream files now live at
`skills/last30days/scripts/lib/` — path moved since the 2026-07-09 baseline):
`xai_x.py` + `log.py` at `39cca461aab5` (fixes an AttributeError on the xAI error
path: `http.DEBUG` → lazy `log.is_debug()`); `reddit_listing.py` at `298310ca34a5`
(backward-compatible timeframe param, r/all, discovery helpers — `reddit_lane.py`'s
`fetch_listings` call unchanged). `http.py` deliberately **held** at the
`ae8c32327f86` baseline: upstream's version is now coupled to a `health.py`
module / fixture tooling we don't vendor. All 20 tests pass after the re-pull.

**2026-10-05** — re-vendor to v3.26.0 (`5103ba478b38`; audit
`research/audits/2026-10-05-last30d-v3.26.0-revendor.md`, verdict SAFE). Reddit shuts off
RSS on 2026-11-13, and upstream `39a0adda954f` (#1189) replaced `reddit_rss.py` with
`reddit_search.py` (`/svc/shreddit/search/` and `/svc/shreddit/r/{sub}/search/`). So:
`reddit_search.py` added, `reddit_rss.py` and its fixture removed, `reddit_listing.py`
re-pulled, `http.py` un-held and re-pulled with its new dependency `health.py` (brings
`a46c419` #1069: credential headers dropped on cross-origin redirects). `reddit_lane.py`
rewired; the listing score-backfill step is gone because search results already carry
scores. Lazy imports: `reddit_search → .reddit._window_to_time_filter` is on the hot path,
so its two helper functions are extracted verbatim into `reddit.py`;
`reddit_listing → .reddit_arctic` and `http → .env` sit on paths this skill never runs, so
they stay unvendored — the same treatment as the older `reddit_enrich → .reddit` — and are
listed with reasons in `tests/test_vendored_symbols_resolve.py`. `relevance.py` held
(upstream's change only adds stopwords for a planner we don't vendor). New parser tests use
upstream's `reddit_search_{page1,last_page,challenge,no_results}.html` fixtures.

## Re-sync rule (for skill-evolve)

`sources.lock` pins the upstream commit the vendored files were copied from. On drift:
**re-pull the changed leaf file verbatim** (don't hand-merge) — especially when a Reddit
`/svc/shreddit/...` endpoint or the xAI `x_search` contract changes upstream. The parser
regression tests (`tests/test_reddit_parsers.py`) guard that a re-pull didn't break parsing;
`tests/test_vendored_symbols_resolve.py` guards that every helper a vendored file calls or
imports from a sibling exists here.
The original `reddit_lane.py` orchestration is ours and does not track upstream.
