<!-- See skills/coding/SKILL.md for how to fill this template. -->
---
id: PLAN-{ee}-{ff}-{nn}
title: {short plan title}
date: {YYYY-MM-DD}
feature-refs: []
adr-refs: []
supersedes: null
superseded-by: null
pair-id: {human-handle}-{model-slug}
---

# PLAN-{ee}-{ff}-{nn}: {title}

{Plan body produced by the coding agent. For Claude Code, paste the
plan-mode output verbatim. See skills/project-conventions/SKILL.md#canonical-specs
(Writing style, Section policy).}

## Coverage Gate

Fill before the backlog row flips to In Progress. One row per Success
Criterion of every referenced FEATURE and per referenced ADR.

| Gate item | Status | Evidence |
|---|---|---|
| FEAT-{ee}-{ff} SC-01 | Mapped / Deferred: {reason} | Task {N} |
| ADR-{ee}-{nn} | Operationalized | Task {N} |
| Verify commands | Defined | `{build cmd}`, `{test cmd}` |

## Change Log

Append-only. Each mid-course deviation appends an entry. Never rewrite
past entries.

## Implementation Notes

Filled when the backlog row reaches Done or Superseded.

- Per-task commit SHAs (short form) or "Not executed because ..."
- Deviations from the original plan
- Test count delta (new / adjusted / removed)
- Cycle time: first commit to last commit
- ARCHITECTURE.map / JSDoc-header updates landed in commits: ...
