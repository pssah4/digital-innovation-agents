<!--
Instructions for the agent: produce this file as
`_devprocess/context/BACKLOG.md`. Write the prose in the user's
working language. Keep status, phase, claim, and refs vocabulary in
English so it greps consistently across projects.

This file is the SINGLE SOURCE OF TRUTH for:

1. Implementation status of every artifact (Feature, ADR, Plan, Fix,
   Improvement, Epic). Status fields in artifact frontmatter are
   removed from the convention; the backlog row carries them.
2. The relation graph between artifacts. The Refs column lists
   parent and child IDs, which forms the directed graph used by
   /consistency-check for orphan detection, cycle detection, and the
   graph render.

Every status-changing action goes through this file FIRST. The
artifact files (FEATURE, ADR, PLAN, FIX, IMP) follow the backlog
row, never lead it.
-->

# Backlog for {PROJECT}

> Single source of truth for project state and the artifact relation
> graph. Updated by every skill on every status-changing action,
> BEFORE the artifact body is touched.
>
> Maintaining skills: `/business-analysis`, `/requirements-engineering`,
> `/reverse-engineering`, `/security-audit`, `/architecture`,
> `/coding`, `/testing`, `/release`, `/consistency-check`.
>
> Cross-references: Bug rows (FIX-{ee}-{ff}-{nn}) live directly in this
> file under the affected Epic; the substance lives in
> `_devprocess/requirements/fixes/FIX-*.md`. Handoffs in `HANDOFFS.md`.
> Metrics in `METRICS.md`.

Last update: {YYYY-MM-DD} by {skill-or-user}

---

## Dashboard

| Status   | Count | | Phase      | Count |
|----------|-------|-|------------|-------|
| Planned  | 0     | | Released   | 0     |
| Active   | 0     | | Building   | 0     |
| Review   | 0     | | Planned    | 0     |
| Done     | 0     | | Candidates | 0     |
| Waiting  | 0     | |            |       |
| Deferred | 0     | |            |       |

| Priority | Count |
|----------|-------|
| P0       | 0     |
| P1       | 0     |
| P2       | 0     |
| P3       | 0     |

Counts are recomputed on every backlog write by the writing skill.

---

## Vocabulary

### Status (artifact lifecycle)

- `Planned`: created, not yet started
- `Active`: in progress (spec, plan, and implementation rolled up)
- `Review`: work complete, in review
- `Done`: finished. Row stays under its Epic.
- `Waiting`: blocked, waiting for decision or dependency
- `Deferred`: deliberately postponed, not committed

### Phase (epic-level temporal stage)

- `Released`: shipped to users
- `Building`: under active development
- `Planned`: scheduled for the next iteration
- `Candidates`: idea stage, needs refinement before commitment

### Type

- `Feature`, `Epic`, `Improvement`, `Fix`, `Plan`, `ADR`,
  `Security`, `Bug-Followup`

### Source

- `BA`, `RE`, `REV` (reverse-engineering), `SEC`, `USER`, `BUG`,
  `CONSISTENCY-CHECK`

### Priority

- `P0`: blocker, immediate
- `P1`: short-term
- `P2`: mid-term
- `P3`: idea, not committed

### ID schema

- `FEAT-{ee}-{ff}`, `EPIC-{nn}`, `ADR-{nn}`, `PLAN-{nn}`,
  `FIX-{ee}-{ff}-{nn}`, `IMP-{ee}-{ff}-{nn}`, `BL-{NNN}` (backlog-only items, not
  matching another artifact type)
- IDs are monotonic and never reused.

### Claim

- Format: `{pair-id} @ {YYYY-MM-DD}`
- Empty cell means free.
- Example: `sebastian-opus-4.7 @ 2026-04-19`

### Refs

- Comma-separated list of related artifact IDs forming the relation
  graph. Examples: `EPIC-01, ADR-03, PLAN-09, FIX-013`. Edges in
  the graph derive from this column.

---

## Active Epics

### EPIC-01: {Epic title}

Source: `_devprocess/requirements/epics/EPIC-01-{slug}.md`
Phase: Building | Target: {Q2 2026}

| ID                | Type    | Title          | Status   | Phase    | Prio | Refs                              | Source | Commit    | Claim                          | Last change | Notes |
|-------------------|---------|----------------|----------|----------|------|------------------------------------|--------|-----------|--------------------------------|-------------|-------|
| FEAT-01-01   | Feature | {short title}  | Active   | Building | P1   | EPIC-01, ADR-03, PLAN-01        | BA     |           | sebastian-opus-4.7 @ 2026-04-19 | 2026-04-19  | {note} |
| FEAT-01-02   | Feature | {short title}  | Done     | Released | P1   | EPIC-01, ADR-02, PLAN-02        | BA     | `a1b2c3d` |                                | 2026-04-10  |       |
| ADR-03           | ADR     | {short title}  | Accepted | Released | P1   | FEAT-01-01                    | RE     |           |                                | 2026-04-15  |       |
| PLAN-01          | Plan    | {short title}  | Active   | Building | P1   | FEAT-01-01                    | RE     |           | sebastian-opus-4.7 @ 2026-04-19 | 2026-04-19  |       |
| FIX-013           | Fix     | {short title}  | Done     | Released | P0   | FEAT-01-02, PLAN-02          | BUG    | `e4f5g6h` |                                | 2026-04-17  | BUG-013 |

---

### EPIC-02: {Epic title}

{...}

---

## Standalone Items (no Epic)

Items without an Epic mapping: reverse-engineering findings, security
findings, direct stakeholder requests, technical debt.

| ID     | Type     | Title              | Status  | Phase    | Prio | Refs              | Source | Commit | Claim | Last change | Notes |
|--------|----------|--------------------|---------|----------|------|-------------------|--------|--------|-------|-------------|-------|
| BL-050 | Security | CSRF token missing | Planned | Building | P1   |                   | SEC    |        |       | 2026-04-19  | H-2   |
| BL-051 | Improvement | lodash outdated | Planned | Candidates | P3 |                   | REV    |        |       | 2026-04-19  |       |

---

## Open Bugs (index)

FIX rows live as regular rows under their parent Epic above. The
substance (symptom, root cause, fix, regression test) lives in
`_devprocess/requirements/fixes/FIX-{ee}-{ff}-{nn}-{slug}.md`. This
section is a flat index for PM overview, regenerated from the Epic
sections by `/coding` and `/consistency-check`.

| FIX-ID         | Title             | Prio | Status | Linked to                  |
|----------------|-------------------|------|--------|----------------------------|
| FIX-01-01-01   | Login race on SSO | P0   | Open   | EPIC-01 / FEAT-01-01 / PLAN-01 |

---

## Deferred / Ideas

Deliberately postponed items. No SLA, no commitment.

| ID     | Title          | Reason                       | Revisit       |
|--------|----------------|------------------------------|---------------|
| BL-099 | {short title}  | Waits on ADR decision        | Q3 2026       |

---

## Refs and the relation graph

Each row carries the related artifact IDs in its `Refs` column. The
graph is implicit in those columns; no separate file is needed.

`/consistency-check` builds the graph from the Refs columns and
checks:

- Every reference resolves to an existing row.
- Every artifact file has exactly one row, no orphans on either side.
- The graph is acyclic (Epic -> Feature -> Plan -> Fix forms a DAG).
- Status combinations make sense (e.g. PLAN Done implies the parent
  FEATURE is Done or in Review).

The `--view` flag of `/consistency-check` renders the graph as
mermaid or JSON for visualization.

---

## Writing rules for agents (binding)

This file is the single source of truth for project state. Every
status-changing action MUST update the backlog row BEFORE the
corresponding artifact body is touched. Skills that touch a feature,
ADR, plan, fix, or improvement run this sequence:

1. Update the backlog row (status, phase, claim, last-change, refs)
2. Then update the artifact body with the substance change
3. Update commit SHA in the backlog row after the commit lands
4. Recompute the dashboard counts at the bottom of the write
5. Run `/consistency-check` mode A at the end of the skill phase

**What counts as a status-changing action:**

- New entry created (Feature, ADR, Plan, Fix, Improvement, BL-Item)
- Status transition (Planned -> Active -> Review -> Done, etc.)
- Phase transition (Candidates -> Planned -> Building -> Released)
- Priority or Epic mapping changed
- Implementation complete (status Done with commit SHA)
- Item deferred, blocked, abandoned, or reactivated
- Bug linked or closed

**Forbidden:**

- Bug entries written in full text into the backlog (reference row only)
- Deleting Done items (they stay under their Epic for traceability)
- Writing a row without recomputing dashboard counts
- Two pairs writing simultaneously without rebasing on the latest version
- Status fields duplicated into artifact frontmatter
