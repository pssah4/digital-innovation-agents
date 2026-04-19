---
name: coding
description: >
  Handoff skill: loads plan-context.md and all design artifacts, performs a
  critical review against the real codebase, and ensures continuous writeback
  to the artifacts during and after implementation. Use this skill when the
  user mentions "implement", "code", "realize plan-context", "build feature",
  or similar and a plan-context.md or FEATURE specs exist. This skill does
  NOT take over the coding workflow -- the Default Claude Code agent remains
  responsible for the actual implementation. This skill ensures the context
  is critically reviewed, cleanly handed off, and artifacts stay up to date.
disable-model-invocation: false
---

# Coding -- Review, Handoff & Living Documents

This skill has three main responsibilities:

1. **Load context** from the design phases
2. **Critically review** it before implementation begins
3. **Continuously write back** so artifacts always reflect the current state

The actual implementation is done by the Default Claude Code agent. This
skill briefs that agent with precise guidelines (see Phase 3 subsections
below) so the agent's work is structured, verified, and documented.

---

## Phase 1: Load Context

Read these documents in order:

```
REQUIRED:
1. _devprocess/requirements/handoff/plan-context.md    (primary input)
2. _devprocess/architecture/ADR-*.md                   (architecture decisions)
3. _devprocess/requirements/features/FEATURE-*.md      (feature details + Success Criteria)
4. CLAUDE.md                                           (project-specific rules)

OPTIONAL (if present):
5. _devprocess/architecture/arc42.md                   (overall architecture)
6. _devprocess/requirements/epics/EPIC-*.md            (strategic context)
7. _devprocess/context/10_backlog.md                   (open items)
8. _devprocess/context/20_bugs.md                      (known bugs, FIX-NN entries)
9. _devprocess/context/30_handoffs.md                  (last handoff entry from /architecture)
10. memory/MEMORY.md                                   (architecture key facts)
```

If no `plan-context.md` exists:

```
No plan-context.md found. Options:

A) I have FEATURE-*.md files -- work directly with them
B) I want to run the V-Model workflow -> /v-model-workflow
C) I have an informal description -- work with it
```

---

## Phase 2: Critical Review

BEFORE an implementation plan is created, critically check the design
artifacts against the real codebase. This is the most important step.

### 2a: Codebase reconciliation

Read the existing codebase and check:

- Do the ADR proposals match the real architecture?
- Are there existing patterns that contradict the proposals?
- Are the tech-stack assumptions in plan-context.md correct?
- Are dependencies or constraints missing?
- Are modules affected by the planned changes but not mentioned in the
  architecture?

### 2b: Review output

```
=== Critical Review: {project/feature} ===

Tech Stack: {from plan-context.md, with corrections if needed}
ADRs: {count} reviewed
Features: {count} reviewed
Success Criteria: {count} to verify

--- Codebase reconciliation ---

CONFIRMED (matches codebase):
- ADR-001: {title} -- proposal fits, {justification}
- FEATURE-001-001 SC-01: {criterion} -- realistic

CHANGES NEEDED (divergence from codebase):
- ADR-002: {title} -- proposal: {original}
  Problem: {what doesn't fit}
  Recommendation: {what to do instead}
- FEATURE-002-003 SC-02: {criterion}
  Problem: {why not as specified}
  Recommendation: {alternative}

MISSING (not addressed in designs):
- {module/pattern affected but not addressed}

RISKS:
- {risk 1}: {description and mitigation}

--- Decisions ---

Please confirm or correct the change proposals before I create the
implementation plan.
```

### 2c: Write changes back

Every change from the review is IMMEDIATELY written back into the source
artifacts BEFORE implementation begins:

- **ADR changed** -> update ADR file:
  - Adjust Decision section
  - Status -> `Accepted (modified by review)`
  - Document the justification for the change
- **ADR rejected** -> update ADR file:
  - Status -> `Deprecated`
  - Justification and reference to alternative
- **Feature SC changed** -> update FEATURE file:
  - Adjust Success Criteria
  - Reason for change as a comment
- **plan-context.md corrected** -> update file
- **New ADR needed** -> create new ADR file

After writing back: emit a summary of the changed files.

### 2d: Signal writeback (drift count)

Append a row to `_devprocess/context/40_metrics.md` under the
"Drift count (plan-context.md vs. real code)" table:

- Date: today
- ADR count: how many ADRs were reviewed
- arc42 section count: how many arc42 sections were reviewed
- plan-context item count: how many plan-context entries were checked
- Drift flagged: count of CHANGES NEEDED + MISSING items from the review
- Drift resolved: count of items actually written back in step 2c
- Open: count that remained unresolved (for example because the user
  wanted to discuss first)

If `40_metrics.md` does not yet exist, copy
`skills/v-model-workflow/templates/METRICS-TEMPLATE.md` into the
file first, then append. A rising drift count over multiple
reconciliation runs signals that the ADRs or plan-context are losing
touch with reality.

---

## Phase 3: Implementation (delegated to Default Agent)

After the review, implementation is handed off to the Default Claude Code
agent. Before handing off, the `/coding` skill provides the agent with the
following guidelines, which are mandatory for this session.

### Phase 3a: Task-breakdown guidelines

Pass these rules to the Default agent before it enters plan-mode:

**Bite-size tasks (2-5 minutes per step):**

Every task decomposes into:
1. Write the failing test (one test, one behavior)
2. Run the test -- it MUST fail with the expected reason
3. Write the minimal implementation to make it pass
4. Run the test -- it MUST pass
5. Commit with a conventional prefix (feat/fix/chore/docs/refactor)

**Every task has a file list:**
- Create: `exact/path/to/file.py`
- Modify: `exact/path/to/existing.py:123-145`
- Test: `tests/exact/path/to/test.py`

**No placeholders in the plan:**
- Forbidden: "TBD", "TODO", "implement later", "fill in details"
- Forbidden: "Add appropriate error handling", "handle edge cases" (without concrete cases)
- Forbidden: "Write tests for the above" (without actual test code)
- Forbidden: "Similar to Task N" (repeat the code -- tasks may be read out of order)
- Forbidden: Steps that describe WHAT without showing HOW

**Self-review after plan creation:**

The agent re-reads the plan and checks:
1. **Spec Coverage:** Does every requirement from plan-context.md map to at least one task?
2. **Placeholder Scan:** Does the plan contain any red-flag patterns from the list above?
3. **Type Consistency:** Do function/type/property names match across tasks?

Fix gaps and placeholders inline before implementation starts.

### Phase 3b: TDD Mode (optional)

**Activation:** The user can enable TDD mode explicitly with "enable TDD
mode" or by starting `/coding` with a `--tdd` hint. Default is: TDD is NOT
enforced (because throwaway prototypes and exploration suffer under TDD
pressure).

When active, `/coding` hands this rule to the Default agent for this session:

**The rule:** No production code without a failing test written first.

**The cycle:**
1. **RED:** Write a failing test (one behavior, one assertion)
2. **Verify RED:** Run the test -- it MUST fail with the expected reason
   - If it passes immediately: the test isn't testing the new functionality, fix it
   - If it fails with a syntax error: fix the error and re-run
3. **GREEN:** Write the minimal code to pass the test (no more)
4. **Verify GREEN:** Run the test -- it MUST pass, no other tests broken
5. **REFACTOR:** Clean up while keeping tests green (no new behavior)

**Exceptions (only with user confirmation):**
- Throwaway prototypes
- Generated code
- Configuration files

### Phase 3c: Debugging protocol (if a bug appears)

When a test fails unexpectedly during implementation, or behavior is
incorrect, or a fix doesn't work, `/coding` hands the following 4-phase
protocol to the Default agent:

**The rule:** No fixes without root-cause investigation.

**Phase A: Root Cause (BEFORE any fix attempt)**
1. Read the error message completely -- stack trace, line numbers, codes
2. Check reproducibility -- does it happen every time?
3. Check recent changes -- `git diff`, last commits, new dependencies
4. In multi-component systems: add logging at every component boundary
5. Trace the data flow backwards -- where does the bad value originate?

**Phase B: Pattern Analysis**
1. Find working examples in the codebase
2. Read the reference implementation completely (don't skim)
3. List every difference -- even ones that seem irrelevant
4. Check dependencies and config assumptions

**Phase C: Hypothesis**
1. State one hypothesis: "Root cause is X because Y"
2. Make the smallest possible change to test it
3. One variable at a time
4. If the hypothesis is wrong: form a new one, don't pile fixes

**Phase D: Implementation**
1. Write a failing test that reproduces the bug
2. Apply exactly one fix that addresses the root cause
3. Verify: test passes, no regressions elsewhere
4. Document the bug in `_devprocess/context/20_bugs.md` with a FIX-NN ID,
   the causal chain (step 1 -> step 2 -> ... -> error), and priority (P0/P1/P2)

**Phase D.5: Architecture alarm (after 3+ failed fix attempts)**

If three or more fix attempts fail to resolve the situation, this is an
architecture problem, not a bug:
- Each fix reveals a new problem in a different place?
- Fixes require "massive refactoring"?
- Each fix creates new symptoms?

Then STOP. No fourth attempt. Instead:
- Question the pattern fundamentally -- is the approach sound?
- Discuss with the user before any more fixes
- This is not a failed hypothesis -- it's a wrong architecture

**Writeback:** Every bug found, even if the fix is trivial, gets an entry
in `_devprocess/context/20_bugs.md` with: symptom, root cause, causal chain,
fix commit SHA, FIX-NN ID, and priority.

### Continuous writeback during implementation

When changes to the planned architecture or features become necessary
during implementation, write back IMMEDIATELY:

**For every deviation from the plan:**

```
Change during implementation:

WHAT: {what changed}
WHY: {why it was necessary}
AFFECTED ARTIFACTS:
- {ADR-XXX}: {what to adjust}
- {FEATURE-XXX}: {what to adjust}

Should I write these changes back now? [Y/N]
```

**Triggers for writeback:**
- A technical decision deviates from an ADR
- A Success Criterion isn't implementable as specified
- New pattern or new dependency introduced
- Scope change (feature larger/smaller than planned)
- Unexpected constraint discovered

**What gets written back:**
- ADR: Decision, Status, Implementation Notes
- FEATURE: Success Criteria, Technical NFRs, Definition of Done
- plan-context.md: Tech Stack, Integrations (if fundamentally changed)
- arc42: affected sections (if architecture changes)

---

## Phase 4: Completion -- Final Synchronization

After implementation, final checks and writeback.

### Phase 4a: Verification gate before completion

Before `/coding` declares a task or the whole implementation as done, the
following gate function must run. This rule holds regardless of how
confident the agent is.

**The rule:** No completion claims without fresh verification evidence.

If the agent hasn't run the verification command in this message, it cannot
claim the task is successful.

**The gate function (5 steps, all mandatory):**

1. **Identify:** Which command proves the claim?
   - "Tests pass" -> concrete test command with path
   - "Build works" -> concrete build command
   - "Bug fixed" -> test that reproduces the original symptom
2. **Run:** Execute the command fully -- not cached, not partial
3. **Read:** Read the complete output, check exit code, count failures
4. **Verify:** Does the output confirm the claim?
   - No -> report actual status with evidence
   - Yes -> formulate the claim with evidence
5. **Claim:** Only now state the status

**Forbidden language without fresh verification:**
- "should work", "probably okay", "looks good"
- "tests should be green now"
- "the change should fix the bug"
- Any statement implying success without running the command

**Common failures -- what is not enough:**

| Claim | Sufficient proof |
|---|---|
| Tests pass | Test command output with 0 failures |
| Linter clean | Linter output with 0 errors |
| Build works | Build command with exit code 0 |
| Bug fixed | Test reproducing the original symptom passes |
| Subagent done | VCS diff shows the expected changes |
| Requirements met | Line-by-line checklist against the plan |

### Phase 4b: Regression test cycle (for bug fixes)

Every bug fix goes through this 6-step cycle to prove the regression test
actually catches the regression:

1. **Write the regression test** reproducing the bug behavior
2. **Run 1:** Run the test -- it MUST pass (because the fix is already in)
3. **Temporarily revert the fix** (`git stash` or code revert)
4. **Run 2:** Run the test -- it MUST FAIL
   - If it passes: the test isn't catching the bug, fix the test
5. **Restore the fix** (`git stash pop` or code restore)
6. **Run 3:** Run the test -- it MUST pass again

Only when all three runs return the expected result is the bug marked as
resolved and the regression test marked as valid.

**Documentation:** The entry in `_devprocess/context/20_bugs.md` gets a
note: "Regression test verified via red-green cycle on {date}".

### Mid-course bug discovery (binding trigger)

If a NEW bug surfaces while implementing the current plan (not in
the original feature specs, ADRs, or FIX-list), the coding flow
MUST pause and route through the artefact layer BEFORE writing the
fix. Skipping this step leaks code changes without backlog trace.

```
Mid-course handling, do NOT fix the bug silently:

1. STOP the current code edit. Do not write the fix yet.
2. Triage:
   - Is this a BUG in shipped code?         -> create BUG-NNN
   - Is this a missing requirement in plan? -> create FEATURE-NNNN
   - Is this a design gap?                  -> amend ADR / arc42
3. Write a minimal root-cause analysis in _devprocess/analysis/
   (3-10 lines is fine: problem, cause, fix direction, risk)
4. Add the new item to _devprocess/context/10_backlog.md under
   the active Epic so it appears in the backlog before any code
   touches disk
5. NOW write the fix. Commit message cites BOTH the in-progress
   FEATURE-NNNN and the new BUG-NNN (e.g.
   `Refs: FEATURE-0507, BUG-018`)
6. After the fix: run the standard Final synchronization block
   below, marking the new BUG-NNN as resolved
```

Why this matters: BUG-017 (tool_use pairing) and BUG-018 (plugin
routing) were found during Obsilo v2.5.0 beta testing. Without
this trigger they got fixed in code first and documented only
after release, the backlog then drifted from the code state for
days.

### Mid-course design discovery (binding trigger)

If the implementation reveals that an architectural decision does not
match reality (ADR says X, the codebase proves Y works better, or the
constraints the ADR relied on turned out to be wrong), pause the
coding flow and route through the architecture layer BEFORE continuing
the feature. Silent design drift is worse than a bug: the ADR keeps
claiming a state of the world that no longer exists.

```
Mid-course handling for a design finding, do NOT silently deviate:

1. STOP the current code edit. Do not keep coding around the
   mismatched ADR.
2. Triage:
   - Can the ADR be amended with a small correction?
     -> update ADR, keep status "Accepted (modified)"
   - Is the original decision wrong at the root?
     -> supersede ADR: old one becomes "Superseded by ADR-NNN",
        new ADR captures the actual decision
   - Does the discovery only clarify wording, not decision?
     -> update ADR Context or Consequences in place
3. Write a root-cause entry in _devprocess/analysis/ADR-{NNN}-review.md
   (3-10 lines: what the ADR claimed, what the code proves, what
   changes, what still holds)
4. Update arc42.md and plan-context.md if the discovery affects
   either. Keep them consistent with the ADR change.
5. Only NOW resume or rewrite the code. Commit message cites the ADR
   change alongside the in-progress FEATURE
   (e.g. `Refs: FEATURE-0507, ADR-012 (amended)`)
6. After the fix: run the standard Final synchronization block
   below. The amended or superseded ADR is part of the writeback.
```

Why this matters: an ADR that silently diverges from the code stops
being a decision record and becomes a historical fiction. The next
reviewer who consults it makes worse decisions because they trust a
document that no longer reflects reality.

### Final synchronization (cross-artifact)

After implementation is verified, check:

```
MANDATORY -- artifacts must reflect the actual state:

1. Feature specs:
   - Status -> "Implemented"
   - Add How-It-Works section (key files, dependencies)
   - Mark Success Criteria as verified (or adjusted if changed)
   - Explicitly document unimplemented criteria with reason

2. ADRs:
   - All statuses finalized (Accepted / Accepted (modified) / Deprecated)
   - Add Implementation Notes with the actual outcome
   - Document deviations from the original proposal

3. Backlog (single source of truth for project state):
   - Update _devprocess/context/10_backlog.md per the binding format
     in skills/requirements-engineering/templates/BACKLOG-TEMPLATE.md
   - For each BL-NNN implemented: set Status -> Done, add commit SHA,
     entry stays with its Epic
   - Add new findings (chores, tech debt, follow-ups) as new rows in
     the matching Epic section or Standalone Items
   - Refresh dashboard counts (status + priority) and "Letztes Update"
   - **Per-commit gate (binding):** The backlog MUST reflect the
     post-implementation state BEFORE every commit that references
     a FEATURE-NNNN or BUG-NNN. Stricter than "before handoff
     ritual" because phase-end writeback drifts when phases stretch
     across multiple commits or when new bugs appear mid-phase.
   - **Commit message must cite the artefacts it touches:**
     `Refs: FEATURE-0409, BUG-013` (or similar). This creates a
     searchable trail from code back to backlog, so a future
     verification query `git log --grep="FEATURE-0409"` lists every
     commit that claimed to move that item forward.

4. Bug log:
   - All FIX-NN entries in _devprocess/context/20_bugs.md updated
     (Status=resolved with commit SHA, regression test verified)

5. Metrics (signal layer):
   - Append a row to _devprocess/context/40_metrics.md under the
     "Cycle time per FEATURE" table for each FEATURE that reached
     Status=Implemented this session
   - Columns: FEATURE ID, Started (first commit with Refs:FEATURE-NNNN),
     Completed (latest commit with Refs:FEATURE-NNNN), Cycle time,
     Scope, Notes
   - Append a row to "Phase transition counts" under "Coding -> Testing"
     (or the next phase) if this session ended a phase
   - Append a row to "Cross-phase trigger counts" for every
     mid-course trigger that fired during this session

IF APPLICABLE:
6. plan-context.md: update if tech stack has changed
7. arc42: update affected sections
8. memory/MEMORY.md: if architecture key facts have changed
9. CLAUDE.md: if new project conventions emerged
```

### Completion summary

```
Implementation complete!

Artifact status:
- {N} Features updated (Status: Implemented)
- {N} ADRs finalized ({N} accepted, {N} modified, {N} deprecated)
- {N} artifacts written back during implementation
- {N} bugs in 20_bugs.md (resolved: {N}, open: {N})
- Backlog updated

Deviations from the original design:
- {summary of most important changes, or "None"}
```

---

## Handoff Ritual (mandatory at end of phase)

`/coding` always runs this ritual at the end, regardless of how it was
started (directly or via `/v-model-workflow`).

### Part 1: Artifact report

List all artifacts produced or updated with full paths:

```
Produced / updated:
- src/{files}: {summary}
- _devprocess/requirements/features/FEATURE-*.md: {status updates}
- _devprocess/architecture/ADR-*.md: {status and implementation notes}
- _devprocess/requirements/handoff/plan-context.md: {tech stack updates if any}
- _devprocess/context/20_bugs.md: {FIX-NN entries}
- _devprocess/context/10_backlog.md: {new/resolved items}
```

### Part 2: Handoff context

Append a new entry to `_devprocess/context/30_handoffs.md` with:

- Summary of what was implemented
- Deviations from plan (with references to the updated ADRs/Features)
- Bugs found and their FIX-NN IDs (resolved and open)
- Open concerns for testing or security phase
- Assumptions that were made and should be verified

### Part 3: Transition question

Ask the user:

> "Implementation is complete. The next step in the V-Model is `/testing`
> with input from the new code plus the updated FEATURE specs.
>
> Shall I start `/testing` now, or would you like to review first?"

**On agreement** ("yes" / "go" / "next") or when running inside
`/v-model-workflow`:
-> Start `/testing` and pass the handoff context

**On rejection** ("no" / "stop" / "I want to check first"):
-> Pause and wait for user instruction

---

## Core principle: Living Documents

The artifacts (ADRs, Features, plan-context.md, arc42) are NOT one-off
specifications. They are continuously updated and always reflect the
actually-implemented state at the end.

```
Design -> Review (corrections) -> Implementation (running updates) -> Final Sync
   ^              |                        |                                  |
   |              v                        v                                  v
   |         Artifacts              Artifacts                          Artifacts
   |         adjusted               adjusted                           finalized
   |                                                                        |
   +------ Documentation == Code (always in sync) <------------------------+
```

## Keywords
Implement, code, build, plan-context, feature realization, review,
task breakdown, TDD, debugging, verification gate, regression test,
living documents, handoff, writeback
