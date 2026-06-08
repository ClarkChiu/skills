---
name: knowledge-graph-helper
description: Builds a small knowledge graph (concepts, relations, sources) for a topic from a YAML concept library.
version: 1.0.0
---

# Knowledge Graph Helper

Turns a topic into a concept map. Load the relevant `concepts/*.yaml`, expand nodes and
relations, and emit a graph plus a sourced reading list.

## Steps

1. Pick the matching concept file under `concepts/`.
2. Expand its nodes/relations; pull `sources` and `community` fields into the reading list.
3. Emit the graph (nodes + edges) and a sourced "who to follow" list from the data.

## Output

A concept graph and a reading/follow list drawn from the YAML `sources` and `community`
fields.
