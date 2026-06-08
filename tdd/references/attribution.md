# Attribution

`tdd` is adapted from **mattpocock/skills** → `engineering/tdd` (MIT). The red-green-
refactor discipline is universal (Beck); Matt's contribution is a tight skill formulation
of it. This is an **original rewrite**, no files copied. Full evaluation:
`research/audits/2026-06-08-mattpocock-skills.md` (verdict: 🟦 build-your-own).

## What changed vs upstream (and why)

- **Re-aimed at this user's stack.** Upstream leans TypeScript + an Ousterhout "deep
  modules" thread. This keeps the language-agnostic loop but uses **pytest** examples and
  adds a **network-protocol integration** example (real loopback socket) — the user's
  actual domain (NAT traversal, RTP, protocol work).
- **Wired into the existing pipeline.** Positioned explicitly as the BUILD middle:
  `design-gate` (plan) → tdd (build) → `verify-before-done` (gate). design-gate's
  `writing-plans` owns the canonical "failing-test-first / red step"; this executes it.
- **Mocking guidance reframed** around "use the real thing in the middle, mock the edge,"
  with the protocol case calling for a real socket over a mock.
- Trimmed to the load-bearing loop + two reference files (test-design, mocking) rather than
  upstream's five.

## Re-sync

`sources.lock` pins upstream. On `skill-evolve`, mine sharper rule phrasings or
test-design ideas; keep the pytest/protocol re-aiming and the pipeline wiring.
