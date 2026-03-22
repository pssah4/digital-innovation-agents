---
name: coding
description: >
  Uebergabe-Skill: Laedt plan-context.md und alle Entwurfsartefakte, fuehrt einen
  kritischen Review durch, und sorgt fuer kontinuierliche Rueckschreibung in die
  Artefakte waehrend und nach der Implementierung. Nutze diesen Skill wenn der User
  "implementieren", "coden", "plan-context umsetzen", "Feature bauen" oder aehnliches
  erwaehnt und ein plan-context.md oder Feature-Specs vorliegen. Dieser Skill
  uebernimmt NICHT den Coding-Workflow -- der Default Claude Code Agent bleibt
  dafuer zustaendig. Der Skill stellt sicher, dass der Kontext kritisch geprueft,
  sauber uebergeben und die Artefakte immer aktuell gehalten werden.
disable-model-invocation: false
---

# Coding -- Review, Uebergabe & Living Documents

Dieser Skill hat drei Aufgaben:

1. **Kontext laden** aus den Entwurfsphasen
2. **Kritisch reviewen** bevor implementiert wird
3. **Kontinuierlich rueckschreiben** damit Artefakte immer den Ist-Zustand reflektieren

Die eigentliche Implementierung macht der Default Claude Code Agent.

---

## Phase 1: Kontext laden

Lies diese Dokumente in dieser Reihenfolge:

```
PFLICHT:
1. _devprocess/requirements/handoff/plan-context.md    (Primaer-Input)
2. _devprocess/architecture/ADR-*.md                   (Architektur-Entscheidungen)
3. _devprocess/requirements/features/FEATURE-*.md      (Feature-Details + Success Criteria)
4. CLAUDE.md                                           (Projekt-spezifische Regeln)

OPTIONAL (wenn vorhanden):
5. _devprocess/architecture/arc42.md                   (Gesamtarchitektur)
6. _devprocess/requirements/epics/EPIC-*.md            (Strategischer Kontext)
7. memory/MEMORY.md                                    (Architektur-Eckdaten)
```

Falls kein plan-context.md vorhanden:

```
Kein plan-context.md gefunden. Optionen:

A) Ich habe FEATURE-*.md Dateien -- arbeite direkt damit
B) Ich moechte den V-Model Workflow durchlaufen -> /v-model-workflow
C) Ich habe eine informelle Beschreibung -- arbeite damit
```

---

## Phase 2: Kritischer Review

BEVOR ein Implementierungsplan erstellt wird, pruefe die Entwurfsartefakte
kritisch gegen die reale Codebase. Das ist der wichtigste Schritt.

### 2a: Codebase-Abgleich

Lies die bestehende Codebase und pruefe:

- Passen die ADR-Vorschlaege zur realen Architektur?
- Gibt es bestehende Patterns die den Vorschlaegen widersprechen?
- Sind die Tech-Stack-Annahmen in plan-context.md korrekt?
- Fehlen Abhaengigkeiten oder Constraints die nicht beruecksichtigt wurden?
- Gibt es Module die von den geplanten Aenderungen betroffen waeren,
  aber in der Architektur nicht beruecksichtigt sind?

### 2b: Review-Ergebnis ausgeben

```
=== Kritischer Review: {Projekt/Feature} ===

Tech Stack: {aus plan-context.md, mit Korrekturen wenn noetig}
ADRs: {Anzahl} geprueft
Features: {Anzahl} geprueft
Success Criteria: {Anzahl} zu verifizieren

--- Codebase-Abgleich ---

BESTAETIGT (passt zur Codebase):
- ADR-001: {Title} -- Vorschlag passt, {Begruendung}
- FEATURE-001 SC-01: {Criterion} -- realistisch

AENDERUNGSBEDARF (Abweichung zur Codebase):
- ADR-002: {Title} -- Vorschlag: {Original}
  Problem: {Was nicht passt}
  Empfehlung: {Was stattdessen}
- FEATURE-003 SC-02: {Criterion}
  Problem: {Warum nicht wie spezifiziert umsetzbar}
  Empfehlung: {Alternative}

FEHLEND (in Entwuerfen nicht beruecksichtigt):
- {Modul/Pattern das betroffen ist aber nicht adressiert wurde}

RISIKEN:
- {Risiko 1}: {Beschreibung und Mitigation}

--- Entscheidungen ---

Bitte bestaetige oder korrigiere die Aenderungsvorschlaege bevor
ich den Implementierungsplan erstelle.
```

### 2c: Aenderungen zurueckschreiben

Jede Aenderung aus dem Review wird SOFORT in die Quell-Artefakte
zurueckgeschrieben, BEVOR die Implementierung beginnt:

- **ADR geaendert** -> ADR-Datei aktualisieren:
  - Decision Section anpassen
  - Status -> `Accepted (modified by review)`
  - Begruendung der Aenderung dokumentieren
- **ADR abgelehnt** -> ADR-Datei aktualisieren:
  - Status -> `Deprecated`
  - Begruendung und Verweis auf Alternative
- **Feature SC geaendert** -> FEATURE-Datei aktualisieren:
  - Success Criteria anpassen
  - Aenderungsgrund als Kommentar
- **plan-context.md korrigiert** -> Datei aktualisieren
- **Neues ADR noetig** -> Neue ADR-Datei erstellen

Nach dem Zurueckschreiben: Zusammenfassung der geaenderten Dateien ausgeben.

---

## Phase 3: Implementierung (Default Claude Code Agent)

Nach dem Review wird die Implementierung an den Default Claude Code Agent
uebergeben. Dieser Skill schreibt nicht vor, WIE implementiert wird.

### Kontinuierliche Rueckschreibung waehrend der Implementierung

Wenn waehrend der Implementierung Aenderungen an der geplanten Architektur
oder den Features noetig werden, SOFORT zurueckschreiben:

**Bei jeder Abweichung vom Plan:**

```
Aenderung waehrend Implementierung:

WAS: {Was hat sich geaendert}
WARUM: {Warum war die Aenderung noetig}
BETROFFENE ARTEFAKTE:
- {ADR-XXX}: {Was angepasst wird}
- {FEATURE-XXX}: {Was angepasst wird}

Schreibe ich die Aenderungen jetzt in die Artefakte zurueck? [J/N]
```

**Trigger fuer Rueckschreibung:**
- Technische Entscheidung weicht von ADR ab
- Success Criterion ist nicht wie spezifiziert umsetzbar
- Neues Pattern oder neue Abhaengigkeit eingefuehrt
- Scope-Aenderung (Feature groesser/kleiner als geplant)
- Unerwartete Constraint entdeckt

**Was zurueckgeschrieben wird:**
- ADR: Decision, Status, Implementation Notes
- FEATURE: Success Criteria, Technical NFRs, Definition of Done
- plan-context.md: Tech Stack, Integrations (wenn grundlegend geaendert)
- arc42: Betroffene Sections (wenn Architektur sich aendert)

---

## Phase 4: Abschluss -- Finale Synchronisation

Nach Abschluss der Implementierung, finale Pruefung:

```
PFLICHT -- Artefakte muessen den Ist-Zustand reflektieren:

1. Feature-Specs:
   - Status -> "Implemented"
   - How-It-Works Section ergaenzen (Key Files, Dependencies)
   - Success Criteria als verifiziert markieren (oder angepasst wenn geaendert)
   - Nicht-umgesetzte Criteria explizit dokumentieren mit Begruendung

2. ADRs:
   - Alle Status finalisiert (Accepted / Accepted (modified) / Deprecated)
   - Implementation Notes mit tatsaechlicher Umsetzung ergaenzen
   - Abweichungen vom urspruenglichen Vorschlag dokumentiert

3. Backlog:
   - _devprocess/context/10_backlog.md aktualisieren
   - Neue Erkenntnisse/Findings eintragen

BEI BEDARF:
4. plan-context.md: Aktualisieren wenn Tech Stack sich geaendert hat
5. arc42: Betroffene Sections aktualisieren
6. memory/MEMORY.md: Wenn Architektur-Eckdaten sich geaendert haben
7. CLAUDE.md: Wenn neue Projekt-Konventionen entstanden sind
```

### Abschluss-Zusammenfassung

```
Implementierung abgeschlossen!

Artefakt-Status:
- {N} Features aktualisiert (Status: Implemented)
- {N} ADRs finalisiert ({N} accepted, {N} modified, {N} deprecated)
- {N} Artefakte waehrend der Implementierung zurueckgeschrieben
- Backlog aktualisiert

Abweichungen vom urspruenglichen Entwurf:
- {Zusammenfassung der wichtigsten Aenderungen, oder "Keine"}

Empfohlene naechste Schritte:
  /testing -- Unit & Integration Tests erstellen/aktualisieren
  /security-audit -- Security Review der Codebase

Tipp: Fuer einen strukturierten Durchlauf aller Phasen nutze /v-model-workflow
```

---

## Kernprinzip: Living Documents

Die Artefakte (ADRs, Features, plan-context.md, arc42) sind KEINE
Einmal-Spezifikationen. Sie werden kontinuierlich aktualisiert und
reflektieren am Ende immer den tatsaechlich implementierten Zustand.

```
Entwurf -> Review (Korrekturen) -> Implementierung (laufende Updates) -> Finale Sync
   ^              |                        |                                  |
   |              v                        v                                  v
   |         Artefakte              Artefakte                          Artefakte
   |         angepasst              angepasst                          finalisiert
   |                                                                        |
   +------ Dokumentation == Code (immer synchron) <-------------------------+
```

## Keywords
Implementieren, coden, bauen, plan-context, Feature umsetzen, Review
