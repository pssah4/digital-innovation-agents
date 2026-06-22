# Metrics for {PROJECT}

<!-- See skills/dia-guide/SKILL.md for how to fill -->

**Last update:** {YYYY-MM-DD}

## Legend

Status values for hypotheses: `Validated`, `Confirmed by usage`, `Contradicted by usage`, `Inconclusive`.
Backlog status vocabulary: see skills/project-conventions/SKILL.md#canonical-specs (Backlog vocabulary).

## Cycle time per FEATURE

| FEATURE | Started | Completed | Cycle time | Scope | Notes |
|---|---|---|---|---|---|
| FEAT-01-01 | 2026-04-19 | 2026-04-20 | 1d 3h | PoC | Signal-Layer itself |

## Drift count (plan-context.md vs. real code)

| Date | ADR count | arc42 sections | plan-context items | Drift flagged | Drift resolved | Open |
|---|---|---|---|---|---|---|
| 2026-04-19 | 5 | 8 | 12 | 0 | 0 | 0 |

## BA hypothesis validation status

| Hypothesis | Status | Evidence | Last checked |
|---|---|---|---|
| H-01 | Validated | Placeholder until first post-release review | 2026-04-19 |

## Transitions and triggers

| Transition or trigger | Count | Last fired or rooted in |
|---|---|---|
| BA -> RE | 0 | never |
| RE -> Architecture | 0 | never |
| Architecture -> Coding | 0 | never |
| Coding -> Testing | 0 | never |
| Testing -> Security Audit | 0 | never |
| Security Audit -> Release | 0 | never |
| Mid-course: Coding -> bug | 0 | n/a |
| Mid-course: Coding -> design | 0 | n/a |
| Mid-course: Architecture -> requirements | 0 | n/a |

## Reading the signals

- Rising cycle time without scope increase: team is fighting drift, check the drift-count table.
- Rising drift count: ADRs and plan-context fall behind code, trigger a reconciliation run.
- Hypothesis stuck at `Validated`: no post-release review happened, invoke `/business-analysis` Post-Release Review.
- All phase transitions zero on a shipped feature: workflow got skipped, the backlog entry should record why.
