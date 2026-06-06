# Attribution

`p2pscout` is an original Go tool. Its swarm-probing approach — verifying real
downloadability via DHT lookups, tracker scrapes, and optional peer handshakes
(reading the bitfield to confirm a peer holds all pieces) rather than trusting an
indexer's self-reported seed counts — draws on prior BitTorrent-liveness work.

## Reference upstream (pinned in `sources.lock`)

- **joway/gardener** — BitTorrent/DHT liveness-probing reference. The "don't trust
  the indexer, probe the swarm yourself" stance and the DHT/tracker verification
  technique are informed by it. Pinned by commit in `sources.lock`.

Not vendored verbatim — p2pscout is a fresh implementation (multi-provider search +
downloadability ranking + aria2 hand-off for the actual transfer). The reference is
recorded so `skill-evolve` can flag upstream technique changes worth folding in.
