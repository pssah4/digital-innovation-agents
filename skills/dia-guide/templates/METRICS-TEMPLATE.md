# Metrics for {PROJECT}

> Lightweight signal layer for the V-Model workflow. Every phase-skill
> appends to this file during its Handoff Ritual. No separate metrics
> ceremony, no external dashboard. Readers check the file to tell
> whether the system is pulsing in the right direction or just moving
> fast somewhere else.

**Last update:** {YYYY-MM-DD}

## Cycle time per FEATURE

> How long each FEATURE spent from `Status: Ready` to
> `Status: Done`. Derived from commit timestamps using the
> `Refs: FEAT-NN-NN` cite. The `/coding` skill updates this during
> its Final synchronization block.

| FEATURE | Started | Completed | Cycle time | Scope | Notes |
|---|---|---|---|---|---|
| FEAT-01-01 | 2026-04-19 | 2026-04-20 | 1d 3h | PoC | Signal-Layer itself |

## Drift count (plan-context.md vs. real code)

> Number of items the `/coding` codebase reconciliation flagged as
> "plan-context.md claims X, the code shows Y". A rising drift count
> signals that the ADRs or plan-context are losing touch with reality.
> `/coding` writes this after every Phase 2a (codebase reconciliation).

| Date | ADR count | arc42 section count | plan-context item count | Drift flagged | Drift resolved | Open |
|---|---|---|---|---|---|---|
| 2026-04-19 | 5 | 8 | 12 | 0 | 0 | 0 |

## BA hypothesis validation status

> Status per Critical Hypothesis from `_devprocess/analysis/BA-{PROJECT}.md`
> Section 7.3. The `/business-analysis` skill updates this after
> Phase 8 (Post-Release Review) or during any re-validation session.
> Status values: `Validated` (by reasoning), `Confirmed by usage`,
> `Contradicted by usage`, `Inconclusive`.

| Hypothesis | Status | Evidence | Last checked |
|---|---|---|---|
| H-01 | Validated | Placeholder until first post-release review | 2026-04-19 |

## Phase transition counts

> Number of times each phase handoff fired. Useful to see whether the
> workflow is actually being followed or whether people jump straight
> to coding. Phase skills update this row themselves during their
> Handoff Ritual; `/dia-guide` only reads it.

| Transition | Count | Last fired |
|---|---|---|
| BA -> RE | 0 | never |
| RE -> Architecture | 0 | never |
| Architecture -> Coding | 0 | never |
| Coding -> Testing | 0 | never |
| Testing -> Security Audit | 0 | never |
| Security Audit -> Release | 0 | never |
| (mid-course) Coding -> bug trigger | 0 | never |
| (mid-course) Coding -> design trigger | 0 | never |
| (mid-course) Architecture -> requirements trigger | 0 | never |

## Cross-phase trigger counts

> How often each cross-phase feedback trigger fired and where it
> landed. Rising counts on a single trigger type hint at a weak
> upstream phase. For example, many mid-course requirements
> discoveries suggest that `/requirements-engineering` is leaving
> gaps that `/architecture` has to catch.

| Trigger | Count | Rooted in phase |
|---|---|---|
| Mid-course bug | 0 | n/a |
| Mid-course design | 0 | n/a |
| Mid-course requirements | 0 | n/a |

## Reading the signals

- **Rising cycle time** without scope increase suggests the team is
  fighting drift. Check the drift-count table.
- **Rising drift count** means ADRs and plan-context are falling
  behind the code. Trigger a reconciliation run.
- **Hypothesis status stuck at Validated forever** means no
  post-release review happened. Invoke `/business-analysis` Post-Release
  Review.
- **Phase transitions all zero on a feature that got built** means
  the workflow got skipped. The backlog entry should record why.

This file is additive. Rows are never deleted. When a cell becomes
stale, a new row gets appended with the same FEATURE ID or date.
