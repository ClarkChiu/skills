package search

import (
	"strings"
	"testing"
)

func TestCleanMagnet_lowercasesHashAndDropsBadSchemes(t *testing.T) {
	// WHY: the infohash is the cross-provider merge key, so it MUST be normalized
	// to lowercase or the same torrent from two sources won't dedup. And wss://
	// trackers MUST be stripped — anacrolix/torrent panics on them.
	in := "magnet:?xt=urn:btih:ABCDEF0123456789ABCDEF0123456789ABCDEF01" +
		"&tr=udp%3A%2F%2Ftracker.example%3A1337%2Fannounce" +
		"&tr=wss%3A%2F%2Fws.example%3A443"
	ih, trackers, cleaned := CleanMagnet(in)

	if ih != "abcdef0123456789abcdef0123456789abcdef01" {
		t.Fatalf("infohash not lowercased: %q", ih)
	}
	if len(trackers) != 1 || !strings.HasPrefix(trackers[0], "udp://") {
		t.Fatalf("want only the udp tracker, got %v", trackers)
	}
	if strings.Contains(cleaned, "wss") {
		t.Fatalf("cleaned magnet still carries wss tracker: %s", cleaned)
	}
}

func TestCleanMagnet_invalidInputYieldsNoHash(t *testing.T) {
	// WHY: the aggregator drops rows with an empty infohash (undownloadable).
	// A magnet without a btih xt must therefore produce "".
	if ih, _, _ := CleanMagnet("magnet:?dn=no+hash+here"); ih != "" {
		t.Fatalf("expected empty infohash, got %q", ih)
	}
}

func TestMagnetFor_buildsDialableMagnet(t *testing.T) {
	// WHY: apibay hands back only a bare hash; MagnetFor must produce a usable
	// magnet (lowercased xt, escaped name, only dialable trackers) so a
	// downstream client / handshake can act on it.
	m := MagnetFor("ABCDEF0123456789ABCDEF0123456789ABCDEF01", "My File",
		[]string{"udp://ok.example:1337/announce", "wss://bad.example:443"})

	if !strings.Contains(m, "xt=urn:btih:abcdef0123456789abcdef0123456789abcdef01") {
		t.Fatalf("xt missing or not lowercased: %s", m)
	}
	if !strings.Contains(m, "dn=My+File") {
		t.Fatalf("display name not escaped: %s", m)
	}
	if strings.Contains(m, "wss") {
		t.Fatalf("non-dialable tracker leaked in: %s", m)
	}
}
