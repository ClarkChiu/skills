package swarm

import (
	"context"
	"fmt"
	"net/netip"
	"os"
	"sync"
	"time"

	"github.com/anacrolix/dht/v2"
	analog "github.com/anacrolix/log"
	"github.com/anacrolix/torrent"
	"github.com/anacrolix/torrent/storage"
)

// Budget bounds each probe phase. Zero fields fall back to defaults.
type Budget struct {
	Depth   Depth
	DHT     time.Duration // DHT get_peers window per torrent
	Tracker time.Duration // per-tracker scrape timeout
	Inspect time.Duration // handshake/metadata window per torrent (Full only)
}

func (b Budget) orDefaults() Budget {
	if b.DHT == 0 {
		b.DHT = 15 * time.Second
	}
	if b.Tracker == 0 {
		b.Tracker = 8 * time.Second
	}
	if b.Inspect == 0 {
		b.Inspect = 25 * time.Second
	}
	return b
}

// Scout owns the shared, bootstrapped DHT node and (in Full depth) a torrent
// client used for handshakes. Build one, reuse it across every candidate, Close
// when done.
type Scout struct {
	dht    *dht.Server
	client *torrent.Client // nil in Shallow depth
	tmpDir string
}

// NewScout starts the probes. In Full depth it also brings up a leech-only
// torrent client (no upload, no seeding, never writes piece data) for handshake
// inspection, then bootstraps the DHT routing table best-effort.
func NewScout(ctx context.Context, full bool, bootstrap time.Duration) (*Scout, error) {
	srv, err := dht.NewServer(dht.NewDefaultServerConfig())
	if err != nil {
		return nil, fmt.Errorf("dht: %w", err)
	}

	s := &Scout{dht: srv}
	if full {
		if err := s.startClient(); err != nil {
			srv.Close()
			return nil, err
		}
	}

	bctx, cancel := context.WithTimeout(ctx, bootstrap)
	_, _ = srv.BootstrapContext(bctx) // deadline is expected; table is usable early
	cancel()
	return s, nil
}

func (s *Scout) startClient() error {
	dir, err := os.MkdirTemp("", "p2pscout-*")
	if err != nil {
		return err
	}
	cfg := torrent.NewDefaultClientConfig()
	cfg.DataDir = dir
	cfg.DefaultStorage = storage.NewFile(dir)
	cfg.NoUpload = true
	cfg.Seed = false
	cfg.NoDefaultPortForwarding = true
	cfg.DisableAcceptRateLimiting = true
	cfg.ListenPort = 0 // ephemeral; avoids clashing on 42069
	cfg.Logger = cfg.Logger.WithFilterLevel(analog.Disabled)
	cl, err := torrent.NewClient(cfg)
	if err != nil {
		os.RemoveAll(dir)
		return fmt.Errorf("torrent client: %w", err)
	}
	s.client, s.tmpDir = cl, dir
	return nil
}

func (s *Scout) Close() {
	if s.client != nil {
		s.client.Close()
	}
	if s.tmpDir != "" {
		os.RemoveAll(s.tmpDir)
	}
	if s.dht != nil {
		s.dht.Close()
	}
}

// Assess fills r's swarm fields and grades it. DHT discovery and tracker scrape
// run concurrently; in Full depth the discovered peers are then fed into the
// handshake inspection. r must already carry InfoHash and (for Full) Magnet.
func (s *Scout) Assess(ctx context.Context, r *Report, trackers []string, b Budget) {
	b = b.orDefaults()
	r.Depth = b.Depth

	var (
		wg    sync.WaitGroup
		peers []netip.AddrPort
	)
	wg.Add(2)

	go func() {
		defer wg.Done()
		dctx, cancel := context.WithTimeout(ctx, b.DHT)
		defer cancel()
		peers = s.discover(dctx, r.InfoHash)
		r.DHTPeers = len(peers)
	}()
	go func() {
		defer wg.Done()
		r.Trackers = scrape(ctx, r.InfoHash, trackers, b.Tracker)
	}()
	wg.Wait()

	if b.Depth == Full && s.client != nil {
		ictx, cancel := context.WithTimeout(ctx, b.Inspect)
		defer cancel()
		r.Probe = s.inspect(ictx, r.Magnet, peers)
	}

	r.grade()
}
