package search

import (
	"context"
	"errors"
	"fmt"
	"net/http"
	"net/url"
	"regexp"
	"strconv"
	"strings"
	"sync"
	"time"

	"github.com/PuerkitoBio/goquery"
)

// torrentz2 is a meta-search index: one query already spans many underlying
// trackers, giving breadth that complements apibay's single source. The cost is
// fragility — results come from scraped HTML, and the magnet lives on a separate
// detail page that must be fetched per hit.
func init() {
	register("torrentz2", func() Provider { return &torrentz2{http: &http.Client{Timeout: 20 * time.Second}} })
}

const (
	tzBase   = "https://torrentz2.nz"
	tzAgent  = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
	tzFanout = 8 // concurrent detail-page fetches
)

type torrentz2 struct{ http *http.Client }

func (t *torrentz2) Key() string { return "torrentz2" }

// listing is the partial data we can read from the result list before fetching
// the detail page that holds the magnet.
type listing struct {
	id        string
	title     string
	size      int64
	seeds     int
	peers     int
	published time.Time
}

func (t *torrentz2) Find(ctx context.Context, query string, limit int) ([]Result, error) {
	doc, err := t.get(ctx, fmt.Sprintf("%s/search?q=%s&sort=seeders", tzBase, url.QueryEscape(query)))
	if err != nil {
		return nil, fmt.Errorf("torrentz2 search: %w", err)
	}

	var listings []listing
	doc.Find("div.results > dl").EachWithBreak(func(_ int, s *goquery.Selection) bool {
		if len(listings) >= limit {
			return false
		}
		a := s.Find("dt > a").First()
		href, _ := a.Attr("href")
		id := strings.TrimPrefix(href, "/torrent/")
		if id == "" || id == href {
			return true // not a torrent row
		}
		l := listing{
			id:    id,
			title: strings.TrimSpace(a.Text()),
			size:  humanToBytes(s.Find("dd > span.s").First().Text()),
			seeds: atoiTrim(s.Find("dd > span.u").First().Text()),
			peers: atoiTrim(s.Find("dd > span.d").First().Text()),
		}
		if title, ok := s.Find("dd > span.a > span").First().Attr("title"); ok {
			l.published = parseListDate(title)
		}
		listings = append(listings, l)
		return true
	})
	if len(listings) == 0 {
		return nil, errors.New("torrentz2: no rows parsed")
	}

	results := make([]Result, len(listings))
	gate := make(chan struct{}, tzFanout)
	var wg sync.WaitGroup
	for i, l := range listings {
		wg.Add(1)
		gate <- struct{}{}
		go func(i int, l listing) {
			defer wg.Done()
			defer func() { <-gate }()
			magnet, err := t.magnet(ctx, l.id)
			if err != nil {
				return
			}
			ih, trackers, cleaned := CleanMagnet(magnet)
			if ih == "" {
				return
			}
			results[i] = Result{
				Source:       t.Key(),
				Title:        l.title,
				InfoHash:     ih,
				Magnet:       cleaned,
				SizeBytes:    l.size,
				ClaimedSeeds: l.seeds,
				ClaimedPeers: l.peers,
				Published:    l.published,
				Trackers:     trackers,
			}
		}(i, l)
	}
	wg.Wait()

	out := results[:0]
	for _, r := range results {
		if r.InfoHash != "" {
			out = append(out, r)
		}
	}
	return out, nil
}

func (t *torrentz2) get(ctx context.Context, u string) (*goquery.Document, error) {
	req, err := http.NewRequestWithContext(ctx, http.MethodGet, u, nil)
	if err != nil {
		return nil, err
	}
	req.Header.Set("User-Agent", tzAgent)
	resp, err := t.http.Do(req)
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()
	if resp.StatusCode != http.StatusOK {
		return nil, fmt.Errorf("status %d", resp.StatusCode)
	}
	return goquery.NewDocumentFromReader(resp.Body)
}

func (t *torrentz2) magnet(ctx context.Context, id string) (string, error) {
	doc, err := t.get(ctx, fmt.Sprintf("%s/torrent/%s", tzBase, id))
	if err != nil {
		return "", err
	}
	href, ok := doc.Find("a[href^='magnet:']").First().Attr("href")
	if !ok || href == "" {
		return "", errors.New("no magnet on detail page")
	}
	return href, nil
}

func atoiTrim(s string) int { n, _ := strconv.Atoi(strings.TrimSpace(s)); return n }

var sizeExpr = regexp.MustCompile(`(?i)^\s*([0-9]*\.?[0-9]+)\s*(B|KB|MB|GB|TB)\s*$`)

func humanToBytes(s string) int64 {
	m := sizeExpr.FindStringSubmatch(s)
	if m == nil {
		return 0
	}
	v, _ := strconv.ParseFloat(m[1], 64)
	switch strings.ToUpper(m[2]) {
	case "KB":
		v *= 1 << 10
	case "MB":
		v *= 1 << 20
	case "GB":
		v *= 1 << 30
	case "TB":
		v *= 1 << 40
	}
	return int64(v)
}

// dates look like "Thu Apr 18 2019 17:11:32 GMT+0000 (Coordinated Universal Time)"
var tzDateLayouts = []string{
	"Mon Jan 02 2006 15:04:05 GMT-0700",
	"Mon Jan 2 2006 15:04:05 GMT-0700",
}

func parseListDate(s string) time.Time {
	if i := strings.Index(s, " ("); i > 0 {
		s = s[:i]
	}
	for _, layout := range tzDateLayouts {
		if ts, err := time.Parse(layout, s); err == nil {
			return ts
		}
	}
	return time.Time{}
}
