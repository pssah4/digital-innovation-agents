---
name: v-model-workflow
description: >
  Orchestriert den V-Model Entwicklungszyklus: Business Analyse -> Requirements
  Engineering -> Architecture -> Coding (Implementierung). Nutze diesen Skill
  wenn der User "V-Model", "kompletter Workflow", "neues Projekt aufsetzen",
  "von der Analyse bis zur Implementierung", "Full Cycle" oder aehnliches erwaehnt.
  Auch wenn unklar ist, mit welcher Phase gestartet werden soll.
  Alle Phasen folgen den Konventionen aus /project-conventions.
disable-model-invocation: true
---

# V-Model Workflow Orchestrator

Dieser Skill fuehrt dich durch den V-Model Entwicklungszyklus.
Jede Phase baut auf der vorherigen auf und erzeugt Artefakte als Input fuer
die naechste Phase. Alle Phasen folgen den Konventionen aus `/project-conventions`.

## Workflow-Uebersicht

```
Phase 1: /business-analyse                         ENTWURF
  Output: _devprocess/analysis/BA-{PROJECT}.md       (linke Seite
    |                                                 des V)
    v
Phase 2: /requirements-engineering
  Input:  BA-Dokument
  Output: Epics, Features, architect-handoff.md
    |
    v
Phase 3: /architecture
  Input:  Features, ASRs, NFRs
  Output: ADRs, arc42, plan-context.md
    |
    v
Phase 4: /coding                                   IMPLEMENTIERUNG
  Input:  plan-context.md + ADRs + Features          (Spitze des V)
  Action: Plan erstellen, ADRs finalisieren,
          inkrementell implementieren,
          Feature-Specs + Backlog aktualisieren
    |
    v
Post-Impl: /security-audit                         VERIFIKATION
  Input:  Implementierte Codebase                    (rechte Seite
  Output: Security Report + Remediation Plan          des V)
```

## Projektstruktur sicherstellen

Bevor eine Phase startet, pruefe ob die Verzeichnisstruktur existiert.
Falls nicht, initialisiere sie gemaess `/project-conventions`:

```bash
mkdir -p _devprocess/{analysis/security,requirements/{epics,features,handoff},architecture,context}
mkdir -p src docs scripts memory
```

## Start: Phase bestimmen

Frage den User:

```
V-Model Workflow -- Wo stehst du?

A) Ganz am Anfang -- Projekt/Feature noch nicht analysiert
   -> Starte mit /business-analyse

B) Problem ist klar, brauche strukturierte Requirements
   -> Starte mit /requirements-engineering

C) Requirements stehen, brauche Architektur-Vorschlaege
   -> Starte mit /architecture

D) Architektur steht, plan-context.md liegt vor
   -> Starte mit /coding

E) Implementierung fertig, brauche Security Review
   -> Starte mit /security-audit

F) Unsicher -- hilf mir einzuordnen
   -> Kurzes Interview zur Standortbestimmung
```

## Phase-Uebergaenge

### Nach Business Analyse -> Requirements Engineering

Pruefe Quality Gates aus `/business-analyse`, dann:

```
BA abgeschlossen! Naechster Schritt:
/requirements-engineering
Input: _devprocess/analysis/BA-{PROJECT}.md
```

### Nach Requirements Engineering -> Architecture

Pruefe: Features haben tech-agnostische SC, architect-handoff.md existiert.

```
Requirements abgeschlossen! Naechster Schritt:
/architecture
Input: _devprocess/requirements/handoff/architect-handoff.md
```

### Nach Architecture -> Coding

Pruefe: plan-context.md existiert und ist konsistent mit ADRs.

```
Architektur-Vorschlaege stehen! Naechster Schritt:
/coding
Input: _devprocess/requirements/handoff/plan-context.md

Der Coding-Skill wird:
1. plan-context.md + alle ADRs + Features lesen
2. ADR-Vorschlaege final akzeptieren/modifizieren
3. Implementierungsplan erstellen (Plan-Mode)
4. Inkrementell implementieren (Build+Deploy nach jedem Schritt)
5. Feature-Specs und Backlog aktualisieren
```

### Nach Coding -> Security Audit

Coding-Skill empfiehlt automatisch den Security Audit nach Abschluss:

```
Implementierung abgeschlossen!

Empfohlener naechster Schritt vor dem Release:
/security-audit
-> Prueft die Codebase auf OWASP, CWE, Dependencies
-> Erstellt priorisierten Remediation-Plan
```

## Artefakt-Verzeichnisstruktur

```
_devprocess/
  analysis/
    BA-{PROJECT}.md                    <- Phase 1: Business Analyse
    security/
      AUDIT-{PROJECT}-{DATE}.md        <- Post-Impl: Security Audit
  requirements/
    epics/
      EPIC-{XXX}-{slug}.md             <- Phase 2: Requirements
    features/
      FEATURE-{XXX}-{slug}.md          <- Phase 2: Requirements
    handoff/
      architect-handoff.md             <- Phase 2 -> 3: Uebergabe
      plan-context.md                  <- Phase 3 -> 4: Uebergabe
  architecture/
    ADR-{XXX}-{slug}.md                <- Phase 3: Architecture
    arc42.md                           <- Phase 3: Architecture
  context/
    10_backlog.md                      <- Phase 4: wird aktualisiert
```

## Traceability-Kette

```
BA-Dokument (Warum?)
  -> Epic (Was, strategisch?)
    -> Feature (Was, konkret?)
      -> ASR (Was ist architektur-relevant?)
        -> ADR (Wie loesen wir es?)
          -> plan-context.md (Kontext-Bruecke)
            -> Implementierungsplan (Wie bauen wir es?)
              -> Code (Ergebnis)
                -> Security Audit (Ist es sicher?)
```

## Konventionen

Dieser Workflow folgt den Standards aus `/project-conventions`:
- Dateinamen: 3-stellige Nummern, kebab-case, Englisch
- Sprache: Konversation Deutsch, Code/Commits Englisch
- Verzeichnisse: `_devprocess/` fuer interne Dokumente
- Feature-Lebenszyklus: BACKLOG -> SPEC -> PLAN -> IMPL -> UPDATE

## Keywords
V-Model, Workflow, Full Cycle, neues Projekt, Entwicklungszyklus,
von Analyse bis Implementierung, kompletter Durchlauf
