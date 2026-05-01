# Verzeichnisstruktur -- Vollstaendige Referenz

## Gesamtstruktur

```
{project}/
│
├── _devprocess/                         INTERNES WISSENSARCHIV (nicht public)
│   ├── analysis/                        Flache Ablage. Prefix pro Artefakttyp.
│   │   ├── BA-{PROJECT}.md              Hauptdokument Business Analyse (Singleton)
│   │   ├── EXPLORE-{PROJECT}.md         Exploration Board (Singleton, optional)
│   │   ├── AUDIT-{PROJECT}-{DATE}.md    Security Audit Reports (n)
│   │   ├── RESEARCH-{TOPIC}.md          Research-Notizen (n, optional)
│   │   ├── constitution-draft.md        Optional: Projekt-Prinzipien
│   │   └── sources/                     User-bereitgestellte Quelldokumente, behalten
│   │       └── SOURCE-{name}.{ext}
│   │
│   ├── requirements/                    Requirements Engineering
│   │   ├── epics/                       Strategische Initiativen
│   │   │   └── EPIC-{nn}-{slug}.md
│   │   ├── features/                    Feature-Spezifikationen (epic-lokal)
│   │   │   └── FEAT-{ee}-{ff}-{slug}.md
│   │   ├── fixes/                       Bug-Detail-Dateien (feature-lokal)
│   │   │   └── FIX-{ee}-{ff}-{nn}-{slug}.md
│   │   ├── improvements/                Improvement-Detail-Dateien (feature-lokal)
│   │   │   └── IMP-{ee}-{ff}-{nn}-{slug}.md
│   │   └── handoff/                     Uebergabe-Dokumente zwischen Phasen
│   │       ├── architect-handoff.md     RE -> Architect
│   │       └── plan-context.md          Architect -> Claude Code
│   │
│   ├── architecture/                    Architektur-Dokumentation
│   │   ├── ADR-{nn}-{slug}.md          Architecture Decision Records
│   │   └── arc42.md                     arc42 Gesamtdokument
│   │
│   └── context/                         Projekt-Status & Index
│       ├── BACKLOG.md                Lebendes Backlog (per BACKLOG-TEMPLATE.md), FIX-Rows leben hier
│       ├── HANDOFFS.md               Append-only Phasen-Handoffs
│       └── METRICS.md                Signal-Layer (per METRICS-TEMPLATE.md)
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

### Phase 5: Coding (bei Bedarf)
```
_devprocess/implementation/plans/
_devprocess/requirements/fixes/         beim ersten FIX
_devprocess/requirements/improvements/  beim ersten IMP
```

### Phase 6: Nach Implementierung (Security)

Der AUDIT-Report landet flach unter `_devprocess/analysis/AUDIT-{PROJECT}-{DATE}.md`.
Kein separater Unterordner mehr.

## Regeln

- `_devprocess/` ist IMMER in `.gitignore` fuer Public Repos
- `_devprocess/` wird NICHT geloescht, nur ueber Stripping aus Public entfernt
- `docs/` bleibt im Public Repo (fuer GitHub Pages)
- `memory/` bleibt im Private Repo, wird via Stripping entfernt
- `.claude/` wird via Stripping entfernt
