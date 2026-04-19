# Architect Handoff for {PROJECT}

> Handoff document from `/requirements-engineering` to `/architecture`.
> Aggregates everything the Architect needs in one place: ASRs, NFR
> summary, constraints, open questions. Also carries a Dialog channel
> back from the Architect to the Requirements Engineer.

**Status:** {Draft / Ready for Architect / Accepted / Superseded}
**Last update:** {YYYY-MM-DD}
**Author:** {Requirements Engineer}

---

## 1. Scope

- **Scope:** {Simple Test / PoC / MVP}
- **Main goal:** {from BA Executive Summary}
- **Target release:** {release or sprint identifier}

## 2. Architecturally Significant Requirements (ASRs)

> Aggregated from every FEATURE. Critical ASRs MUST produce at least
> one ADR. Moderate ASRs get reviewed case by case.

| ID | Source FEATURE | Classification | Constraint | Notes |
|---|---|---|---|---|
| ASR-001 | FEATURE-001-002 | Critical | {constraint} | {note} |
| ASR-002 | FEATURE-001-003 | Moderate | {constraint} | |

## 3. Non-Functional Requirements summary

> Every NFR across the backlog, rolled up. Numbers, not adjectives.

| Category | Target | Source FEATUREs |
|---|---|---|
| Performance (response time p95) | {ms} | FEATURE-001-001, 001-002 |
| Availability | {uptime %} | FEATURE-001-003 |
| Scalability (concurrent users) | {N} | FEATURE-001-002 |
| Security (authN, authZ, data class) | {list} | all |
| Compliance | {standard, e.g. GDPR, SOC2} | {features} |

## 4. Constraints

- **Stack constraints:** {allowed languages, frameworks, prohibited choices}
- **Integration constraints:** {existing systems, APIs to consume or expose}
- **Operational constraints:** {deployment target, SRE owner, on-call rotation}
- **Team constraints:** {skills available, out-of-scope}

## 5. Open Questions

> Gaps or contradictions that the Requirements Engineer could not
> resolve before handoff. The Architect may address them via the
> Dialog section below rather than stalling the handoff.

- {open question 1}
- {open question 2}

## 6. Dialog

> Bidirectional channel between Architect and Requirements Engineer.
> NOT a blocker: the Architect proceeds with the ADRs that do not
> depend on open questions. Pending questions get answered async or
> surfaced to the user at the next phase touchpoint.

### Questions from Architect to RE

| ID | Date | Question | Addressed by | Status |
|---|---|---|---|---|
| Q-001 | 2026-04-19 | {concrete question} | FEATURE-001-002 SC-03 | Pending |

### Answers from RE

| ID | Date | Answer | Affected artifacts | Status |
|---|---|---|---|---|
| A-001 | 2026-04-20 | {concrete answer, with updated numbers} | FEATURE-001-002 (SC-03 updated) | Resolved |

### Dialog rules

- **Not a blocker.** Pending entries do not stop the Architect's work on
  unrelated ADRs. Only the ADR that depends on the pending question
  waits.
- **Try to self-answer first.** When a new skill session starts and
  sees pending dialog entries, it attempts to answer from existing
  artifacts (codebase, other docs) BEFORE asking the user.
- **One question per session to the user.** If self-answering fails,
  the skill surfaces ALL unresolved entries in a single
  `AskUserQuestion` at session start: "N questions from Architect
  could not be answered from existing artifacts. Address now, defer
  to end of session, or record as open issues?"
- **Entries are append-only.** Answers supersede questions by setting
  Status to Resolved. Rows are never deleted.

---

## 7. Ready-to-design checklist

- [ ] All Critical ASRs have quantified constraints
- [ ] NFR table has numbers, not adjectives
- [ ] Every FEATURE listed in section 2 or 3
- [ ] Open questions categorized (blocker vs. async)
- [ ] Handoff written in the canonical style (no em dashes, no AI vocab)
