# Artifact formats for the reverse walk

Binding detail formats for every artifact `/dia-realign` produces in
Mode A and in the gap walk. The templates named here are canonical;
this file only fixes how realign fills them. The anti-hallucination
rules from SKILL.md apply to every block below.

## 1. Rules layer (Phase A2)

Templates: `skills/architecture/templates/RULES-*-TEMPLATE.md`. Hard
cap 500 lines across all three files. Extract the stack from the
manifests and entry points into `_devprocess/rules/technical.md`.
One `Sources:` line per block is sufficient (not per row):

```
## Stack

- Runtime: Node.js >=20
- Language: TypeScript 5.4
- Framework: Next.js 14 App Router
- Database: PostgreSQL via Prisma
- Testing: Vitest + Playwright

Sources: package.json, tsconfig.json, prisma/schema.prisma, vitest.config.ts
```

Versions and dependency lists stay in the manifests; `technical.md`
names the stack and points at them (derivability table in SKILL.md).
`design.md` only when a UI surface exists; `domain.md` glossary only
from names and invariants visible in code. Lean profile: seed
`_devprocess/SYSTEM-MAP.md` and `decisions/README.md` instead
(templates in the same directory).

## 2. plan-context.md (Phase A2)

Template: `skills/architecture/templates/plan-context-TEMPLATE.md`.
Pure reference index, cap 20 lines. It names WHERE decisions live
and never restates them: stack facts live in the manifests plus
`rules/technical.md`, current paths in `src/ARCHITECTURE.map`.
Realign fills the three tables (Stack refs, ADR impact, Quality
refs) with the ADRs produced in Phase A3 and closes with the
"Read next" line. No prose sections, no codebase-layout dump (the
old long-form plan-context is a legacy format; see Mode C).
Location: `_devprocess/requirements/handoff/plan-context.md`.

```yaml
---
source: /dia-realign on {date}
---
```

## 3. ADRs (Phase A3)

Template: `skills/architecture/templates/ADR-TEMPLATE.md` with
`kind: post-hoc` (the decision is documented after implementation).
Required sections: Context, Decision, Consequences, Sources.
Considered Options is omitted for post-hoc; when existing docs or
comments name the alternatives, upgrade to `kind: choice` and cite
them. Core sections carry no code paths (A-1); the paths that embody
the decision go into `## Sources`.

```yaml
---
id: ADR-{nn}
title: {short title}
date: {YYYY-MM-DD}
kind: post-hoc
status: Inferred from codebase
source: /dia-realign on {date}
read-when: "{one-line trigger}"
---
```

- `Context:` what the code shows that implies the decision was made.
- `Decision:` the observable choice, one to three sentences.
- `Consequences:` only what is visible (lock-in, operational
  implications in CI config).
- `## Sources`: all files, commits, or docs that support the
  decision (`src/path/file.ts`, PR link, measurement).

Write only decisions that are consequential AND non-obvious from
framework defaults. Location: `_devprocess/architecture/ADR-{nn}-{slug}.md`
(consolidated into `adr/` where that root is canonical), numbered in
discovery order.

## 4. arc42 snapshot (Phase A3)

Template: `skills/architecture/templates/arc42-REFERENCE-TEMPLATE.md`,
project file `_devprocess/architecture/arc42-REFERENCE.md`.
Post-code, cap-exempt, omit any section without substance. Evidence
sources per section:

| Section | Fill from |
|---|---|
| 3 Context and scope | entry points, external integrations visible in config |
| 4 Solution strategy | the inferred ADRs (table row per ADR) |
| 5 Building block view | observable module boundaries; NEVER the raw directory tree |
| 6 Runtime view | explicit docs only; otherwise omit |
| 7 Deployment view | CI config, Dockerfile, k8s manifests |
| 9 Architecture decisions | ADR catalog table |

Header:

```yaml
---
status: Inferred from codebase
source: /dia-realign on {date}
---
```

Do NOT write arc42-CONSTRAINTS (`arc42.md`): quality goals,
constraints, and risks are pre-code content that `/architecture`
creates when new work starts.

## 5. Anticipated Epics (Phase A4a)

Template: `skills/requirements-engineering/templates/EPIC-TEMPLATE.md`,
reduced. Location: `_devprocess/requirements/epics/EPIC-{nn}-{slug}.md`.

```yaml
---
id: EPIC-{nn}
title: {thematic name}
date: {YYYY-MM-DD}
status: Anticipated (not yet validated)
source: /dia-realign on {date}
needs-validation: true
---

# EPIC-{nn}: {thematic name, e.g. "User and access management"}

> Anticipated. Derived from observed capabilities, not from a
> validated business motivation. /business-analysis refines or
> replaces the hypothesis and outcomes.

## Anticipated scope

{1-2 sentences: which observed capabilities this epic groups, why}

## Evidence

- {module or directory, short description}
- {route or API surface}
- {test file describing this capability cluster}
```

No obvious clusters: single `EPIC-01-observed-capabilities.md`,
split later. Hypothesis prose is written by `/business-analysis`,
never invented here.

## 6. FEATURE files (Phase A4b)

Template: `skills/requirements-engineering/templates/FEATURE-TEMPLATE.md`,
reduced scope. Location:
`_devprocess/requirements/features/FEAT-{ee}-{ff}-{slug}.md`; `{ee}`
is the anticipated Epic number, `{ff}` the local counter.

```yaml
---
id: FEAT-{ee}-{ff}
title: {short capability name}
date: {YYYY-MM-DD}
epic: EPIC-{ee}
status: Observed (not validated)
source: /dia-realign on {date}
---

# FEAT-{ee}-{ff}: {short name}

## Feature Description

{What the code does, 2-3 sentences.}

Source: {file paths and line ranges that implement this feature}

## Benefits Hypothesis

[NEEDS USER INPUT. /requirements-engineering defines this after
/business-analysis has validated the WHY.]

## User Stories

[NEEDS USER INPUT]

## Success Criteria

{Observable SC table, see section 7.}

## Technical NFRs

{Non-functional constraints visible in code: rate limits, timeouts,
retry policies, auth requirements.}

Source: {config or middleware locations}
```

Names stay short and capability-focused ("User login", "Project
export"). One capability per feature, never lumped.

## 7. Observable Success Criteria (Phase A4c)

One SC per observable capability. Capability line derived from
routes/handlers/tests. Target and Measurement are `[AWAITING BA]`
unless the code declares a deterministic target (timeout constants,
rate limits, perf assertions); then the observed value goes in with
`Source:`.

```
| ID | Kriterium (observable) | Target | Messung |
|---|---|---|---|
| SC-01 | Nutzer kann Unterhaltung erneut oeffnen | [AWAITING BA] | Pilot-Interview |
| SC-02 | Startup-Abbruch wenn Sandbox nach 30s nicht bereit | 30s (Source: src/main/index.ts:1088) | Integration-Test |
```

This satisfies invariant N-4 (every feature has at least one SC).
`/business-analysis` later replaces `[AWAITING BA]` with validated
business targets.

## 8. BA draft (Phase A5)

Template: `skills/business-analysis/templates/BA-TEMPLATE.md` (five
questions, cap 40 lines). Location:
`_devprocess/analysis/BA-{PROJECT}.md` (Project-BA singleton;
Item-BAs come later from `/business-analysis`).

```yaml
---
id: BA-{PROJECT}
title: {project name}
date: {YYYY-MM-DD}
target-type: project
target-id: {PROJECT}
scope: {simple-test | poc | mvp}
status: Draft (reverse-engineered, awaiting validation)
source: /dia-realign on {date}
needs-validation: true
filled-from-sources: {n}
needs-user-input: {m}
---
```

Per template section, evidence rules:

- **1 Problem (observed):** only from README motivation / "why this
  exists" sections or explicit docs. Otherwise placeholder.
- **2 Who has it:** ONLY if docs explicitly name a user type; quote
  the exact phrase. Never inferred from routes or directories.
- **3 Solution hypothesis and strongest assumption:** HMW framing
  only if the docs contain an explicit problem statement; the
  assumption only if the docs mention one. Otherwise placeholder.
- **4 Scope:** In-list from observed capabilities (cite Phase A4
  evidence); Out-list only from explicit "non-goals" docs.
- **5 Success signal and top risk:** only from documented metrics or
  stated risks. Otherwise placeholder.

Every non-placeholder sentence carries `Source:`. Placeholders use
the full form: `[NEEDS USER INPUT. No evidence found in {searched
sources}. /business-analysis will fill this in.]` The two header
counts tell `/business-analysis` how much work remains. Long-form
content goes to BA-EXTENDED only when the user asks for it.

## 9. Backlog seed rows (Phase A6)

Format: binding table spec in
`skills/requirements-engineering/templates/BACKLOG-TEMPLATE.md` and
`skills/project-conventions/references/canonical-specs.md` (column
order is parsed by index). Reverse-engineered findings go into
Standalone Items:

| Column | Value |
|---|---|
| Type | `Chore` (default), `Security` (audit findings), `Bug-Followup` (failing/skipped tests) |
| Title | bare title only, no ID prefix (`flow.py` builds `<id>: <title>`) |
| Status | `Backlog` |
| Phase | `Building` (default; verification gate promotes/demotes) |
| Prio | `P2` (team reprioritizes during BA/RE) |
| Source | `REV` |
| Notes | `anticipated; needs verification: code-vs-doc` plus `Evidence = path:line` |

The verification gate (SKILL.md) clears the marker: `Done/Released`
when the target is already satisfied, marker removed when the gap is
confirmed, escalation when undecidable. No row reaches GitHub while
the marker is present.
