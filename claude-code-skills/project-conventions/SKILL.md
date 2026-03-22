---
name: project-conventions
description: >
  Definiert die Projektstruktur, Namenskonventionen und Arbeitsweise fuer alle
  Projekte. Wird von anderen Skills referenziert und sorgt fuer konsistente
  Verzeichnisstrukturen, Dateinamen und Dokumentationsstandards. Nutze diesen
  Skill wenn der User "Projekt aufsetzen", "Projektstruktur", "Konventionen",
  "init", "Projekt initialisieren", "Verzeichnisstruktur" oder aehnliches
  erwaehnt. Auch automatisch relevant wenn ein neues Projekt gestartet wird.
disable-model-invocation: false
---

# Projektstruktur & Konventionen

Dieses Skill definiert die verbindlichen Standards fuer Verzeichnisstrukturen,
Dateinamen und Arbeitsweisen. Alle anderen Skills (BA, RE, Architecture,
Coding, Testing, Security Audit) folgen diesen Konventionen.

## Codebase-Awareness -- Grundprinzip

Alle Skills arbeiten im Kontext der bestehenden Codebase, nie im Vakuum.
Lies `references/codebase-awareness.md` fuer die vollstaendigen Regeln.

Kurzfassung: Vor jeder Arbeit bestehenden Code lesen, Patterns erkennen,
Abhaengigkeiten verstehen, Referenz-Implementierung pruefen. Projekt-CLAUDE.md
hat VORRANG vor generischen Skill-Anweisungen.

## Verzeichnisstruktur

Jedes Projekt hat diese Grundstruktur. Nicht alle Verzeichnisse werden
sofort angelegt -- sie entstehen im Lauf des V-Model Workflows.

Lies `references/directory-structure.md` fuer die vollstaendige Referenz.

### Kurzuebersicht

```
{project}/
  _devprocess/                    -- Internes Wissensarchiv (nicht public)
    analysis/                     -- Business Analyse & Security Audits
    requirements/                 -- Epics, Features, Handoff-Dokumente
    architecture/                 -- ADRs, arc42
    context/                      -- Backlog, Statusdokumente
  src/                            -- Quellcode
  docs/                           -- Public Dokumentation (Englisch)
  scripts/                        -- Build/Deploy/Utility Scripts
  memory/                         -- MEMORY.md + Referenz-Dateien
  .claude/                        -- Claude Code Konfiguration
    skills/                       -- Projekt-spezifische Skills (optional)
  CLAUDE.md                       -- Projekt-spezifischer Kontext
```

## Dateinamen-Konventionen

Lies `references/naming-conventions.md` fuer die vollstaendige Referenz.

### Kurzuebersicht

| Artefakt | Muster | Beispiel |
|----------|--------|----------|
| Business Analysis | `BA-{PROJECT}.md` | `BA-obsilo.md` |
| Epic | `EPIC-{XXX}-{slug}.md` | `EPIC-001-ai-agent-core.md` |
| Feature | `FEATURE-{XXX}-{slug}.md` | `FEATURE-042-semantic-search.md` |
| ADR | `ADR-{XXX}-{slug}.md` | `ADR-003-embedding-provider.md` |
| Security Audit | `AUDIT-{PROJECT}-{YYYY-MM-DD}.md` | `AUDIT-obsilo-2026-03-22.md` |
| Handoff | `architect-handoff.md`, `plan-context.md` | Feste Namen |
| Backlog | `10_backlog.md` | Fester Name |

Regeln: 3-stellige Nummern, kebab-case Slugs, keine Leerzeichen, keine Umlaute in Dateinamen.

## Sprach-Konventionen

| Kontext | Sprache |
|---------|---------|
| Konversation | Deutsch |
| Commit-Messages | Englisch, konventionelle Prefixes (feat/fix/chore/docs/refactor) |
| Private Dokumentation (_devprocess/) | Deutsch |
| Public Dokumentation (docs/, README) | Englisch |
| Code, Identifier, Variablen | Englisch |
| Deutsche Umlaute in Texten | ae oe ue (in Dateinamen), ae oe ue ss (in Code/Commits) |
| Deutsche Umlaute in Prosa | Korrekt: ae, oe, ue, ss |

## Feature-Lebenszyklus

Jedes Feature durchlaeuft:

```
1. BACKLOG          -- Eintrag in _devprocess/context/10_backlog.md
2. FEATURE-SPEC     -- Spec schreiben VOR Implementierung
3. PLAN             -- Plan-Mode: Implementierungsplan erstellen
4. IMPLEMENTIERUNG  -- Code, Build+Deploy nach jedem Schritt
5. SPEC UPDATE      -- Feature-Spec wird zur Referenz-Doku
6. BACKLOG UPDATE   -- Unmittelbar nach Implementierung
```

## Plan-Struktur

Jeder nicht-triviale Plan hat:

1. **Kontext** -- Diagnostisch, nicht deskriptiv. Root-Cause-Analyse
2. **Aenderungen** -- Pro Datei ein Unterabschnitt, VORHER/NACHHER Code
3. **Dateien-Zusammenfassung** -- Tabelle (Datei | Aenderung | Risiko)
4. **Nicht betroffen** -- Explizite Liste der NICHT geaenderten Dateien
5. **Verifikation** -- Akzeptanzkriterien, Build immer Schritt 1

## Git-Workflow

- Dual-Remote: privat (origin, alle Branches) + public (nur main)
- Branch-Flow: `feature/*` -> `dev` -> `main` -> `public/main`
- Safe-Merge: Merges nach dev ueber `scripts/merge-to-dev.sh`
- Commit: Konventionelle Prefixes, Co-Authored-By Claude
- Zwei-Stufen-Stripping fuer Public (Dev-Tooling, dann interne Docs)

## Debugging-Konventionen

Bugs als kausale Ketten:
```
Problem: [beobachtbares Verhalten]
Root Cause: [warum es passiert]
Kette: Schritt 1 -> Schritt 2 -> ... -> Fehler
```

Bug-IDs: `FIX-NN` (P0 = sofort, P1 = kurzfristig, P2 = mittelfristig)
Security-Findings: `H-N` / `M-N` / `L-N` (High/Medium/Low)

## Memory-Konventionen

- `CLAUDE.md` (global `~/.claude/`): WIE wir arbeiten (projektuebergreifend)
- `CLAUDE.md` (projekt-root): Projekt-spezifischer Kontext
- `memory/MEMORY.md`: Eckdaten, Kurzreferenzen (<200 Zeilen)
- Detaillierte Referenzen: Eigene Dateien, aus MEMORY.md verlinkt
- Bestehende Eintraege aktualisieren statt neue anlegen
- Veraltete Eintraege aktiv loeschen

## Projekt initialisieren

Wenn ein neues Projekt aufgesetzt wird, erstelle diese Grundstruktur:

```bash
mkdir -p _devprocess/{analysis/security,requirements/{epics,features,handoff},architecture,context}
mkdir -p src docs scripts memory
```

Und erstelle die initialen Dateien:
- `_devprocess/context/10_backlog.md` (leeres Backlog-Template)
- `CLAUDE.md` (Projekt-Kontext-Template)
- `memory/MEMORY.md` (leeres Memory-Template)

## Keywords
Projektstruktur, Konventionen, init, Projekt aufsetzen, Verzeichnisstruktur,
Namenskonventionen, Coding Standards, Arbeitsweise
