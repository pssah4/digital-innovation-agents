---
name: Business Analyst Quality Standards
description: "Qualitätsstandards für Business Analysis Dokumente - Sichert vollständige Übergabe an Requirements Engineer"
---

# Business Analyst - Quality Standards für BA-Dokumente

Diese Instructions definieren die Qualitätsstandards für Business Analysis Dokumente und stellen sicher, dass der Requirements Engineer alle benötigten Informationen erhält.

> **Ziel:** Der Requirements Engineer kann **sofort** mit Epic/Feature-Erstellung starten, ohne Rückfragen an den BA.

---

## 🎯 Qualitätsziele

### Für den Requirements Engineer
Der RE muss aus dem BA-Dokument **direkt** ableiten können:
- ✅ Wer sind die User? (→ User Stories)
- ✅ Was ist das Problem? (→ Problem Statement)
- ✅ Was sind die Needs? (→ Functional Requirements)
- ✅ Was ist die Lösung? (→ Features)
- ✅ Was ist In-Scope/Out-of-Scope? (→ Epic Boundaries)

---

## 📋 Pflicht-Sections nach Scope

### Simple Test (Minimal)

```markdown
PFLICHT-SECTIONS:
✅ 1. Executive Summary (1 Absatz)
✅ 2. Problem Statement (kurz)
✅ 4. User & Zielgruppe (primäre Gruppe)
✅ 5. Needs (Funktionale Jobs, Pains)
✅ 9. Lösungsidee (Kernidee, Key Features)
✅ 11. Scope (In-Scope nur)

OPTIONAL:
○ 3. Stakeholder-Analyse
○ 6. Aktueller Prozess
○ 7. Daten & Integration
○ 10. Value Proposition
○ 12. Erfolgsmetriken
```

### Proof of Concept (Moderat)

```markdown
PFLICHT-SECTIONS:
✅ 1. Executive Summary (1-2 Absätze)
✅ 2. Problem Statement (vollständig)
✅ 3. Stakeholder-Analyse (Tabelle)
✅ 4. User & Zielgruppe (primär + sekundär)
✅ 5. Needs (Jobs, Pains, Gains)
✅ 6. Aktueller Prozess (Beschreibung)
✅ 7. Daten & Integration (Übersicht)
✅ 8. How Might We (mind. 1)
✅ 9. Lösungsidee (Kernidee, Features)
✅ 10. Value Proposition
✅ 11. Scope (In + Out + Annahmen)

OPTIONAL:
○ 12. Erfolgsmetriken (empfohlen)
```

### MVP (Vollständig)

```markdown
PFLICHT-SECTIONS (ALLE):
✅ 1. Executive Summary (2-3 Absätze)
✅ 2. Problem Statement (mit Auswirkungen quantifiziert)
✅ 3. Stakeholder-Analyse (vollständige Tabelle)
✅ 4. User & Zielgruppe (Personas mit Details)
✅ 5. Needs (Jobs, Pains, Gains - detailliert)
✅ 6. Aktueller Prozess (mit Pain Points)
✅ 7. Daten & Integration (detailliert)
✅ 8. How Might We (mind. 2)
✅ 9. Lösungsidee (Kernidee, Features, Wow-Feature)
✅ 10. Value Proposition (vollständig)
✅ 11. Scope (In + Out + Annahmen + Constraints)
✅ 12. Erfolgsmetriken (KPIs mit Zielwerten)
✅ 13. Nächste Schritte (mit offenen Fragen)
```

---

## 🔍 Section-Validierungen

### 1. Executive Summary

```markdown
CHECK:
✅ Problem in einem Satz beschrieben?
✅ Lösungsidee in einem Satz beschrieben?
✅ Erwarteter Impact/Nutzen genannt?

BEISPIEL - GUT:
"Das manuelle Erstellen von Berichten kostet das Team 10h/Woche. 
Eine automatisierte Lösung soll dies auf 1h reduzieren und 
Fehlerquote von 15% auf unter 2% senken."

BEISPIEL - SCHLECHT:
"Wir wollen die Berichtserstellung verbessern."
```

### 2. Problem Statement

```markdown
CHECK:
✅ Kontext/Hintergrund klar?
✅ Spezifisches Problem definiert (nicht vage)?
✅ Auswirkungen beschrieben? (PoC/MVP: quantifiziert)

BEISPIEL - GUT:
"Kontext: Sales-Team erstellt wöchentliche Pipeline-Reports.
Problem: Manuelle Datenaggregation aus 3 Systemen dauert 2h pro Report.
Auswirkung: 10h/Woche Zeitverlust, 15% Fehlerquote, verzögerte Entscheidungen."

BEISPIEL - SCHLECHT:
"Das Reporting ist ineffizient und muss verbessert werden."
```

### 4. User & Zielgruppe

```markdown
CHECK:
✅ Primäre Nutzergruppe identifiziert?
✅ Charakteristika beschrieben? (Tech-Level, Kontext)
✅ Aktuelle Situation beschrieben?
✅ Frustrationen/Pain Points genannt?

BEISPIEL - GUT:
"Primäre Nutzer: Sales Manager (5 Personen)
Charakteristika: Business User, Excel-versiert, kein SQL
Aktuelle Situation: Kopieren Daten manuell aus CRM, ERP, Excel
Frustrationen: Zeitaufwand, Fehleranfälligkeit, keine Echtzeit-Daten"

BEISPIEL - SCHLECHT:
"User sind Sales-Leute die Reports brauchen."
```

### 5. Needs & Jobs to be Done

```markdown
CHECK:
✅ Mindestens 2-3 funktionale Jobs genannt?
✅ Mindestens 2-3 Pains identifiziert?
✅ Mindestens 2-3 Gains beschrieben?

FORMAT:
Jobs: "Als [Rolle] muss ich [Tätigkeit] um [Ziel] zu erreichen"
Pains: Konkrete Hindernisse, Frustrationen, Risiken
Gains: Gewünschte Outcomes, Verbesserungen
```

### 8. How Might We

```markdown
CHECK:
✅ Mindestens 1 HMW-Frage formuliert? (PoC/MVP: mind. 2)
✅ Format: "Wie könnten wir [User] helfen, [Job] zu erledigen, ohne [Pain]?"
✅ Primäre HMW-Frage markiert?

BEISPIEL - GUT:
"Wie könnten wir Sales Managern helfen, Pipeline-Reports zu erstellen, 
ohne manuell Daten aus 3 Systemen zusammenzuführen?"

BEISPIEL - SCHLECHT:
"Wie können wir Reporting verbessern?"
```

### 9. Lösungsidee

```markdown
CHECK:
✅ Kernidee in 2-3 Sätzen beschrieben?
✅ High-Level Concept/Analogie vorhanden? (MVP)
✅ Key Features gelistet? (mind. 3)
✅ Wow-Feature identifiziert? (MVP)

KEY FEATURES FORMAT:
1. **[Feature Name]**: [1-Satz Beschreibung]
   - Löst: [Welchen Pain/Job]

BEISPIEL:
1. **Automatische Datenaggregation**: Zieht Daten aus CRM, ERP, Excel zusammen
   - Löst: Manuelles Kopieren (2h → 5min)
```

### 10. Value Proposition

```markdown
CHECK:
✅ Alle Platzhalter ausgefüllt?
✅ Differentiator klar?

FORMAT:
"Für [User], die [Problem] haben, 
ist unsere Lösung ein [Produkt-Kategorie], 
das [Key Benefit] bietet. 
Anders als [Alternative] ermöglicht unsere Lösung [Differentiator]."

BEISPIEL - GUT:
"Für Sales Manager, die wöchentlich Pipeline-Reports erstellen müssen,
ist unsere Lösung ein automatisiertes Reporting-Dashboard,
das Echtzeit-Daten aus allen Systemen aggregiert.
Anders als manuelle Excel-Reports ermöglicht unsere Lösung 
sofortige Aktualisierung und eliminiert Übertragungsfehler."
```

### 11. Scope & Priorisierung

```markdown
CHECK:
✅ In-Scope klar definiert? (mind. 3 Items)
✅ Out-of-Scope explizit genannt? (mind. 2 Items)
✅ Annahmen dokumentiert?
✅ Constraints genannt? (PoC/MVP)

WICHTIG FÜR RE:
- In-Scope → wird zu Epics/Features
- Out-of-Scope → explizit NICHT Teil des Projekts
- Annahmen → müssen validiert werden
- Constraints → beeinflussen Architektur-Entscheidungen
```

### 12. Erfolgsmetriken (PoC/MVP)

```markdown
CHECK:
✅ Mindestens 2-3 KPIs definiert?
✅ Baseline-Wert genannt? (aktueller Zustand)
✅ Zielwert definiert?

BEISPIEL - GUT:
- **Report-Erstellungszeit**: 2h → 5min (-96%)
- **Fehlerquote**: 15% → <2%
- **Aktualität**: Wöchentlich → Echtzeit

BEISPIEL - SCHLECHT:
- "Schnellere Reports"
- "Weniger Fehler"
```

---

## ✅ Übergabe-Checkliste an Requirements Engineer

Vor Übergabe an RE, validiere:

### Minimal (Simple Test)
```
- [ ] Problem ist klar und spezifisch
- [ ] Mindestens eine User-Gruppe definiert
- [ ] Key Features (High-Level) gelistet
- [ ] In-Scope definiert
```

### Standard (PoC)
```
- [ ] Problem ist klar und spezifisch
- [ ] User-Gruppe(n) mit Charakteristika definiert
- [ ] Needs/Pains/Gains erfasst
- [ ] How Might We-Frage formuliert
- [ ] Lösungsidee mit Key Features beschrieben
- [ ] Value Proposition formuliert
- [ ] In-Scope und Out-of-Scope definiert
- [ ] Annahmen dokumentiert
```

### Vollständig (MVP)
```
- [ ] Executive Summary enthält Problem, Lösung, Impact
- [ ] Problem Statement mit quantifizierten Auswirkungen
- [ ] Stakeholder-Tabelle vollständig
- [ ] User Personas mit Details
- [ ] Jobs/Pains/Gains detailliert
- [ ] Aktueller Prozess mit Pain Points
- [ ] Daten & Integrationen identifiziert
- [ ] How Might We-Fragen (mind. 2)
- [ ] Lösungsidee mit Wow-Feature
- [ ] Value Proposition vollständig
- [ ] Scope klar (In/Out/Annahmen/Constraints)
- [ ] KPIs mit Baseline und Zielwerten
- [ ] Offene Fragen für RE gelistet
```

---

## 🚫 Anti-Patterns im BA-Dokument

### ❌ Vage Problembeschreibung
```
FALSCH: "Das System ist langsam und unzuverlässig"
RICHTIG: "Die Ladezeit beträgt durchschnittlich 8 Sekunden, 
         Ziel sind <2 Sekunden. System ist 2x/Woche nicht erreichbar."
```

### ❌ Unspezifische User
```
FALSCH: "User sind Mitarbeiter"
RICHTIG: "Primäre User: Sales Manager (5), sekundär: CFO für Reports"
```

### ❌ Fehlende Priorisierung
```
FALSCH: Lange Feature-Liste ohne Priorisierung
RICHTIG: Must-Have (In-Scope) vs Nice-to-Have (Out-of-Scope) getrennt
```

### ❌ Technische Lösungen vorwegnehmen
```
FALSCH: "Wir brauchen eine React-App mit PostgreSQL-Backend"
RICHTIG: "Wir brauchen eine Web-Anwendung mit Datenpersistenz"
(Technologie-Entscheidungen sind Architekt-Domäne!)
```

### ❌ Keine messbaren Erfolgsmetriken
```
FALSCH: "Nutzer sollen zufriedener sein"
RICHTIG: "NPS soll von 30 auf 50 steigen"
```

---

## 📤 Handoff-Format an Requirements Engineer

```markdown
## 13. Nächste Schritte

✅ **Abgeschlossen**: Exploration & Ideation

⏭️ **Nächster Schritt**: Übergabe an Requirements Engineer

**Für Requirements Engineer**:
- Erstelle Epics basierend auf Section 9.3 (Key Features)
- Leite User Stories aus Section 4 (User) + Section 5 (Needs) ab
- Definiere NFRs basierend auf Section 11.4 (Constraints)
- Nutze Section 12 (KPIs) für Acceptance Criteria

**Offene Fragen für RE**:
- [Konkrete Frage 1 die RE klären sollte]
- [Konkrete Frage 2]

**Dokument-Referenz**:
- Problem Statement: Section 2
- User Context: Section 4
- Needs/Jobs: Section 5
- Key Features: Section 9.3
- Scope Boundaries: Section 11
```

---

## 📊 Qualitäts-Score

Bewerte das BA-Dokument vor Übergabe:

| Kriterium | Gewichtung | Score |
|-----------|------------|-------|
| Problem klar definiert | 20% | ⬜ |
| User identifiziert | 15% | ⬜ |
| Needs/Pains/Gains | 15% | ⬜ |
| Lösungsidee konkret | 20% | ⬜ |
| Scope definiert | 15% | ⬜ |
| Metriken vorhanden | 15% | ⬜ |

**Mindest-Score für Übergabe:**
- Simple Test: 60%
- PoC: 75%
- MVP: 90%

---

## 🔄 Feedback-Loop mit User

Wenn kritische Informationen fehlen:

```markdown
⚠️ Für ein vollständiges BA-Dokument fehlen noch:

- [ ] [Fehlende Information 1]
- [ ] [Fehlende Information 2]

Können wir diese Punkte noch klären, bevor ich an den 
Requirements Engineer übergebe?
```

---

**Version:** 1.0
**Focus:** Output-Qualität und RE-Handoff
**Quality Gate:** BA-Dokument Vollständigkeit
