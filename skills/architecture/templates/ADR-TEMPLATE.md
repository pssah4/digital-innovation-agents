<!-- See skills/architecture/SKILL.md for how to fill -->
---
id: ADR-{nn}
title: {short title}
date: {YYYY-MM-DD}
kind: constraint | choice | post-hoc
reversal-cost: low | medium | high
applies-to: []
read-when: "{one-line trigger: changing X, adding Y}"
asr-refs: []
feature-refs: []
related-adrs: []
supersedes: null
superseded-by: null
---

# ADR-{nn}: {Title}

<!--
Required sections by kind:
  post-hoc (the default case: decision documented AFTER implementation,
            the post-hoc CDR practice): Context, Decision, Consequences,
            Sources. Considered Options omitted.
  choice   (a real pre-code choice between alternatives): plus
            Decision drivers; Considered Options recommended.
  constraint (pre-decided: compliance, hard-to-reverse): full MADR,
            Considered Options REQUIRED.
`kind` missing = treated as choice (legacy files stay valid).
`applies-to` (domain tags) + `read-when` (trigger phrase) feed the
decisions/README.md router table.

German heading variants recognized by tools/consistency-check.py (A-1):
  ## Context = ## Kontext, ## Decision = ## Entscheidung,
  ## Consequences = ## Konsequenzen, ## Decision drivers = ## Begruendung.
Use one language consistently within one ADR; both are LOCKED anchors.
-->

## Context

{Two to three sentences: the architectural question, the trigger, the
constraint. No code paths (A-1). Triggering ASR: {ref}, quality
attribute {Performance / Security / ...}.}

## Decision drivers

<!-- choice + constraint only -->
{Driver 1}, {Driver 2}, {Driver 3}.

## Considered Options

<!-- REQUIRED for kind: constraint; recommended for choice; omit for post-hoc -->
| Option | Pros | Cons |
| --- | --- | --- |
| {Option 1} | {pro} | {con} |
| {Option 2} | {pro} | {con} |

## Decision

Chosen option: {Option Name}. {One to three sentences on why this fits
the drivers.}

## Consequences

- Positive: {effect}
- Negative: {trade-off}
- Risk: {risk} -> {mitigation}

## Sources

<!-- post-hoc only; code paths ARE allowed here (not an A-1 core
     section). Point at the files that embody the decision. -->
- `{src/path/file.ts}`
- {PR / commit / measurement that grounded the decision}

---

## Implementation Notes

<!-- Optional appendix. Allowed to go stale. Wayfinder is the source of
     truth for current paths. Omit if empty. -->
