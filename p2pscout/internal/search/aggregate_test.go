package search

import (
	"strings"
	"testing"
)

func TestMerge_dedupsByInfoHashAcrossSources(t *testing.T) {
	// WHY: the whole point of multi-provider search is that the same torrent
	// from two indexes collapses into one row — unioning trackers and taking the
	// best claimed seeder count — instead of showing two near-duplicate hits.
	rows := []Result{
		{Source: "apibay", InfoHash: "aa", Title: "X", ClaimedSeeds: 10,
			Magnet: "magnet:?xt=urn:btih:aa&tr=udp://a", Trackers: []string{"udp://a"}},
		{Source: "torrentz2", InfoHash: "aa", Title: "X", ClaimedSeeds: 42,
			Magnet: "magnet:?xt=urn:btih:aa&tr=udp://b", Trackers: []string{"udp://b"}},
	}
	out := merge(rows)

	if len(out) != 1 {
		t.Fatalf("same infohash must merge to one row, got %d", len(out))
	}
	r := out[0]
	if !strings.Contains(r.Source, "apibay") || !strings.Contains(r.Source, "torrentz2") {
		t.Fatalf("merged row should credit both sources, got %q", r.Source)
	}
	if r.ClaimedSeeds != 42 {
		t.Fatalf("merged row should keep the max claimed seeds, got %d", r.ClaimedSeeds)
	}
	if len(r.Trackers) != 2 {
		t.Fatalf("trackers should be unioned, got %v", r.Trackers)
	}
}

func TestMerge_dropsRowsWithoutInfoHash(t *testing.T) {
	// WHY: a row with no infohash can't be verified or downloaded, so it must be
	// discarded rather than shown as a dead-end result.
	out := merge([]Result{{Source: "x", InfoHash: "", Title: "junk"}})
	if len(out) != 0 {
		t.Fatalf("hashless row should be dropped, got %d rows", len(out))
	}
}

func TestMerge_sortsByClaimedSeedsDesc(t *testing.T) {
	// WHY: the swarm pass works through candidates in order; pre-sorting by
	// claimed seeders puts the likeliest-healthy ones first.
	out := merge([]Result{
		{InfoHash: "a", ClaimedSeeds: 5},
		{InfoHash: "b", ClaimedSeeds: 50},
	})
	if out[0].InfoHash != "b" {
		t.Fatalf("higher claimed-seed row should sort first, got %q", out[0].InfoHash)
	}
}
