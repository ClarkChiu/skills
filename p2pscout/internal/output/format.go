package output

import (
	"encoding/json"
	"fmt"
	"io"
	"strings"
	"time"

	"github.com/olekukonko/tablewriter"

	"github.com/freebooters/p2pscout/internal/swarm"
)

func Table(w io.Writer, reports []*swarm.Report, verbose bool) error {
	t := tablewriter.NewWriter(w)
	if verbose {
		t.Header("#", "title", "src", "size", "age", "verdict", "conf", "dht", "trk", "claimed", "score", "magnet")
	} else {
		t.Header("#", "title", "src", "size", "age", "verdict", "conf", "dht", "trk", "score", "magnet")
	}
	for i, r := range reports {
		row := []string{
			fmt.Sprintf("%d", i+1),
			clip(r.Title, 50),
			r.Source,
			bytesHuman(r.SizeBytes),
			age(r.Published),
			string(r.Verdict),
			confirmedCell(r),
			fmt.Sprintf("%d", r.DHTPeers),
			fmt.Sprintf("%.1f", r.TrackerSeeds),
		}
		if verbose {
			row = append(row, fmt.Sprintf("%d/%d", r.ClaimedSeeds, r.ClaimedPeers))
		}
		row = append(row, fmt.Sprintf("%.1f", r.Score), magnetShort(r.InfoHash))
		if err := t.Append(row); err != nil {
			return err
		}
	}
	return t.Render()
}

// confirmedCell shows confirmed seeders, or "-" in shallow mode where no
// handshake ran (0 would misread as "verified empty").
func confirmedCell(r *swarm.Report) string {
	if r.Depth != swarm.Full {
		return "-"
	}
	return fmt.Sprintf("%d", r.Probe.Confirmed)
}

func magnetShort(infoHash string) string { return "magnet:?xt=urn:btih:" + strings.ToUpper(infoHash) }

func JSON(w io.Writer, reports []*swarm.Report) error {
	type row struct {
		Rank         int     `json:"rank"`
		Title        string  `json:"title"`
		Source       string  `json:"source"`
		Depth        string  `json:"depth"`
		Verdict      string  `json:"verdict"`
		InfoHash     string  `json:"infohash"`
		Magnet       string  `json:"magnet"`
		SizeBytes    int64   `json:"size_bytes"`
		Published    string  `json:"published,omitempty"`
		ClaimedSeeds int     `json:"claimed_seeders"`
		ClaimedPeers int     `json:"claimed_peers"`
		DHTPeers     int     `json:"dht_peers"`
		TrackerSeeds float64 `json:"tracker_seeders_avg"`
		TrackerCount int     `json:"tracker_count"`
		TrackerOK    int     `json:"tracker_responded"`
		GotMetadata  bool    `json:"got_metadata"`
		Pieces       int     `json:"pieces"`
		Connected    int     `json:"peers_connected"`
		Confirmed    int     `json:"seeders_confirmed"`
		Partial      int     `json:"peers_partial"`
		Score        float64 `json:"score"`
	}
	out := make([]row, 0, len(reports))
	for i, r := range reports {
		ok := 0
		for _, ts := range r.Trackers {
			if ts.Err == nil {
				ok++
			}
		}
		var pub string
		if !r.Published.IsZero() {
			pub = r.Published.Format(time.RFC3339)
		}
		out = append(out, row{
			Rank: i + 1, Title: r.Title, Source: r.Source, Depth: r.Depth.String(),
			Verdict: string(r.Verdict), InfoHash: r.InfoHash, Magnet: r.Magnet,
			SizeBytes: r.SizeBytes, Published: pub, ClaimedSeeds: r.ClaimedSeeds,
			ClaimedPeers: r.ClaimedPeers, DHTPeers: r.DHTPeers, TrackerSeeds: r.TrackerSeeds,
			TrackerCount: len(r.Trackers), TrackerOK: ok, GotMetadata: r.Probe.GotMetadata,
			Pieces: r.Probe.Pieces, Connected: r.Probe.Connected, Confirmed: r.Probe.Confirmed,
			Partial: r.Probe.Partial, Score: r.Score,
		})
	}
	enc := json.NewEncoder(w)
	enc.SetIndent("", "  ")
	return enc.Encode(out)
}

func bytesHuman(b int64) string {
	const unit = 1024.0
	if b < int64(unit) {
		return fmt.Sprintf("%d B", b)
	}
	div, exp := unit, 0
	for n := float64(b) / unit; n >= unit; n /= unit {
		div *= unit
		exp++
	}
	return fmt.Sprintf("%.2f %s", float64(b)/div, []string{"KB", "MB", "GB", "TB", "PB"}[exp])
}

func age(t time.Time) string {
	if t.IsZero() {
		return "-"
	}
	d := time.Since(t)
	switch {
	case d < 24*time.Hour:
		return fmt.Sprintf("%dh", int(d.Hours()))
	case d < 30*24*time.Hour:
		return fmt.Sprintf("%dd", int(d.Hours()/24))
	case d < 365*24*time.Hour:
		return fmt.Sprintf("%dmo", int(d.Hours()/24/30))
	default:
		return fmt.Sprintf("%dy", int(d.Hours()/24/365))
	}
}

func clip(s string, n int) string {
	s = strings.TrimSpace(s)
	if len(s) <= n {
		return s
	}
	return s[:n-1] + "…"
}
