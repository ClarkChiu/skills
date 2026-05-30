package search

import (
	"fmt"
	"net/url"
	"strings"
)

// usableScheme reports whether a tracker URL uses a scheme anacrolix/torrent can
// actually dial. wss:// and friends must be dropped or the client's tracker
// dispatcher panics on them.
func usableScheme(raw string) bool {
	switch {
	case strings.HasPrefix(raw, "udp://"),
		strings.HasPrefix(raw, "http://"),
		strings.HasPrefix(raw, "https://"):
		return true
	default:
		return false
	}
}

// CleanMagnet parses a magnet URI and returns the lowercase-hex infohash, the
// dialable trackers, and a rebuilt magnet that contains only those trackers.
func CleanMagnet(magnet string) (infoHash string, trackers []string, cleaned string) {
	u, err := url.Parse(magnet)
	if err != nil {
		return "", nil, magnet
	}
	q := u.Query()

	if xt := q.Get("xt"); strings.HasPrefix(xt, "urn:btih:") {
		infoHash = strings.ToLower(strings.TrimPrefix(xt, "urn:btih:"))
	}
	for _, tr := range q["tr"] {
		if usableScheme(strings.ToLower(tr)) {
			trackers = append(trackers, tr)
		}
	}

	q.Del("tr")
	for _, tr := range trackers {
		q.Add("tr", tr)
	}
	u.RawQuery = q.Encode()
	return infoHash, trackers, u.String()
}

// MagnetFor builds a minimal magnet from a bare infohash plus an optional
// display name and tracker list. Used by providers (e.g. apibay) that hand back
// an infohash rather than a full magnet URI.
func MagnetFor(infoHash, name string, trackers []string) string {
	var b strings.Builder
	fmt.Fprintf(&b, "magnet:?xt=urn:btih:%s", strings.ToLower(infoHash))
	if name != "" {
		fmt.Fprintf(&b, "&dn=%s", url.QueryEscape(name))
	}
	for _, tr := range trackers {
		if usableScheme(strings.ToLower(tr)) {
			fmt.Fprintf(&b, "&tr=%s", url.QueryEscape(tr))
		}
	}
	return b.String()
}
