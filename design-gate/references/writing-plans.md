# Plan phase: breaking a design into executable tasks

Adapted from obra/superpowers' `writing-plans`, rewritten to fit this project. The bar: **a skilled engineer who knows almost nothing about this codebase can execute the plan independently, without coming back to ask.**

> Assume the executor is a good engineer but knows almost nothing about our toolset or problem domain. So every step must hand them what they need directly.

## Global constraints (plan header)

Open the plan with a short **Global Constraints** block that holds for every task — so an
executor picking up Task 7 in isolation doesn't re-derive or contradict project-wide
decisions. Keep it to what actually constrains the work: target runtime/versions, the
non-negotiable conventions (naming, error model, logging), the public boundary that must
not change, and anything explicitly out of scope. One screen, not an essay; if a constraint
only affects one task, put it in that task, not here.

## Task granularity

- Each task is **one action, 2–5 minutes**. Don't pack several things into one task.
- A typical task cycle (tuned to this user's domain — TDD):
  1. Write a failing test
  2. Run it, confirm it actually fails
  3. Write the minimal implementation to pass
  4. Run tests, confirm they pass
  5. Commit

> **TDD rule — the red step matters** (canonical statement; `systematic-debugging` and `verify-before-done` point here): no production code without a failing test you have *watched* fail. A test that goes green before you wrote the implementation is a false green (it asserts nothing, or exercises the wrong path) — fix the test, not the code. As upstream puts it: *"If you didn't watch the test fail, you don't know if it tests the right thing."*

## What every task must contain

- **Files section**: exact paths — which to create, which to modify (with line numbers), where the test is.
- **Interfaces**: when a later task consumes what this one produces, state the contract explicitly — the exact function/type signature, endpoint shape, or data schema other tasks will call. This is what lets independently-executed tasks compose without each one re-inventing the boundary. A task with no downstream consumer needs none.
- **Complete code**: real runnable code — not pseudocode, not "same as above", no `TODO`. Define every type, function name, and signature before it's used.
- **Verification steps**: exact commands + expected output (e.g. `pytest …::test_x -v` → expect PASS).
- **Commit**: what to stage, what the commit message looks like.

## What never to write (anti-patterns)

- `TBD`, `TODO`, "implement later", "fill in the details".
- Empty instructions with no code, like "add appropriate error handling" or "write tests for the above".
- Forward references: using a type or function that isn't defined yet.
- Tasks pointing at each other ("same as Task 3") instead of repeating the complete code.
- Describing "what to do" without "how" — code changes always need a code block.

## File organization principles

- Each file has one clear responsibility; boundaries clear, interfaces well-defined.
- Follow the existing codebase's conventions; don't unilaterally restructure.
- Things that change together live together.
- If the design actually spans several independent subsystems → split into multiple plans, one per subsystem.

## Example task

````markdown
### Task N: <component name>

**Files:**
- Create: `exact/path/to/file.py`
- Modify: `exact/path/to/existing.py:123-145`
- Test: `tests/exact/path/to/test_file.py`

- [ ] **Step 1: Write the failing test**

```python
def test_specific_behavior():
    result = function(input)
    assert result == expected
```

- [ ] **Step 2: Run the test, confirm it fails**

Run: `pytest tests/path/test_file.py::test_specific_behavior -v`
Expect: FAIL (function not defined)

- [ ] **Step 3: Write the minimal implementation**

```python
def function(input):
    return expected
```

- [ ] **Step 4: Run the test, confirm it passes**

Run: `pytest tests/path/test_file.py::test_specific_behavior -v`
Expect: PASS

- [ ] **Step 5: Commit**

```bash
git add tests/path/test_file.py src/path/file.py
git commit -m "✨ feat: add specific behavior"
```
````

## Save and hand off

- Write the plan to `docs/plans/YYYY-MM-DD-<topic>.md`.
- After saving, hand back to execution: by default, execute task-by-task in the current session, following `CLAUDE.md`'s discipline (Rule 4 goal-driven, Rule 9 tests verify intent, Rule 12 fail loud).
- Commit messages follow this project's convention: gitmoji + Conventional, no `Co-Authored-By` trailer.
