# Feature: {Name}

> **Feature ID**: FEATURE-{EPIC}-{NNN} (epic-local: `EPIC` = 3-digit
> epic number identical to the parent epic's filename number,
> `NNN` = 3-digit feature counter inside the epic)
> **Epic**: EPIC-{NNN} - {Link}
> **Backlog ID**: BL-{NNN} (link from `_devprocess/context/10_backlog.md`)
> **Priority**: [P0-Critical / P1-High / P2-Medium]
> **Effort Estimate**: [S / M / L]

## Feature Description

{1-2 paragraphs: What is the feature and why is it needed?}

## Benefits Hypothesis

**We believe that** {description of the feature}
**Delivers the following measurable outcomes:**
- {Outcome 1 with metric}
- {Outcome 2 with metric}

**We know we are successful when:**
- {Success metric 1}
- {Success metric 2}

## Jobs to be Done (from BA)

> Reference: BA Section 5.4. Forms the foundation for user stories.
> Each prioritized job should be addressed in at least one user story.

| Job Type | Job | Addressed in Story |
|----------|-----|-------------------|
| Functional | {What does the user want to accomplish concretely?} | Story {N} |
| Emotional | {How does the user want to feel?} | Story {N} |
| Social | {How does the user want to be perceived?} | Story {N} |

## User Stories

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

## Success Criteria (Tech-Agnostic)

> NO technology terms! See references/tech-agnostic-rules.md
> Technical details belong in "Technical NFRs" below.

| ID | Criterion | Target | Measurement |
|----|-----------|--------|-------------|
| SC-01 | {User-outcome based} | {Target value} | {How to measure} |
| SC-02 | {Behavior, not implementation} | {Target value} | {How to measure} |
| SC-03 | {Performance as user experience} | {Target value} | {How to measure} |

---

## Technical NFRs (for Architect) -- TECHNOLOGY OK

> This section MAY contain technical details!

### Performance
- **Response Time**: {X ms for Y% of requests}
- **Throughput**: {X requests/second}
- **Resource Usage**: {Max CPU/Memory}

### Security
- **Authentication**: {OAuth 2.0, JWT, etc.}
- **Authorization**: {RBAC, ABAC}
- **Data Encryption**: {At rest: AES-256, In transit: TLS 1.3}

### Scalability
- **Concurrent Users**: {X simultaneous users}
- **Data Volume**: {Y GB/TB}
- **Growth Rate**: {Z% per year}

### Availability
- **Uptime**: {99.9% = ~8.7h downtime/year}
- **Recovery Time Objective (RTO)**: {X minutes}
- **Recovery Point Objective (RPO)**: {X minutes}

---

## Architecture Considerations

### Architecturally Significant Requirements (ASRs)

**CRITICAL ASR #1**: {Description}
- **Why ASR**: {Rationale}
- **Impact**: {Which architecture decisions does this affect?}
- **Quality Attribute**: {Performance / Security / Scalability / etc.}

**MODERATE ASR #2**: {Description}
- **Why ASR**: {Rationale}
- **Impact**: {Influence}
- **Quality Attribute**: {Attribute}

### Constraints
- **Technology**: {Must be X because...}
- **Platform**: {Cloud provider X because...}
- **Compliance**: {GDPR, HIPAA, etc.}

### Open Questions for Architect
- {Technical decision}
- {Architecture pattern question}

---

## Definition of Done

### Functional
- [ ] All user stories implemented
- [ ] All success criteria met (verified)

### Quality
- [ ] Unit tests (coverage > {X}%)
- [ ] Integration tests passed
- [ ] Security scan passed
- [ ] Performance tests passed

### Documentation
- [ ] Feature spec updated (Status: Implemented)
- [ ] Backlog updated (`10_backlog.md`: BL-NNN row set to `Done`,
      commit SHA added, dashboard counts refreshed)

---

## Hypothesis Validation (if applicable)

> Only fill in if this feature validates a critical hypothesis from the BA.
> Reference: BA Section 7.3, Epic Section "Critical Hypotheses"

| Hypothesis (BA Ref) | Test Method | Success Criterion | Result |
|--------------------|-------------|-------------------|--------|
| H-{XX}: {Hypothesis} | {How is it tested?} | {When is it validated?} | {Open / Validated / Disproven} |

**If disproven:** {What is the pivot plan? What alternative?}

---

## Dependencies
- **{Dependency 1}**: {Feature/System}, {Impact if delayed}

## Assumptions
- {Assumption 1}

## Out of Scope
- {Explicitly not part of this feature}
