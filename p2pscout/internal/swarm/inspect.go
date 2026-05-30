package swarm

import (
	"context"
	"net/netip"
	"time"

	"github.com/anacrolix/torrent"
)

const (
	peerSampleCap = 30
	settleWindow  = 8 * time.Second // let bitfields arrive after metadata
)

// inspect is the proof-of-life pass: add the magnet, seed it with the DHT peers
// we already found, wait for metadata, then read each connected peer's bitfield.
// A peer that holds every piece is a confirmed seeder — the only signal that
// guarantees the torrent downloads right now.
func (s *Scout) inspect(ctx context.Context, magnet string, peers []netip.AddrPort) Probe {
	var p Probe

	tr, err := s.client.AddMagnet(magnet)
	if err != nil {
		return p
	}
	defer tr.Drop()
	tr.SetMaxEstablishedConns(peerSampleCap)

	if len(peers) > 0 {
		if len(peers) > peerSampleCap {
			peers = peers[:peerSampleCap]
		}
		seed := make([]torrent.PeerInfo, 0, len(peers))
		for _, ap := range peers {
			seed = append(seed, torrent.PeerInfo{Addr: dialAddr(ap), Source: torrent.PeerSourceDhtGetPeers})
		}
		tr.AddPeers(seed)
	}

	select {
	case <-tr.GotInfo():
		p.GotMetadata = true
	case <-ctx.Done():
		return p
	}
	if info := tr.Info(); info != nil {
		p.Pieces = info.NumPieces()
	}

	// Give peers a moment to exchange bitfields before sampling.
	settle, cancel := context.WithTimeout(ctx, settleWindow)
	<-settle.Done()
	cancel()

	for _, conn := range tr.PeerConns() {
		bits := conn.PeerPieces()
		if bits == nil {
			continue
		}
		have := int(bits.GetCardinality())
		if have == 0 {
			continue
		}
		p.Connected++
		if p.Pieces > 0 && have >= p.Pieces {
			p.Confirmed++
		} else {
			p.Partial++
		}
	}
	return p
}

// dialAddr adapts a netip.AddrPort to the net.Addr the torrent client wants.
type dialAddr netip.AddrPort

func (d dialAddr) Network() string { return "tcp" }
func (d dialAddr) String() string  { return netip.AddrPort(d).String() }
