# FEATURE-XXX: [Feature Title]

> **Epic:** [EPIC-XXX](../epics/EPIC-XXX-*.md) - [Epic Name] *(nur PoC/MVP)*  
> **ID:** FEATURE-XXX  
> **Priority:** P0-Critical | P1-High | P2-Medium  
> **Effort:** S (1-2 Sprints) | M (3-5 Sprints) | L (6+ Sprints)  
> **Status:** 📋 Not Started | 🚧 In Progress | ✅ Done  
> **Created:** YYYY-MM-DD  

---

## 📝 Feature Description

[1-2 Absätze: Was ist das Feature und warum wird es benötigt? Business Context klar machen.]

---

## 🎯 Benefits Hypothesis

**Wir glauben dass** [Beschreibung des Features]  
**Folgende messbare Outcomes liefert:**
- [Outcome 1 mit Metrik]
- [Outcome 2 mit Metrik]

**Wir wissen dass wir erfolgreich sind wenn:**
- [Erfolgs-Metrik 1 mit konkretem Zielwert]
- [Erfolgs-Metrik 2 mit konkretem Zielwert]

---

## 👤 User Stories

### Story 1: [Name]

**Als** [spezifische User-Rolle - nicht nur "User"]  
**möchte ich** [konkrete Funktionalität]  
**um** [Business-Wert] zu erreichen

**Beispiel-Szenario:**
> [Konkretes Beispiel wie der User diese Funktionalität nutzt]

### Story 2: [Name]

**Als** [User-Rolle]  
**möchte ich** [Funktionalität]  
**um** [Business-Wert] zu erreichen

### Story 3: [Name]

**Als** [User-Rolle]  
**möchte ich** [Funktionalität]  
**um** [Business-Wert] zu erreichen

---

## ✅ Functional Acceptance Criteria

> ⚠️ **Jedes Kriterium muss testbar sein!** Pass/Fail muss eindeutig bestimmbar sein.

**Dieses Feature ist funktional vollständig wenn:**

- [ ] **AC1:** [Konkret und testbar]
  - Verification: [Wie wird das getestet?]
  
- [ ] **AC2:** [Konkret und testbar]
  - Verification: [Wie wird das getestet?]
  
- [ ] **AC3:** [Konkret und testbar]
  - Verification: [Wie wird das getestet?]
  
- [ ] **AC4:** [Konkret und testbar]
  - Verification: [Wie wird das getestet?]
  
- [ ] **AC5:** [Konkret und testbar]
  - Verification: [Wie wird das getestet?]

**Beispiele:**
- ✅ "API Endpoint GET /api/users gibt HTTP 200 und JSON-Array zurück"
- ✅ "Login mit ungültigen Credentials zeigt Fehlermeldung innerhalb 500ms"
- ❌ "System soll schnell sein" (nicht testbar!)
- ❌ "User-friendly Interface" (nicht testbar!)

---

## 🥒 Gherkin Scenarios

### Scenario 1: [Happy Path]

```gherkin
Feature: [Feature Name]

Scenario: [Beschreibender Name - erfolgreicher Fall]
  Given [Vorbedingung mit konkreten Werten]
  And [Weitere Vorbedingung]
  When [Aktion des Users mit konkreten Werten]
  And [Weitere Aktion falls nötig]
  Then [Erwartetes Ergebnis mit konkreten Werten]
  And [Weitere erwartete Ergebnisse]
  And [Zustandsänderungen/Side Effects]
```

### Scenario 2: [Error Case]

```gherkin
Scenario: [Beschreibender Name - Fehlerfall]
  Given [Vorbedingung]
  And [Fehlerbedingung die zum Fehler führt]
  When [Aktion des Users]
  Then [Erwartete Fehlerbehandlung]
  And [Keine unerwünschten Side Effects]
```

### Scenario 3: [Edge Case]

```gherkin
Scenario: [Beschreibender Name - Grenzfall]
  Given [Grenzwert-Bedingung]
  When [Aktion]
  Then [Erwartetes Verhalten am Grenzwert]
```

---

## 📊 Non-Functional Requirements (NFRs)

> ⚠️ **KRITISCH für Architekt!** Alle NFRs müssen quantifiziert sein - keine vagen Aussagen!

### Performance

| Requirement | Target | Messmethode |
|-------------|--------|-------------|
| Response Time | < [X] ms für [Y]% der Requests | [Tool/Methode] |
| Throughput | [X] Requests/Second | Load Test |
| Resource Usage | Max [X] MB RAM, [Y] CPU Cores | Monitoring |

### Security

| Requirement | Spezifikation | Compliance |
|-------------|---------------|------------|
| Authentication | [OAuth 2.0 / JWT / Session] | [Standard] |
| Authorization | [RBAC / ABAC] mit Rollen: [X, Y, Z] | [Standard] |
| Encryption at Rest | [AES-256] | [GDPR Art. X] |
| Encryption in Transit | [TLS 1.3] | [Standard] |
| Input Validation | [XSS, SQL Injection Prevention] | OWASP |

### Scalability

| Requirement | Target | Wachstum |
|-------------|--------|----------|
| Concurrent Users | [X] simultane User | +[Y]% pro Jahr |
| Data Volume | [X] GB/TB | +[Y] GB/Monat |
| Horizontal Scaling | [Ja/Nein] - [Strategie] | - |

### Availability

| Requirement | Target | Bedeutung |
|-------------|--------|-----------|
| Uptime | [99.9]% | Max [8.7h] Downtime/Jahr |
| RTO (Recovery Time) | [X] Minuten | Max Zeit bis Wiederherstellung |
| RPO (Recovery Point) | [X] Minuten | Max Datenverlust |

### Maintainability

| Requirement | Target |
|-------------|--------|
| Code Coverage | Min. [X]% |
| Documentation | [API Docs, Inline Comments] |
| Logging | [Structured Logging, Log Levels] |

---

## 🏛️ Architecture Considerations (für Architekt)

### Architecturally Significant Requirements (ASRs)

> ASRs sind NFRs die fundamentale Architektur-Entscheidungen beeinflussen.

#### 🔴 CRITICAL ASRs (Must address in Architecture)

**ASR #1:** [Beschreibung - z.B. "Response Time < 200ms für 95% der Requests"]
- **Warum ASR:** [Begründung warum architektur-relevant]
- **Quality Attribute:** [Performance / Security / Scalability / Availability]
- **Architectural Impact:** [Welche Entscheidungen werden beeinflusst?]
  - Benötigt: [z.B. Caching-Layer, CDN, Load Balancing]
- **Constraint:** [Technische/Business Constraints]
- **Empfehlung:** [Falls vorhanden]

**ASR #2:** [Beschreibung]
- **Warum ASR:** [Begründung]
- **Quality Attribute:** [Attribut]
- **Architectural Impact:** [Impact]
- **Constraint:** [Constraint]

#### 🟡 MODERATE ASRs (Should address in Architecture)

**ASR #3:** [Beschreibung]
- **Warum ASR:** [Begründung]
- **Quality Attribute:** [Attribut]
- **Architectural Impact:** [Impact]

### Context & Boundaries

**Interagierende Systeme:**
- [System A]: [Art der Interaktion]
- [System B]: [Art der Interaktion]

**Integration Points:**
- [API/Message Queue/Database]

**Data Flow:**
```
[User] → [Frontend] → [API Gateway] → [Service] → [Database]
                                    ↘ [External API]
```

### Constraints (für Architekt)

**Technical:**
- [Constraint 1]: [Begründung]

**Platform:**
- [Cloud-Provider / On-Premise]

**Compliance:**
- [GDPR / HIPAA / SOC2 / PCI-DSS]

### ❓ Open Questions für Architekt

> Fragen die der Architekt beantworten/entscheiden muss.

**High Priority (blocking):**
- ❓ [Technische Entscheidung die Architekt treffen muss]
- ❓ [Architektur-Pattern-Frage]

**Medium Priority (non-blocking):**
- ❓ [Integration-Strategie-Frage]
- ❓ [Optionale Optimierung]

---

## ✅ Definition of Done

**Functional:**
- [ ] Alle Functional Acceptance Criteria erfüllt
- [ ] Alle Gherkin Scenarios bestehen

**Quality:**
- [ ] Alle NFRs validiert
- [ ] Unit Tests geschrieben (Coverage > [X]%)
- [ ] Integration Tests bestanden
- [ ] Performance Tests bestanden (wenn relevant)
- [ ] Security Scan bestanden

**Process:**
- [ ] Architecture Review abgeschlossen (QG2)
- [ ] Code Review abgeschlossen
- [ ] API Dokumentation aktualisiert
- [ ] Deployed in Staging
- [ ] UAT bestanden

---

## 🔗 Dependencies

### Blocked By (Muss zuerst fertig sein)

| Dependency | Typ | Status | Impact wenn verzögert |
|------------|-----|--------|----------------------|
| [FEATURE-XXX](./FEATURE-XXX-*.md) | Feature | 📋/🚧/✅ | [Auswirkung] |
| [External System] | External | 🟢/🟡/🔴 | [Auswirkung] |

### Blocks (Wartet auf dieses Feature)

| Abhängiges Feature | Warum blockiert |
|-------------------|-----------------|
| [FEATURE-XXX](./FEATURE-XXX-*.md) | [Begründung] |

---

## 🚫 Out of Scope

> Explizit was NICHT Teil dieses Features ist (häufig verwechselt).

| Feature/Capability | Begründung | Wo behandelt |
|--------------------|------------|--------------|
| [Capability X] | [Warum nicht hier] | [FEATURE-XXX / Phase 2 / Never] |
| [Capability Y] | [Warum nicht hier] | [Wo stattdessen] |

---

## 📐 Assumptions

| Annahme | Risk wenn falsch | Validierungsmethode |
|---------|------------------|---------------------|
| [Technische Annahme] | [Impact] | [Wie validieren] |
| [Business Annahme] | [Impact] | [Wie validieren] |
| [Daten Annahme] | [Impact] | [Wie validieren] |

---

## ✅ Quality Gate 1 (QG1) - Feature Ready for Architect

**Feature ist bereit für Architect wenn:**

- [ ] Feature Description klar (Business Context)
- [ ] Benefits Hypothesis mit messbaren Outcomes
- [ ] Min. 1-3 User Stories (Als/möchte/um)
- [ ] Min. 3-5 testbare Acceptance Criteria
- [ ] Min. 2-3 Gherkin Scenarios (Happy Path + Error)
- [ ] NFRs quantifiziert (ALLE mit Zahlen!)
  - [ ] Performance (Response Time, Throughput)
  - [ ] Security (spezifisch: OAuth, TLS, etc.)
  - [ ] Scalability (Concurrent Users, Data Volume)
  - [ ] Availability (Uptime %, RTO, RPO)
- [ ] ASRs identifiziert und markiert (🔴/🟡)
- [ ] Architectural Impact beschrieben
- [ ] Definition of Done vollständig
- [ ] Dependencies dokumentiert
- [ ] Out of Scope definiert
- [ ] Dateiname-Pattern: `FEATURE-XXX-descriptive-slug.md`

**Wenn alle Checks ✅:** Feature kann in Architect-Handoff aufgenommen werden!

---

## 📝 Change Log

| Datum | Änderung | Autor |
|-------|----------|-------|
| YYYY-MM-DD | Feature erstellt | [Name] |

---

## 📚 References

- **Epic:** [Link] *(nur PoC/MVP)*
- **BA Document:** [Link]
- **Related ADRs:** [Nach Architect-Phase hinzufügen]

---

**Template Version:** 2.0  
**Workflow:** BA → RE (erstellt Feature) → Architect → Developer  
**Erstellt von:** Requirements Engineer
