# Epic: {Name}

> **Epic ID**: EPIC-{NNN} (3-digit)
> **Feature Prefix**: FEATURE-{EPIC}-... (where EPIC is this epic's
> 3-digit number; e.g. EPIC-001 -> FEATURE-001-001, FEATURE-001-002, ...)
> **Business Alignment**: _devprocess/analysis/BA-[PROJECT].md
> **Scope**: [PoC / MVP]

## How-Might-We (from BA)

> Carried over from the Exploration Board / BA Section 1.2.
> Forms the foundation for the Epic Hypothesis Statement.

**How might we** help {user} **achieve** {need}, **despite** {obstacle}?

## Epic Hypothesis Statement

> Derived from the HMW question and the Value Proposition of the BA.

FOR {target customer segment, from HMW "user"}
WHO {have need/problem, from HMW "need" and "obstacle"}
THE {product/solution, from BA Value Proposition}
IS A {product category, from BA High-Level Concept}
THAT {provides key benefit, from BA Idea Potential "Value"}
UNLIKE {competitive alternative, from BA Competitor Analysis}
OUR SOLUTION {primary differentiator, from BA "The Wow" or "Unfair Advantage"}

## Business Outcomes (measurable)

1. **{Outcome 1}**: {Metric} increases from {Baseline} to {Target} within {Timeframe}
2. **{Outcome 2}**: {Metric} decreases from {Baseline} to {Target} within {Timeframe}

## Leading Indicators

> Derived from the Critical Hypotheses of the BA (Section 7.3).

- {Indicator 1}: {Description, how to measure}. Validates Hypothesis H-{XX}.
- {Indicator 2}: {Description, how to measure}. Validates Hypothesis H-{XX}.

## Critical Hypotheses (from BA)

> Reference to BA Section 7.3. These hypotheses must be validated through features.

| BA Ref | Hypothesis | Validated by Feature | Status |
|--------|-----------|---------------------|--------|
| H-01 | {Hypothesis from BA} | FEATURE-{EPIC}-{NNN} | {Open / Validated / Disproven} |
| H-02 | {Hypothesis from BA} | FEATURE-{EPIC}-{NNN} | {Open / Validated / Disproven} |

## MVP Features

| Feature ID      | Name   | Priority | Effort | Status      |
|-----------------|--------|----------|--------|-------------|
| FEATURE-001-001 | {Name} | P0       | M      | Not Started |
| FEATURE-001-002 | {Name} | P1       | L      | Not Started |

**Priority:** P0-Critical (MVP does not work without it), P1-High (important), P2-Medium (value-adding)
**Effort:** S (1-2 sprints), M (3-5 sprints), L (6+ sprints)

## Explicitly Out-of-Scope

- {Feature X}: {Rationale}
- {Feature Y}: Planned for Phase 2

## Dependencies & Risks

### Dependencies
- {Dependency 1}: {Team/System}, {Impact if delayed}

### Risks
| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| {Risk 1} | H/M/L | H/M/L | {Mitigation} |

## Technical Debt (PoC only)

| Shortcut | Description | MVP Conversion Impact |
|----------|-------------|----------------------|
| {Shortcut 1} | {Description} | {Effort for cleanup} |
