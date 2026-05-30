// Package download hands a chosen magnet to aria2 over JSON-RPC. p2pscout does
// not transfer bytes itself — inspecting a swarm needs a BT client to read peer
// bitfields, but the download proper is a solved problem, so it is delegated to
// aria2c (mature, resumable, rate-limitable).
//
// Start aria2 in RPC mode first:
//
//	aria2c --enable-rpc --rpc-listen-all=false --rpc-secret=TOKEN
package download

import (
	"bytes"
	"context"
	"encoding/json"
	"fmt"
	"net/http"
	"time"
)

// Client is a minimal aria2 JSON-RPC client.
type Client struct {
	endpoint string
	secret   string
	http     *http.Client
}

func New(endpoint, secret string) *Client {
	if endpoint == "" {
		endpoint = "http://127.0.0.1:6800/jsonrpc"
	}
	return &Client{endpoint: endpoint, secret: secret, http: &http.Client{Timeout: 15 * time.Second}}
}

type request struct {
	JSONRPC string `json:"jsonrpc"`
	ID      string `json:"id"`
	Method  string `json:"method"`
	Params  []any  `json:"params"`
}

type response struct {
	Result json.RawMessage `json:"result"`
	Error  *struct {
		Code    int    `json:"code"`
		Message string `json:"message"`
	} `json:"error"`
}

func (c *Client) call(ctx context.Context, method string, params []any, out any) error {
	if c.secret != "" {
		params = append([]any{"token:" + c.secret}, params...)
	}
	body, err := json.Marshal(request{JSONRPC: "2.0", ID: "p2pscout", Method: method, Params: params})
	if err != nil {
		return err
	}
	req, err := http.NewRequestWithContext(ctx, http.MethodPost, c.endpoint, bytes.NewReader(body))
	if err != nil {
		return err
	}
	req.Header.Set("Content-Type", "application/json")
	resp, err := c.http.Do(req)
	if err != nil {
		return fmt.Errorf("aria2 %s: %w (is aria2c running with --enable-rpc?)", method, err)
	}
	defer resp.Body.Close()
	if resp.StatusCode != http.StatusOK {
		return fmt.Errorf("aria2 %s: http %d", method, resp.StatusCode)
	}
	var r response
	if err := json.NewDecoder(resp.Body).Decode(&r); err != nil {
		return err
	}
	if r.Error != nil {
		return fmt.Errorf("aria2 %s: %s (code %d)", method, r.Error.Message, r.Error.Code)
	}
	if out != nil {
		return json.Unmarshal(r.Result, out)
	}
	return nil
}

// AddMagnet queues a magnet and returns its GID. dir, if set, overrides the
// download directory for this task.
func (c *Client) AddMagnet(ctx context.Context, magnet, dir string) (string, error) {
	opts := map[string]string{}
	if dir != "" {
		opts["dir"] = dir
	}
	var gid string
	if err := c.call(ctx, "aria2.addUri", []any{[]string{magnet}, opts}, &gid); err != nil {
		return "", err
	}
	return gid, nil
}

// Status is the subset of aria2.tellStatus fields we surface.
type Status struct {
	GID             string `json:"gid"`
	Status          string `json:"status"`
	TotalLength     string `json:"totalLength"`
	CompletedLength string `json:"completedLength"`
	DownloadSpeed   string `json:"downloadSpeed"`
	NumSeeders      string `json:"numSeeders"`
	ErrorMessage    string `json:"errorMessage,omitempty"`
}

func (c *Client) Status(ctx context.Context, gid string) (Status, error) {
	keys := []string{"gid", "status", "totalLength", "completedLength", "downloadSpeed", "numSeeders", "errorMessage"}
	var s Status
	if err := c.call(ctx, "aria2.tellStatus", []any{gid, keys}, &s); err != nil {
		return Status{}, err
	}
	return s, nil
}
