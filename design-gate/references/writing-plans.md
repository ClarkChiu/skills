# Plan phase: breaking a design into executable tasks

Adapted from obra/superpowers' `writing-plans`, rewritten to fit this project. The bar: **a skilled engineer who knows almost nothing about this codebase can execute the plan independently, without coming back to ask.**

> Assume the executor is a good engineer but knows almost nothing about our toolset or problem domain. So every step must hand them what they need directly.

## Global constraints (plan header)

Start the plan header with a **`Spec:`** line pointing at the approved design doc (`Spec: docs/specs/YYYY-MM-DD-<topic>-design.md`), so whoever executes the plan reads the design too instead of reverse-engineering intent from the tasks.

Then add a short **Global Constraints** block that holds for every task — so an
executor picking up Task 7 in isolation doesn't re-derive or contradict project-wide
decisions. Keep it to what actually constrains the work: target runtime/versions, the
non-negotiable conventions (naming, error model, logging), the public boundary that must
not change, and anything explicitly out of scope. One screen, not an essay; if a constraint
only affects one task, put it in that task, not here.

Close the header with a **Review Focus** list: the inputs or failure modes the spec implies
but no task's tests exercise yet — the ones most likely to bite a real user (an empty capture
file, a peer that never answers, IPv6-only, a clock jump). One line each: the condition and the
behavior a reasonable person would expect, most likely first, a handful at most. The spec's
silence on an input isn't permission for it to crash the program. Then pin each line with a
test in the task that owns that code.

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
- **Signature + tests, not the program**: the exact signature (name, parameters, return type) and file, the test's name and assertions as real code, and the exact values the spec pins. The executor writes the body. Include a body only for an algorithm the signature and tests don't determine (or copy the spec fixes verbatim). When this task uses another task's output, point at that task's **Interfaces** block instead of repeating its code. Define every type and function before it's used.
- **Verification steps**: exact commands + expected output (e.g. `pytest …::test_x -v` → expect PASS).
- **Commit**: what to stage, what the commit message looks like.

## What never to write (anti-patterns)

- `TBD`, `TODO`, "implement later", "fill in the details".
- Lines that decide nothing, like "add appropriate error handling" or "write tests for the above".
- Forward references: using a type or function that isn't defined yet.
- "Same as Task 3" with nothing to anchor it — name the Interfaces block being used.
- A code step with no signature, or a test step with no assertions.
- The opposite failure: a function body the signature and tests already determine. That's a transcript of the program, not a plan.

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

- [ ] **Step 3: Implement `function(input: InputType) -> ResultType` in `exact/path/to/file.py`**

One line on the approach if the signature and test leave a real choice (which library call,
which data structure); a code block only for an algorithm they don't determine.

- [ ] **Step 4: Run the test, confirm it passes**

Run: `pytest tests/path/test_file.py::test_specific_behavior -v`
Expect: PASS

- [ ] **Step 5: Commit**

```bash
git add tests/exact/path/to/test_file.py exact/path/to/file.py
git commit -m "✨ feat: add specific behavior"
```
````

## Self-review

Before handing the plan over, check it against the spec:

- **Spec coverage**: every requirement maps to a task.
- **Type consistency**: names and signatures in later tasks match where they were defined.
- **Review Focus covered**: every line in the list has its test in the owning task. An empty list means you looked and found none, not that you skipped the look.
- **Proportion**: if the plan is longer than the code it describes, or code blocks are most of the document, it's a copy of the program. Cut bodies back to signatures and assertions, then check each step still leaves the executor exactly one reasonable thing to write.

## Save and hand off

- Write the plan to `docs/plans/YYYY-MM-DD-<topic>.md`.
- Give the user the path and wait for them to review it — approving the design authorized writing the plan, not running it.
- After their yes, hand back to execution: by default, execute task-by-task in the current session, following `CLAUDE.md`'s discipline (Rule 4 goal-driven, Rule 9 tests verify intent, Rule 12 fail loud).
- Commit messages follow this project's convention: gitmoji + Conventional, no `Co-Authored-By` trailer.
