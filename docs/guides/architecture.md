---
title: Architecture
description: Transform requirements into Architecture Decision Records (ADRs), arc42 documentation, and the plan-context bridge.
---

# Architecture

`/architecture` transforms requirements into architecture **proposals**.
The final decisions are made by `/coding` based on the real codebase.

**Input:** Epics, Features, ASRs, NFRs from `/requirements-engineering`
**Output:** ADRs, arc42, plan-context.md

## Key features

- **ADRs in MADR format**: one ADR per Critical ASR. Each ADR must have
  Status, Context with Triggering ASR, at least 2 Decision Drivers,
  at least 2 Considered Options (each with Pros/Cons), a proposed
  Decision with justification, and Consequences (Positive/Negative/Risks)
- **arc42 documentation**: scope-dependent section count (Simple Test:
  Sections 1/3/4. PoC: 1-5/8. MVP: 1-12)
- **plan-context.md**: the context bridge to implementation. Must contain
  Technical Stack, Architecture Style, ADR summary table, Data Model,
  External Integrations, Performance & Security (with concrete numbers)

## Quality gates

- **ADR-ASR Traceability**: every Critical ASR must have an ADR
- **plan-context.md Consistency**: tech stack must match the ADRs
- **No ADR without real alternatives**: "We chose React because it's
  popular" is not acceptable

## Handoff

Ends with the 3-part Handoff Ritual. Next phase: `/coding`. The
handoff context captures tech-stack justification, rejected alternatives
(so `/coding` doesn't reopen them without a fresh reason), and known
risks.

## Read the skill file

[`skills/architecture/SKILL.md`](https://github.com/pssah4/digital-innovation-agents/blob/main/skills/architecture/SKILL.md) on GitHub.
