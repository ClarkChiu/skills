package search

import (
	"context"
	"encoding/json"
	"fmt"
	"net/http"
	"net/url"
	"strconv"
	"time"
)

// apibay is The Pirate Bay's JSON backend. Unlike an HTML index it returns the
// infohash and seeder count directly, so there is no markup to break and no
// per-result detail fetch — one request yields everything. That robustness is
// why it is the primary provider.
func init() {
	register("apibay", func() Provider { return &apibay{http: &http.Client{Timeout: 15 * time.Second}} })
}

const apibaySearch = "https://apibay.org/q.php"

// apibay returns only a bare infohash, so we attach a set of well-known open
// trackers to make the magnet dialable. DHT fills in the rest.
var apibayTrackers = []string{
	"udp://tracker.opentrackr.org:1337/announce",
	"udp://open.tracker.cl:1337/announce",
	"udp://tracker.openbittorrent.com:6969/announce",
	"udp://exodus.desync.com:6969/announce",
	"udp://tracker.torrent.eu.org:451/announce",
}

type apibay struct{ http *http.Client }

func (a *apibay) Key() string { return "apibay" }

// apibayRow mirrors the q.php response. Numeric fields arrive as JSON strings.
type apibayRow struct {
	Name     string `json:"name"`
	InfoHash string `json:"info_hash"`
	Seeders  string `json:"seeders"`
	Leechers string `json:"leechers"`
	Size     string `json:"size"`
	Added    string `json:"added"`
}

func (a *apibay) Find(ctx context.Context, query string, limit int) ([]Result, error) {
	u := fmt.Sprintf("%s?q=%s&cat=0", apibaySearch, url.QueryEscape(query))
	req, err := http.NewRequestWithContext(ctx, http.MethodGet, u, nil)
	if err != nil {
		return nil, err
	}
	resp, err := a.http.Do(req)
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()
	if resp.StatusCode != http.StatusOK {
		return nil, fmt.Errorf("apibay status %d", resp.StatusCode)
	}

	var rows []apibayRow
	if err := json.NewDecoder(resp.Body).Decode(&rows); err != nil {
		return nil, err
	}

	out := make([]Result, 0, len(rows))
	for _, r := range rows {
		// apibay signals "nothing found" with a single zero-hash sentinel row.
		if r.InfoHash == "" || r.InfoHash == "0000000000000000000000000000000000000000" {
			continue
		}
		ih, trackers, magnet := CleanMagnet(MagnetFor(r.InfoHash, r.Name, apibayTrackers))
		if ih == "" {
			continue
		}
		out = append(out, Result{
			Source:       a.Key(),
			Title:        r.Name,
			InfoHash:     ih,
			Magnet:       magnet,
			SizeBytes:    atoi64(r.Size),
			ClaimedSeeds: atoi(r.Seeders),
			ClaimedPeers: atoi(r.Leechers),
			Published:    epoch(r.Added),
			Trackers:     trackers,
		})
		if len(out) >= limit {
			break
		}
	}
	return out, nil
}

func atoi(s string) int     { n, _ := strconv.Atoi(s); return n }
func atoi64(s string) int64 { n, _ := strconv.ParseInt(s, 10, 64); return n }
func epoch(s string) time.Time {
	sec, err := strconv.ParseInt(s, 10, 64)
	if err != nil || sec <= 0 {
		return time.Time{}
	}
	return time.Unix(sec, 0)
}
