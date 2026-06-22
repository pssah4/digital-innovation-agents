<!-- See skills/architecture/SKILL.md for how to fill -->
---
id: ADR-{nn}
title: {short title}
date: {YYYY-MM-DD}
asr-refs: []
feature-refs: []
related-adrs: []
supersedes: null
superseded-by: null
---

# ADR-{nn}: {Title}

<!--
German heading variants recognized by tools/consistency-check.py (A-1 ADR abstraction check):
  ## Context           = ## Kontext
  ## Decision          = ## Entscheidung
  ## Consequences      = ## Konsequenzen
  ## Decision drivers  = ## Begruendung  (also ## Begründung)
  ## Considered Options, ## Implementation Notes: no German variant.
Use either language consistently within one ADR; both are LOCKED anchors.
-->

## Context

{Two to three sentences: the architectural question, the trigger, the constraint. No code paths. Triggering ASR: {ref}, quality attribute {Performance / Security / Scalability / ...}.}

## Decision drivers

{Driver 1}, {Driver 2}, {Driver 3}.

## Considered Options

| Option | Pros | Cons |
| --- | --- | --- |
| {Option 1} | {pro} | {con} |
| {Option 2} | {pro} | {con} |
| {Option 3} | {pro} | {con} |

## Decision

Chosen option: {Option Name}. {One to three sentences on why this fits the drivers.}

## Consequences

- Positive: {effect}
- Negative: {trade-off}
- Risk: {risk} -> {mitigation}

---

## Implementation Notes

<!-- Optional appendix. Allowed to go stale. Wayfinder (src/ARCHITECTURE.map + JSDoc headers) is the source of truth for current paths. consistency-check does NOT verify this section. Omit the entire section if you have nothing to add. -->

{First rough hint at where the implementation will land. The PLAN-{nn} file carries the current task list.}
