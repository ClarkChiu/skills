package swarm

import (
	"testing"
	"time"
)

func TestGrade_fullWithConfirmedIsDownloadable(t *testing.T) {
	// WHY: a confirmed seeder (handshook + holds every piece) is the ONLY signal
	// that proves the torrent downloads now. In full depth, that must read as
	// downloadable — this is the verdict `get` gates the download on.
	r := &Report{Depth: Full, DHTPeers: 5, Probe: Probe{Confirmed: 2, Pieces: 100}}
	r.grade()
	if r.Verdict != Downloadable {
		t.Fatalf("full + confirmed>0 must be downloadable, got %q", r.Verdict)
	}
}

func TestGrade_fullWithoutConfirmedIsLiveNotDownloadable(t *testing.T) {
	// WHY: peers exist (DHT) but none confirmed holding all pieces — a dying
	// swarm. Must NOT be downloadable, or `get` would queue an unfetchable torrent.
	r := &Report{Depth: Full, DHTPeers: 8, Probe: Probe{Confirmed: 0}}
	r.grade()
	if r.Verdict != Live {
		t.Fatalf("full + 0 confirmed but peers present must be live, got %q", r.Verdict)
	}
}

func TestGrade_shallowNeverClaimsDownloadable(t *testing.T) {
	// WHY: shallow mode does no handshake, so it cannot prove downloadability.
	// Even with peers it must stay at live, never downloadable.
	r := &Report{Depth: Shallow, DHTPeers: 200, TrackerSeeds: 50}
	r.grade()
	if r.Verdict != Live {
		t.Fatalf("shallow must cap at live, got %q", r.Verdict)
	}
}

func TestGrade_noSignalsIsDead(t *testing.T) {
	// WHY: no DHT peers, no tracker seeders, no connections → nothing to download
	// from. Must be dead so it's never recommended.
	r := &Report{Depth: Full}
	r.grade()
	if r.Verdict != Dead {
		t.Fatalf("zero signals must be dead, got %q", r.Verdict)
	}
}

func TestGrade_confirmedSeedersDominateScore(t *testing.T) {
	// WHY: scoring must rank a torrent with confirmed seeders above one with only
	// raw DHT noise, even when the latter has far more DHT peers — otherwise the
	// "proven" signal loses to unverified swarm size.
	confirmed := &Report{Depth: Full, DHTPeers: 5, Probe: Probe{Confirmed: 3, Pieces: 10}}
	dhtOnly := &Report{Depth: Full, DHTPeers: 20}
	confirmed.grade()
	dhtOnly.grade()
	if confirmed.Score <= dhtOnly.Score {
		t.Fatalf("confirmed=3 (%.1f) should outscore dht=20 only (%.1f)", confirmed.Score, dhtOnly.Score)
	}
}

func TestRecency_newerScoresHigher(t *testing.T) {
	// WHY: recency is only a tie-breaker, but it must be monotonic — a fresher
	// torrent should never get a lower recency weight than an older one.
	newer := recency(time.Now().Add(-30 * 24 * time.Hour))
	older := recency(time.Now().Add(-5 * 365 * 24 * time.Hour))
	if !(newer > older) {
		t.Fatalf("newer (%.3f) should exceed older (%.3f)", newer, older)
	}
	if recency(time.Time{}) != 0 {
		t.Fatalf("unknown date should yield 0 recency")
	}
}
