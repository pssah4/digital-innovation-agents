# Plan Context: {Project/Feature Name}

> **Purpose:** Technische Zusammenfassung fuer Claude Code
> **Created by:** Architect
> **Date:** {Datum}

---

## Technical Stack

**Backend:**
- Language: {aus ADR-XXX}
- Framework: {aus ADR-XXX}
- Database: {aus ADR-XXX}
- ORM: {aus ADR-XXX}

**Frontend:** (falls applicable)
- Framework: {aus ADR-XXX}
- State Management: {aus ADR-XXX}

**Infrastructure:**
- Cloud Provider: {aus ADR-XXX}
- Deployment: {aus ADR-XXX}
- CI/CD: {aus ADR-XXX}

**API & Integration:**
- API Style: {REST/GraphQL}
- Authentication: {aus ADR-XXX}

## Architecture Style

- Pattern: {Modular Monolith / Microservices / Serverless}
- Key Quality Goals:
  1. {Quality Goal 1}
  2. {Quality Goal 2}
  3. {Quality Goal 3}

## Key Architecture Decisions (ADR Summary)

| ADR | Title | Vorgeschlagene Entscheidung | Impact |
|-----|-------|-----------------------------|--------|
| ADR-001 | {Title} | {Decision} | High |
| ADR-002 | {Title} | {Decision} | High |
| ADR-003 | {Title} | {Decision} | Medium |

**Detail pro ADR:**

1. **{ADR-001 Title}:** {Decision}
   - Rationale: {Kurze Begruendung}

2. **{ADR-002 Title}:** {Decision}
   - Rationale: {Kurze Begruendung}

3. **{ADR-003 Title}:** {Decision}
   - Rationale: {Kurze Begruendung}

## Data Model (Core Entities)

```
{Entity 1}
  {attribute}: {type}
  relations: [{related}]

{Entity 2}
  {attribute}: {type}
  relations: [{related}]
```

## External Integrations

| System | Type | Protocol | Purpose |
|--------|------|----------|---------|
| {System 1} | Inbound/Outbound | REST/Events | {Purpose} |

## Performance & Security

**Performance:**
- Response Time: {X}ms for {Y}th percentile
- Throughput: {Z} req/sec
- Concurrent Users: {N}

**Security:**
- Authentication: {Method}
- Authorization: {Model}
- Encryption: {At rest / In transit}

---

## Kontext-Dokumente fuer Claude Code

Claude Code sollte folgende Dokumente als Kontext lesen:

1. `_devprocess/architecture/ADR-*.md` (alle ADR-Vorschlaege)
2. `_devprocess/architecture/arc42.md` (Architektur-Entwurf)
3. `_devprocess/requirements/features/FEATURE-*.md` (alle Features)
4. `_devprocess/requirements/epics/EPIC-*.md` (wenn vorhanden)

---

## Dialog

> Bidirectional channel between Coder and Architect. NOT a blocker:
> the Coder proceeds with implementation that does not depend on
> pending questions. Only the specific change that needs clarification
> waits.

### Questions from Coder to Architect

| ID | Date | Question | Addressed by | Status |
|---|---|---|---|---|
| Q-001 | 2026-04-19 | {concrete question about an ADR or a stack choice} | ADR-007 | Pending |

### Answers from Architect

| ID | Date | Answer | Affected artifacts | Status |
|---|---|---|---|---|
| A-001 | 2026-04-20 | {concrete answer; if the Architect updates an ADR, cite it here} | ADR-007 (amended) | Resolved |

### Dialog rules

- **Not a blocker.** Pending entries do not stop unrelated
  implementation work. Only the code change that depends on the
  pending question waits.
- **Try to self-answer first.** When the Coder (or Architect on a
  return pass) starts a new session and sees pending dialog entries,
  it attempts to answer from existing artifacts (ADRs, arc42, code)
  BEFORE asking the user.
- **One question per session to the user.** If self-answering fails,
  the skill surfaces ALL unresolved entries in a single
  `AskUserQuestion` at session start: "N questions from Coder could
  not be answered from existing artifacts. Address now, defer to end
  of session, or record as open issues?"
- **Entries are append-only.** Answers supersede questions by setting
  Status to Resolved. Rows are never deleted.
