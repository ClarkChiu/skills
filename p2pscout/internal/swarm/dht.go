package swarm

import (
	"context"
	"encoding/hex"
	"net/netip"
)

// discover runs a DHT get_peers traversal for the infohash and returns the
// unique peer addresses seen before ctx expires or the traversal settles.
// Returns nil on a malformed hash or DHT error — a failed lookup just means zero
// peers, not a fatal condition.
func (s *Scout) discover(ctx context.Context, infoHash string) []netip.AddrPort {
	raw, err := hex.DecodeString(infoHash)
	if err != nil || len(raw) != 20 {
		return nil
	}
	var key [20]byte
	copy(key[:], raw)

	trav, err := s.dht.AnnounceTraversal(key)
	if err != nil {
		return nil
	}
	defer trav.Close()

	found := map[netip.AddrPort]struct{}{}
	done := trav.Finished()
	for {
		select {
		case <-ctx.Done():
			return collect(found)
		case <-done:
			return collect(found)
		case batch, ok := <-trav.Peers:
			if !ok {
				return collect(found)
			}
			for _, p := range batch.Peers {
				addr, ok := netip.AddrFromSlice(p.IP)
				if !ok || p.Port <= 0 {
					continue
				}
				found[netip.AddrPortFrom(addr.Unmap(), uint16(p.Port))] = struct{}{}
			}
		}
	}
}

func collect(set map[netip.AddrPort]struct{}) []netip.AddrPort {
	out := make([]netip.AddrPort, 0, len(set))
	for ap := range set {
		out = append(out, ap)
	}
	return out
}
