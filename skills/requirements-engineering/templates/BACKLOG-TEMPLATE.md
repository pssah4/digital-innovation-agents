<!-- See skills/requirements-engineering/SKILL.md for how to fill this file -->

# Backlog for {PROJECT}

Single source of truth for project state and the artifact relation graph.
Vocabulary, writing rules, and the relation-graph spec: see
`skills/project-conventions/SKILL.md#canonical-specs` (Backlog vocabulary,
Priority/Effort legend, Three-layer model boundaries). Row columns are
fixed, see `### EPIC-NN` table below. Bug substance lives in
`_devprocess/requirements/fixes/FIX-*.md`; handoffs in `HANDOFFS.md`;
metrics in `METRICS.md`.

Last update: {YYYY-MM-DD} by {skill-or-user}

---

## Dashboard

| Status      | Count | | Phase      | Count | | Priority | Count |
|-------------|-------|-|------------|-------|-|----------|-------|
| Backlog     | 0     | | Released   | 0     | | P0       | 0     |
| Ready       | 0     | | Building   | 0     | | P1       | 0     |
| In Progress | 0     | | Planned    | 0     | | P2       | 0     |
| In Review   | 0     | | Candidates | 0     | | P3       | 0     |
| Done        | 0     | |            |       | |          |       |

---

## Active Epics

### EPIC-01: {Epic title}

Source: `_devprocess/requirements/epics/EPIC-01-{slug}.md` | Phase: Building | Target: {Q2 2026}

| ID           | Type    | Title          | Status      | Phase    | Prio | Refs                     | Source | Commit    | Claim                           | Last change | Notes                |
|--------------|---------|----------------|-------------|----------|------|--------------------------|--------|-----------|---------------------------------|-------------|----------------------|
| FEAT-01-01   | Feature | {short title}  | In Progress | Building | P1   | EPIC-01, ADR-03, PLAN-01 | BA     |           | sebastian-opus-4.7 @ 2026-04-19 | 2026-04-19  | {note}               |
| FEAT-01-02   | Feature | {short title}  | Done        | Released | P1   | EPIC-01, ADR-02, PLAN-02 | BA     | `a1b2c3d` |                                 | 2026-04-10  |                      |
| ADR-03       | ADR     | {short title}  | Done        | Released | P1   | FEAT-01-01               | RE     |           |                                 | 2026-04-15  | ADR-status: Accepted |
| PLAN-01      | Plan    | {short title}  | In Progress | Building | P1   | FEAT-01-01               | RE     |           | sebastian-opus-4.7 @ 2026-04-19 | 2026-04-19  | PLAN-status: Active  |
| FIX-01-01-01 | Fix     | {short title}  | Done        | Released | P0   | FEAT-01-02, PLAN-02      | BUG    | `e4f5g6h` |                                 | 2026-04-17  |                      |

---

## Cross-cutting (ADRs, Plans, no Epic)

| ID     | Type        | Title              | Status  | Phase      | Prio | Refs | Source | Commit | Claim | Last change | Notes |
|--------|-------------|--------------------|---------|------------|------|------|--------|--------|-------|-------------|-------|
| BL-050 | Security    | CSRF token missing | Ready   | Building   | P1   |      | SEC    |        |       | 2026-04-19  | H-2   |
| BL-051 | Improvement | lodash outdated    | Backlog | Candidates | P3   |      | REV    |        |       | 2026-04-19  |       |

---

## Open Bugs (index)

| FIX-ID       | Title             | Prio | Status | Linked to                      |
|--------------|-------------------|------|--------|--------------------------------|
| FIX-01-01-01 | Login race on SSO | P0   | Open   | EPIC-01 / FEAT-01-01 / PLAN-01 |

---

## Deferred / Ideas

| ID     | Title         | Reason                | Revisit |
|--------|---------------|-----------------------|---------|
| BL-099 | {short title} | Waits on ADR decision | Q3 2026 |
