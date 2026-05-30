package search

import (
	"context"
	"sort"
	"strings"
	"sync"
)

// FanOut runs query against every provider concurrently and merges the results
// by infohash. The same torrent seen on two indexes becomes one Result: trackers
// are unioned, claimed counts take the max, and Source lists every index that
// had it. A provider that errors or hangs is skipped — partial coverage beats
// none. The merged slice is pre-sorted by claimed seeders so the swarm pass has
// a reasonable order to work through.
func FanOut(ctx context.Context, providers []Provider, query string, perProvider int) []Result {
	var (
		mu  sync.Mutex
		acc []Result
		wg  sync.WaitGroup
	)
	for _, p := range providers {
		wg.Add(1)
		go func(p Provider) {
			defer wg.Done()
			rows, err := p.Find(ctx, query, perProvider)
			if err != nil {
				return
			}
			mu.Lock()
			acc = append(acc, rows...)
			mu.Unlock()
		}(p)
	}
	wg.Wait()
	return merge(acc)
}

func merge(rows []Result) []Result {
	idx := map[string]int{}
	var out []Result
	for _, r := range rows {
		if r.InfoHash == "" {
			continue // unverifiable / undownloadable without a hash
		}
		if at, ok := idx[r.InfoHash]; ok {
			fold(&out[at], r)
			continue
		}
		idx[r.InfoHash] = len(out)
		out = append(out, r)
	}
	sort.SliceStable(out, func(i, j int) bool { return out[i].ClaimedSeeds > out[j].ClaimedSeeds })
	return out
}

// fold merges src into the already-seen dst.
func fold(dst *Result, src Result) {
	dst.Source = addSource(dst.Source, src.Source)
	dst.Trackers = unionStrings(dst.Trackers, src.Trackers)
	if src.ClaimedSeeds > dst.ClaimedSeeds {
		dst.ClaimedSeeds = src.ClaimedSeeds
	}
	if src.ClaimedPeers > dst.ClaimedPeers {
		dst.ClaimedPeers = src.ClaimedPeers
	}
	if dst.Title == "" {
		dst.Title = src.Title
	}
	if dst.SizeBytes == 0 {
		dst.SizeBytes = src.SizeBytes
	}
	if dst.Published.IsZero() {
		dst.Published = src.Published
	}
	// Prefer a magnet that already carries trackers.
	if !strings.Contains(dst.Magnet, "&tr=") && strings.Contains(src.Magnet, "&tr=") {
		dst.Magnet = src.Magnet
	}
}

func addSource(have, add string) string {
	switch {
	case add == "" || have == add:
		return have
	case have == "":
		return add
	}
	for _, s := range strings.Split(have, "+") {
		if s == add {
			return have
		}
	}
	return have + "+" + add
}

func unionStrings(a, b []string) []string {
	seen := make(map[string]struct{}, len(a)+len(b))
	out := make([]string, 0, len(a)+len(b))
	for _, s := range append(a, b...) {
		if _, ok := seen[s]; !ok {
			seen[s] = struct{}{}
			out = append(out, s)
		}
	}
	return out
}
