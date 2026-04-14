---
title: Coding
description: The handoff skill that loads context, reviews critically, briefs the Default agent with five sub-phase patterns, and writes artifacts back continuously.
---

# Coding

`/coding` is the most involved skill in the workflow. It does not
write code itself. The Default agent in your coding tool does that.
Instead, `/coding` acts as a briefing and review layer that structures
how the Default agent approaches the task.

## Four phases

```
Phase 1: Load context (plan-context.md, ADRs, Features, CLAUDE.md)
Phase 2: Critical review against the real codebase
Phase 3: Implementation (delegated to Default agent with 5 sub-phases)
Phase 4: Completion. Verification gate, regression cycle, final sync.
```

Phase 1, 2, and 4 are the v1 differentiators preserved from the
classic workflow. Phase 3 is where v2 adds the five Default-agent
briefing patterns.

## Phase 2: Critical review

Before any code changes, `/coding` reconciles the design artifacts with
the real codebase:

- Do the ADR proposals match the actual architecture?
- Do existing patterns contradict the proposals?
- Are the tech-stack assumptions in `plan-context.md` correct?
- Are dependencies or constraints missing?
- Are modules affected but not mentioned in the designs?

Every divergence is written back into the source artifacts before
implementation begins. ADRs get their status updated to
`Accepted (modified by review)`. Feature Success Criteria are adjusted.
New ADRs are created when the review reveals missing decisions.

This is the moment where the V-Model turns from plan into reality.

## Phase 3: Implementation (five sub-phase patterns)

Before handing off to the Default agent, `/coding` briefs it with five
mandatory patterns:

### Phase 3a: Task-breakdown guidelines

The Default agent is told:

- Split each task into bite-size steps (2-5 minutes each): write
  failing test, verify it fails, write minimal code, verify it passes, commit
- Every task has a file list (Create/Modify/Test with exact paths)
- No placeholders: "TBD", "TODO", "implement later", "Similar to Task N"
  are forbidden
- Self-review after plan creation: spec coverage, placeholder scan,
  type consistency

### Phase 3b: TDD mode (optional)

Opt-in. When the user enables TDD, `/coding` hands this rule to the
Default agent: "No production code without a failing test first."
RED, verify RED, GREEN, verify GREEN, REFACTOR.

Exceptions (with user confirmation): throwaway prototypes, generated
code, configuration files.

### Phase 3c: Debugging protocol

If a bug appears during implementation, the Default agent follows a
4-phase root-cause process:

- **Phase A: Root Cause.** Read error, reproduce, check recent changes,
  trace data flow backwards.
- **Phase B: Pattern Analysis.** Find working examples, read reference
  completely.
- **Phase C: Hypothesis.** One hypothesis, smallest possible change,
  one variable at a time.
- **Phase D: Implementation.** Failing test, single fix, verify.
- **Phase D.5: Architecture alarm.** After 3+ failed fix attempts, STOP.
  This is not a bug, it is a wrong architecture. Discuss with the user.

Every bug, even a trivial one, gets an entry in
`_devprocess/context/20_bugs.md` with a `FIX-NN` ID, causal chain, and
priority (P0/P1/P2).

## Phase 4: Completion

### Phase 4a: Verification gate

The rule: no completion claims without fresh verification evidence.

Before declaring anything "done", the Default agent must:

1. **Identify** which command proves the claim
2. **Run** it fully (not cached)
3. **Read** the full output, check exit code, count failures
4. **Verify** the output matches the claim
5. **Claim** the status only now, with the evidence

Forbidden language without fresh verification: "should work", "probably
okay", "tests should be green now".

This is the most important pattern from v2. It addresses the "done
hallucination" failure mode that plagues AI coding sessions.

### Phase 4b: Regression test cycle

For every bug fix:

1. Write the regression test reproducing the bug
2. **Run 1**: test MUST pass (fix is in)
3. Revert the fix temporarily
4. **Run 2**: test MUST fail (proves it catches the bug)
5. Restore the fix
6. **Run 3**: test MUST pass again

The bug log in `20_bugs.md` gets a note: "Regression test verified via
red-green cycle on {date}".

### Final synchronization

After implementation is verified, `/coding` updates:

- Feature specs (Status -> "Implemented", How-It-Works section, SC verified)
- ADRs (all statuses finalized, Implementation Notes added)
- Backlog (new findings, deferred items)
- Bug log (all FIX-NN entries updated with commit SHAs)
- plan-context.md, arc42, memory/MEMORY.md (when applicable)

The result: documentation reflects the actual state, not the original plan.

## Living Documents

This continuous writeback is the Living Documents pattern. Artifacts are
never frozen after Phase 3. They evolve with the code. See
[Living Documents](../concepts/living-documents) for the full pattern.

## Handoff

`/coding` ends with the 3-part Handoff Ritual (Artifact report, Handoff
context in `30_handoffs.md` with references to FIX-NN bugs, Transition
question for `/testing`).

## Read the skill file

Want to see the exact instructions the agent follows? The skill file
is [`skills/coding/SKILL.md`](https://github.com/pssah4/digital-innovation-agents/blob/main/skills/coding/SKILL.md)
on GitHub.

## What's next

- [Testing guide](./testing), the next phase with the role-alongside-TDD section
- [Living Documents concept](../concepts/living-documents), the writeback pattern
- [Verification Gates concept](../concepts/verification-gates), why evidence matters
