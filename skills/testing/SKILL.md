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

Creates tests that fit seamlessly into the existing codebase. Detects the
framework, patterns, and conventions automatically from the project.

## MANDATORY Phase 0: Artefakt-Triage (2026-04-21)

Neue Tests zaehlen als Doku-/Code-Aenderung und muessen an ein
existierendes Artefakt gebunden sein. Bevor der erste Test geschrieben
wird, muss eine dieser Zuordnungen vorliegen:

- **FEATURE-ID** -- Tests zu neuen oder bestehenden Feature-Specs
- **IMP-ID** -- Tests als Teil eines Improvements (z. B. Coverage-
  Erhoehung, Refactor-Sicherung)
- **FIX-ID** -- Regressionstests zu einem behobenen Bug

**Ausnahme:** reine Test-Analyse (Coverage-Report lesen, Gaps
identifizieren, bestehende Tests lesen) ist read-only und braucht keine
Triage.

Wenn die Zuordnung nicht aus dem User-Prompt ableitbar ist, stellt der
Skill vor dem ersten neuen Test genau eine Frage:

> "Gehoert dieser Test-Lauf zu einem FEATURE, einem IMP oder einem
> FIX? Bitte die ID nennen."

Details und Entscheidungsbaum:
`skills/project-conventions/references/graph-invariants.md`
(Abschnitt "Artefakt-Triage am Einstiegspunkt").

## Codebase analysis first

Before writing a single test, analyze the project:

```
1. Detect test framework:
   - package.json -> jest/vitest/mocha? (scripts.test, devDependencies)
   - pyproject.toml -> pytest? (tool.pytest)
   - Cargo.toml -> Rust built-in?
   - Existing test files -> which pattern?

2. Detect existing test structure:
   - Where are tests? (tests/, __tests__/, src/**/*.test.ts, *.spec.ts?)
   - Naming convention? (.test.ts, .spec.ts, _test.py?)
   - Is there conftest.py / jest.config.ts / vitest.config.ts?
   - Are there test utilities, fixtures, factories?

3. Adopt existing patterns:
   - How are mocks created? (jest.mock, vi.mock, unittest.mock?)
   - How is async handled?
   - Which assertions are used?
   - Are there shared test helpers?

4. What is NOT tested? (identify gaps)
```

Always follow existing patterns. Don't introduce new test frameworks or
patterns unless the project has none yet.

## Testing Pyramid

```
        /\
       /E2E\           Few, slow, expensive
      /------\
     / Integr. \       Moderate count
    /------------\
   /  Unit Tests  \    Many, fast, cheap
  /________________\
```

Focus of this skill: **Integration Tests** (primary) and **Unit Tests**
(either as TDD fallback or gap-filling -- see next section).
E2E tests are a separate topic.

## Role alongside TDD

When `/coding` runs in TDD mode (see `coding/SKILL.md` Phase 3b), unit
tests for new modules already exist when this skill runs. In that case,
`/testing` focuses on three things, in this priority:

### 1. Integration tests (primary)

Tests that exercise multiple modules together:

- API endpoints: request -> response -> side effects
- Database interactions: with test DB or in-memory DB
- Event and message flows between components
- External integrations with mocked boundaries

### 2. Unit test gaps (secondary)

Even after TDD, gaps can remain:

- Edge cases that weren't explicitly in the RED test
- Error cases for exceptions and failure paths
- Boundary conditions (min/max, empty arrays, null/undefined)

`/testing` scans the TDD-generated test code and suggests missing cases.

### 3. Coverage check (tertiary)

A coverage report against the targets (85% line / 80% branch / 90%
function). Gaps are listed but not auto-filled -- the user decides whether
trivial code actually needs testing.

## When `/coding` ran WITHOUT TDD mode (fallback)

`/testing` takes over unit test creation as well (its historical role).
In fallback mode, `/testing` analyzes the new modules and creates unit
tests following the AAA pattern and FIRST principles, just like the
unit-test sections below.

## Unit Tests

### When to write unit tests

- For every public function/method with logic
- For utility functions and helpers
- For data transformations
- For error handling and edge cases
- NOT for trivial getters/setters without logic
- NOT for pure pass-through functions

### AAA Pattern (Arrange, Act, Assert)

Every test follows the AAA pattern:

```typescript
// Example (TypeScript/Jest -- adapt to project framework)
describe('ToolRegistry', () => {
  describe('registerTool', () => {
    it('should register a tool and make it retrievable by name', () => {
      // Arrange
      const registry = new ToolRegistry();
      const tool = createMockTool({ name: 'read-file' });

      // Act
      registry.registerTool(tool);

      // Assert
      expect(registry.getTool('read-file')).toBe(tool);
    });

    it('should throw when registering duplicate tool names', () => {
      // Arrange
      const registry = new ToolRegistry();
      const tool = createMockTool({ name: 'read-file' });
      registry.registerTool(tool);

      // Act & Assert
      expect(() => registry.registerTool(tool))
        .toThrow(/already registered/);
    });
  });
});
```

### FIRST Principles

- **Fast**: tests must run quickly (< 1s per test)
- **Independent**: no test depends on another
- **Repeatable**: same input = same output, always
- **Self-validating**: pass or fail, no manual checking
- **Timely**: tests written with the feature, not later

### What to test -- per-function checklist

Read `references/test-checklist.md` for the complete checklist.

Short version:
- Happy path (normal flow)
- Edge cases (empty inputs, boundary values, null/undefined)
- Error cases (invalid inputs, missing dependencies)
- Boundary conditions (min/max, empty arrays, large data)

### Mocking rules

- Mock **external dependencies** (APIs, file system, database)
- Do NOT mock the unit under test
- Prefer dependency injection over global mocks
- Reuse existing mock patterns from the project

## Integration Tests

### When to write integration tests

- Multiple modules interacting
- API endpoints (request -> response)
- Database access (test DB or in-memory)
- Event/message flows between components

### Integration test rules

- Real dependencies where possible, mock only external services
- Each test is independent (own state, own teardown)
- Realistic test data, not "foo" / "bar" / "test"
- Set timeouts for async operations
- Setup/teardown in beforeAll/afterAll for shared resources

### File naming

Follow the existing project pattern. If none exists:

- Unit tests: `{module}.test.ts` or `{module}.spec.ts`
- Integration tests: `{module}.integration.test.ts`
- Same directory as source, or under `tests/`

## Test workflow

### For existing feature without tests

```
/testing {file or module}

1. Analyze the file and its dependencies
2. Identify testable functions/methods
3. Recognize existing test patterns in the project
4. Create tests (AAA pattern, FIRST principles)
5. Run tests and verify
6. Check coverage of new tests
```

### For new feature (after /coding)

```
/testing

1. Read the feature spec (FEATURE-*.md) for Success Criteria
2. Identify all new/changed files
3. Create integration tests for module interactions
4. Fill unit-test gaps if any
5. Verify Success Criteria from the feature spec
```

### Coverage targets

| Metric | Target | Minimum |
|--------|--------|---------|
| Line Coverage | 85% | 70% |
| Branch Coverage | 80% | 65% |
| Function Coverage | 90% | 75% |

These are guidelines. Project-specific targets in `CLAUDE.md` or feature
specs take precedence.

## Anti-patterns to avoid

Read `references/test-anti-patterns.md` for details.

Short version:
- **No testing of implementation details**: test behavior, not internals
- **No excessive mocking**: if you need 5+ mocks, the code has a design problem
- **No trivial tests**: `expect(1+1).toBe(2)` helps no one
- **No fragile tests**: tests that break on every refactoring test the wrong thing
- **No testing of setTimeout/setInterval**: test the result, not the timer

## Codebase-awareness

Before writing tests, ALWAYS:
- Read existing test files and adopt patterns
- Reuse test utilities and shared fixtures
- Follow existing naming conventions
- Respect project-specific test configuration (jest.config, vitest.config, etc.)

---

## Fix-Loop: Tests -> Fix -> Re-Test

When tests fail, a fix-loop starts. The user decides how to proceed.

### Step 1: Summarize test results

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

After all fixes: run the full test suite again.

```
=== Re-Test Result ===

Before: {N} failed
After:  {N} failed

{If still failures: back to step 1}
{If all green:}

All tests passed! Coverage: {line}% / {branch}% / {function}%
```

The loop repeats until all tests are green or the user aborts.

### Step 5: Update artifacts

After a successful test run:
- Feature specs: update test status
- Backlog: document test coverage
- If code fixes were needed: write the changes back into ADRs/Features
  (same Living-Documents rule as the `/coding` skill)

---

## Handoff Ritual (mandatory at end of phase)

`/testing` always runs this ritual at the end, regardless of how it was
started (directly or via `/v-model-workflow`).

### Part 1: Artifact report

```
Produced / updated:
- tests/{paths}: {new or updated test files}
- Coverage report: {line}% / {branch}% / {function}%
- Fix-loop status: {N iterations, N fixes applied}
- _devprocess/requirements/features/FEATURE-*.md: {test-status updates}
- _devprocess/context/10_backlog.md: {new coverage items added per BACKLOG-TEMPLATE.md, dashboard refreshed}
```

### Part 2: Handoff context

Append a new entry to `_devprocess/context/30_handoffs.md` with:

- Coverage gaps that the user accepted (with justification)
- Open test cases deferred to the next cycle
- Brittle tests or flaky patterns noted during the fix-loop
- Any security-adjacent concerns (e.g. input validation holes noticed while
  writing tests) for the security-audit phase

### Part 3: Transition question

Ask the user:

> "Tests are complete and all green. Coverage: {line}% / {branch}% /
> {function}%. The next step in the V-Model is `/security-audit`.
>
> Shall I start `/security-audit` now, or would you like to review first?"

**On agreement** ("yes" / "go" / "next") or when running inside
`/v-model-workflow`:
-> Start `/security-audit` and pass the handoff context

**On rejection** ("no" / "stop" / "I want to check first"):
-> Pause and wait for user instruction

## Keywords
Tests, unit tests, integration tests, test coverage, testing, TDD,
coverage gaps, test pyramid, fix-loop, re-test, regression, handoff
