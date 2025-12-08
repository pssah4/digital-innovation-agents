---
name: Requirements Engineer Quality Standards
applyTo: "requirements/epics/**/*.md, requirements/features/**/*.md, requirements/handoff/**/*.md"
description: "Qualitätsregeln für Requirements Engineering - Epics und Features"
---

# Requirements Engineer - Quality Standards für Epics & Features

Diese Instructions werden **automatisch** angewendet beim Arbeiten mit Epic- und Feature-Dateien. Sie definieren die Qualitätsstandards für die Übergabe an den Architekten.

> **Wichtig:** Diese Regeln ergänzen den Requirements Engineer Agent und stellen sicher, dass alle Requirements architect-ready sind.

---

## 📁 Unterstützte Dateitypen

Diese Validierungsregeln greifen bei:

```
✅ requirements/epics/EPIC-*.md
✅ requirements/features/FEATURE-*.md
✅ requirements/handoff/*.md
```

**NICHT unterstützt** (werden vom Developer Agent erstellt):
```
❌ requirements/issues/ISSUE-*.md       → Developer Agent
❌ requirements/tasks/TASK-*.md         → Developer Agent
❌ architecture/adr/ADR-*.md            → Architect Agent
❌ architecture/arc42/**                → Architect Agent
```

---

## 🎯 Qualitätsziele

### Für den Architekten
Der Architekt muss **sofort starten** können mit:
- ✅ Klar identifizierten Architecturally Significant Requirements (ASRs)
- ✅ Quantifizierten Non-Functional Requirements (NFRs)
- ✅ Dokumentierten Constraints
- ✅ Priorisierten Open Questions

### Für den Developer Agent
Nach Architektur-Phase muss der Developer Agent:
- ✅ Klare Acceptance Criteria haben
- ✅ Testbare Definition of Done haben
- ✅ Verstehen was zu bauen ist (nicht wie)

---

## 🔍 Automatische Validierungen

### 1. Dateinamen-Konventionen

**Pattern-Validierung beim Erstellen/Speichern:**

```javascript
const patterns = {
  epic: /^EPIC-\d{3}-[a-z0-9-]+\.md$/,
  feature: /^FEATURE-\d{3}-[a-z0-9-]+\.md$/
};
```

**Beispiele:**

```markdown
✅ EPIC-001-customer-portal.md
✅ FEATURE-042-user-authentication.md

❌ epic-001.md                       (missing prefix)
❌ EPIC-1-portal.md                  (number not 3-digit)
❌ EPIC-001-Customer Portal.md       (spaces not allowed)
❌ FEATURE-001-userAuth.md           (camelCase not allowed)
```

---

### 2. Epic-Level Validierung (nur PoC & MVP)

#### Pflicht-Sections für Epics:

```markdown
CHECK beim Speichern:

1. ✅ Epic Hypothesis Statement vorhanden und vollständig?
2. ✅ Business Outcomes quantifiziert? (Zahlen, Metriken)
3. ✅ Leading Indicators definiert?
4. ✅ MVP Features Liste vorhanden? (min. 3 Features)
5. ✅ Features priorisiert? (P0/P1/P2)
6. ✅ Out-of-Scope explizit definiert?
7. ✅ Dependencies dokumentiert?
8. ✅ Risks identifiziert?
9. ✅ Technical Debt dokumentiert? (nur PoC)
```

#### Epic Hypothesis Statement - Vollständigkeits-Check:

```markdown
Pflicht-Komponenten:

✅ FÜR [Zielkunden-Segment] - spezifisch, nicht "User"
✅ DIE [Bedarf/Problem haben] - klar beschrieben
✅ IST DAS [Produkt/Lösung] - Lösung benannt
✅ EIN [Produktkategorie] - kategorisiert
✅ DAS [Hauptnutzen bietet] - quantifiziert
✅ IM GEGENSATZ ZU [Alternative] - Wettbewerb genannt
✅ UNSERE LÖSUNG [Differenzierung] - USP klar
```

#### Business Outcomes - Quantifizierungs-Check:

```markdown
ERLAUBT (konkret):
✅ "Conversion Rate steigt von 12% auf 18% (+50%) innerhalb 6 Monate"
✅ "Support-Tickets sinken um 40% (von 200/Woche auf 120/Woche)"
✅ "Time-to-Market reduziert von 8 Wochen auf 4 Wochen (-50%)"

VERBOTEN (zu vage):
❌ "Verbessert User Experience"
❌ "Macht den Prozess schneller"
❌ "Erhöht die Zufriedenheit"
```

---

### 3. Feature-Level Validierung

#### Pflicht-Sections für Features:

```markdown
CHECK beim Speichern:

1. ✅ Feature Description vorhanden? (1-2 Absätze)
2. ✅ Benefits Hypothesis vollständig?
3. ✅ User Stories vorhanden? (min. 1-3)
4. ✅ Functional Acceptance Criteria testbar? (min. 3)
5. ✅ Non-Functional Requirements quantifiziert?
6. ✅ Architecture Considerations vorhanden?
7. ✅ ASRs identifiziert und markiert? (🔴/🟡)
8. ✅ Definition of Done vollständig?
9. ✅ Dependencies dokumentiert?
10. ✅ Out of Scope definiert?
```

#### User Story Format Validierung:

```markdown
CHECK jede User Story:

✅ "Als [Rolle] möchte ich [Ziel], um [Nutzen] zu erreichen"
✅ Rolle ist spezifisch (nicht nur "User")
✅ Ziel ist klar und actionable
✅ Nutzen ist business-orientiert

Beispiel - GUT:
✅ "Als Premium-Kunde möchte ich meine Bestellhistorie filtern,
    um schnell bestimmte Käufe zu finden"

Beispiel - SCHLECHT:
❌ "Als User möchte ich Daten sehen"
```

#### Acceptance Criteria - Testbarkeits-Check:

```markdown
ERLAUBT (testbar):
✅ "API Endpoint GET /api/users gibt HTTP 200 zurück"
✅ "Response Zeit < 200ms für 95% der Requests"
✅ "Alle User-Eingaben werden XSS-sanitized"
✅ "Max 3 Klicks bis zur Ziel-Funktion"

VERBOTEN (nicht testbar):
❌ "System soll schnell sein"
❌ "Sicheres System"
❌ "User-friendly Interface"
❌ "Gute Performance"
```

---

### 4. Non-Functional Requirements (NFRs) - KRITISCH!

#### NFR Quantifizierungs-Validation:

```markdown
PFLICHT-KATEGORIEN:

1. **Performance**
   ✅ Response Time: [X ms für Y% der Requests]
   ✅ Throughput: [X Requests/Second]
   ✅ Resource Usage: [Max CPU/Memory]

2. **Security**
   ✅ Authentication: [OAuth 2.0, JWT, etc.]
   ✅ Authorization: [RBAC, ABAC, etc.]
   ✅ Encryption: [At Rest: AES-256, In Transit: TLS 1.3]
   ✅ Compliance: [GDPR Art. X, SOC2, HIPAA]

3. **Scalability**
   ✅ Concurrent Users: [X simultane User]
   ✅ Data Volume: [Y GB/TB]
   ✅ Growth Rate: [Z% pro Jahr]

4. **Availability**
   ✅ Uptime: [99.9% = ~8.7h Downtime/Jahr]
   ✅ RTO (Recovery Time): [X Minuten]
   ✅ RPO (Recovery Point): [X Minuten]

5. **Maintainability**
   ✅ Code Coverage: [Min. X%]
   ✅ Documentation Requirements
   ✅ Logging Requirements
```

**Beispiele - GUT vs SCHLECHT:**

```markdown
❌ SCHLECHT (vage):
"System soll schnell und skalierbar sein mit hoher Verfügbarkeit"

✅ GUT (quantifiziert):
Performance:
  - Response Time: < 200ms für 95% der Requests, < 500ms für 99%
  - Throughput: Min. 100 Requests/Second

Scalability:
  - Support für 10,000 concurrent users
  - Handling von 1TB Datenvolumen

Availability:
  - Uptime: 99.9% (max 8.7h Downtime/Jahr)
  - RTO: 15 Minuten
  - RPO: 5 Minuten
```

---

### 5. Architecturally Significant Requirements (ASRs) - KRITISCH!

#### ASR Identifikation & Markierung:

```markdown
CHECK Architecture Considerations Section:

✅ Mindestens 1 ASR identifiziert?
✅ ASRs mit 🔴 (Critical) oder 🟡 (Moderate) markiert?
✅ Für jedes ASR erklärt WARUM es architektur-relevant ist?
✅ Quality Attribute zugeordnet? (Performance/Security/etc.)
✅ Impact auf Architektur beschrieben?

ASR Template:
🔴 **CRITICAL ASR #1**: [Beschreibung]
- **Warum ASR**: [Begründung]
- **Impact**: [Architektur-Entscheidung die benötigt wird]
- **Quality Attribute**: [Performance/Security/Scalability/etc.]
- **Constraint**: [Technische/Business Constraints]
```

**Beispiele für ASRs:**

```markdown
✅ GUT - ASR richtig identifiziert:

🔴 **CRITICAL ASR**: Response Time < 200ms für 95% der Requests
- **Warum ASR**: Beeinflusst fundamentale Architektur-Entscheidungen
- **Impact**: 
  - Benötigt Caching-Layer (Redis/Memcached)
  - Benötigt CDN für statische Assets
  - Benötigt Load Balancing
- **Quality Attribute**: Performance

🟡 **MODERATE ASR**: GDPR Art. 17 (Right to be Forgotten)
- **Warum ASR**: Beeinflusst Data Architecture
- **Impact**:
  - Soft Delete Pattern erforderlich
  - Data Retention Policies
- **Quality Attribute**: Security/Compliance

❌ SCHLECHT - Kein ASR, nur NFR:

"Code Coverage > 80%"
→ Das ist ein NFR, aber KEIN ASR (beeinflusst keine Architektur)
```

---

### 6. Definition of Done Vollständigkeits-Check

```markdown
CHECK Definition of Done:

✅ Alle Functional Acceptance Criteria als Checkboxen?
✅ NFR-Validierung inkludiert?
✅ Testing Requirements definiert?
   - Unit Tests (Coverage %)
   - Integration Tests
   - Performance Tests (wenn relevant)
   - Security Tests
✅ Review Gates definiert?
   - Architecture Review
   - Code Review
   - UAT
✅ Documentation Requirements?

Minimum DoD:
- [ ] Alle Functional Acceptance Criteria erfüllt
- [ ] Alle NFRs validiert
- [ ] Unit Tests (Coverage > [X%])
- [ ] Integration Tests bestanden
- [ ] Security Scan bestanden
- [ ] Architecture Review abgeschlossen
- [ ] Code Review abgeschlossen
- [ ] Documentation aktualisiert
- [ ] Deployed in Staging
- [ ] UAT bestanden
```

---

### 7. Architect-Handoff-Dokument Validierung

#### Pflicht-Sections für Architect Handoff:

```markdown
CHECK requirements/handoff/architect-handoff.md:

1. ✅ Executive Summary vorhanden?
2. ✅ Requirements Package vollständig?
3. ✅ ASRs Section vorhanden?
4. ✅ NFR Summary Table vorhanden?
5. ✅ Context & Integration Section?
6. ✅ Technology Stack Recommendations?
7. ✅ Constraints dokumentiert?
8. ✅ Open Questions Section?
9. ✅ Next Steps for Architect definiert?
10. ✅ Traceability Matrix vorhanden?
11. ✅ Success Criteria definiert?
```

---

## 📊 Quality Gate: Architect-Ready Check

**Ein Feature/Epic ist Architect-Ready wenn:**

### Epic-Level (PoC/MVP):
```
✅ Hypothesis Statement vollständig (7/7 Komponenten)
✅ Business Outcomes quantifiziert (Baseline, Target, Timeframe)
✅ Leading Indicators definiert
✅ Features priorisiert (P0/P1/P2)
✅ Out-of-Scope explizit definiert
✅ Dependencies dokumentiert
✅ Technical Debt dokumentiert (PoC only)
```

### Feature-Level:
```
✅ Benefits Hypothesis klar
✅ User Stories vollständig (Als/möchte/um)
✅ Acceptance Criteria testbar (pass/fail)
✅ NFRs quantifiziert (ALLE mit Zahlen!)
✅ ASRs identifiziert und markiert (🔴/🟡)
✅ Architecture Impact beschrieben
✅ Definition of Done vollständig
✅ Dependencies dokumentiert
✅ Out of Scope definiert
```

### Handoff-Level:
```
✅ Alle Epics/Features verlinkt
✅ Alle ASRs in Handoff-Dokument gelistet
✅ NFR Summary Table vorhanden
✅ Open Questions priorisiert
✅ Constraints dokumentiert
✅ Traceability Matrix vorhanden
✅ Success Criteria definiert
```

**Wenn ALLE Checks ✅:**
```
🎉 ARCHITECT-READY!

Status: Alle Validierungen bestanden
Next: Übergabe an Architect Agent

Der Architekt kann jetzt:
  1. ASRs reviewen
  2. ADRs erstellen
  3. ARC42 Documentation starten
  4. Technology Stack Decisions treffen
```

---

## 🔄 Feedback-Loops

### Mit Business Analyst

```markdown
Feedback-Types an BA:

1. **MISSING_CRITICAL_INFO**
   → Beispiel: "User Personas nicht definiert"
   
2. **UNCLEAR_SCOPE**
   → Beispiel: "In-Scope vs Out-of-Scope unklar"
   
3. **MISSING_BUSINESS_OUTCOMES**
   → Beispiel: "Keine messbaren Business Outcomes"
```

### Mit Architekt

```markdown
Feedback-Types von Architect:

1. **REQUIREMENTS_UNCLEAR**
   → Konkretisiere betroffenes Feature
   
2. **NEED_ADDITIONAL_NFR**
   → Ergänze fehlende NFR mit Zahlen
   
3. **ASR_NOT_CLEAR**
   → Erkläre besser WARUM es ein ASR ist
```

---

## 📋 Zusammenfassung

Diese Instructions stellen sicher:

✅ **Epic-Qualität** - Vollständige Business-Context für Architekt  
✅ **Feature-Qualität** - Testbare Acceptance Criteria, quantifizierte NFRs  
✅ **ASR-Identifikation** - Architekt weiß welche Requirements kritisch sind  
✅ **NFR-Quantifizierung** - Keine vagen Aussagen, nur Zahlen  
✅ **Handoff-Vollständigkeit** - Architekt hat alle Informationen  
✅ **Traceability** - Jedes Requirement zu Business Goal verbunden  

**Ziel:** Architekt kann **sofort** mit ADRs und ARC42 starten, ohne zurück zu fragen!

---

**Version:** 4.0 (Aktualisiert für GitHub Copilot Agents)
**Focus:** Epics & Features only (keine Issues/Tasks)
**Quality Gate:** Architect-Ready Validation
