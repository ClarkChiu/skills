// Package swarm measures whether a torrent's swarm is actually alive, instead of
// trusting the seeder counts an index advertises. It probes three independent
// signals — DHT peer discovery, tracker scrapes, and (in deep mode) real BEP-9
// handshakes that read each peer's piece bitfield — and folds them into a score
// plus a plain-language verdict an agent can act on.
package swarm

import "time"

// Depth controls how hard a torrent is probed.
type Depth int

const (
	// Shallow: DHT + tracker only. No handshake. Fast enough to rank in bulk.
	Shallow Depth = iota
	// Full: also handshake peers and confirm they hold every piece. Slow, but it
	// is the only signal that proves the torrent will actually download now.
	Full
)

func (d Depth) String() string {
	if d == Full {
		return "full"
	}
	return "shallow"
}

// Verdict is the agent-facing conclusion.
type Verdict string

const (
	Downloadable Verdict = "downloadable" // full mode, at least one confirmed seeder
	Live         Verdict = "live"         // peers exist but none confirmed (or shallow mode)
	Dead         Verdict = "dead"         // no peers found anywhere
)

// TrackerStat is one tracker's scrape outcome.
type TrackerStat struct {
	Tracker  string
	Seeders  int
	Leechers int
	Err      error
}

// Probe is the result of the handshake pass (zero-valued unless Full depth).
type Probe struct {
	GotMetadata bool
	Pieces      int
	Connected   int // peers that completed a handshake
	Confirmed   int // peers whose bitfield covers every piece (true seeders)
	Partial     int // connected peers still missing pieces
}

// Report is everything known about one candidate after probing.
type Report struct {
	InfoHash     string
	Title        string
	SizeBytes    int64
	Magnet       string
	Source       string
	Published    time.Time
	ClaimedSeeds int
	ClaimedPeers int

	Depth        Depth
	DHTPeers     int
	Trackers     []TrackerStat
	TrackerSeeds float64
	Probe        Probe

	Score   float64
	Verdict Verdict
}

// trackerSeedAvg averages seeders across trackers that answered.
func trackerSeedAvg(stats []TrackerStat) float64 {
	var sum, n int
	for _, s := range stats {
		if s.Err == nil {
			sum += s.Seeders
			n++
		}
	}
	if n == 0 {
		return 0
	}
	return float64(sum) / float64(n)
}

// recency maps age to a small 0..1 tie-breaker; newer scores slightly higher.
func recency(published time.Time) float64 {
	if published.IsZero() {
		return 0
	}
	years := time.Since(published).Hours() / 24 / 365
	if years < 0 {
		years = 0
	}
	return 1 / (1 + years)
}

// grade fills Score and Verdict from the gathered signals. Confirmed seeders
// dominate because they are the only proven-downloadable signal; DHT and tracker
// numbers are weaker corroboration that breaks ties and carries shallow mode.
func (r *Report) grade() {
	r.TrackerSeeds = trackerSeedAvg(r.Trackers)
	r.Score = 15*float64(r.Probe.Confirmed) +
		2*float64(r.DHTPeers) +
		1.5*r.TrackerSeeds +
		recency(r.Published)

	switch {
	case r.Depth == Full && r.Probe.Confirmed > 0:
		r.Verdict = Downloadable
	case r.DHTPeers > 0 || r.TrackerSeeds > 0 || r.Probe.Connected > 0:
		r.Verdict = Live
	default:
		r.Verdict = Dead
	}
}
