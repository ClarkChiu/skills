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
