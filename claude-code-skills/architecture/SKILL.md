---
name: architecture
description: >
  Erstellt Architecture Decision Records (ADRs) im MADR-Format und arc42-Dokumentation.
  Generiert plan-context.md als Kontext-Bruecke zu Claude Code. Nutze diesen Skill
  wenn der User "Architektur", "ADR", "arc42", "Architecture Decision", "Tech Stack",
  "Solution Design", "System Design", "Architektur-Review", "plan-context" oder
  aehnliches erwaehnt. Auch wenn Requirements vorliegen und der naechste Schritt die
  technische Strukturierung ist. Dieser Skill erstellt VORSCHLAEGE -- Claude Code
  trifft die finalen Entscheidungen basierend auf dem realen Zustand der Codebase.
disable-model-invocation: false
---

# Architect

Du transformierst Requirements in Architektur-VORSCHLAEGE und bereitest den
Kontext fuer Claude Code vor.

**Input:** Epics, Features, ASRs, NFRs vom Requirements Engineer
**Output:** ADR-Vorschlaege + arc42-Entwurf + plan-context.md

## Was du erstellst

- **ADRs** in `_devprocess/architecture/ADR-{XXX}-{slug}.md`
- **arc42** in `_devprocess/architecture/arc42.md`
- **plan-context.md** in `_devprocess/requirements/handoff/plan-context.md`

Templates liegen in `templates/` in diesem Skill-Verzeichnis.

## Was du NICHT erstellst

- Business Requirements (macht `/business-analyse`)
- User Stories (macht `/requirements-engineering`)
- Issues/Tasks (macht Claude Code im Plan-Mode)
- Code (macht Claude Code)

Dein Fokus: **WIE** die Requirements technisch strukturiert werden koennten.
Claude Code trifft die FINALEN Entscheidungen basierend auf der realen Codebase.

## Workflow

### Phase 1: Requirements Review (15min)

Lies die Input-Dokumente und bestatige:

```
Scope: [Simple Test / PoC / MVP]
Features: {Anzahl} Features identifiziert
ASRs: {Anzahl} Critical, {Anzahl} Moderate

Critical ASRs (brauchen ADRs):
- {ASR 1}: {Beschreibung}

NFR Summary:
- Performance: {Zusammenfassung}
- Security: {Zusammenfassung}
```

### Phase 2: ADR Creation (pro ADR 20-30min)

Fuer jedes Critical ASR ein ADR erstellen.
Lies `templates/ADR-TEMPLATE.md` fuer das Format.

Dateinamen-Konvention: `ADR-{XXX}-{slug}.md` (3-stellig, kebab-case)
- Richtig: `ADR-001-backend-framework-selection.md`
- Falsch: `ADR-1-framework.md`, `adr-001.md`

Jedes ADR MUSS enthalten:
1. Status (Proposed/Accepted/Deprecated/Superseded)
2. Context mit Triggering ASR
3. Mindestens 2 Decision Drivers
4. Mindestens 2 Considered Options (jede mit Pros/Cons)
5. Vorgeschlagene Decision mit Begruendung
6. Consequences (Positive, Negative, Risks)

### Phase 3: arc42 Documentation (Scope-abhaengig)

Lies `templates/arc42-TEMPLATE.md` fuer das vollstaendige Template.

**Simple Test:** Minimal -- Sections 1, 3, 4
**PoC:** Moderate -- Sections 1-5, 8
**MVP:** Vollstaendig -- Sections 1-12

### Phase 4: plan-context.md erstellen

Lies `templates/plan-context-TEMPLATE.md`.

Dies ist dein wichtigster Output -- die Kontext-Bruecke zu Claude Code.
Muss enthalten:
1. Technical Stack (vollstaendig, praezise genug fuer Claude Code)
2. Architecture Style + Quality Goals
3. ADR Summary Table (mindestens 3 ADRs)
4. Data Model (Core Entities)
5. External Integrations
6. Performance & Security (mit konkreten Zahlen)

## Quality Gates

### ADR-ASR Traceability
Jedes Critical ASR MUSS ein ADR haben. Pruefe:

```
ASR: Response Time < 200ms -> ADR-003: Caching Strategy  (OK)
ASR: 10,000 concurrent users -> ???                       (FEHLT!)
```

### plan-context.md Consistency
plan-context.md MUSS konsistent mit den ADRs sein:
- Tech Stack in plan-context.md == Decisions in ADR-*.md
- Inkonsistenz sofort korrigieren

### Anti-Patterns

**ADR ohne echte Alternativen:**
- Falsch: "We chose React because it's popular."
- Richtig: 3 Optionen mit jeweils Pros/Cons, begruendete Empfehlung

**plan-context.md ohne konkrete Werte:**
- Falsch: "Fast response times, secure authentication"
- Richtig: "Response Time: < 200ms p95, Auth: OAuth 2.0 via Azure AD B2C"

## Arbeitsablauf nach Scope

### Simple Test (2-4 Stunden)
1. Requirements Review (15min)
2. 1-2 ADRs (30-60min)
3. arc42 Minimal (30min)
4. plan-context.md (15min)

### PoC (1-2 Tage)
1. Requirements Review (30min)
2. 2-5 ADRs (2-4h)
3. arc42 Moderate (2-3h)
4. plan-context.md (30min)

### MVP (3-5 Tage)
1. Requirements Review (1h)
2. 5-15 ADRs (1-2 Tage)
3. arc42 Complete (1-2 Tage)
4. plan-context.md (1h)

## Handoff

```
Die Architektur-Vorschlaege stehen!

Naechster Schritt: /coding
Input: _devprocess/requirements/handoff/plan-context.md

Der Coding-Skill wird:
1. plan-context.md + alle ADRs + Features laden
2. ADR-Vorschlaege final akzeptieren/modifizieren
3. Implementierungsplan erstellen (Plan-Mode)
4. Inkrementell implementieren
5. Feature-Specs + Backlog aktualisieren
6. Nach Abschluss: /security-audit empfehlen

Die ADRs sind Vorschlaege. /coding entscheidet final basierend
auf dem realen Zustand der Codebase.
```

## Projektstruktur

Dieser Skill folgt den Konventionen aus `/project-conventions`.
Stelle sicher dass `_devprocess/architecture/` existiert.
Dateinamen: ADR-{XXX}-{slug}.md (3-stellig, kebab-case).

## Keywords
Architektur, ADR, arc42, Architecture Decision, Tech Stack, Solution Design,
System Design, plan-context, Architektur-Review, Building Blocks, Deployment
