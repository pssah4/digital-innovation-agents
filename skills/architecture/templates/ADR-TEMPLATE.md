<!--
Instructions for the agent: produce this file as
`_devprocess/architecture/ADR-{nn}-{slug}.md`. Write the prose in the
user's working language. Keep section names (Context, Decision,
Consequences, etc.) in English so the file greps consistently across
projects.

Hard rule: NO code paths in the core sections (Context, Decision
Drivers, Considered Options, Decision, Consequences). Code paths,
file names, line numbers, and method signatures belong in the
optional `## Implementation Notes` appendix at the bottom, which is
explicitly allowed to go stale. The wayfinder
(`src/ARCHITECTURE.map` plus JSDoc headers) is the source of truth
for current paths.

Status, phase, last-change, and claim live in the backlog row for
this ADR in `_devprocess/context/BACKLOG.md`. The frontmatter
below carries identity and relations only.
-->

---
id: ADR-{nn}
title: {short title}
date: {YYYY-MM-DD}
deciders: [{stakeholder1}, {stakeholder2}]
asr-refs: []
feature-refs: []
related-adrs: []
supersedes: null
superseded-by: null
---

# ADR-{nn}: {Title}

## Context

{Description of the problem and its context. State the architectural
question, not the implementation.}

**Triggering ASR:**
- {ASR reference from a feature spec}
- Quality attribute: {Performance / Security / Scalability / etc.}

## Decision drivers

- {Driver 1}: {description}
- {Driver 2}: {description}
- {Driver 3}: {description}

## Considered options

### Option 1: {Name}

{Description.}

- Pro: {advantage}
- Pro: {advantage}
- Con: {disadvantage}

### Option 2: {Name}

{Description.}

- Pro: {advantage}
- Con: {disadvantage}
- Con: {disadvantage}

### Option 3: {Name}

{Description.}

- Pro: {advantage}
- Con: {disadvantage}

## Decision

**Proposed option:** {Option Name}

**Reasoning:**
{Why this option is the best fit. One to three sentences.}

**Note:** This is a PROPOSAL. The /coding skill makes the final call
based on the real codebase state.

## Consequences

### Positive

- {positive consequence 1}
- {positive consequence 2}

### Negative

- {negative consequence 1}
- {trade-off 1}

### Risks

- {risk 1}: {mitigation}

## Related decisions

- ADR-{nn}: {related decision}

## References

- {external reference 1}
- {feature reference}

---

## Implementation Notes (optional, may go stale)

> This appendix is allowed to go stale after refactoring. The
> wayfinder (`src/ARCHITECTURE.map` plus the JSDoc header of the
> entry-point file) is the source of truth for current paths. The
> /consistency-check skill does NOT verify the contents of this
> section.

{First rough hint at where the implementation will land. File paths,
module names, or sketch code can appear here. The PLAN-{nn} file
carries the real, currently-valid task list with up-to-date paths.}
