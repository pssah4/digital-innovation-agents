---
name: testing
description: >
  Creates and manages unit tests and integration tests. Analyzes the existing
  codebase, auto-detects the test framework, and generates tests that follow
  project conventions. Use this skill when the user mentions "write tests",
  "unit tests", "integration tests", "test coverage", "testing", "tests
  missing", "TDD" or similar. Also after implementation when tests need to
  be created or updated.
disable-model-invocation: false
---

# Testing -- Unit & Integration Tests

Creates tests that fit into the existing codebase. Detects the
framework, patterns, and conventions automatically from the project.

Writing style and frontmatter rules:
See `skills/project-conventions/SKILL.md#canonical-specs` (Writing style,
Frontmatter spec).

## MANDATORY Pre-Phase 0: Branch and item check

Tests bind to a specific backlog item. Run the team-workflow check (full
rules: `skills/project-conventions/references/team-workflow.md`):

1. Identify the active item from the prompt or via AskUserQuestion;
   tests usually continue on the same FEAT/FIX/IMP item branch.
2. Verify the branch matches `feature/<item-id-lower>-<slug>`. On a
   wrong branch, AskUserQuestion to switch.
3. Skill-triggered GitHub integration (idempotent):
   ```
   python3 tools/github-integration/flow.py create-issue --item <ID>
   python3 tools/github-integration/flow.py open-draft-pr --item <ID>
   ```
4. At Handoff Ritual end, tag the phase via
   `python3 tools/github-integration/flow.py tag-phase --item <ID> --phase test`.
5. Write `.git/dia-active-skill` so subsequent invocations stay silent.

## MANDATORY Phase 0: Artifact triage

New tests bind to an existing FEATURE, IMP, or FIX id. **Exception:**
read-only analysis (coverage report, gap identification, reading
existing tests) does not need triage.

If the binding cannot be derived from the prompt, ask once before the
first new test (user's working language):

> "Does this test run belong to a FEATURE, an IMP, or a FIX? Please
> name the ID."

Triage details:
`skills/project-conventions/references/graph-invariants.md`, section
"Artifact triage at entry point".

## MANDATORY: Verify gate language

`/testing` shares the verify gate with `/coding`. No completion claim
without fresh verification evidence in the current message.

Hard threshold for "all green": 0 test failures, 0 lint errors (if lint
runs in the suite), coverage not regressed (line/branch/function each at
or above the project target from `_devprocess/rules/technical.md` or
Coverage section).

Forbidden without fresh verification: "should pass", "tests should be
green now", "looks good", "probably fine". The skill executes the test
command IN THIS MESSAGE before any completion claim. Cached output and
stale logs are not evidence.

## Codebase analysis first

Before writing tests, scan the project for:

- Test framework and config (package.json scripts/devDeps, pyproject.toml, Cargo.toml, existing test files)
- Test location and naming (tests/, __tests__/, .test.ts vs .spec.ts vs _test.py, conftest.py, fixtures)
- Conventions in use (mocking style, async handling, assertions, shared helpers, untested areas)

This is internal analysis; do not write back into FEATURE/BACKLOG. Adopt the
patterns the project already uses. Do not introduce new frameworks unless
the project has none.

## Priority order

Unit > integration > e2e, scope-aware. Focus of this skill: integration tests
(primary) and unit tests (TDD fallback or gap-filling). E2E is a separate topic.

## Role alongside TDD

When `/coding` runs in TDD mode (see `coding/SKILL.md` Phase 3b), unit
tests already exist. `/testing` then focuses on, in priority:

1. **Integration tests (primary).** Multi-module flows: API endpoints,
   DB access, event/message flows, external integrations with mocked
   boundaries.
2. **Unit test gaps (secondary).** Edge cases, error paths, boundary
   conditions missed by the RED tests.
3. **Coverage check (tertiary).** Report against targets; gaps listed,
   not auto-filled.

If `/coding` ran without TDD, `/testing` also creates the unit tests
following AAA and FIRST.

## Unit Tests

**When.** Public functions with logic, utilities, data transformations,
error handling. Skip trivial getters/setters and pure pass-throughs.

### AAA Pattern (Arrange, Act, Assert)

Every test follows the AAA shape:

- Arrange: build inputs, fixtures, mocks
- Act: invoke the unit under test once
- Assert: check return value, state change, or thrown error
- One behavior per test; name it after the behavior, not the method

Match the project's existing assertion verbosity; do not add `// Arrange`
comments unless they already exist.

### FIRST Principles

Fast (<1s/test), Independent, Repeatable, Self-validating, Timely.

### Per-function checklist

Full version: `references/test-checklist.md`. Short version: happy path,
edge cases (empty/null/undefined/boundary), error cases (invalid inputs,
missing dependencies), boundary conditions (min/max, empty, large).

### Mocking rules

Mock external dependencies (APIs, FS, DB) only. Never mock the unit
under test. Prefer dependency injection over global mocks. Reuse the
project's existing mock patterns.

## Integration Tests

**When.** Multi-module interactions, API request -> response, DB access
(test DB or in-memory), event/message flows.

**Rules.** Real dependencies where possible; mock only external services.
Each test independent (own state and teardown). Realistic test data, not
`foo`/`bar`/`test`. Set timeouts for async. Use beforeAll/afterAll only
for shared resources.

### File naming

Follow the existing project pattern. If none exists: `{module}.test.ts`
or `{module}.spec.ts` for unit, `{module}.integration.test.ts` for
integration. Same directory as source, or under `tests/`.

## Test workflow

| Trigger | Steps |
|---|---|
| Existing feature without tests | Analyze file -> identify testables -> recognize patterns -> create tests (AAA/FIRST) -> run -> coverage |
| New feature after `/coding` | Read FEATURE spec Success Criteria -> identify changed files -> integration tests -> fill unit gaps -> verify SC |

### Coverage targets

| Metric | Target | Minimum |
|--------|--------|---------|
| Line Coverage | 85% | 70% |
| Branch Coverage | 80% | 65% |
| Function Coverage | 90% | 75% |

Guidelines only. Project-specific targets in `CLAUDE.md`, feature specs,
or `_devprocess/rules/technical.md` take precedence.

## Anti-patterns

Full version: `references/test-anti-patterns.md`. Short version: no
testing of implementation details (test behavior); no excessive mocking
(5+ mocks signals a design problem); no trivial tests; no fragile tests
that break on refactor; no testing of timers (test the result).

---

## Fix-Loop: Tests -> Fix -> Re-Test

When tests fail, a fix-loop starts. The user decides how to proceed.

### Step 1: Summarize test results

Emit the canonical Test Result block (referenced as `TEST-RESULT-BLOCK`
elsewhere in this skill):

```
=== Test Result ===

Passed: {N} tests
Failed: {N} tests
Coverage: {line}% / {branch}% / {function}%

Failed tests:
- {test name}: {short error description}
  Cause: code bug / wrong test expectation / missing implementation
  Fix effort: S/M/L
  File: {src/path/file.ts} or {tests/path/test.ts}

Coverage gaps:
- {src/path/file.ts}: {function} not tested
```

### Step 2: Ask user how to proceed

```
How should I proceed?

A) Fix all findings automatically
   -> I fix everything, retest, repeat until all tests are green

B) Approve fixes one by one
   -> I show each fix before implementation

C) Only adjust tests (the code is correct, the tests are wrong)

D) Abort -- I want to look at findings manually first
```

### Step 3: Fix implementation

For each fix:
1. Identify cause (code bug vs. test error)
2. Implement fix
3. Run affected tests
4. On Option B: show fix to user before continuing

### Step 4: Re-test (automatic)

After all fixes: run the full test suite again and emit the
`TEST-RESULT-BLOCK` from Step 1. If failures remain, return to Step 1.
The loop repeats until all tests are green or the user aborts.

### Step 5: Update artifacts (backlog-first)

After a successful test run:

1. **Backlog row first.** Update every FEATURE/FIX/IMP/PLAN row whose
   status the test run changed. Coverage notes go into Notes column.
   Transitions: `In Progress -> In Review` or `In Progress -> Done`.
2. **Feature specs (substance only).** Verify Success Criteria accuracy.
   Status lives in the backlog row, not the spec.
3. **Wayfinder.** New entry-point or undocumented module discovered:
   add the row to `src/ARCHITECTURE.map` and write the JSDoc header.
4. **Living Documents writeback (per `/coding` rules)** if code fixes
   were needed during the test run.
5. **`/consistency-check` mode A** at phase end. Catches orphan tests,
   missing coverage entries, dashboard mismatches, dead links. The
   Handoff Ritual reports the result.

---

## Handoff Ritual (mandatory at end of phase)

`/testing` always runs this ritual at the end, regardless of how it was
started (directly or via `/dia-guide`).

### Part 1: Artifact report

Reference the final `TEST-RESULT-BLOCK` from the fix-loop (Step 1) for
pass/fail and coverage numbers. Add the produced or updated artifacts:

```
Produced / updated:
- tests/{paths}
- Fix-loop status: {N iterations, N fixes applied}
- _devprocess/requirements/features/FEATURE-*.md: {test-status updates}
- _devprocess/context/BACKLOG.md: {coverage items added, dashboard refreshed}
```

### Part 2: Handoff context

Append a new entry to `_devprocess/context/HANDOFFS.md` with:

- Coverage gaps that the user accepted (with justification)
- Open test cases deferred to the next cycle
- Brittle tests or flaky patterns noted during the fix-loop
- Any security-adjacent concerns (e.g. input validation holes noticed while
  writing tests) for the security-audit phase

### Part 3: Phase-end commit

Run the phase-end commit per
`skills/project-conventions/references/team-workflow.md` section
"Phase-end commit (binding)". It stages every artefact produced (tests,
coverage config, FEATURE updates, BACKLOG updates), commits, tags the
phase, and opens a draft PR if missing.

Canonical commit message for TESTING:

```
test: <ITEM-ID> testing complete

<one-line summary: N tests added, coverage L%/B%/F%>

Refs: <ITEM-ID>
```

After the commit lands:

```
python3 tools/github-integration/flow.py tag-phase --item <ID> --phase test
python3 tools/github-integration/flow.py sync-status --item <ID>
```

`sync-status` mirrors BACKLOG Status to the GitHub issue/project (and
Assignee back to Claim). No-op outside `mode = "github-sync"`. Skip
the commit silently if the working tree has no changes.

### Part 4: Transition question

Ask the user:

> "Tests are complete and all green. Coverage: {line}% / {branch}% /
> {function}%. Recommended next: `/security-audit`.
>
> Shall I start `/security-audit` now, or would you like to review first?"

**On agreement** ("yes" / "go" / "next") or when running inside
`/dia-guide`:
-> Start `/security-audit` and pass the handoff context

**On rejection** ("no" / "stop" / "I want to check first"):
-> Pause and wait for user instruction

## Keywords
Tests, unit tests, integration tests, test coverage, testing, TDD,
coverage gaps, test pyramid, fix-loop, re-test, regression, handoff
