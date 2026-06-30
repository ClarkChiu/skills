# Spec conventions — RFC 2119 + Given/When/Then

Use these when a design needs **testable** acceptance criteria — not for every
trivial change. They make each requirement's force unambiguous and give the PLAN
phase (and downstream tdd / verify-before-done) concrete scenarios to check against.

## Requirement language (RFC 2119)

State each requirement with one keyword so its force is explicit:

- **MUST / MUST NOT / REQUIRED / SHALL** — absolute requirement or prohibition.
- **SHOULD / SHOULD NOT / RECOMMENDED** — strong default; deviating needs a stated reason.
- **MAY / OPTIONAL** — genuinely optional, no implied preference.

Keep one keyword per line so the requirement is greppable and unambiguous.

```
- The keepalive interval MUST default to 25 s and MUST be configurable.
- The client SHOULD fall back to a TCP relay after 3 failed UDP hole-punch attempts.
- The agent MAY log per-candidate RTT.
```

## Acceptance scenarios (Given/When/Then)

One scenario per behaviour. Cover the happy path **and** the failure/edge paths —
the edge cases are where the spec earns its keep.

```
Scenario: symmetric NAT falls back to relay
  Given a symmetric NAT on both peers
  When direct UDP hole-punching is attempted
  Then the connection MUST fall back to a TURN relay within 5 s
```

Each `Then` line should map to exactly one assertion in a test — the scenario name
becomes the test name, the `Then` becomes the failing assertion (Rule 9: tests verify
intent). This is the bridge from the design's acceptance criteria to the PLAN phase's
"write a failing test first" cycle.
