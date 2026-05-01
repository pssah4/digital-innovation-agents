---
title: Verification Gates
description: The "no completion without fresh evidence" rule that prevents AI agents from hallucinating success.
---

# Verification Gates

The most common failure mode of AI coding sessions is hallucinating
success. The agent says "tests are green", "the build works", "the
bug is fixed", without actually having run the verification command
in that message. Digital Innovation Agents addresses this with a
verification gate in `/coding` Phase 4a.

## The rule

> No completion claims without fresh verification evidence.
>
> If the agent has not run the verification command in this message,
> it cannot claim the task is successful.

This rule is handed to the Default agent before implementation starts
and is enforced at the end of every task and every phase.

## The gate function

Five steps, all mandatory:

1. **Identify** which command proves the claim
   - "Tests pass" -> a concrete test command with path
   - "Build works" -> a concrete build command
   - "Bug fixed" -> the test reproducing the original symptom
2. **Run** the command fully, not cached, not partial
3. **Read** the complete output, check the exit code, count failures
4. **Verify** the output actually confirms the claim
5. **Claim** the status only now, with the evidence

Skipping any step is lying, not verifying.

## Forbidden language

Before fresh verification, these phrases are forbidden:

- "should work"
- "probably okay"
- "looks good"
- "tests should be green now"
- "the change should fix the bug"
- any statement that implies success without evidence

## Common failures: what is not enough

| Claim | What is not sufficient | What is sufficient |
|---|---|---|
| Tests pass | "Looks like tests should pass" | Test command output with 0 failures |
| Linter clean | "Linter passed earlier" | Linter output with 0 errors |
| Build works | "Linter passed" | Build command with exit code 0 |
| Bug fixed | "Code changed, assumed fixed" | Test reproducing the original symptom passes |
| Subagent done | "Subagent reported success" | VCS diff shows the expected changes |
| Requirements met | "Tests pass, phase complete" | Line-by-line checklist against the plan |

## Regression test cycle (Phase 4b)

For bug fixes, a stricter variant applies: the 6-step regression
cycle.

1. Write the regression test reproducing the bug behavior
2. **Run 1**: test MUST pass (because the fix is already in)
3. Temporarily revert the fix (`git stash` or code revert)
4. **Run 2**: test MUST FAIL. This proves the test actually catches the bug.
5. Restore the fix
6. **Run 3**: test MUST pass again

Only when all three runs produce the expected result is the bug
marked as resolved and the regression test marked as valid. The
`FIX-{ee}-{ff}-{nn}` row in `BACKLOG.md` records the commit SHA, and
the FIX detail file under `_devprocess/requirements/fixes/` carries
a `## Regression test` section: "Regression test verified via
red-green cycle on {date}".

Without this cycle, a regression test might always pass regardless of
the fix. You would never know it is not actually catching the bug.

## Why this matters

AI agents are helpful by default. They want to report success. They
try to make the user happy. That helpfulness is valuable, but it makes
agents bad at verification. They will round up a "probably works" into
"done" if you let them.

Verification gates force the agent to be honest by default. You
cannot claim success without evidence. The command has to run, the
output has to be read, the verification has to succeed. No shortcuts.

## Where the rule is enforced

- **`/coding` Phase 4a**: applied to every task completion and to the
  final implementation report
- **`/testing` fix-loop**: each iteration verifies that previously
  failing tests now pass, with fresh command output
- **`/security-audit` fix-loop**: each iteration re-runs the audit
  phase for the affected category, with fresh output
- **the Closing Handoff**: before release notes are generated,
  the guide verifies that the final test run and security audit
  are both green

## See also

- [Coding guide](../guides/coding): Phase 4a Verification Gate detail
- [V-Model concept](./v-model)
- [Living Documents](./living-documents): why accurate artifacts matter
