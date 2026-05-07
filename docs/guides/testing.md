---
title: Testing
description: Unit and integration tests with the AAA pattern, FIRST principles, coverage targets, and a fix-loop until green.
---

# Testing

`/testing` creates unit and integration tests, then runs a fix-loop
until all tests are green and coverage targets are met.

**Input:** Implemented codebase + FEAT specs from
[`/coding`](./coding)
**Output:** Unit and integration tests, coverage report, FEAT
backlog rows updated to reflect verified Success Criteria

## Phase 0: Triage and codebase analysis

Before writing tests, the skill confirms the inbound item type
(`FEAT-{ee}-{ff}`, `IMP-{ee}-{ff}-{nn}`, or
`FIX-{ee}-{ff}-{nn}`) and analyses the codebase:

- **Framework detection**: Jest, Vitest, Pytest, Go test, JUnit,
  XCTest, the project's actual choice from `package.json`,
  `pyproject.toml`, or equivalent
- **Naming convention**: `*.test.ts` vs `*.spec.ts`, `test_*.py` vs
  `*_test.py`, the project's existing pattern
- **Mocking patterns**: which mock library, which fakes already
  exist
- **Existing test pyramid**: how many unit, integration, end-to-end
  tests exist today

Tests follow the project's existing patterns. The skill never
introduces a new framework or convention without confirmation.

## Role alongside TDD

If `/coding` ran in TDD mode (Phase 3c), unit tests already exist
for the happy paths. In that case, `/testing` focuses on:

1. **Integration tests (primary)**: API endpoints, database
   interactions, event flows, external integrations with mocked
   boundaries
2. **Unit test gaps (secondary)**: edge cases, error cases, boundary
   conditions that the TDD RED-test did not catch
3. **Coverage check (tertiary)**: report against targets

If `/coding` ran without TDD mode, `/testing` takes over unit test
creation as the fallback.

## The testing pyramid

```
            ___
           / E \         End-to-end (few, expensive, full stack)
          /-----\
         /  IT   \       Integration (some, real boundaries)
        /---------\
       /    UT     \     Unit (many, cheap, fast)
      /-------------\
```

Most tests are unit tests. Integration tests cover the seams
between modules and the real boundaries (database, queue, third-
party API). End-to-end tests cover only the critical user
journeys.

## AAA pattern

Every test follows Arrange / Act / Assert:

```ts
test("auto-resolve replies to password reset tickets", () => {
  // Arrange
  const ticket = makeTicket({ subject: "I forgot my password" });
  const agent = new TriageAgent({ kb: passwordKb });

  // Act
  const reply = agent.resolve(ticket);

  // Assert
  expect(reply.status).toBe("resolved");
  expect(reply.body).toContain("reset link");
});
```

The three blocks are visually separated. Setup belongs in Arrange,
the single behaviour under test belongs in Act, the expectations
belong in Assert. A test that mixes them is a test that nobody can
debug six months later.

## FIRST principles

Every test is:

- **Fast**: milliseconds, not seconds. Slow tests do not run on
  every save.
- **Independent**: tests run in any order, no shared mutable state.
- **Repeatable**: same input, same output, every time, on every
  machine.
- **Self-validating**: pass or fail, no human reads the log to
  decide.
- **Timely**: written when the code is, not three months later.

## Coverage targets

| Coverage type | Default target |
|---|---|
| Line coverage | 85% |
| Branch coverage | 80% |
| Function coverage | 90% |

Targets are defaults. Real numbers come from the project's
`CLAUDE.md` or `_devprocess/rules/technical.md`. Some projects
deliberately accept lower coverage on UI glue or generated code.
The skill does not chase coverage for its own sake.

## Anti-patterns

The skill rejects tests that:

- Test the test framework instead of the code (`expect(true).toBe(true)`)
- Assert on internal state instead of observable behaviour
- Mock everything (the test then verifies the mock, not the code)
- Share fixtures across files in ways that hide order dependence
- Use sleeps to wait for async work instead of proper handles

## Fix-loop

Failing tests trigger a fix-loop with 4 user options:

- **A)** Fix all findings automatically
- **B)** Approve fixes one by one
- **C)** Only adjust tests (code is correct, tests are wrong)
- **D)** Abort, review findings manually first

Each iteration verifies that previously failing tests now pass with
fresh command output (no caches, no "should pass now"). The loop
repeats until all tests are green or the user aborts. See
[Verification Gates](../concepts/verification-gates) for the
forbidden language list.

## Step 5: Update artifacts

After tests are green, the skill writes back in this order (state
first, substance second):

1. **Backlog row** for the FEAT / IMP / FIX (Status -> tested or
   Done, last-change, commit SHA, claim cleared if no further phase
   pending).
2. **FEAT spec** (substance only: which Success Criterion is
   verified by which test, optional `## Code Pointer` appendix that
   names the test concept, not the file path).
3. **Wayfinder** (`src/ARCHITECTURE.map` row updated if a new test
   harness or test entry-point was added).
4. **`METRICS.md`** (cycle time per FEAT for the testing phase
   appended).

## Handoff

Ends with the 4-part [Handoff Ritual](../concepts/handoff-rituals):
artifact report, handoff context appended to `HANDOFFS.md`,
phase-end commit (`test: {ITEM-ID} testing complete`) plus
`tag-phase --phase test` and `sync-status --item {ITEM-ID}` (no-op outside `mode = "github-sync"`), transition question. The guide
runs `/consistency-check` Mode A on the changed artifacts at the
boundary. The next phase is [`/security-audit`](./security-audit).
The handoff context documents any accepted coverage gaps with
justification, brittle tests, and security-adjacent observations
noticed during test writing.

## Read the skill file

[`skills/testing/SKILL.md`](https://github.com/pssah4/digital-innovation-agents/blob/main/skills/testing/SKILL.md) on GitHub.
