---
title: Testing
description: Integration tests and unit-test gap-filling with a clear role alongside TDD in /coding.
---

# Testing

`/testing` creates integration tests and fills unit-test gaps, then
runs a fix-loop until all tests are green.

**Input**: Implemented codebase + Feature specs
**Output**: Unit and integration tests, coverage report

## Role alongside TDD

If `/coding` ran in TDD mode (Phase 3b), unit tests already exist
for all new modules. In that case, `/testing` focuses on:

1. **Integration tests (primary)**: API endpoints, database
   interactions, event flows, external integrations with mocked boundaries
2. **Unit test gaps (secondary)**: edge cases, error cases, boundary
   conditions that the TDD RED-test did not catch
3. **Coverage check (tertiary)**: report against targets (85% line,
   80% branch, 90% function)

If `/coding` ran without TDD mode, `/testing` takes over unit test
creation as the fallback. Same AAA pattern and FIRST principles as
before.

## Fix-loop

Failing tests trigger a fix-loop with 4 user options:

- **A)** Fix all findings automatically
- **B)** Approve fixes one by one
- **C)** Only adjust tests (code is correct, tests are wrong)
- **D)** Abort, review findings manually first

The loop repeats until all tests are green or the user aborts.

## Handoff

Ends with the 3-part Handoff Ritual. Next phase: `/security-audit`.
The handoff context documents any accepted coverage gaps with
justification, brittle tests, and security-adjacent observations
noticed during test writing.

## Read the skill file

[`skills/testing/SKILL.md`](https://github.com/pssah4/digital-innovation-agents/blob/main/skills/testing/SKILL.md) on GitHub.
