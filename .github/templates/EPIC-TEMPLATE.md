# EPIC-XXX: [Epic Title]

> **ID:** EPIC-XXX  
> **Scope:** PoC | MVP  
> **Status:** 📋 Not Started | 🚧 In Progress | ✅ Done  
> **Priority:** P0-Critical | P1-High | P2-Medium  
> **Created:** YYYY-MM-DD  
> **BA Document:** [Link to Business Analysis Document]

---

## 🎯 Epic Hypothesis Statement (SAFe Format)

**FÜR** [Zielkunden-Segment - spezifisch, nicht "User"]  
**DIE** [konkreten Bedarf/Problem haben]  
**IST DAS** [Produkt/Lösung]  
**EIN** [Produktkategorie]  
**DAS** [Hauptnutzen bietet - quantifiziert]  
**IM GEGENSATZ ZU** [Wettbewerbs-Alternative]  
**UNSERE LÖSUNG** [primäre Differenzierung]

---

## 💰 Business Outcomes (Quantifiziert!)

> ⚠️ **Keine vagen Aussagen!** Jedes Outcome muss messbar sein.

### Primäre Outcomes

| Outcome | Baseline (Ist) | Target (Soll) | Zeitrahmen | Messmethode |
|---------|----------------|---------------|------------|-------------|
| [Outcome 1] | [Aktueller Wert] | [Zielwert] | [X Monate] | [Wie gemessen] |
| [Outcome 2] | [Aktueller Wert] | [Zielwert] | [X Monate] | [Wie gemessen] |
| [Outcome 3] | [Aktueller Wert] | [Zielwert] | [X Monate] | [Wie gemessen] |

**Beispiele für gute Outcomes:**
- ✅ "Conversion Rate steigt von 12% auf 18% (+50%) innerhalb 6 Monate"
- ✅ "Support-Tickets sinken um 40% (von 200/Woche auf 120/Woche)"
- ❌ "Verbessert User Experience" (zu vage!)

### Leading Indicators (Frühindikatoren)

| Indikator | Beschreibung | Messzyklus | Zielwert |
|-----------|--------------|------------|----------|
| [Indikator 1] | [Was zeigt früh ob wir auf Kurs sind] | [Wöchentlich/Monatlich] | [Wert] |
| [Indikator 2] | [Früher Erfolgsmesser] | [Wöchentlich/Monatlich] | [Wert] |

---

## 📋 MVP Features

| Feature ID | Name | Priority | Effort | Status | Link |
|------------|------|----------|--------|--------|------|
| FEATURE-001 | [Name] | P0-Critical | M | 📋 Not Started | [Link](../features/FEATURE-001-*.md) |
| FEATURE-002 | [Name] | P0-Critical | L | 📋 Not Started | [Link](../features/FEATURE-002-*.md) |
| FEATURE-003 | [Name] | P1-High | S | 📋 Not Started | [Link](../features/FEATURE-003-*.md) |

**Priority Legend:**
- **P0-Critical:** Ohne geht MVP nicht
- **P1-High:** Wichtig für vollständige User Experience
- **P2-Medium:** Wertsteigernd, aber nicht essentiell

**Effort Legend:**
- **S:** 1-2 Sprints
- **M:** 3-5 Sprints
- **L:** 6+ Sprints

---

## 🚫 Explizit Out-of-Scope

> Klar definieren was NICHT Teil dieses Epics ist!

| Feature/Capability | Begründung | Geplant für |
|--------------------|------------|-------------|
| [Feature X] | [Warum out-of-scope] | Phase 2 / Never |
| [Feature Y] | [Warum out-of-scope] | Phase 2 / Never |
| [Feature Z] | [Warum out-of-scope] | Phase 2 / Never |

---

## 🔗 Dependencies

### Upstream (Blockiert dieses Epic)

| Dependency | Typ | Owner | Status | Impact wenn verzögert |
|------------|-----|-------|--------|----------------------|
| [Dependency 1] | Technical/Business/External | [Team/Person] | 🟢/🟡/🔴 | [Auswirkung] |

### Downstream (Wird von diesem Epic blockiert)

| Abhängiges Epic/Feature | Warum blockiert |
|-------------------------|-----------------|
| [Epic/Feature] | [Begründung] |

---

## ⚠️ Risks

| Risk | Wahrscheinlichkeit | Impact | Mitigation |
|------|-------------------|--------|------------|
| [Risk 1] | H/M/L | H/M/L | [Strategie] |
| [Risk 2] | H/M/L | H/M/L | [Strategie] |
| [Risk 3] | H/M/L | H/M/L | [Strategie] |

---

## 💳 Technical Debt (Nur PoC!)

> ⚠️ **Nur für PoC relevant!** MVP sollte keine bewusste Tech Debt haben.

| Shortcut | Beschreibung | Impact für MVP-Konversion | Geschätzter Cleanup-Aufwand |
|----------|--------------|---------------------------|----------------------------|
| [Shortcut 1] | [Was wird vereinfacht] | [Was muss für MVP geändert werden] | [X Tage] |
| [Shortcut 2] | [Was wird vereinfacht] | [Was muss für MVP geändert werden] | [X Tage] |

**MVP-Konversion Impact:**
- [ ] Low (1-2 Wochen Cleanup)
- [ ] Medium (1 Monat Refactor)
- [ ] High (2-3 Monate Neu-Entwicklung)

---

## 📐 Assumptions

| Annahme | Risk wenn falsch | Validierungsmethode |
|---------|------------------|---------------------|
| [Annahme 1] | [Impact] | [Wie validieren] |
| [Annahme 2] | [Impact] | [Wie validieren] |

---

## 🚧 Constraints

### Technical Constraints
- [Constraint 1]: [Beschreibung und Begründung]

### Business Constraints
- **Budget:** [Limit]
- **Timeline:** [Deadline]
- **Resources:** [Team-Verfügbarkeit]

### Compliance/Regulatory
- [Regulation]: [Anforderung]

---

## 📅 Timeline & Milestones

| Milestone | Zieldatum | Status | Quality Gate |
|-----------|-----------|--------|--------------|
| Requirements Complete | YYYY-MM-DD | 📋 | QG1 |
| Architecture Complete | YYYY-MM-DD | 📋 | QG2 |
| Feature 1-3 Complete | YYYY-MM-DD | 📋 | QG3 |
| All Features Complete | YYYY-MM-DD | 📋 | QG4 |
| Production Release | YYYY-MM-DD | 📋 | QG5 |

---

## ✅ Quality Gate 1 (QG1) - Requirements Complete

**Epic ist bereit für Architect wenn:**

- [ ] Epic Hypothesis Statement vollständig (alle 7 Komponenten)
- [ ] Business Outcomes quantifiziert (Baseline → Target → Timeframe)
- [ ] Leading Indicators definiert
- [ ] Min. 3 Features definiert und priorisiert (P0/P1/P2)
- [ ] Alle Features existieren als separate Dokumente
- [ ] Out-of-Scope explizit definiert
- [ ] Dependencies dokumentiert
- [ ] Risks identifiziert
- [ ] Technical Debt dokumentiert (nur PoC)
- [ ] Dateiname-Pattern korrekt: `EPIC-XXX-descriptive-slug.md`

**Wenn alle Checks ✅:** Übergabe an Architect möglich!

---

## 📝 Change Log

| Datum | Änderung | Autor |
|-------|----------|-------|
| YYYY-MM-DD | Epic erstellt | [Name] |
| YYYY-MM-DD | [Änderung] | [Name] |

---

## 📚 References

- **BA Document:** [Link]
- **Related ADRs:** [Nach Architect-Phase hinzufügen]
- **arc42 Documentation:** [Nach Architect-Phase hinzufügen]

---

**Template Version:** 2.0  
**Workflow:** BA → RE (erstellt Epic) → Architect → Developer  
**Scope:** Nur für PoC und MVP (Simple Test hat keine Epics)
