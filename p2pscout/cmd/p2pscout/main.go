package main

import (
	"context"
	"fmt"
	"io"
	"os"
	"os/signal"
	"sort"
	"strings"
	"sync"
	"syscall"
	"time"

	"github.com/spf13/cobra"

	"github.com/freebooters/p2pscout/internal/download"
	"github.com/freebooters/p2pscout/internal/output"
	"github.com/freebooters/p2pscout/internal/search"
	"github.com/freebooters/p2pscout/internal/swarm"
)

type opts struct {
	limit       int
	providers   string
	full        bool
	jsonOut     bool
	verbose     bool
	overall     time.Duration
	dht         time.Duration
	tracker     time.Duration
	inspect     time.Duration
	concurrency int
}

func main() {
	var o opts
	root := &cobra.Command{
		Use:   "p2pscout <query>",
		Short: "Search several P2P indexes and rank hits by verified downloadability.",
		Long: "p2pscout fans a query across multiple providers, merges hits by infohash,\n" +
			"and ranks them by live swarm signals (DHT + trackers, optionally handshake-\n" +
			"confirmed). Built for agents that need the one result that actually downloads.",
		Args: cobra.MinimumNArgs(1),
		RunE: func(cmd *cobra.Command, args []string) error {
			reports, err := scout(cmd.Context(), strings.Join(args, " "), &o)
			if err != nil {
				return err
			}
			if o.jsonOut {
				return output.JSON(os.Stdout, reports)
			}
			return output.Table(os.Stdout, reports, o.verbose)
		},
	}
	f := root.PersistentFlags()
	f.IntVarP(&o.limit, "limit", "n", 20, "max candidates per provider")
	f.StringVar(&o.providers, "providers", "all", "comma-separated providers, or 'all'")
	f.BoolVar(&o.full, "full", false, "full depth: handshake peers and confirm bitfields (slow)")
	f.BoolVar(&o.jsonOut, "json", false, "emit JSON instead of a table")
	f.BoolVarP(&o.verbose, "verbose", "v", false, "show index-claimed seed/peer counts")
	f.DurationVar(&o.overall, "timeout", 90*time.Second, "overall wall-clock budget")
	f.DurationVar(&o.dht, "dht-timeout", 15*time.Second, "per-torrent DHT lookup budget")
	f.DurationVar(&o.tracker, "tracker-timeout", 8*time.Second, "per-tracker scrape timeout")
	f.DurationVar(&o.inspect, "inspect-timeout", 25*time.Second, "per-torrent handshake budget (full)")
	f.IntVar(&o.concurrency, "concurrency", 4, "torrents probed in parallel")

	root.AddCommand(getCmd(&o))

	ctx, stop := signal.NotifyContext(context.Background(), os.Interrupt, syscall.SIGTERM)
	defer stop()
	if err := root.ExecuteContext(ctx); err != nil {
		fmt.Fprintln(os.Stderr, "p2pscout:", err)
		os.Exit(1)
	}
}

// scout is the shared pipeline: pick providers → fan out + merge → probe each
// candidate concurrently → sort by score.
func scout(parent context.Context, query string, o *opts) ([]*swarm.Report, error) {
	ctx, cancel := context.WithTimeout(parent, o.overall)
	defer cancel()

	providers, err := search.Select(o.providers)
	if err != nil {
		return nil, err
	}
	keys := make([]string, len(providers))
	for i, p := range providers {
		keys[i] = p.Key()
	}
	fmt.Fprintf(os.Stderr, "→ searching [%s] for %q (top %d each)…\n", strings.Join(keys, ","), query, o.limit)

	candidates := search.FanOut(ctx, providers, query, o.limit)
	if len(candidates) == 0 {
		return nil, fmt.Errorf("no results for %q", query)
	}
	fmt.Fprintf(os.Stderr, "  %d unique candidates after merge\n", len(candidates))

	depth := swarm.Shallow
	if o.full {
		depth = swarm.Full
	}
	sc, err := swarm.NewScout(ctx, o.full, 10*time.Second)
	if err != nil {
		return nil, fmt.Errorf("scout init: %w", err)
	}
	defer sc.Close()

	budget := swarm.Budget{Depth: depth, DHT: o.dht, Tracker: o.tracker, Inspect: o.inspect}

	reports := make([]*swarm.Report, len(candidates))
	var wg sync.WaitGroup
	gate := make(chan struct{}, o.concurrency)
	for i, c := range candidates {
		wg.Add(1)
		gate <- struct{}{}
		go func(i int, c search.Result) {
			defer wg.Done()
			defer func() { <-gate }()
			r := &swarm.Report{
				InfoHash: c.InfoHash, Title: c.Title, SizeBytes: c.SizeBytes,
				Magnet: c.Magnet, Source: c.Source, Published: c.Published,
				ClaimedSeeds: c.ClaimedSeeds, ClaimedPeers: c.ClaimedPeers,
			}
			sc.Assess(ctx, r, c.Trackers, budget)
			reports[i] = r
			fmt.Fprintf(os.Stderr, "  ✓ %-46s %-12s dht=%d trk=%.0f score=%.1f\n",
				clip(r.Title, 46), r.Verdict, r.DHTPeers, r.TrackerSeeds, r.Score)
		}(i, c)
	}
	wg.Wait()

	out := make([]*swarm.Report, 0, len(reports))
	for _, r := range reports {
		if r != nil {
			out = append(out, r)
		}
	}
	sort.SliceStable(out, func(i, j int) bool { return out[i].Score > out[j].Score })
	return out, nil
}

func getCmd(o *opts) *cobra.Command {
	var (
		rpc, secret, dir string
		magnet           string
		auto             bool
	)
	cmd := &cobra.Command{
		Use:   "get <query>",
		Short: "Confirm downloadability, then queue the healthiest hit in aria2.",
		Long: "With a query: search all providers, verify, pick the healthiest.\n" +
			"With --magnet: skip search and verify that exact magnet directly.\n" +
			"With --magnet -: read the magnet from stdin, so it composes in a pipe\n" +
			"(e.g. `p2p-ranking-board get <id> | p2pscout get --magnet - --auto`).",
		Args: cobra.ArbitraryArgs,
		RunE: func(cmd *cobra.Command, args []string) error {
			o.full = true // queuing an unverified swarm defeats the point

			var best *swarm.Report
			switch {
			case magnet != "":
				if magnet == "-" {
					data, err := io.ReadAll(os.Stdin)
					if err != nil {
						return err
					}
					if magnet = strings.TrimSpace(string(data)); magnet == "" {
						return fmt.Errorf("no magnet on stdin")
					}
				}
				r, err := verifyMagnet(cmd.Context(), magnet, o)
				if err != nil {
					return err
				}
				best = r
			case len(args) > 0:
				reports, err := scout(cmd.Context(), strings.Join(args, " "), o)
				if err != nil {
					return err
				}
				best = reports[0]
			default:
				return fmt.Errorf("provide a search query or --magnet")
			}

			if best.Verdict != swarm.Downloadable {
				return fmt.Errorf("candidate %q is %s, not downloadable — refusing to queue", best.Title, best.Verdict)
			}
			fmt.Fprintf(os.Stderr, "→ best: %s (confirmed=%d score=%.1f)\n", best.Title, best.Probe.Confirmed, best.Score)
			if !auto {
				fmt.Fprintf(os.Stderr, "  pass --auto to queue, or hand this magnet to your client:\n  %s\n", best.Magnet)
				return nil
			}
			gid, err := download.New(rpc, secret).AddMagnet(cmd.Context(), best.Magnet, dir)
			if err != nil {
				return err
			}
			fmt.Fprintf(os.Stderr, "  queued in aria2, gid=%s\n", gid)
			fmt.Println(gid)
			return nil
		},
	}
	cmd.Flags().StringVar(&magnet, "magnet", "", "verify this exact magnet instead of searching; use '-' to read it from stdin")
	cmd.Flags().StringVar(&rpc, "aria2-rpc", "", "aria2 JSON-RPC endpoint (default http://127.0.0.1:6800/jsonrpc)")
	cmd.Flags().StringVar(&secret, "aria2-secret", "", "aria2 --rpc-secret token")
	cmd.Flags().StringVar(&dir, "dir", "", "download directory passed to aria2")
	cmd.Flags().BoolVar(&auto, "auto", false, "actually queue the download (otherwise just print the magnet)")
	return cmd
}

// verifyMagnet probes one explicit magnet in full depth — no search. Used for a
// precise handoff when the caller already knows the exact infohash.
func verifyMagnet(parent context.Context, magnet string, o *opts) (*swarm.Report, error) {
	ih, trackers, cleaned := search.CleanMagnet(magnet)
	if ih == "" {
		return nil, fmt.Errorf("invalid magnet: no infohash")
	}
	ctx, cancel := context.WithTimeout(parent, o.overall)
	defer cancel()

	sc, err := swarm.NewScout(ctx, true, 10*time.Second)
	if err != nil {
		return nil, fmt.Errorf("scout init: %w", err)
	}
	defer sc.Close()

	r := &swarm.Report{InfoHash: ih, Magnet: cleaned, Title: "(magnet)", Source: "magnet"}
	fmt.Fprintf(os.Stderr, "→ verifying magnet %s…\n", ih)
	sc.Assess(ctx, r, trackers, swarm.Budget{Depth: swarm.Full, DHT: o.dht, Tracker: o.tracker, Inspect: o.inspect})
	fmt.Fprintf(os.Stderr, "  %s confirmed=%d dht=%d trk=%.0f score=%.1f\n", r.Verdict, r.Probe.Confirmed, r.DHTPeers, r.TrackerSeeds, r.Score)
	return r, nil
}

func clip(s string, n int) string {
	if len(s) <= n {
		return s
	}
	return s[:n-1] + "…"
}
