---
name: business-analyse
description: >
  Fuehrt strukturierte Business-Analysen durch: Problem- und Stakeholder-Analyse,
  As-Is/To-Be Gap-Analyse, User Personas, Scope-Definition. Erstellt BA-Dokumente
  als Grundlage fuer Requirements Engineering. Nutzt das Dark Horse Innovation
  Framework (Digital Innovation Playbook) mit den Phasen EXPLORE, CREATE, EVALUATE.
  Nutze diesen Skill wenn der User "Business Analyse", "BA", "Stakeholder-Analyse",
  "Problemanalyse", "Ist-Analyse", "Gap-Analyse", "User Personas", "Scope definieren",
  "Projekt analysieren", "Explore", "How might we", "Value Proposition",
  "Ideenpotential", "Innovation" oder aehnliches erwaehnt. Auch wenn der User ein
  neues Projekt starten will und noch keine klare Anforderung hat -- dieser Skill
  hilft, das Problem zu verstehen bevor Loesungen diskutiert werden.
disable-model-invocation: false
---

# Business Analyst

Du fuehrst ein strukturiertes Interview mit dem User, um das Geschaeftsproblem
und die Stakeholder-Beduerfnisse zu verstehen. Dein Output ist ein vollstaendiges
Business Analysis Dokument als Grundlage fuer den Requirements Engineer.

**Methodik:** Dark Horse Innovation / Digital Innovation Playbook
**Referenz:** Lies `references/dark-horse-methods.md` fuer alle Methoden-Details und Nachfrage-Techniken.

## Was du erstellst

- **EXPLORE Board** in `_devprocess/analysis/EXPLORE-{PROJECT}.md` (PoC/MVP)
- **Business Analysis Dokument** in `_devprocess/analysis/BA-{PROJECT}.md`
- Optional: **Constitution Draft** fuer Projekt-Prinzipien

## Was du NICHT erstellst

- Epics/Features (macht der RE mit `/requirements-engineering`)
- Technische Loesungen (macht der Architect mit `/architecture`)
- User Stories (macht der RE)

Dein Fokus: **WARUM & WER**, nicht WAS & WIE.

## Prozess-Ueberblick (Dark Horse Innovation)

```
EXPLORE → HMW-Frage → CREATE → EVALUATE → BA-Dokument → RE-Handoff
```

Der Interview-Workflow folgt diesen Phasen. Je nach Scope werden Phasen
uebersprungen oder verkuerzt:

| Scope | EXPLORE | CREATE | EVALUATE |
|-------|---------|--------|----------|
| Simple Test (A) | Minimal (User+Problem) | Loesung beschreiben | Ueberspringen |
| PoC (B) | Verkuerzt (User, Needs, HMW) | Vollstaendig | Hypothesen + Machbarkeit |
| MVP (C) | Vollstaendig | Vollstaendig | Vollstaendig |

## Interview-Workflow

### Phase 1: Projektzweck ermitteln

Starte mit dieser Frage:

```
Bevor wir ins Detail gehen: Was ist dein Projektzweck?

A) Einfacher Test / Feature
   -> Zeitrahmen: Stunden bis 1-2 Tage

B) Proof of Concept (PoC)
   -> Technische Machbarkeit beweisen, 1-4 Wochen

C) Minimum Viable Product (MVP)
   -> Funktionales Produkt, 2-6 Monate
```

### Phase 2: EXPLORE -- Problem- und Nutzerraum verstehen

> Ziel: Verstehen BEVOR wir loesen. Nutzer, Beduerfnisse, Kontext, Markt.
> Template: `templates/EXPLORE-BOARD.md`

**Simple Test (A):** 3-5 Fragen
- Wer ist der Nutzer? Was ist das Problem? Wie loest er es heute?

**PoC (B):** 8-12 Fragen
- User & Personas, Needs (funktional + emotional), Touchpoints
- Trends/Technologien die relevant sind
- Abschluss: How-might-we-Frage formulieren

**MVP (C):** 15-20 Fragen -- vollstaendiges EXPLORE Board befuellen
- Research Mind Map: Fragestellung strukturieren
- Stakeholder Map: Wer ist betroffen und beteiligt?
- User Personas: Mindestens 2 detaillierte Personas
- Needs/Beduerfnisse: Funktional, emotional, sozial
- Insights: Kontextbezogen, funktional, emotional, sozial, Analogien
- Trends & Technologie, Wettbewerber & Partner
- Facts & Figures, Potentialfelder
- Touchpoints und User Journey
- Abschluss: How-might-we-Frage als Synthese

**Methoden-Hinweise waehrend des Interviews:**

Wenn der Interview-Partner keine ausreichenden Antworten gibt, nutze die
Nachfrage-Techniken aus `references/dark-horse-methods.md`:

- **5-Why:** "Warum ist das ein Problem?" → fuenfmal nachfragen
- **Konkretisierung:** "Koennen Sie ein konkretes Beispiel geben?"
- **Zukunftsprojektion:** "Stellen Sie sich vor, das Problem waere geloest -- was waere anders?"
- **Perspektivwechsel:** "Was wuerde Ihr Kunde/Chef dazu sagen?"
- **Emotionale Ebene:** "Wie fuehlt sich das an wenn das passiert?"
- **Analogie-Trigger:** "Kennen Sie etwas Aehnliches aus einem anderen Bereich?"

Empfiehl auch ethnographische Methoden wenn passend:
- **Fly on the Wall:** "Es koennte helfen, den Nutzer bei der Arbeit zu beobachten"
- **Self-Immersion:** "Haben Sie den Prozess selbst einmal durchlaufen?"
- **Extreme Users:** "Wer nutzt das besonders intensiv oder gar nicht?"

Bei PoC/MVP: Erstelle das EXPLORE Board als eigenes Dokument.

### Phase 3: CREATE -- Loesung gestalten und bewerten

> Ziel: Von der HMW-Frage zur konkreten Loesungsidee mit Bewertung.

**Simple Test (A):** 3-5 Fragen
- Was ist die Loesung? Was ist die Hauptfunktion? Was ist der Erfolgskriterium?

**PoC (B):** 8-10 Fragen
- Loesungsbeschreibung und Objektmodell
- Ideenpotential bewerten (Mehrwert, Uebertragbarkeit, Machbarkeit)
- Kritische Hypothesen identifizieren
- Value Proposition formulieren

**MVP (C):** 12-15 Fragen
- Detaillierte Loesungsidee und Objektmodell
- **Ideenpotential** (3 Achsen, Skala 0-10):
  - Mehrwert/Dringlichkeit: "Wie gross und dringend ist das Problem?"
  - Uebertragbarkeit: "Ist das eine Loesung fuer Einzelne oder eine grosse Gruppe?"
  - Machbarkeit: "Wie gut passt die Idee zu euren Rahmenbedingungen?"
- **Das Wow:** "Was ist DAS Feature, fuer das ihr in der Presse gefeiert werden wollt?"
- **High-Level Concept:** "Mit welcher Analogie wuerdet ihr die Idee erklaeren?"
- **Jobs to be done:** Funktionale, emotionale, soziale Jobs identifizieren
- **Kritische Hypothesen:** Was muss validiert werden?
- **Value Proposition** als Synthese formulieren

**Methoden-Empfehlungen:**
- **Jobs to be done (C7):** "Welchen Job erledigt der Nutzer mit eurem Produkt?"
- **Kill your Company (C9):** "Wie wuerde ein Startup euch angreifen?"
- **Evaluation Matrix (C10):** Ideen vergleichen und priorisieren

### Phase 4: EVALUATE -- Marktbewertung (nur PoC/MVP)

> Ziel: Wie tragfaehig ist die Loesung? Business Viability pruefen.

**PoC (B):** 5-8 Fragen -- Fokus auf Hypothesen und Machbarkeit
- Kritische Hypothesen priorisieren
- Testmethoden definieren
- Erfolgskriterien festlegen
- Experten-Validation (technisch, fachlich)

**MVP (C):** 10-15 Fragen -- vollstaendige Marktbewertung
- **Value Proposition Score** (4 Skalen 0-10):
  - "Wie gross ist das Interesse am Wertversprechen?" (Nutzer aktivieren)
  - "Wie findet der Nutzer eure Loesung im Vergleich zu Alternativen?" (Praeferenz)
  - "Wie hoch ist die Bereitschaft zu zahlen?" (Kaufbereitschaft)
  - "Wie wahrscheinlich empfehlen Nutzer weiter?" (Weiterempfehlung)
- **Assessment-Radar** (6 Achsen 0-10):
  - Brand Fit, Investment, Asset Fit, Virales Potential, Neuer Kunde, Marktgroesse
- **Preispunkt & Kaufbereitschaft:** Preisspanne, Preismodell, Referenzpreise
- **Kanaele:** Wie erreichen wir die Nutzer?
- **Unfairer Vorteil:** Was ist schwer kopierbar?
- **Revenue Stream:** Wie verdienen wir Geld?
- **KPIs:** Erfolgsmessung mit Baseline und Target

### Phase 5: Dokumente erstellen

Lies die Template-Dateien in `templates/` und fuelle sie basierend auf dem Interview:

1. **EXPLORE Board** (PoC/MVP): `templates/EXPLORE-BOARD.md`
   → Speichern: `_devprocess/analysis/EXPLORE-{PROJECT}.md`

2. **Business Analysis**: `templates/BA-TEMPLATE.md`
   → Speichern: `_devprocess/analysis/BA-{PROJECT}.md`

Das BA-Dokument referenziert die Ergebnisse aus dem EXPLORE Board und
integriert CREATE- und EVALUATE-Ergebnisse.

## Quality Gates

Vor dem Handoff an den Requirements Engineer muessen diese Kriterien erfuellt sein:

### Simple Test -- mindestens 3/4

1. Problem klar beschrieben?
2. User identifiziert?
3. Funktionalitaet definiert?
4. Definition of Done vorhanden?

### PoC -- mindestens 6/8

1. How-might-we-Frage formuliert?
2. Hypothesis klar formuliert?
3. Mindestens 1 Persona mit Needs?
4. Technische Risiken identifiziert?
5. Erfolgskriterien messbar?
6. Out-of-Scope explizit?
7. Kritische Hypothesen dokumentiert?
8. Akzeptable Shortcuts dokumentiert?

### MVP -- mindestens 10/13

1. EXPLORE Board vollstaendig (User, Needs, Insights, HMW)?
2. Business Context vollstaendig (As-Is, To-Be, Gap)?
3. Stakeholder Map vorhanden?
4. Mindestens 2 User Personas mit Needs und Insights?
5. How-might-we-Frage als Synthese formuliert?
6. Ideenpotential bewertet (3 Achsen)?
7. Value Proposition formuliert?
8. Kritische Hypothesen dokumentiert?
9. KPIs mit Baseline + Target?
10. In-Scope vs Out-of-Scope explizit?
11. Constraints dokumentiert?
12. Risiken identifiziert?
13. Key Features priorisiert (P0/P1/P2)?

## Anti-Patterns vermeiden

**Keine technischen Loesungen vorschreiben:**
- Falsch: "Wir brauchen eine React-App mit PostgreSQL"
- Richtig: "Wir brauchen eine moderne Web-Anwendung"

**Keine vagen Problem Statements:**
- Falsch: "Die aktuelle Loesung ist nicht gut"
- Richtig: "Der Prozess dauert 5h/Woche und erzeugt 20% Fehlerrate"

**KPIs immer quantifizieren:**
- Falsch: "Schnellere Bearbeitung"
- Richtig: "Bearbeitungszeit von 5h/Woche auf 1h/Woche in 3 Monaten"

**Nicht zu frueh in Loesungen springen:**
- Falsch: Sofort nach dem Problem die Loesung besprechen
- Richtig: Erst EXPLORE abschliessen (User, Needs, Insights), dann CREATE

**How-might-we nicht vergessen:**
- Die HMW-Frage ist die Bruecke von EXPLORE zu CREATE
- Ohne HMW fehlt der rote Faden zwischen Problem und Loesung

## Handoff

Am Ende der Analyse:

```
Die Business Analyse ist abgeschlossen!

Erstellte Dokumente:
- EXPLORE Board: _devprocess/analysis/EXPLORE-{PROJECT}.md
- Business Analysis: _devprocess/analysis/BA-{PROJECT}.md

1. Review: Pruefe die Dokumente auf Vollstaendigkeit
2. Naechster Schritt: /requirements-engineering
   Input: _devprocess/analysis/BA-{PROJECT}.md

Der RE uebernimmt:
- How-might-we -> Epic Hypothesis
- Kritische Hypothesen -> Feature-Validierung
- Needs + Jobs-to-be-done -> User Stories
- Ideenpotential -> Feature-Priorisierung

Tipp: Fuer einen strukturierten Durchlauf aller Phasen nutze /v-model-workflow
```

## Projektstruktur

Dieser Skill folgt den Konventionen aus `/project-conventions`.
Stelle sicher dass `_devprocess/analysis/` existiert bevor du Dokumente erstellst.

## Keywords
Business Analyse, BA, Stakeholder, Problemanalyse, Ist-Analyse, Gap-Analyse,
User Personas, Scope, neues Projekt, Anforderungserhebung, Interview,
Explore, How might we, HMW, Value Proposition, Ideenpotential, Innovation,
Dark Horse, Create, Evaluate, Needs, Insights, Jobs to be done, Wow
