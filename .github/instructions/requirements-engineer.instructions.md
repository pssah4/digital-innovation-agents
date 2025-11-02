---
applyTo: "requirements/epics/**/*.md, requirements/features/**/*.md, requirements/handoff/**/*.md"
description: "Qualitätsregeln für Requirements Engineering - Epics und Features"
autoLoad: true
---

# Requirements Engineer - Quality Standards für Epics & Features

Diese Instructions werden **automatisch** angewendet beim Arbeiten mit Epic- und Feature-Dateien. Sie definieren die Qualitätsstandards für die Übergabe an den Architekten.

> **Wichtig:** Diese Regeln ergänzen den Requirements Engineer Chatmode und stellen sicher, dass alle Requirements architect-ready sind.

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

**Fehlermeldung bei Verstoß:**

```
❌ Dateiname-Validierung fehlgeschlagen

Datei: epic-customer-portal.md
Problem: Entspricht nicht dem Pattern EPIC-XXX-slug.md

Korrekt wäre: EPIC-001-customer-portal.md

Format-Regeln:
  • PREFIX-XXX-descriptive-slug.md
  • PREFIX: EPIC|FEATURE
  • XXX: 3-stellige Nummer (001-999)
  • slug: lowercase, nur a-z, 0-9, Bindestriche
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

Beispiel-Header:
> **Epic ID:** EPIC-001
> **Scope:** [PoC / MVP]
> **Business Alignment:** [Link zu BA Dokument]
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

**Fehlermeldung bei unvollständigem Hypothesis Statement:**

```
❌ Epic Hypothesis Statement unvollständig

Datei: EPIC-001-customer-portal.md
Problem: 2 von 7 Komponenten fehlen

Gefunden:
  ✅ FÜR [Zielkunden]
  ✅ DIE [Bedarf haben]
  ✅ IST DAS [Produkt]
  ❌ EIN [Produktkategorie] - FEHLT
  ✅ DAS [Hauptnutzen]
  ✅ IM GEGENSATZ ZU [Alternative]
  ❌ UNSERE LÖSUNG [Differenzierung] - FEHLT

Aktion erforderlich:
  Vervollständige das Hypothesis Statement mit allen 7 Komponenten.
```

#### Business Outcomes - Quantifizierungs-Check:

```markdown
CHECK Business Outcomes:

✅ Enthält messbare Metriken?
✅ Verwendet konkrete Zahlen?
✅ Definiert Zeitrahmen?
✅ Vermeidet vage Aussagen?

ERLAUBT (konkret):
✅ "Conversion Rate steigt von 12% auf 18% (+50%) innerhalb 6 Monate"
✅ "Support-Tickets sinken um 40% (von 200/Woche auf 120/Woche)"
✅ "Time-to-Market reduziert von 8 Wochen auf 4 Wochen (-50%)"
✅ "Customer Satisfaction Score steigt von 7.2 auf 8.5"

VERBOTEN (zu vage):
❌ "Verbessert User Experience"
❌ "Macht den Prozess schneller"
❌ "Erhöht die Zufriedenheit"
❌ "Reduziert Kosten deutlich"
```

**Fehlermeldung bei vagen Business Outcomes:**

```
⚠️ Business Outcomes nicht ausreichend quantifiziert

Datei: EPIC-001-customer-portal.md
Gefunden: "Improves efficiency and user satisfaction"

Problem: Keine messbaren Metriken

Benötigt wird mindestens:
  • Baseline-Wert (aktuell)
  • Ziel-Wert (nach Implementation)
  • Zeitrahmen (wann)
  • Einheit (%, €, Stunden, etc.)

Beispiel:
  ✅ "Login-Zeit sinkt von 5 Minuten auf 2 Minuten (-60%) innerhalb 3 Monate"
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
   - Performance (mit Zahlen)
   - Security (spezifisch)
   - Scalability (messbar)
   - Availability (Uptime %)
6. ✅ Architecture Considerations vorhanden?
7. ✅ ASRs identifiziert und markiert? (🔴/🟡)
8. ✅ Definition of Done vollständig?
9. ✅ Dependencies dokumentiert?
10. ✅ Out of Scope definiert?

Beispiel-Header:
> **Feature ID:** FEATURE-001
> **Epic:** EPIC-001 - [Link]
> **Priority:** P0-Critical
> **Effort:** M (3-5 Sprints)
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
CHECK Acceptance Criteria:

✅ Jedes Kriterium hat pass/fail Bedingung
✅ Konkrete Werte (keine vagen Aussagen)
✅ Messbare Metriken
✅ Technologie-agnostisch (kein "wie")

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

**Fehlermeldung bei untestbaren Acceptance Criteria:**

```
❌ Acceptance Criteria nicht testbar

Datei: FEATURE-042-user-authentication.md
Problem: 3 von 5 Criteria sind vage

Gefunden:
  1. ✅ "Login Endpoint gibt JWT Token zurück" - TESTBAR
  2. ❌ "System ist sicher" - VAGE
     Fix: "OAuth 2.0 Authentication, TLS 1.3, AES-256 Encryption"
  
  3. ❌ "Schnelle Response" - VAGE
     Fix: "Response Time < 200ms für 95% der Requests"
  
  4. ✅ "Session Cookie expires nach 24h" - TESTBAR
  5. ❌ "User-friendly Login" - VAGE
     Fix: "Max 3 Schritte bis zum erfolgreichen Login"

Aktion erforderlich:
  Konkretisiere alle vagen Criteria mit messbaren Werten.
```

---

### 4. Non-Functional Requirements (NFRs) - KRITISCH!

#### NFR Quantifizierungs-Validation:

```markdown
CHECK für JEDES Feature:

✅ Performance NFRs mit konkreten Zahlen?
✅ Security NFRs spezifisch (nicht "sicher")?
✅ Scalability NFRs messbar?
✅ Availability NFRs als Uptime %?
✅ Maintainability NFRs definiert?

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
  - Resource Usage: Max 512MB RAM, 2 CPU Cores

Scalability:
  - Support für 10,000 concurrent users
  - Handling von 1TB Datenvolumen
  - Wachstum von 50% pro Jahr einkalkuliert

Availability:
  - Uptime: 99.9% (max 8.7h Downtime/Jahr)
  - RTO: 15 Minuten
  - RPO: 5 Minuten
```

**Fehlermeldung bei vagen NFRs:**

```
❌ Non-Functional Requirements zu vage

Datei: FEATURE-042-user-authentication.md
Problem: NFRs enthalten keine konkreten Zahlen

Gefunden:
  Performance: "System soll schnell sein"
  Security: "Sicheres Login"
  Scalability: "Skalierbar für Wachstum"

KRITISCH: Architekt braucht konkrete Zahlen für Architektur-Entscheidungen!

Aktion erforderlich:
  Quantifiziere ALLE NFRs:
  
  Performance:
    - Response Time: < [X] ms für [Y]% der Requests
    - Throughput: [Z] Requests/Second
  
  Security:
    - Authentication: [OAuth 2.0 / JWT / ...]
    - Encryption: [AES-256 / TLS 1.3 / ...]
    - Compliance: [GDPR / SOC2 / HIPAA]
  
  Scalability:
    - Concurrent Users: [X] simultane User
    - Data Volume: [Y] GB/TB
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

🟡 **MODERATE ASR #2**: [Beschreibung]
- [...]
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
  - Benötigt Performance Monitoring
- **Quality Attribute**: Performance
- **Constraint**: Budget für CDN verfügbar

🟡 **MODERATE ASR**: GDPR Art. 17 (Right to be Forgotten)
- **Warum ASR**: Beeinflusst Data Architecture
- **Impact**:
  - Soft Delete Pattern erforderlich
  - Data Retention Policies
  - Audit Trail für Deletions
- **Quality Attribute**: Security/Compliance
- **Constraint**: 30-Tage Frist für Datenlöschung

❌ SCHLECHT - Kein ASR, nur NFR:

"Code Coverage > 80%"
→ Das ist ein NFR, aber KEIN ASR (beeinflusst keine Architektur)

"API Dokumentation erforderlich"
→ Das ist ein Prozess-Requirement, aber KEIN ASR
```

**Fehlermeldung bei fehlenden ASRs:**

```
⚠️ Keine Architecturally Significant Requirements (ASRs) identifiziert

Datei: FEATURE-042-user-authentication.md
Problem: Architecture Considerations Section hat keine ASRs

KRITISCH: Architekt braucht ASRs um zu wissen:
  - Welche Requirements beeinflussen Architektur-Entscheidungen
  - Welche Quality Attributes kritisch sind
  - Welche ADRs erstellt werden müssen

Aktion erforderlich:
  Identifiziere ASRs aus deinen NFRs:
  
  Frage dich für jede NFR:
  - Beeinflusst diese Requirement fundamentale Architektur-Entscheidungen?
  - Muss der Architekt ein Pattern/Technology wählen um diese zu erfüllen?
  
  Wenn JA → Markiere als ASR mit 🔴 oder 🟡
  
  Beispiele:
  - Response Time < 200ms → ASR (braucht Caching/CDN)
  - 10,000 concurrent users → ASR (braucht Scalability Architecture)
  - GDPR Compliance → ASR (braucht Data Architecture)
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

**Fehlermeldung bei unvollständiger DoD:**

```
⚠️ Definition of Done unvollständig

Datei: FEATURE-042-user-authentication.md
Problem: 4 von 10 Standard-Items fehlen

Gefunden:
  ✅ Functional Acceptance Criteria
  ✅ Unit Tests
  ✅ Code Review
  ❌ NFR-Validierung - FEHLT
  ❌ Integration Tests - FEHLT
  ❌ Security Scan - FEHLT
  ❌ Architecture Review - FEHLT

Aktion erforderlich:
  Vervollständige Definition of Done mit allen relevanten Items.
  DoD = Vertrag zwischen RE, Architect und Developer!
```

---

### 7. Architect-Handoff-Dokument Validierung

#### Pflicht-Sections für Architect Handoff:

```markdown
CHECK requirements/handoff/architect-handoff.md:

1. ✅ Executive Summary vorhanden?
2. ✅ Requirements Package vollständig?
   - Links zu allen Epics (wenn vorhanden)
   - Links zu allen Features
3. ✅ ASRs Section vorhanden?
   - Critical ASRs gelistet (🔴)
   - Moderate ASRs gelistet (🟡)
   - Für jeden ASR: Quality Attribute + Impact + Constraint + Empfehlung
4. ✅ NFR Summary Table vorhanden?
   - Quality Attribute, Requirement, Target Value, Measurement, Priority
5. ✅ Context & Integration Section?
   - System Context Diagram
   - Primary Users
   - External Systems
   - Integration Points
   - Data Flow
6. ✅ Technology Stack Recommendations?
   - Core Libraries/Frameworks
   - Begründung für Empfehlungen
7. ✅ Constraints dokumentiert?
   - Technical Constraints
   - Business Constraints
   - Functional Constraints
8. ✅ Open Questions Section?
   - High Priority (blocking)
   - Medium Priority (non-blocking)
9. ✅ Next Steps for Architect definiert?
10. ✅ Traceability Matrix vorhanden?
11. ✅ Success Criteria definiert?
```

**Fehlermeldung bei unvollständigem Architect Handoff:**

```
❌ Architect-Handoff-Dokument unvollständig

Datei: requirements/handoff/architect-handoff.md
Problem: 3 kritische Sections fehlen

Status: 8/11 Sections vorhanden

Fehlende Sections:
  ❌ ASRs Section - KRITISCH für Architekten!
     → Architekt kann keine ADRs erstellen ohne ASRs
  ❌ Open Questions - Architekt muss wissen was zu klären ist
  ❌ Traceability Matrix - Business Alignment fehlt

Aktion erforderlich:
  1. Erstelle ASRs Section mit allen Critical + Moderate ASRs
  2. Liste alle Open Questions mit Priorität (High/Medium)
  3. Erstelle Traceability Matrix (Epic/Feature → BA Doc Section)
  
Ohne diese Sections kann der Architect nicht mit ADRs starten!
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
  ✅ Performance (Response Time, Throughput)
  ✅ Security (spezifisch: OAuth, TLS, etc.)
  ✅ Scalability (Concurrent Users, Data Volume)
  ✅ Availability (Uptime %, RTO, RPO)
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

**Wenn ANY Check ❌:**
```
❌ NOT READY für Architect

Status: [X] von [Y] Validierungen fehlgeschlagen

Blocker:
  [Liste aller fehlgeschlagenen Checks]

Aktion erforderlich:
  Behebe alle Blocker bevor Handoff zu Architect.
  Architect kann NICHT effektiv arbeiten ohne vollständige Requirements!
```

---

## 🔄 Feedback-Loop mit Business Analyst

**Wenn RE feststellt, dass BA-Input unvollständig ist:**

```markdown
Feedback-Types an BA:

1. **MISSING_CRITICAL_INFO**
   → Beispiel: "User Personas nicht definiert"
   → Aktion: RE fragt direkt User und updated BA-Dokument

2. **UNCLEAR_SCOPE**
   → Beispiel: "In-Scope vs Out-of-Scope unklar"
   → Aktion: RE klärt mit User und dokumentiert

3. **MISSING_BUSINESS_OUTCOMES**
   → Beispiel: "Keine messbaren Business Outcomes"
   → Aktion: RE arbeitet mit User um Outcomes zu quantifizieren

4. **VAGUE_REQUIREMENTS**
   → Beispiel: "Key Features zu high-level"
   → Aktion: RE konkretisiert mit User

Template für Feedback:
"⚠️ BA-Input unvollständig: [ISSUE]
Ich habe das mit dem User geklärt und das BA-Dokument aktualisiert.
Update: [Was wurde geändert]"
```

---

## 🔄 Feedback-Loop mit Architekt

**Wenn Architekt Feedback gibt:**

```markdown
Feedback-Types von Architect:

1. **REQUIREMENTS_UNCLEAR**
   → Konkretisiere betroffenes Feature
   → Füge fehlende Details hinzu
   → Update Feature-Dokument

2. **NEED_ADDITIONAL_NFR**
   → Ergänze fehlende NFR
   → Quantifiziere mit konkreten Zahlen
   → Update Feature & Handoff

3. **CONSTRAINT_MISSING**
   → Dokumentiere Constraint
   → Kläre Impact mit User wenn nötig
   → Update Handoff

4. **ASR_NOT_CLEAR**
   → Erkläre besser WARUM es ein ASR ist
   → Konkretisiere Impact auf Architektur
   → Update Feature & Handoff

Template für Response:
"✅ Feedback verarbeitet: [ISSUE]
Updated: [Was wurde geändert]
Review-Request: Bitte prüfe ob jetzt klar"
```

---

## 🎨 Validation Messages - Best Practices

### Success Message Format:

```
✅ {DATEINAME}

Validation successful:
  ✅ {Check 1 bestanden}
  ✅ {Check 2 bestanden}
  ✅ {Check 3 bestanden}

Status: Architect-Ready ✅
Next: Add to Handoff-Dokument
```

### Warning Message Format:

```
⚠️ {DATEINAME}

Quality warnings (non-blocking):
  ⚠️ {Warning 1}
  ⚠️ {Warning 2}

Recommendations:
  1. {Empfehlung 1}
  2. {Empfehlung 2}

Status: Acceptable but should improve before handoff
```

### Error Message Format:

```
❌ {DATEINAME}

Validation failed ({X}/{Y} checks passed):
  ❌ {Fehler 1 - konkrete Beschreibung}
  ❌ {Fehler 2 - konkrete Beschreibung}

CRITICAL for Architect:
  {Warum dieser Fehler die Architektur-Arbeit blockiert}

Actions required:
  1. {Konkrete Aktion 1}
  2. {Konkrete Aktion 2}

Next: Fix errors and re-validate
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

**Version:** 3.0 (Optimiert für BA→RE→Architect Workflow)
**Focus:** Epics & Features only (keine Issues/Tasks)
**Quality Gate:** Architect-Ready Validation