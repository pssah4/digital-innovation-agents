<!--
Instructions for the agent: produce this file as
`_devprocess/requirements/features/FEAT-{ee}-{ff}-{slug}.md`.
Write the prose in the user's working language. Keep section names
(Feature description, Success criteria, etc.) in English so the file
greps consistently across projects.

Hard rule: NO `status:` field in frontmatter. Status, phase, last-change,
and claim live in the backlog row for this feature in
`_devprocess/context/BACKLOG.md`. The frontmatter carries identity,
parent epic, and relations only.

Hard rule: NO `## How It Works`, `## Key Files`, or `## Source` sections
that list current code paths. These age silently and become drift. The
wayfinder (`src/ARCHITECTURE.map` plus JSDoc headers) is the source of
truth for current paths. If a code pointer is needed, use the optional
`## Code Pointer` appendix at the bottom and reference an ARCHITECTURE.map
concept name, not a file path.
-->

---
id: FEAT-{ee}-{ff}
title: {short title}
epic: EPIC-{nn}
subtype: user-facing  # user-facing | library
priority: {P0 | P1 | P2}
effort: {S | M | L}
asr-refs: []
adr-refs: []
depends-on: []
created: {YYYY-MM-DD}
---

# Feature: {Name}

> Backlog row: `_devprocess/context/BACKLOG.md` -> FEAT-{ee}-{ff}
> (status, phase, claim, last-change live there).

## Feature description

{1 to 2 paragraphs: what is the feature and why is it needed?}

## Benefits hypothesis

**We believe that** {description of the feature}
**delivers the following measurable outcomes:**

- {outcome 1 with metric}
- {outcome 2 with metric}

**We know we are successful when:**

- {success metric 1}
- {success metric 2}

## Jobs to be Done (from BA)

> Reference: BA Section 5.4. Each prioritized job should be addressed
> in at least one user story.

| Job type   | Job                                                  | Addressed in story |
|------------|------------------------------------------------------|--------------------|
| Functional | {what does the user want to accomplish concretely?}  | Story {N}          |
| Emotional  | {how does the user want to feel?}                    | Story {N}          |
| Social     | {how does the user want to be perceived?}            | Story {N}          |

## User stories

### Story 1: {Name} (Functional Job)

**As a** {user role}
**I want to** {functionality}
**so that** I can accomplish {functional job}

### Story 2: {Name} (Emotional Job)

**As a** {user role}
**I want to** {functionality}
**so that** I experience {desired feeling/experience}

### Story 3: {Name} (Social Job)

**As a** {user role}
**I want to** {functionality}
**so that** I am perceived as {external perception}

---

## Success criteria (tech-agnostic)

> No technology terms. See references/tech-agnostic-rules.md.
> Technical details belong in "Technical NFRs" below.

| ID    | Criterion                            | Target          | Measurement       |
|-------|--------------------------------------|-----------------|-------------------|
| SC-01 | {user-outcome based}                 | {target value}  | {how to measure}  |
| SC-02 | {behavior, not implementation}       | {target value}  | {how to measure}  |
| SC-03 | {performance as user experience}     | {target value}  | {how to measure}  |

---

## Technical NFRs (for the architect): technology terms allowed

> This section MAY contain technical detail.

### Performance

- Response time: {X ms for Y% of requests}
- Throughput: {X requests/second}
- Resource usage: {max CPU/memory}

### Security

- Authentication: {OAuth 2.0, JWT, etc.}
- Authorization: {RBAC, ABAC}
- Data encryption: {at rest: AES-256, in transit: TLS 1.3}

### Scalability

- Concurrent users: {X simultaneous users}
- Data volume: {Y GB/TB}
- Growth rate: {Z% per year}

### Availability

- Uptime: {99.9% = ~8.7h downtime/year}
- RTO: {X minutes}
- RPO: {X minutes}

---

## Architecture considerations

### Architecturally Significant Requirements (ASRs)

**CRITICAL ASR #1:** {description}

- Why ASR: {rationale}
- Impact: {which architecture decisions does this affect?}
- Quality attribute: {Performance / Security / Scalability / etc.}

**MODERATE ASR #2:** {description}

- Why ASR: {rationale}
- Impact: {influence}
- Quality attribute: {attribute}

### Constraints

- Technology: {must be X because...}
- Platform: {cloud provider X because...}
- Compliance: {GDPR, HIPAA, etc.}

### Open questions for architect

- {technical decision}
- {architecture pattern question}

---

## Definition of Done

### Activation Path (mandatory)

> The trigger or public symbol through which this FEATURE is reached.
> See `/requirements-engineering` SKILL.md section "FEATURE subtype
> and Activation Path requirement".
>
> For `subtype: user-facing` -- pick one type and fill it in.
> For `subtype: library` -- fill the public-API entry.

- Type: {command | route | UI-element | endpoint | scheduled-job | tool | hotkey | public-API}
- Identifier: `{command name | route path | URL | symbol name}`
- Where it lives: {file or section pointer, or ARCHITECTURE.map concept}
- How a user (or caller) reaches it: {one sentence}

### Functional

- [ ] All user stories implemented
- [ ] All success criteria met (verified)
- [ ] Activation Path entry above is filled and the trigger or symbol exists in code (verified by `/coding` Phase 4a step 7)
- [ ] New top-level symbols introduced in this FEATURE are reachable from outside the definition file or exported as public API (verified by `/coding` Phase 4a step 6)

### Quality

- [ ] Unit tests (coverage > {X}%)
- [ ] Integration tests passed
- [ ] Security scan passed
- [ ] Performance tests passed

### Documentation

- [ ] Backlog row updated to status `Done`, commit SHA recorded
- [ ] ARCHITECTURE.map updated if a new entry-point landed

---

## Hypothesis validation (if applicable)

> Only fill in if this feature validates a critical hypothesis from the BA.
> Reference: BA Section 7.3, Epic Section "Critical Hypotheses".

| Hypothesis (BA Ref) | Test method | Success criterion | Result |
|---------------------|-------------|-------------------|--------|
| H-{XX}: {hypothesis} | {how is it tested?} | {when is it validated?} | {Open / Validated / Disproven} |

**If disproven:** {what is the pivot plan? what alternative?}

---

## Dependencies

- **{dependency 1}**: {feature/system}, {impact if delayed}

## Assumptions

- {assumption 1}

## Out of scope

- {explicitly not part of this feature}

---

## Code Pointer (optional, may go stale)

> The wayfinder is the source of truth for current paths. Reference
> by ARCHITECTURE.map concept name, not by file path.

ARCHITECTURE.map concept: `{concept-name}` (run
`grep "{concept-name}" src/ARCHITECTURE.map` for the entry-point and
extension pattern).
