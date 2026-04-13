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
