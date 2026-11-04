# Test design — pin intent, not implementation

A test earns its place by being able to **fail when the behaviour is wrong**. If no
realistic logic change could make it fail, delete it.

## What to test

- **Behaviour at the boundary**: the contract a caller depends on (inputs → outputs,
  errors raised, side effects), not the private internals.
- **Edge cases that encode a real risk**: empty, zero, max, malformed, the off-by-one, the
  timeout, the partial read. Each test name should say *why it matters*.
- **The bug, before the fix** (when fixing): write the failing test that reproduces it
  first, then fix — so the test would catch the regression forever.

## What NOT to test

- The framework, the language, or a mock's own behaviour.
- Private helpers in isolation when the public behaviour already covers them (you'll just
  freeze the implementation and block refactoring).
- Getters/setters and constants with no logic.

## Intent over implementation (Rule 9)

```python
# worthless — passes even if the logic is hardcoded
def test_name():
    assert get_user_name(1) == "John"   # what if it returns "John" for any id?

# pins intent — fails if the lookup logic breaks
def test_name_comes_from_the_record():
    repo = {7: "Mei", 8: "Sam"}
    assert get_user_name(8, repo) == "Sam"
    assert get_user_name(7, repo) == "Mei"   # two cases ⇒ can't be a hardcoded constant
```

## Tautological tests — the expected value cheats

The mirror image of the hardcoded case above: there the *code* cheats, here the *test*
does. If `expected` is computed with the same algorithm the implementation uses, the two
can never disagree — the test stays green even when the algorithm is wrong. This is the
most common failure mode of LLM-generated tests.

```python
# always green — expected is built by the same sum the code runs
def test_total():
    items = [10, 25, 7]
    assert order_total(items) == sum(items)   # wrong together, forever

# independent — expected is a hand-computed known answer
def test_total_adds_the_items():
    assert order_total([10, 25, 7]) == 42
```

Expected values must come from an **independent source of truth** — a known constant, a
hand-computed example, or the spec. Never re-derived inside the test.

## One behaviour per test

```python
# bad — asserts five things; a failure tells you little
def test_parse():
    r = parse(line)
    assert r.kind == "DATA" and r.len == 12 and r.ok and r.seq == 3 and not r.eof

# good — each test names one behaviour and one reason to fail
def test_parse_reads_the_kind(): ...
def test_parse_rejects_a_truncated_frame(): ...
```

## Naming

`test_<unit>_<behaviour>_<condition>` — the name should read as the spec line:
`test_parse_rejects_a_truncated_frame`. When it fails, the name alone tells you what broke.

## Checking the suite with mutation testing

Rule 9 says a test must fail when the logic breaks. Mutation testing checks that by machine:
it breaks the code in small ways and reports every break the suite still passes (a
*survivor*). Green tests and high coverage don't show this.

- **When:** by hand, on pure logic with fast tests where a silent bug is costly (parsers,
  normalizers, codecs). Not on every change, not in CI. For tests that touch ports, devices
  or shared state, use `--max-children 1`: any failure counts as a catch, so a collision
  between parallel mutants inflates the score.
- **Tool:** `mutmut` for Python: `mutmut run`, then `mutmut results` and `mutmut show <name>`.
  It also mutates strings inside functions, so inline regexes get a crude break. Module-level
  patterns and tables aren't mutated at all: test those directly.
- **Read survivors, don't count them.** A survivor is a gap only if it changes real
  behaviour, so run it over real inputs or read its diff. Ignore help text, messages and
  equivalent rewrites, and don't chase 100%.
- **Distrust the score first.** A perfect score or a suspiciously fast run may mean errors
  are being counted as catches. Re-run a few verdicts in a fresh process, from `mutants/`:
  `MUTANT_UNDER_TEST=<name> python -m pytest -q`. Functions called at import need this most.
- **Setup traps in 3.8.0:** pin `pytest<9` (9.2 crashes it with a `_nodeid` error) and keep
  pytest test IDs ASCII (others gave false kills). It needs pytest tests and an import name
  that matches the file it mutates, so a script-style suite needs a thin wrapper. For a flat
  layout, set `source_paths` (and `also_copy` for data files) under `[tool.mutmut]`.
