---
name: p2pscout
description: >
  Search BitTorrent resources across multiple index sources and rank by REAL,
  measured downloadability (DHT + trackers, optional handshake verification) — so you
  surface the one that can actually be fetched right now, not just one that exists in a
  listing. This tool does not transfer data; downloads are delegated to aria2. USE
  WHEN the user wants to 「找某資源的種子 / 磁力連結」, 「確認資源還活著」, or 「下載前先驗證可下載性」 —
  i.e. find a torrent/magnet for something, check whether a resource still has seeders,
  or verify downloadability before downloading.
---

# p2pscout — agent usage guide

Searches across multiple sources and ranks by **measured** downloadability. An
indexer's self-reported seed count is often stale or inflated, so p2pscout probes the
swarm itself: DHT lookups, tracker scrapes, and optionally a real handshake that reads
a peer's bitfield to confirm it holds every piece.

## When to call

- The user wants to find a torrent/magnet for X, or asks whether X still has seeders.
- Before downloading, to confirm a resource is actually alive.
- **Do NOT** use it for: fetching arbitrary URLs, or transferring non-torrent content.
  Transfer is delegated to aria2 by `p2pscout get`.

## Prerequisites

Needs local Go 1.25+. **No manual build** — invoke via `go run` (compiles once, then
cached and instant). Run all commands **from this skill's directory** (the folder this
SKILL.md lives in), because the Go source is here. `get --auto` additionally needs
aria2c running in RPC mode.

## Invocation

Run from this skill's directory (replace `<query>` with keywords):

```sh
go run ./cmd/p2pscout <query>                      # shallow: multi-source + downloadability ranking (seconds)
go run ./cmd/p2pscout --full <query>               # full: adds handshake verification (tens of seconds)
go run ./cmd/p2pscout --json <query>               # machine-readable; use this for scripts
go run ./cmd/p2pscout --providers apibay,torrentz2 <query>   # pick sources (comma-separated, or all)
go run ./cmd/p2pscout get --auto --aria2-secret=TOKEN --dir ~/Downloads <query>
```

> Want a resident binary to skip recompiling each time:
> `go build -o p2pscout ./cmd/p2pscout`, then use `./p2pscout <query>`.

| flag | default | meaning |
|------|---------|---------|
| `-n, --limit` | 20 | max results per provider |
| `--providers` | all | comma-separated providers, or `all` |
| `--full` | false | add handshake verification (slow, but proves downloadability) |
| `--json` | false | JSON output |
| `-v, --verbose` | false | include the indexer's self-reported seed/peer counts |
| `--timeout` | 90s | overall budget |
| `--concurrency` | 4 | how many to probe at once |

## Reading the verdict

- `verdict=downloadable` (full mode only): fetchable right now, ranked first.
- `verdict=live`: has peers but not handshake-confirmed (or shallow mode). Run `--full`
  before downloading.
- `verdict=dead`: no peers found, don't recommend.
- `--json` `score` is already sorted descending; the `magnet` field can go straight to a
  torrent client or to `p2pscout get`.

## Download delegation

`p2pscout get <query>` auto-enables `--full` and picks the highest-scoring item judged
`downloadable`. If you already know the exact resource, use
`p2pscout get --magnet "<magnet>"` to skip search and verify that magnet directly.
`--magnet -` reads a magnet from stdin for pipelining (an upstream that only emits
magnets and this tool that verifies+downloads stay decoupled):
`p2p-ranking-board get <id> | p2pscout get --magnet - --auto`.

Behavior:
- Without `--auto`: prints the magnet only, no download (the user decides).
- With `--auto`: queues the download via aria2 RPC, prints the job id.
- Top result not `downloadable`: refuses to queue, returns a clear message.
- aria2 not running / unreachable: returns a clear error
  (`is aria2c running with --enable-rpc?`), never fails silently.

## Failure modes

- No results: non-zero exit `no results`. Try different keywords.
- Network blocks UDP: DHT degrades to zero; trackers + handshake still work, ranking
  compresses but stays meaningful.
- `torrentz2` redesign: that provider returns zero rows, parsing needs updating. Other
  providers are unaffected.

## Don't

- Don't run it in a tight loop (each run joins the DHT and opens many connections) — one
  run per query.
- Don't feed a magnet straight to a downloader without showing the user — they may want a
  result other than #1.
- Don't parse the table output downstream; use `--json`.
