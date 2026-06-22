<!-- See skills/requirements-engineering/SKILL.md for how to fill -->

# Architect Handoff for {PROJECT}

**Author:** {Requirements Engineer} | **Target release:** {release or sprint}

See skills/project-conventions/SKILL.md#canonical-specs (Reader budget, Writing style, Priority/Effort legend).

## 1. Scope

- Scope: {Simple Test / PoC / MVP}
- Main goal: {from BA Executive Summary}
- Source BA: {path to BA-{PROJECT}.md}

## 2. Architecturally Significant Requirements

| ID | Source FEATURE | Classification | Constraint | Notes |
|---|---|---|---|---|
| ASR-001 | FEAT-01-02 | Critical | {constraint} | {note} |
| ASR-002 | FEAT-01-03 | Moderate | {constraint} | |

## 3. NFR summary

| Category | Target | Source FEATUREs |
|---|---|---|
| Performance (response time p95) | {ms} | FEAT-01-01 |
| Availability | {uptime %} | FEAT-01-03 |
| Scalability (concurrent users) | {N} | FEAT-01-02 |
| Security (authN, authZ, data class) | {list} | all |
| Compliance | {standard} | {features} |

## 4. Constraints

- Stack: {allowed languages, frameworks, prohibited choices}
- Integration: {existing systems, APIs to consume or expose}
- Operational: {deployment target, SRE owner, on-call rotation}
- Team: {skills available, out-of-scope}

## 5. Open Questions

- {open question 1}
- {open question 2}

## 6. Dialog

### Questions from Architect to RE

| ID | Date | Question | Addressed by | Status |
|---|---|---|---|---|
| Q-001 | YYYY-MM-DD | {question} | FEAT-EE-FF SC-NN | Pending |

### Answers from RE

| ID | Date | Answer | Affected artifacts | Status |
|---|---|---|---|---|
| A-001 | YYYY-MM-DD | {answer} | FEAT-EE-FF (SC-NN updated) | Resolved |

## 7. Ready-to-design checklist

- [ ] All Critical ASRs have quantified constraints
- [ ] NFR table has numbers, not adjectives
- [ ] Every FEATURE listed in section 2 or 3
- [ ] Open questions categorized (blocker vs. async)
