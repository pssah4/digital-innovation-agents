# V-Model-Artefakt-Graph - Invarianten

Single Source of Truth fuer die Konsistenz-Invarianten, die der Skill
`/consistency-check` und alle anderen V-Model-Skills einhalten. Jede
Invariante hat eine ID (`N-n` fuer Node-Invarianten, `E-n` fuer Edge-
Invarianten, `S-n` fuer semantische Invarianten), einen Text und eine
Pruefregel.

Wenn ein V-Model-Skill diese Datei aktualisiert, muss `/consistency-check`
Mode A entsprechend angepasst werden.

## Graph-Modell

**Knoten (Artefakt-Typen):**

- `Project-BA` - `docs/analysis/BA-{PROJECT}.md` (One-Pager, Produkt-Schicht)
- `Epic-BA` - `docs/requirements/epics/EPIC-{NNN}-ba.md` (Mini, optional pro Epic)
- `BA-Section` - eine Ueberschrift in `Project-BA` oder `Epic-BA`
  (Personas, JTBDs, Problem, Value Props, KPIs, Risks, usw.)
- `Epic` - `docs/requirements/epics/EPIC-{NNN}-{slug}.md`
- `Feature` - `docs/requirements/features/FEATURE-*.md`
- `SC` - eine Zeile in der Success-Criteria-Tabelle eines Features
- `ADR` - `docs/adr/ADR-{NNN}-{slug}.md`
- `arc42-Section` - eine Ueberschrift in
  `docs/architecture/arc42.md` (§1..§12)
- `PLAN` - `docs/implementation/plans/PLAN-{NNN}-{slug}.md`
- `BL-Item` - eine Zeile in `docs/context/10_backlog.md`
- `Code` - eine Datei oder Zeilenspanne unter `src/`

**Kanten (Referenz-Typen):**

- `Project-BA.Persona -> Epic-BA` (Epic-BA referenziert Persona-ID)
- `Epic-BA -> Epic` (erklaert: Epic-BA liefert Problem-Vertiefung)
- `Epic-BA.KPI -> Project-BA.KPI` (einzahlend: Frontmatter `project-kpi-ref`)
- `BA.Persona -> Epic` (Zugehoerigkeit: welches Epic adressiert welche Persona)
- `BA.JTBD -> Feature` (adressiert: welcher JTBD wird durch welches Feature geloest)
- `Epic -> Feature` (enthaelt: MVP-Features-Tabelle im Epic)
- `Feature -> SC` (hat: Success-Criteria-Tabelle im Feature)
- `Feature -> ADR` (referenziert: Related-ADRs-Abschnitt im Feature)
- `Feature -> Code` (implementiert: Source-Pfade im Feature)
- `ADR -> arc42-Section` (belegt: arc42 §9 Tabelle)
- `ADR -> ADR` (supersedes / related)
- `PLAN -> Feature` (realisiert: feature-refs im PLAN-Frontmatter)
- `PLAN -> ADR` (realisiert: adr-refs im PLAN-Frontmatter)
- `BL-Item -> (Feature | ADR | Bug | PLAN | Code)` (zeigt auf)

## Node-Invarianten

| ID   | Invariante                                                                              | Pruefregel                                                                 |
| ---- | --------------------------------------------------------------------------------------- | -------------------------------------------------------------------------- |
| N-1  | Jedes Feature hat genau einen Epic-Parent.                                              | Feature-Frontmatter oder -Header enthaelt `Epic:` Link zu existierendem Epic. |
| N-2  | Jedes Epic hat mindestens ein Feature in MVP-Tabelle oder ist `Phase: Candidates`.         | Epic-Datei `## MVP Features` Tabelle ist nicht leer, oder Phase-Candidates-Marker vorhanden. |
| N-3  | Jede ADR ist mindestens einmal referenziert (Feature, arc42 oder Backlog).              | Grep nach ADR-ID in allen Features, arc42, Backlog.                       |
| N-4  | Jedes Feature hat mindestens einen Success-Criterion-Eintrag (Platzhalter erlaubt).     | Feature `## Success Criteria`-Tabelle hat mind. eine Zeile, auch `[AWAITING BA]` ist gueltig. |
| N-5  | Jedes Feature mit `status: Implemented` hat einen `## Codebase-Verifikation` Abschnitt. | Section-Header existiert.                                                  |
| N-6  | Jedes BL-Item hat ein Phase-Label (`Released | Building | Planned | Candidates`).       | Spalte oder Notizen-Prefix `[Phase: ...]` vorhanden.                       |
| N-7  | Jedes BL-Item mit `Phase: Candidates` hat `needs refinement: {Grund}`-Marker.           | Notizen-Feld enthaelt den Marker.                                          |
| N-8  | Epic-BA definiert keine Personas, Value-Dimensionen oder Nordstern - referenziert sie nur via ID. | Epic-BA enthaelt keine `## Personas`-Section mit Persona-Definitionen; `personas:` im Frontmatter listet nur IDs, die in Project-BA §2 existieren. |
| N-9  | Jede Epic-KPI im Epic-BA hat einen `project-kpi-ref:`-Eintrag im Frontmatter, der auf eine KPI in Project-BA referenziert. | Frontmatter-Feld `project-kpi-ref` vorhanden, Wert matcht einen KPI-Namen im Project-BA. |
| N-10 | Jedes Feature-Frontmatter enthaelt `phase: Released|Building|Planned|Candidates` und `status: <Arbeitsstatus>`. | YAML-Frontmatter parsen, Pflicht-Felder pruefen. |
| N-11 | Jedes Epic-Frontmatter enthaelt `phase: Released|Building|Planned|Candidates`. | YAML-Frontmatter parsen, Pflicht-Feld pruefen. |
| N-12 | Jedes ADR-Frontmatter enthaelt `status: Proposed|Accepted|Superseded|Deprecated` und `phase: Released|Building|Planned|Candidates`. | YAML-Frontmatter parsen, beide Felder pruefen. |

## Edge-Invarianten

| ID  | Invariante                                                                         | Pruefregel                                                                                 |
| --- | ---------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------ |
| E-1 | Jeder Markdown-Link auf projekt-interne Pfade ist gueltig.                         | Regex auf `](docs/...)`, `](../...)`, `](src/...)`, Pfad-Existenz-Check.                   |
| E-2 | Jeder `Source (Implementation)`-Pfad im Feature existiert oder Phase in {Planned, Candidates}.      | Feature-Source-Pfade vs. Dateisystem.                                                      |
| E-3 | Jede ADR in Feature `Related-ADRs` existiert unter `docs/adr/`.                    | ADR-IDs vs. `docs/adr/`-Inhalt.                                                            |
| E-4 | Jede ADR in arc42 §9 Tabelle existiert unter `docs/adr/`.                          | arc42 §9 Zeilen vs. `docs/adr/`-Inhalt.                                                    |
| E-5 | Jede ADR unter `docs/adr/` ist in arc42 §9 Tabelle ODER als deprecated markiert.   | `docs/adr/`-Inhalt vs. arc42 §9.                                                           |
| E-6 | Jede BL-Item-Zeile mit Feature/ADR/PLAN-Spalte zeigt auf existierendes Artefakt.   | Link-Check pro Zeile.                                                                      |
| E-7 | Backlog-Feature-Zeile `Phase` stimmt mit Feature-Frontmatter `phase:` ueberein.   | Fuer jedes FEATURE-NNN: Feature-Tabellenzeile im Backlog vs `phase:` im Frontmatter.       |
| E-8 | Backlog-Epic-Header `Phase: ...` stimmt mit Epic-Frontmatter `phase:` ueberein.   | Fuer jedes EPIC-NNN: Header-Zeile `Phase: X` im Backlog vs `phase:` im Frontmatter.        |
| E-9 | Dashboard-Counts im Backlog stimmen mit Summe der Feature-/Epic-/Chore-Phasen ueberein. | Dashboard-Tabelle neu berechnen aus Frontmatters + Standalone-Chores-Tabelle.         |

## Semantische Invarianten (Mode B, nur on-demand)

| ID  | Invariante                                                                        | Pruefregel                                                                                 |
| --- | --------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------ |
| S-1 | Feature-Beschreibung widerspricht nicht den referenzierten ADRs.                  | Subagent liest Feature + alle Related ADRs, meldet inhaltliche Widersprueche.              |
| S-2 | Feature ohne passendes BA-JTBD ist explizit geflaggt.                             | Subagent prueft: hat das Feature einen JTBD-Verweis in BA? Wenn nein, BL-Item `needs BA-anchor`. |
| S-3 | arc42-Sektion zur ADR-Decision spiegelt aktuellen ADR-Text, nicht eine alte Revision. | Subagent liest arc42-Sektion + zitierte ADR, meldet Drift.                                 |
| S-4 | Features mit `status: Implemented` haben ihre SCs plausibel im Code belegbar.     | Subagent stichprobenartig pro Feature; Ergebnis im Codebase-Verifikations-Abschnitt.       |

## Phase/Status-Frontmatter-Konvention (verbindlich fuer alle Skills)

**Pflichtfelder im YAML-Frontmatter:**

| Artefakt | Pflichtfelder                                                           | Default beim Anlegen            |
| -------- | ----------------------------------------------------------------------- | ------------------------------- |
| Feature  | `phase: <Lebenszyklus>`, `status: <Arbeitsstatus>`                      | `phase: Building`, `status: Planned` |
| Epic     | `phase: <Lebenszyklus>`                                                 | `phase: Building` (abgeleitet worst-wins) |
| ADR      | `phase: <Lebenszyklus>`, `status: Proposed|Accepted|Superseded|Deprecated` | `phase: Building`, `status: Proposed` |
| PLAN     | `status: Draft|Active|Completed`                                        | `status: Draft`                 |
| BL-Item  | Phase-Spalte in Backlog-Tabelle                                         | `Building`                      |

**Phase-Werte (Enum):** `Released | Building | Planned | Candidates`.
Siehe Phase-Schema-Konvention unten fuer Semantik.

**Status-Werte:**

- Feature-Status: `Planned | Observed | Implemented | Done`
- ADR-Status (MADR): `Proposed | Accepted | Superseded | Deprecated`
- PLAN-Status: `Draft | Active | Completed`

**Single Source of Truth:** Das YAML-Frontmatter des Artefakts ist die
Wahrheit. Backlog-Zeilen sind Projektionen davon und muessen beim
Aendern synchron nachgezogen werden.

**Sync-Pflicht beim Aendern von `phase:` oder `status:` in einem Artefakt:**

1. Frontmatter im Artefakt aktualisieren.
2. Backlog-Zeile des Artefakts aktualisieren (Feature-Tabellenzeile
   unter dem Epic-Abschnitt, bzw. Epic-Header `Phase: X`).
3. Wenn Epic-Phase neu abgeleitet werden muss (worst-wins ueber
   Features): Epic-Frontmatter und Epic-Header-Zeile im Backlog
   aktualisieren.
4. Dashboard-Counts im Backlog (Phase-Tabelle) neu berechnen.
5. Epic-KPI-Referenzen (falls betroffen) pruefen.

Diese Sync-Kette wird in Skills `requirements-engineering`,
`architecture`, `coding`, `reverse-engineering` ohne Rueckfrage
ausgefuehrt. `/consistency-check` pruft sie ueber N-10, N-11, N-12,
E-7, E-8, E-9.

**Worst-Wins fuer Epic-Phase:**

`Released < Building < Planned < Candidates` (niedriger = weiter
fortgeschritten). Epic-Phase = maximales Rank-Level der enthaltenen
Features. Ein einziges Building-Feature macht das Epic Building.
Details siehe "Ableitung" im Phase-Schema-Abschnitt.

---

## Phase-Schema-Konvention (2026-04-20, aktualisiert)

Jedes Feature traegt eine **Phase**. Features sind die primaere
Quelle der Phase-Zuordnung. Epics/ADRs/PLANs/BL-Items erben ihre
Phase vom Feature-Graph (Details siehe "Ableitung" unten).

- `Released` - vollstaendig implementiert, ausgeliefert und gegen
  Codebase verifiziert. Alle SCs im Code belegt UND alle
  referenzierten ADRs ebenfalls Released.
- `Building` - in aktiver Umsetzung oder umsetzungsreif; Scope, AK
  und Abhaengigkeiten geklaert.
- `Planned` - vorgesehen, noch nicht gestartet. Refinement
  weitgehend vorhanden.
- `Candidates` - Ideen und Optionen ohne verbindliche Zusage.
  Refinement ausstehend. `needs refinement: {Grund}` Pflicht.
  Moegliche Gruende: `Analyse fehlt`, `Zielgruppe unklar`,
  `Scope offen`, `Architektur offen`, `Baseline-Messung fehlt`.

**Ableitung:**

- **Feature-Phase**: aus `Codebase-Verifikation` (direkte Angabe).
  Downgrade: wenn ein referenzierter ADR nicht Released ist, ist das
  Feature maximal Building, nicht Released.
- **Epic-Phase**: worst-wins ueber alle enthaltenen Features (ein
  Building unter den Features -> Epic Building).
- **ADR-Phase**: Phase des Features, das auf es zeigt; bei mehreren
  Owner-Features worst-wins. Orphan-ADRs fallen in Candidates.
- **PLAN-Phase**: Phase des Features, das der PLAN realisiert.
- **BL-Item-Phase**: Phase des Features (oder ADRs), das das BL-Item
  referenziert.

**Legacy-Mapping** (fuer Projekte mit alten Phase-Labels, automatisch
durch `/consistency-check` und den Graph-Viewer gemappt):

- `Fertig` -> `Released`
- `Umsetzung` -> `Building`
- `Roadmap` -> `Planned`
- Neu: `Candidates` (frueher implizit in Roadmap enthalten).

## Wie Skills mit diesen Invarianten umgehen

- `/reverse-engineering` Phase 8: ruft `/consistency-check` im Mode A
  auf, behandelt gefundene Luecken als Phase-8-Output.
- `/requirements-engineering`: erzeugt Features so, dass N-1, N-4
  eingehalten werden. Verweist auf Epic-ID und legt SCs an (mind. als
  Platzhalter).
- `/architecture`: erzeugt ADRs so, dass N-3, E-5 nicht verletzt
  werden (arc42 §9 Tabelle wird aktualisiert beim Anlegen einer neuen
  ADR).
- `/coding`: fuehrt Mid-Course Feature-Capture-Dialog wenn neue
  user-facing Capabilities hinzukommen (N-1, N-4, BA-Anker).
- `/v-model-workflow`: ruft `/consistency-check` beim Start (Mode A)
  und bei Release-Closure (Mode A+B).
- `/consistency-check`: liest alle Invarianten aus dieser Datei und
  prueft sie. Ergebnisse landen in der Graph-Health-Sektion des
  Backlogs plus als BL-Items.

## Aenderungs-Protokoll

Wer diese Datei aendert, muss `/consistency-check` Mode A
nachziehen, damit die neuen Invarianten auch wirklich geprueft werden.
Ohne Code-Update im Skill bleibt die Invariante nur dokumentiert,
nicht enforced.
