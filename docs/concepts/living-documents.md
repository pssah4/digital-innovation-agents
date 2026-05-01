---
title: Living Documents
description: ADRs, Features, and architecture docs update themselves during and after implementation so documentation always reflects the actual state.
---

# Living Documents

Most software documentation is a snapshot: written once at design time,
then slowly drifts out of sync with the code. By the time someone reads
it, half of it is wrong. Digital Innovation Agents treats documentation
as living documents instead. Artifacts update themselves during and
after implementation so they always reflect the actual state.

## The pattern

```
Design -> Review (corrections) -> Implementation (running updates) -> Final Sync
   ^              |                        |                                  |
   |              v                        v                                  v
   |         Artifacts              Artifacts                          Artifacts
   |         adjusted               adjusted                           finalized
   |                                                                        |
   +------ Documentation == Code (always in sync) <------------------------+
```

The loop runs three times per V-Model cycle:

1. **Design to review.** Phase 2 creates Features, Phase 3 creates
   ADRs. Phase 4 opens with a Critical Review that reconciles them
   against the real codebase. Discrepancies are written back into the
   source files before any implementation.
2. **Implementation to running updates.** During Phase 4
   implementation, whenever a technical decision deviates from an ADR,
   or a Success Criterion cannot be met as specified, or a new
   dependency is introduced, the affected artifact is updated
   immediately.
3. **Completion to final sync.** Phase 4 ends with a final
   synchronization step. All Features get `Status: Implemented`, all
   ADRs get `Implementation Notes`, the backlog is updated, the bug
   log is cross-referenced with commit SHAs.

## What gets written back

| Artifact | What gets updated |
|---|---|
| `_devprocess/context/BACKLOG.md` | The single source of truth. Rows for `FEAT-{ee}-{ff}`, `FIX-{ee}-{ff}-{nn}`, `IMP-{ee}-{ff}-{nn}`, `PLAN-{nn}`, `ADR-{nn}` carry status, phase, last-change, claim, commit SHA. Status changes go HERE FIRST, then the artifact body |
| Feature specs | Substance only: Success Criteria verification, hypothesis updates, scope clarifications, optional `## Code Pointer` appendix referencing an ARCHITECTURE.map concept. No status fields in frontmatter |
| ADRs | Substance only: amendments to Decision Drivers / Considered Options / Decision / Consequences. Optional `## Implementation Notes` appendix may carry stale code-level hints. Status lives in the backlog row |
| FIX detail files | Causal chain (Problem, Root Cause, Chain), regression test reference. Commit SHA and status live in the backlog row |
| Wayfinder (`src/ARCHITECTURE.map`) | Concept rows when an entry-point is created or renamed. JSDoc headers in the entry-point file. Module READMEs |
| Rule sets (`_devprocess/rules/*.md`) | Stable truths, hard cap 500 lines total. Updated when stack, conventions, or domain glossary actually change |
| `plan-context.md` | Tech stack (if changed), integrations, updated performance / security values |
| arc42 | Affected sections when architecture shifts |
| `_devprocess/context/METRICS.md` | Cycle time per FEAT, drift count, hypothesis status, phase transitions, cross-phase trigger counts. Append-additive, written from inside existing phase actions |
| `memory/MEMORY.md` | When architecture key facts change |
| `CLAUDE.md` | When new project conventions emerge |

## Backlog row first, artifact body second

The v3 three-layer model says state lives in one place: the backlog
row. That includes status, phase, last-change date, claim, and
commit SHA. The artifact body holds substance only: problem,
decision, success criteria, reasoning. A status change touches the
backlog row first, then the artifact, never the other way around.
This is the structural fix for the most common drift class (status
fields stuck at "Planned" while the code shipped). See the
[Three-layer documentation model](./three-layer-documentation).

## Why write back before implementation?

The Critical Review in Phase 4 catches the most expensive category of
design mistakes: proposals that do not match reality. ADRs written in
Phase 3 are proposals. The architect does not yet know exactly what
the codebase looks like. When `/coding` reads the codebase and finds
that ADR-003 contradicts an existing pattern, updating the ADR before
implementing is cheaper than writing code to the wrong ADR and fixing
both later.

The same applies when a Feature's Success Criterion is found to be
impossible under the real constraints. Better to update the Feature now
than to ship code that does not match the spec.

## Why write back during implementation?

When implementation reveals an unexpected constraint (for example, a
library does not support a required feature, or a pattern needs to
change to fit the existing code), the running updates capture that
decision immediately. Without the running writeback, these decisions
live in the developer's head (or the PR description) and vanish when
the session ends.

## Why the final sync?

At the end of Phase 4, every artifact is verified one last time. This
is the moment where the cycle promises "documentation equals code". If
a Feature is marked `Implemented` but three of its Success Criteria
were quietly dropped, the final sync catches it and forces an explicit
decision: either the criteria are genuinely met, or they are removed
from the Feature with a reason.

## Integration with the Closing Handoff

The Closing Handoff (after a green `/security-audit`) calls
`/consistency-check` mode B for a cross-phase final synchronization
covering BA, Features, ADRs, arc42, and `plan-context.md`. This is
the last checkpoint before any release act. If the BA's Validation
section has measurable numbers that can now be filled in (for
example, "reduced retro cycle time by 40%"), mode B surfaces the
gap so the BA gets updated.

## The opposite: dead documentation

In many teams, documentation lives in Confluence or a wiki, separate
from the code. That is dead documentation. No writeback, no
synchronization, no integration with the development cycle. It drifts.

Living documents are in the repo, update with the code, and are
enforced by the skills at every phase. Drift is actively prevented.

## Rules of thumb

- **If it affects the design, write it back.** A deviation during
  implementation is a signal to update the ADR or Feature.
- **If you cannot update the artifact, push back.** When the agent is
  not sure whether to write back, it asks the user.
- **The final sync is non-negotiable.** Phase 4 does not close without
  it.
- **Backlog is a living document too.** Every V-Model cycle updates it,
  not just manual housekeeping.

## See also

- [V-Model concept](./v-model): the cycle shape
- [Handoff Rituals](./handoff-rituals): how phases hand off living artifacts
- [Coding guide](../guides/coding): Phase 4 where most writebacks happen
