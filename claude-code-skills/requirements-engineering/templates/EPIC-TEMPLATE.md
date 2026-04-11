# Epic: {Name}

> **Epic ID**: EPIC-{XXX}
> **Business Alignment**: _devprocess/analysis/BA-[PROJECT].md
> **Scope**: [PoC / MVP]

## How-might-we (aus BA)

> Uebernommen aus dem EXPLORE Board / BA Section 1.2.
> Bildet die Grundlage fuer das Epic Hypothesis Statement.

**How might we** {Nutzer} **helfen,** {Beduerfnis} **zu erreichen,** **obwohl** {Hindernis}?

## Epic Hypothesis Statement

> Abgeleitet aus der HMW-Frage und der Value Proposition der BA.

FUER {Zielkunden-Segment -- aus HMW "Nutzer"}
DIE {Bedarf/Problem haben -- aus HMW "Beduerfnis" + "Hindernis"}
IST DAS {Produkt/Loesung -- aus BA Value Proposition}
EIN {Produktkategorie -- aus BA High-Level Concept}
DAS {Hauptnutzen bietet -- aus BA Ideenpotential "Mehrwert"}
IM GEGENSATZ ZU {Wettbewerbs-Alternative -- aus BA Wettbewerber-Analyse}
UNSERE LOESUNG {primaere Differenzierung -- aus BA "Das Wow" / "Unfairer Vorteil"}

## Business Outcomes (messbar)

1. **{Outcome 1}**: {Metrik} steigt von {Baseline} auf {Target} innerhalb {Zeitrahmen}
2. **{Outcome 2}**: {Metrik} sinkt von {Baseline} auf {Target} innerhalb {Zeitrahmen}

## Leading Indicators (Fruehindikatoren)

> Abgeleitet aus den Kritischen Hypothesen der BA (Section 7.3).

- {Indikator 1}: {Beschreibung, wie zu messen} -- validiert Hypothese H-{XX}
- {Indikator 2}: {Beschreibung, wie zu messen} -- validiert Hypothese H-{XX}

## Kritische Hypothesen (aus BA)

> Referenz auf BA Section 7.3. Diese Hypothesen muessen durch Features validiert werden.

| BA-Ref | Hypothese | Validiert durch Feature | Status |
|--------|----------|------------------------|--------|
| H-01 | {Hypothese aus BA} | FEATURE-{XXX} | {Offen / Validiert / Widerlegt} |
| H-02 | {Hypothese aus BA} | FEATURE-{XXX} | {Offen / Validiert / Widerlegt} |

## MVP Features

| Feature ID | Name | Priority | Effort | Status |
|------------|------|----------|--------|--------|
| FEATURE-001 | {Name} | P0 | M | Not Started |
| FEATURE-002 | {Name} | P1 | L | Not Started |

**Priority:** P0-Critical (ohne geht MVP nicht), P1-High (wichtig), P2-Medium (wertsteigernd)
**Effort:** S (1-2 Sprints), M (3-5 Sprints), L (6+ Sprints)

## Explizit Out-of-Scope

- {Feature X}: {Begruendung}
- {Feature Y}: Geplant fuer Phase 2

## Dependencies & Risks

### Dependencies
- {Dependency 1}: {Team/System}, {Impact wenn verzoegert}

### Risks
| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| {Risk 1} | H/M/L | H/M/L | {Mitigation} |

## Technical Debt (nur PoC)

| Shortcut | Description | MVP Conversion Impact |
|----------|-------------|----------------------|
| {Shortcut 1} | {Beschreibung} | {Aufwand fuer Cleanup} |
