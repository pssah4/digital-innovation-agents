# Debugging protocol

When a test fails unexpectedly during implementation, or behavior is
incorrect, or a fix does not work, `/coding` hands this 4-phase
protocol to the coding agent.

**The rule:** No fixes without root-cause investigation.

## Phase A: Root cause (BEFORE any fix attempt)

1. Read the error message completely: stack trace, line numbers, codes
2. Check reproducibility: does it happen every time?
3. Check recent changes: `git diff`, last commits, new dependencies
4. In multi-component systems: add logging at every component boundary
5. Trace the data flow backwards: where does the bad value originate?

## Phase B: Pattern analysis

1. Find working examples in the codebase
2. Read the reference implementation completely (do not skim)
3. List every difference, even ones that seem irrelevant
4. Check dependencies and config assumptions

## Phase C: Hypothesis

1. State one hypothesis: "Root cause is X because Y"
2. Make the smallest possible change to test it
3. One variable at a time
4. If the hypothesis is wrong: form a new one, do not pile fixes

## Phase D: Implementation

1. Write a failing test that reproduces the bug
2. Apply exactly one fix that addresses the root cause
3. Verify: test passes, no regressions elsewhere
4. Document the bug as a FIX artefact:
   - Add a row to `_devprocess/context/BACKLOG.md` under the affected
     Epic with ID `FIX-{ee}-{ff}-{nn}`, status, phase, priority
     (P0/P1/P2), and the commit SHA once the fix lands.
   - Create the detail file at
     `_devprocess/requirements/fixes/FIX-{ee}-{ff}-{nn}-{slug}.md`
     using `templates/FIX-TEMPLATE.md`. The file carries Symptom,
     Root cause (causal chain), Fix, Regression test.

## Phase D.5: Architecture alarm (after 3+ failed fix attempts)

If three or more fix attempts fail to resolve the situation, this is
an architecture problem, not a bug:

- Each fix reveals a new problem in a different place?
- Fixes require massive refactoring?
- Each fix creates new symptoms?

Then STOP. No fourth attempt. Question the pattern fundamentally and
discuss with the user before any more fixes. This is a wrong
architecture, not a failed hypothesis.

**Writeback:** Every bug found, even if the fix is trivial, gets a
BACKLOG row (`FIX-{ee}-{ff}-{nn}`) plus a detail file carrying
symptom, root cause (causal chain), fix description, priority. The
BACKLOG row carries state; the FIX file carries substance.
