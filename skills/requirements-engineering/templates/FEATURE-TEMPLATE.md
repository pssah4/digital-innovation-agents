<!-- See skills/requirements-engineering/SKILL.md for how to fill -->

---
id: FEAT-{ee}-{ff}
title: {short title}
epic: EPIC-{nn}
subtype: user-facing  # user-facing | library
priority: P2          # P0 | P1 | P2
effort: M             # XS | S | M | L | XL
---

# Feature: {Name}

## Feature description

{One paragraph: what is the feature and why is it needed?}

## User stories

| Role | Want | So that | Job type |
|------|------|---------|----------|
| {role} | {capability} | {outcome} | functional |
| {role} | {capability} | {outcome} | emotional |
| {role} | {capability} | {outcome} | social |

## Success criteria

Tech-agnostic. See skills/project-conventions/SKILL.md#canonical-specs (Writing style).

| ID    | Criterion           | Target          | Measurement       |
|-------|---------------------|-----------------|-------------------|
| SC-01 | {user outcome}      | {target value}  | {how to measure}  |
| SC-02 | {behavior}          | {target value}  | {how to measure}  |

## Non-functional requirements

Populated rows only. Omit the section if nothing is binding.

| Category     | Target                       | Notes              |
|--------------|------------------------------|--------------------|
| Performance  | {response time, throughput}  | {context}          |
| Security     | {authn/authz, encryption}    | {context}          |
| Scalability  | {concurrent users, volume}   | {context}          |
| Availability | {uptime, RTO, RPO}           | {context}          |

## Architecturally Significant Requirements

| ID     | Classification     | Constraint            | Quality attribute |
|--------|--------------------|-----------------------|-------------------|
| ASR-01 | CRITICAL | MODERATE | {what must hold}      | {attribute}       |

## Activation Path

- Type: command | route | UI-element | endpoint | scheduled-job | tool | hotkey | public-API
- Identifier: `{command name | route path | URL | symbol name}`
- Where it lives: {file or section pointer, or ARCHITECTURE.map concept}
- How a user (or caller) reaches it: {one sentence}

## Definition of Done

- [ ] All user stories implemented and success criteria verified
- [ ] Activation Path trigger or symbol exists in code
- [ ] Backlog row updated to `Done` with commit SHA recorded
- [ ] ARCHITECTURE.map updated if a new entry-point landed
