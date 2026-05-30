package swarm

import (
	"context"
	"encoding/hex"
	"errors"
	"strings"
	"sync"
	"time"

	"github.com/anacrolix/torrent/tracker"
	"github.com/anacrolix/torrent/types/infohash"
)

// scrape queries every tracker concurrently and returns one stat per tracker.
// Each scrape is bounded independently so a single slow tracker cannot stall the
// rest.
func scrape(ctx context.Context, infoHash string, trackers []string, perTracker time.Duration) []TrackerStat {
	ih, ok := toInfoHash(infoHash)
	if !ok {
		return nil
	}
	stats := make([]TrackerStat, len(trackers))
	var wg sync.WaitGroup
	for i, url := range trackers {
		wg.Add(1)
		go func(i int, url string) {
			defer wg.Done()
			stats[i] = scrapeOne(ctx, url, ih, perTracker)
		}(i, url)
	}
	wg.Wait()
	return stats
}

func scrapeOne(parent context.Context, url string, ih infohash.T, timeout time.Duration) TrackerStat {
	st := TrackerStat{Tracker: url}
	if !dialable(url) {
		st.Err = errors.New("unsupported scheme")
		return st
	}
	ctx, cancel := context.WithTimeout(parent, timeout)
	defer cancel()

	cl, err := tracker.NewClient(url, tracker.NewClientOpts{})
	if err != nil {
		st.Err = err
		return st
	}
	defer cl.Close()

	resp, err := cl.Scrape(ctx, []infohash.T{ih})
	if err != nil {
		st.Err = err
		return st
	}
	if len(resp) == 0 {
		st.Err = errors.New("empty scrape")
		return st
	}
	st.Seeders = int(resp[0].Seeders)
	st.Leechers = int(resp[0].Leechers)
	return st
}

func dialable(url string) bool {
	u := strings.ToLower(url)
	return strings.HasPrefix(u, "udp://") || strings.HasPrefix(u, "http://") || strings.HasPrefix(u, "https://")
}

func toInfoHash(s string) (infohash.T, bool) {
	var ih infohash.T
	raw, err := hex.DecodeString(s)
	if err != nil || len(raw) != 20 {
		return ih, false
	}
	copy(ih[:], raw)
	return ih, true
}
