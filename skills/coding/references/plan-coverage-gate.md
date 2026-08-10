# Plan Coverage Gate (binding, runs before Status flips to In Progress)

Regardless of which agent produced the plan, the skill checks four
things against the source artifacts. The check happens AFTER the plan
body is persisted and BEFORE implementation begins. If any item fails,
the flow loops: update the affected artifact, then re-run the gate.
No code is written while an item is open.

1. **SC coverage.** Every Success Criterion from every referenced
   FEATURE spec either maps to a concrete task in the plan or is
   explicitly marked "Deferred: {reason}" in the plan body.
   - Gap found -> two options:
     (a) add task(s) to the plan body (agent decides shape), or
     (b) amend the FEATURE: remove / split / reword the SC, with
     justification. Every FEATURE amendment gets a one-line comment
     explaining the change.
2. **ADR alignment.** Every ADR listed in `adr-refs` has at least one
   task that operationalizes its Decision section.
   - Gap found -> either add a task, or route through the mid-course
     `design` trigger (the ADR itself may be wrong).
3. **Codebase anchoring.** Every task names at least one concrete file
   path (Create / Modify / Test). Abstract tasks like "clean up state
   management" fail the gate until they name files.
4. **Verification gates.** The plan body contains at least one build
   command and one test command that prove the plan done. If the repo
   has no tests yet, a smoke script is acceptable; the plan names it.

On completion: add a short `## Coverage Gate` block at the bottom of
the plan body (before `## Change Log`) listing which SC mapped to
which task, which SC got deferred, and which ADRs got touched. This
block is what a later reviewer (human or agent) reads to verify the
gate actually ran.

**Re-run the gate whenever a source artifact changes.** If a FEATURE,
ADR, or plan-context.md is amended while a PLAN is In Progress (from
codebase reconciliation, mid-course triggers, or external edits), the
Coverage Gate runs again on that PLAN before the next code edit. Log
the re-run as a Change Log entry with trigger=coverage and the
amended artifact ID.
