# Verzeichnisstruktur -- Vollstaendige Referenz

## Gesamtstruktur

```
{project}/
│
├── _devprocess/                         INTERNES WISSENSARCHIV (nicht public)
│   ├── analysis/                        Business Analyse Dokumente
│   │   ├── BA-{PROJECT}.md              Hauptdokument Business Analyse
│   │   ├── constitution-draft.md        Optional: Projekt-Prinzipien
│   │   └── security/                    Security Audit Reports
│   │       └── AUDIT-{PROJECT}-{DATE}.md
│   │
│   ├── requirements/                    Requirements Engineering
│   │   ├── epics/                       Strategische Initiativen
│   │   │   └── EPIC-{XXX}-{slug}.md
│   │   ├── features/                    Feature-Spezifikationen
│   │   │   └── FEATURE-{XXX}-{slug}.md
│   │   └── handoff/                     Uebergabe-Dokumente zwischen Phasen
│   │       ├── architect-handoff.md     RE -> Architect
│   │       └── plan-context.md          Architect -> Claude Code
│   │
│   ├── architecture/                    Architektur-Dokumentation
│   │   ├── ADR-{XXX}-{slug}.md          Architecture Decision Records
│   │   └── arc42.md                     arc42 Gesamtdokument
│   │
│   └── context/                         Projekt-Status & Backlog
│       └── 10_backlog.md                Lebendes Backlog-Dokument
│
├── src/                                 QUELLCODE
│   ├── core/                            Kern-Logik, Pipeline, Context
│   ├── tools/                           Tool-Implementierungen (je ein File)
│   ├── providers/                       Externe Integrationen (APIs, etc.)
│   ├── ui/                              User Interface Komponenten
│   ├── services/                        Shared Services
│   ├── types/                           TypeScript Type Definitions
│   └── utils/                           Hilfsfunktionen
│
├── docs/                                PUBLIC DOKUMENTATION (Englisch)
│   ├── README.md                        Oeffentliche Projekt-Beschreibung
│   └── ARCHITECTURE.md                  Oeffentliche Architektur-Doku
│
├── scripts/                             BUILD/DEPLOY/UTILITY
│   ├── merge-to-dev.sh                  Safe-Merge Script
│   └── {weitere projekt-spezifische}
│
├── memory/                              CLAUDE CODE MEMORY
│   ├── MEMORY.md                        Eckdaten (<200 Zeilen)
│   └── {detail-referenz}.md             Verlinkt aus MEMORY.md
│
├── .claude/                             CLAUDE CODE KONFIGURATION
│   ├── skills/                          Projekt-spezifische Skills
│   │   └── {skill-name}/SKILL.md
│   └── settings.json                    Permissions etc.
│
├── CLAUDE.md                            PROJEKT-KONTEXT fuer Claude Code
├── package.json                         Dependencies (Node.js Projekte)
├── tsconfig.json                        TypeScript Config
└── .gitignore
```

## Verzeichnis-Erstellungsreihenfolge

Verzeichnisse werden NICHT alle auf einmal erstellt, sondern im Lauf
des V-Model Workflows, wenn sie gebraucht werden:

### Phase 1: Projekt-Init
```
_devprocess/context/
memory/
src/
docs/
scripts/
```

### Phase 2: Business Analyse
```
_devprocess/analysis/
```

### Phase 3: Requirements Engineering
```
_devprocess/requirements/epics/
_devprocess/requirements/features/
_devprocess/requirements/handoff/
```

### Phase 4: Architecture
```
_devprocess/architecture/
```

### Phase 5: Nach Implementierung (Security)
```
_devprocess/analysis/security/
```

## Regeln

- `_devprocess/` ist IMMER in `.gitignore` fuer Public Repos
- `_devprocess/` wird NICHT geloescht, nur ueber Stripping aus Public entfernt
- `docs/` bleibt im Public Repo (fuer GitHub Pages)
- `memory/` bleibt im Private Repo, wird via Stripping entfernt
- `.claude/` wird via Stripping entfernt
