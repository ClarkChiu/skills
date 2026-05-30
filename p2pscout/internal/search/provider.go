// Package search is the multi-source discovery layer: a query is fanned out
// across every registered Provider concurrently, and the rows are merged by
// infohash. Adding a new index means implementing Provider and registering it —
// nothing else in the pipeline needs to know about it.
package search

import (
	"context"
	"time"
)

// Result is one candidate torrent as a single provider saw it. Swarm-health
// fields live elsewhere (the swarm package fills them in a later pass); a
// provider reports only what the index gave it, plus a cleaned magnet.
type Result struct {
	Source       string    // which provider(s) produced this row
	Title        string    // human-readable torrent name
	InfoHash     string    // lowercase hex btih — the cross-provider merge key
	Magnet       string    // cleaned magnet (udp/http/https trackers only)
	SizeBytes    int64     // content size, 0 when the index omits it
	ClaimedSeeds int       // seeders the index advertises (unverified)
	ClaimedPeers int       // leechers the index advertises
	Published    time.Time // listing date, zero when unknown
	Trackers     []string  // trackers pulled from the magnet, for scraping
}

// Provider is one searchable torrent index.
//
// Rules of the contract:
//   - Find honours ctx deadline/cancellation.
//   - Every returned Result.Magnet MUST be run through CleanMagnet so it only
//     carries udp/http/https trackers (anacrolix/torrent panics otherwise).
//   - A nil error with an empty slice means "no hits here" — not fatal; the
//     aggregator simply moves on.
type Provider interface {
	Key() string
	Find(ctx context.Context, query string, limit int) ([]Result, error)
}
