# Feature: {Name}

> **Feature ID**: FEATURE-{XXX}
> **Epic**: EPIC-{XXX} - {Link}
> **Priority**: [P0-Critical / P1-High / P2-Medium]
> **Effort Estimate**: [S / M / L]

## Feature Description

{1-2 Absaetze: Was ist das Feature und warum wird es benoetigt?}

## Benefits Hypothesis

**Wir glauben dass** {Beschreibung des Features}
**Folgende messbare Outcomes liefert:**
- {Outcome 1 mit Metrik}
- {Outcome 2 mit Metrik}

**Wir wissen dass wir erfolgreich sind wenn:**
- {Erfolgs-Metrik 1}
- {Erfolgs-Metrik 2}

## User Stories

### Story 1: {Name}
**Als** {User-Rolle}
**moechte ich** {Funktionalitaet}
**um** {Business-Wert} zu erreichen

### Story 2: {Name}
**Als** {User-Rolle}
**moechte ich** {Funktionalitaet}
**um** {Business-Wert} zu erreichen

---

## Success Criteria (Tech-Agnostic)

> KEINE Technologie-Begriffe! Siehe references/tech-agnostic-rules.md
> Technische Details gehoeren in "Technical NFRs" weiter unten.

| ID | Criterion | Target | Measurement |
|----|-----------|--------|-------------|
| SC-01 | {User-outcome basiert} | {Zielwert} | {Wie messen} |
| SC-02 | {Verhalten, nicht Implementierung} | {Zielwert} | {Wie messen} |
| SC-03 | {Performance als User-Erlebnis} | {Zielwert} | {Wie messen} |

---

## Technical NFRs (fuer Architekt) -- MIT TECHNOLOGIE OK

> Diese Section DARF technische Details enthalten!

### Performance
- **Response Time**: {X ms fuer Y% der Requests}
- **Throughput**: {X Requests/Second}
- **Resource Usage**: {Max CPU/Memory}

### Security
- **Authentication**: {OAuth 2.0, JWT, etc.}
- **Authorization**: {RBAC, ABAC}
- **Data Encryption**: {At Rest: AES-256, In Transit: TLS 1.3}

### Scalability
- **Concurrent Users**: {X simultane User}
- **Data Volume**: {Y GB/TB}
- **Growth Rate**: {Z% pro Jahr}

### Availability
- **Uptime**: {99.9% = ~8.7h Downtime/Jahr}
- **Recovery Time Objective (RTO)**: {X Minuten}
- **Recovery Point Objective (RPO)**: {X Minuten}

---

## Architecture Considerations

### Architecturally Significant Requirements (ASRs)

**CRITICAL ASR #1**: {Beschreibung}
- **Warum ASR**: {Begruendung}
- **Impact**: {Auf welche Architektur-Entscheidungen wirkt das?}
- **Quality Attribute**: {Performance / Security / Scalability / etc.}

**MODERATE ASR #2**: {Beschreibung}
- **Warum ASR**: {Begruendung}
- **Impact**: {Einfluss}
- **Quality Attribute**: {Attribut}

### Constraints
- **Technology**: {Muss X sein weil...}
- **Platform**: {Cloud-Provider X wegen...}
- **Compliance**: {GDPR, HIPAA, etc.}

### Open Questions fuer Architekt
- {Technische Entscheidung}
- {Architektur-Pattern-Frage}

---

## Definition of Done

### Functional
- [ ] Alle User Stories implementiert
- [ ] Alle Success Criteria erfuellt (verifiziert)

### Quality
- [ ] Unit Tests (Coverage > {X}%)
- [ ] Integration Tests bestanden
- [ ] Security Scan bestanden
- [ ] Performance Tests bestanden

### Documentation
- [ ] Feature-Spec aktualisiert (Status: Implemented)
- [ ] Backlog aktualisiert

---

## Dependencies
- **{Dependency 1}**: {Feature/System}, {Impact wenn verzoegert}

## Assumptions
- {Annahme 1}

## Out of Scope
- {Explizit nicht Teil dieses Features}
