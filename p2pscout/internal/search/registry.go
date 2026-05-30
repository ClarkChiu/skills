package search

import (
	"fmt"
	"sort"
	"strings"
)

// factories holds every known provider behind its key. A provider file registers
// itself from init(); the CLI and aggregator only ever see the registry, never
// the concrete types. This is the one place wiring happens.
var factories = map[string]func() Provider{}

// register wires a provider factory under key. Called from each provider's init().
func register(key string, make func() Provider) { factories[key] = make }

// Keys lists the registered provider keys, sorted.
func Keys() []string {
	out := make([]string, 0, len(factories))
	for k := range factories {
		out = append(out, k)
	}
	sort.Strings(out)
	return out
}

// Select turns a spec ("apibay,torrentz2" or "all") into provider instances.
func Select(spec string) ([]Provider, error) {
	spec = strings.TrimSpace(spec)
	var keys []string
	if spec == "" || spec == "all" {
		keys = Keys()
	} else {
		for _, k := range strings.Split(spec, ",") {
			keys = append(keys, strings.TrimSpace(k))
		}
	}
	if len(keys) == 0 {
		return nil, fmt.Errorf("no providers registered")
	}
	out := make([]Provider, 0, len(keys))
	for _, k := range keys {
		make, ok := factories[k]
		if !ok {
			return nil, fmt.Errorf("unknown provider %q (have: %s)", k, strings.Join(Keys(), ", "))
		}
		out = append(out, make())
	}
	return out, nil
}
