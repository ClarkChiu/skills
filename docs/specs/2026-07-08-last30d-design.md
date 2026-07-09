# Design — `last30d` (last-30-days social-signal fetcher)

- **Date**: 2026-07-08
- **Status**: DESIGN — awaiting approval at the hard gate (no code yet)
- **Origin**: skill-curator verdict 🟨 vendor & customize on `mvanhorn/last30days-skill` (MIT). Audit: `research/audits/2026-07-08-last30days.md`.
- **Name**: **`last30d`** (confirmed 2026-07-08).

## 1. Purpose & altitude

A **fetch-and-score tool**, not a report generator. Given a topic/person, it pulls the last 30 days of discussion from a few social lanes, ranks each lane by that lane's **own engagement metric**, and emits a **structured digest**. Synthesis into prose is explicitly OUT of scope — the session model or `deep-research` does that from the digest.

- **In**: a topic string (`"Peter Steinberger"`, `"AI video tools"`), optional depth/lanes/format flags.
- **Out**: a per-lane, engagement-ranked Markdown digest to stdout (`--json` for structured handoff, `--save PATH` to write).
- **Boundary**: this is the *social-signal fetcher* (engagement-scored, platform data); `deep-research` is the *web-verified report* (open-web, cited synthesis); built-in `WebSearch` is generic search. No overlap — the digest can feed `deep-research`.

## 2. Scope — lanes

| Lane | How | Auth | Vendored? |
|---|---|---|---|
| **Reddit** | keyless engine: RSS/Atom discovery + shreddit `/svc` partials for real upvote scores + shreddit comment enrichment | none (browser-UA + rate-limit) | **YES — verbatim** |
| **X** | `xai_x`: `api.x.ai/v1/responses` `x_search` tool (first-party; xAI owns X) | **optional** `XAI_API_KEY` | **YES — verbatim** |
| **Hacker News** | own thin client on HN Algolia Search API | none | no — original |
| **GitHub** | own thin client on GitHub REST Search API | `GITHUB_TOKEN` (already in env) | no — original |
| **arXiv** | own thin client on the arXiv API (Atom) | none | no — original |
| **YouTube** | `yt-dlp` search + transcript + view/like counts | none (needs `yt-dlp` CLI) | no — original, **optional** |

**Two optional lanes, both degrade gracefully (Rule 12):**
- **X**: no `XAI_API_KEY` → section renders `skipped: no XAI_API_KEY`; rest runs free. Cost when enabled ~$0.5–1.5/run (Live Search $0.025/source; confirmed 2026-07-08).
- **YouTube**: no `yt-dlp` on PATH → section renders `skipped: yt-dlp not installed`; rest runs. `yt-dlp` is an external CLI (APM doesn't install it, like `ffmpeg` for `ig-reel`).

So **4 always-on lanes** (Reddit, HN, GitHub, arXiv — all keyless/free) **+ 2 optional** (X keyed, YouTube CLI). arXiv joins HN/GitHub as an original thin official-API client. Full dropped-platform register in §11.

**Explicitly dropped** from upstream: bird/cookie X path (Node + browser-cookie decrypt + rot), web-only X fallback (duplicates `deep-research`/`WebSearch`), Claude plugin wrapper, Go MCP server, setup wizard, author npm CLIs (`digg-pp-cli` etc.), SessionStart hook, hosted remote mode, ScrapeCreators paid backup, and every other platform (TikTok/IG/小紅書/TruthSocial/Pinterest/LinkedIn/Bluesky/Polymarket/YouTube/…).

## 3. Architecture

```
scripts/last30d.py (orchestrator CLI — ORIGINAL)
  ├─ lib/reddit_lane.py (ORIGINAL thin orchestrator — replaces upstream reddit_keyless)
  │     └─ VENDORED verbatim leaf/parser closure (self-closed, all shallow):
  │        reddit_rss, reddit_listing, reddit_shreddit, reddit_enrich,
  │        http, relevance, cjk, dates, log
  ├─ lib/x_lane.py  → VENDORED verbatim xai_x.py (+ http, log)
  ├─ lib/hn.py      (ORIGINAL — HN Algolia)
  ├─ lib/arxiv.py   (ORIGINAL — arXiv Atom API)
  ├─ lib/github.py  (ORIGINAL — GitHub REST Search)
  ├─ lib/youtube.py (ORIGINAL — yt-dlp, optional)
  └─ lib/digest.py  (ORIGINAL — render per-lane markdown / json)
```

**Revised vendoring boundary (2026-07-09, D4 update):** vendoring the upstream
`reddit_keyless` *orchestrator* balloons the closure (`reddit_arctic`→`rerank` 708L;
`reddit_enrich`→ lazy `reddit.py` keyed path 731L →`providers/query/schema/signals`) —
~1700 lines of keyed-path + rerank machinery we never use. The hard-to-reproduce IP
is only in the **leaf fetchers/parsers** (shreddit-endpoint knowledge + HTML-attribute
parsing), a shallow self-closed set. So we vendor **only those 10 leaf files verbatim**
(re-sync stays clean exactly where endpoints rot) and **write our own thin
`reddit_lane.py` orchestrator** (RSS discover → listing score-backfill → shreddit
comment enrich → merge/rank). Dropped: `reddit_keyless`, `reddit_arctic`, `reddit.py`
(keyed), `rerank`. This better honours "vendor hard engineering, write thin glue."

- Lanes run concurrently (ThreadPoolExecutor), each returns `[]` on failure — **never raises** (Rule 12: fail loud via the header counts + stderr, not by crashing the run).
- Depth tiers set per-lane top-N: **quick/default/deep = 10/25/50** (mirrors upstream).
- Ranking: per lane, by that lane's native engagement (Reddit: relevance-floored then upvotes+comments; X: likes/reposts; HN: points; GitHub: stars / PR-issue activity), sorted desc, top-N.

## 4. Output format

Per-lane Markdown sections to stdout; `--json` emits the same data structured; `--save PATH` writes to a file.

```
# last30days: "Peter Steinberger"  (2026-06-08 → 2026-07-08)
# lanes: reddit 8, x 6, hn 3, github 5  |  ranked by per-lane engagement

## Reddit
| # | title | score | comments | sub | date | link |
| 1 | Is he a hero or insufferable? | 569 | 210 | r/ClaudeCode | 06-24 | ↗ |
      ↳ top comment (312↑): "..."
## X   (skipped: no XAI_API_KEY  — or the table when keyed)
## Hacker News   | # | title | points | comments | date | link |
## GitHub        | # | repo/PR | stars/state | date | link |
```

- **Per-lane, never a merged score** — cross-platform engagement scales aren't comparable; a merged ranking would lie.
- **Reddit includes the single top comment** (the discussion's substance is often there); one per post, not the whole tree.
- Header shows per-lane counts so a silently-failing lane (0 results) is **visible** (Rule 12).

## 5. Interface

```
run: python3 scripts/last30d.py "<topic>" [--depth quick|default|deep]
        [--lanes reddit,x,hn,github] [--json] [--save PATH]
```
- SKILL.md instructs the agent to run this via Bash and read the digest; the agent (or a downstream `deep-research` call) synthesizes.
- `allowed-tools`: `Bash`, `Read`.
- Runtime: **Python 3, stdlib-mostly** (no Node). Reddit/HN keyless & keyed-GitHub need no paid key; X needs optional `XAI_API_KEY`.

## 6. Vendoring & re-sync (decision A — verbatim closure)

- Copy the transitive closure **verbatim**, stripping only imports/branches for dropped platforms; keep file structure aligned with upstream so `skill-evolve` yields a clean diff and a broken Reddit endpoint (or changed xAI contract) is a **re-pull**, not a manual port.
- `references/attribution.md`: adapted from `mvanhorn/last30days-skill` (MIT) — which files vendored, what was dropped, HN/GitHub original, audit pointer, the "re-sync = re-pull, keep verbatim" rule.
- `sources.lock`: pin upstream commit for each vendored file group (reddit modules, xai_x). This is a **copied-files** vendor, so drift = upstream edited those files (endpoint fixes) — high value to track.

## 7. Testing (Rule 9 — verify intent)

- **Offline parser tests** against vendored upstream fixtures (`reddit_listing_cards_sample.html`, `reddit_shreddit_comments_sample.html`, `reddit_search_rss_sample.xml`, `reddit_thread_sample.json`) — deterministic, no network: assert scores/comments/permalinks parse correctly. These fail loudly if a re-synced parser breaks.
- **`evals/evals.json`**: intent — per-lane ranking not merged; X skipped-not-crashed without key; digest header surfaces per-lane counts; fetch-only (no prose synthesis); depth tiers change N.
- One runnable self-check on the digest renderer (assert-based).

## 8. Registration & packaging (per CLAUDE.md)

- APM-managed → **skip `package_skill`**.
- Register: `apm.yml` (`- ./last30d/`), README self-built table row, `skill-curator/references/skill-map.md` (Standalone tools; boundary vs `deep-research`/`WebSearch`).
- Symlink into global (Claude Code + OpenCode).
- `attribution.md` + `sources.lock` **paired** (vendored-from-upstream).
- Language: **English** (engineering skill).

## 9. Key decisions (ADR-style, inline)

| # | Decision | Why | Rejected |
|---|---|---|---|
| D1 | Fetch+score only; no LLM synthesis | Don't duplicate `deep-research`; stay thin/composable | End-to-end brief |
| D2 | X via `xai_x` only, optional/keyed; drop bird+cookie+web-fallback | xAI=X first-party, pure-Python, no rot; official X free tier useless; web-fallback duplicates deep-research | bird cookie path; xurl |
| D3 | HN/GitHub written fresh on official APIs | Trivial stdlib clients; vendoring drags in coupling for no gain (Rule 2) | vendor upstream hackernews.py/github.py |
| D4 | Vendor only the **leaf fetchers/parsers** verbatim (10 shallow files) + xai_x; write our own thin `reddit_lane` orchestrator | Vendoring the `reddit_keyless` orchestrator balloons to ~1700L of unused keyed/rerank code; the hard IP is only the leaf parsers. Re-sync stays clean where endpoints rot | vendor whole closure (balloon); aggressive trim; full rewrite |
| D5 | Per-lane ranking, never merged | Cross-platform engagement scales incomparable | single merged score |

## 10. Open items for the gate

1. **Name**: `social-pulse` vs `last30d` vs other.
2. Anything in §2 scope you'd add back or drop further (e.g. do you want GitHub at all, or is it the weakest lane for you?).

## 11. Dropped-platforms register (recorded 2026-07-08 at user request)

Every content source the upstream supports, and why it's in/out for THIS user. Kept the register so a dropped lane can be reconsidered later without re-researching. **Reconsider candidates flagged ⭐.**

| Platform | 給什麼 | 取數方式 | 相關性 | v1 |
|---|---|---|---|---|
| Reddit | 討論＋真實 upvote＋留言 | 收錄免登入引擎 | 高 | **KEEP** |
| X | 貼文＋互動數 | xai_x（選用金鑰） | 高 | **KEEP（選用）** |
| Hacker News | 技術討論＋points | 官方 Algolia API | 高 | **KEEP** |
| GitHub | 近期 repo/PR/issue 活動 | 官方 REST（有 token） | 中高 | **KEEP** |
| ⭐ arXiv | 某主題最近學術預印本 | 官方 API（Atom，免金鑰免規避） | 高——協定/標準研究、論文、追 ML | reconsider（原創薄寫，同 HN） |
| ⭐ YouTube | 影片＋逐字稿＋互動 | yt-dlp（外部 CLI） | 中高——演講/解說/podcast 逐字稿對追 AI 高訊號 | reconsider（要 yt-dlp） |
| ⭐ Bluesky | X 替代站技術圈討論 | 官方 AT protocol（要 handle/app-pw） | 中——部分 dev/AI 外移，來源乾淨 | reconsider（要 creds） |
| Polymarket | 事件賭盤機率（真金） | 官方 API | 中低——投機/主動，與被動指數立場不合 | out |
| Techmeme | 科技新聞頭條聚合 | CLI | 中低——編輯策展，違「靠人不靠編輯」初衷 | out |
| LinkedIn | 公司/職缺/人物動態 | 爬取 | 中低——競品/PoC 情報偶用 | out |
| jobs / hiring_signals | 職缺當「某公司在建什麼」訊號 | 聚合 | 中低——競品情報偶用 | out |
| StockTwits | 散戶炒股情緒 | 爬取 | 低——對被動指數＝雜訊 | out |
| Threads | Meta 版 X | 爬取 | 低 | out |
| Instagram | IG 貼文/互動 | 爬取 | 低（你是產出端非輸入端） | out |
| TikTok | 短影片/互動 | 爬取 | 低 | out |
| Trustpilot | 商家評價 | 爬取 | 低（售前調查） | out |
| Pinterest | 圖釘 | 爬取 | 無 | out |
| 小紅書 Xiaohongshu | 中國社群電商 | API | 無（陸站，與 zh-TW 傾向相斥） | out |
| TruthSocial | Trump 圈政治 | 爬取 | 無 | out |
| Digg | 重啟版 Digg | 作者 CLI | 低 | out |

（web-search providers〔perplexity/serper/brave/parallel/exa〕不是社群來源，是泛網搜後端，本技能不收——那塊 `deep-research`/`WebSearch` 已覆蓋。）

## 12. Self-review

- Placeholder scan: none.
- Internal consistency: lanes in §2 = architecture §3 = output §4 = decisions §9. ✓
- Scope: single skill, one subsystem; not oversized. ✓
- Ambiguity: dependency closure exact file list is a plan-phase detail (will be enumerated by reading upstream imports); vendor approach (verbatim) is fixed. Name unconfirmed (flagged). ✓
- Rule-2 check: HN/GitHub kept to thin stdlib; only the hard-to-reproduce (Reddit keyless, xai_x) vendored. ✓
```
```
