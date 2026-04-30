---
type: epic-ba
epic: EPIC-NNN
project-ba: ../../analysis/BA-{PROJECT}.md
personas: [P1, P3a]
value-dimensions: [1, 3]
project-kpi-ref: [Problem-Solution-Fit, Portabilitaet]
status: Draft
created: YYYY-MM-DD
---

# Epic-BA: {Epic-Titel}

> Mini-BA zur Problem-Vertiefung auf Epic-Ebene. Personas, Value Prop
> und Nordstern werden referenziert, nicht wiederholt. Quelle fuer
> alle Produkt-Fakten: `{project-ba}`.
>
> Max. 80 Zeilen. Wenn groesser: Scope zerschneiden oder Inhalte nach
> oben (Projekt-BA) oder unten (Feature-Spec) ziehen.

---

## Referenzen (nur IDs, keine Duplikation)

- **Personas:** siehe Frontmatter `personas:`. Details in
  `{project-ba}` §2.
- **Value-Dimensionen adressiert:** siehe Frontmatter
  `value-dimensions:`. Vollstaendige Liste in `{project-ba}` §3.
- **Project-KPIs, auf die dieser Epic einzahlt:** siehe Frontmatter
  `project-kpi-ref:`. Definitionen in `{project-ba}` §8.

---

## 1. Teil-Problem (spezifisch fuer diesen Epic)

Ein Absatz, max 5 Zeilen. Was ist an **diesem** Ausschnitt des
Produkt-Problems neu oder besonders? Nicht das Produkt-Problem
wiederholen.

---

## 2. Jobs to be Done (pro adressierter Persona)

| Persona | JTBD                                                             |
| ------- | ---------------------------------------------------------------- |
| P1      | Wenn {Situation}, will ich {Wunsch}, damit {Outcome}.           |
| P3a     | Wenn {Situation}, will ich {Wunsch}, damit {Outcome}.           |

---

## 3. Epic-Hypothesen (3, falsifizierbar)

| ID  | Hypothese                                                                           | Test                                           |
| --- | ----------------------------------------------------------------------------------- | ---------------------------------------------- |
| H-{E}-1 | Wir nehmen an dass {Annahme}                                                    | {Wie falsifizieren: Messung, Pilot, Interview} |
| H-{E}-2 | Wir nehmen an dass {Annahme}                                                    | {Wie falsifizieren}                            |
| H-{E}-3 | Wir nehmen an dass {Annahme}                                                    | {Wie falsifizieren}                            |

---

## 4. Epic-KPIs (leading indicators)

Jede KPI verweist auf eine Project-KPI (Frontmatter `project-kpi-ref`).

| KPI                              | Baseline | Target | Messmethode           | Project-KPI-Bezug           |
| -------------------------------- | -------- | ------ | --------------------- | --------------------------- |
| {Leading Indicator}              | {x}      | {y}    | {Telemetrie / Survey} | {Name aus Project-BA §8}    |

---

## 5. Epic-Risiken (nur neu/epic-spezifisch)

Produkt-weite Risiken NICHT wiederholen.

| ID       | Risiko                                         | W'keit | Impact | Mitigation            |
| -------- | ---------------------------------------------- | ------ | ------ | --------------------- |
| R-{E}-1  | {Beschreibung}                                 | L/M/H  | L/M/H  | {Aktion}              |

---

## 6. Scope-Abgrenzung gegen Nachbar-Epics

- **Innerhalb:** {Was dieser Epic abdeckt}
- **NICHT hier (gehoert zu EPIC-XXX):** {Was bewusst ausgeschlossen ist}

---

Nachweis: `{project-ba}` (Produkt-Schicht). Weitere Details zu
einzelnen Features: `../features/FEATURE-*.md`.
