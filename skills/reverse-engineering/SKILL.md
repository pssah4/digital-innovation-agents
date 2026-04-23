---
name: reverse-engineering
description: >
 Brownfield entry point for the V-Model workflow. Reverse-engineers an
 existing codebase into the standard V-Model artifacts: plan-context.md,
 ADRs, arc42 snapshot, FEATURE inventory, backlog seed, and an
 evidence-based BA draft. Walks the V backwards from Coding up to
 Business Analysis, filling every step only with what can be proven
 from the code or the existing documentation. Every claim is sourced
 (path:line or doc section); nothing is invented. Use this skill when
 the user mentions "existing project", "legacy codebase", "reverse
 engineer", "import existing code", "brownfield", "we already have
 code", "onboard existing project", or when the user wants to enter
 the V-Model workflow but artifacts do not exist yet.
disable-model-invocation: false
---

# Reverse Engineering

## MANDATORY Phase 0: Artefakt-Triage (2026-04-21)

Vor jeder Code-, Doku- oder Spezifikations-Aenderung muss der Skill
feststellen, in welche Artefakt-Kategorie die Arbeit faellt:

1. **Neues FEATURE** (user-facing Capability, die es vorher nicht gab).
2. **IMPROVEMENT (IMP)** an bestehendem Feature (Refactor, Performance,
   Doku-Drift, Tests, Konfig).
3. **FIX** fuer einen Bug oder eine Drift auf bestehendem Feature.
4. **ADR** wenn die Arbeit eine Architektur-Entscheidung ist.

**Regel:** Wenn die Zuordnung aus dem User-Prompt nicht eindeutig
ableitbar ist, stellt der Skill vor allem anderen eine praegnante
Frage:

> "Ist das ein neues Feature, ein Improvement an einem bestehenden
> Feature, oder ein Fix fuer einen Bug? Falls Feature oder IMP/FIX:
> welches Feature und welches Epic?"

Keine Code- oder Spec-Aenderung ohne diese Zuordnung. FIX und IMP
verlangen zwingend `feature:` und `epic:` im Frontmatter
(Invarianten N-13, N-14). Details zum Entscheidungsbaum und den
Ausnahmen stehen in
`skills/project-conventions/references/graph-invariants.md`
(Abschnitt "Artefakt-Triage am Einstiegspunkt").


## MANDATORY: Phase and status in frontmatter + backlog sync (no asking)

Whenever this skill creates or modifies a Feature, Epic, or ADR, the
YAML-frontmatter of the artifact MUST carry `phase:` (Feature, Epic,
ADR) and `status:` (Feature, ADR). The backlog row of the artifact
MUST stay in sync with that frontmatter. No confirmation dialog, no
opt-in, no nudging the user. Execute immediately.

**Defaults when you have no better value:**

- Feature: `phase: Building`, `status: Planned`
- Epic: `phase: Building` (derive via worst-wins once features exist)
- ADR: `phase: Building`, `status: Proposed`

**Sync chain on every phase/status change:**

1. Update frontmatter of the artifact
2. Update the artifact's row in `docs/context/10_backlog.md`
3. If epic phase changed, update the epic header `Phase: X` line in
 the backlog and the epic file frontmatter
4. Recompute the dashboard counts (Phase x Epics/Features/Chores)
5. Run `/consistency-check` mode A at the end of the skill phase

Full rules and enum values: `skills/project-conventions/references/graph-invariants.md`,
section "Phase/Status-Frontmatter-Konvention".


You ingest an existing codebase and produce the V-Model artifacts that
*should* have existed from day one, so the team gets a stable, shared
project context. You walk the V backwards, from Coding up through
Architecture, Requirements, and Business Analysis, and fill each level
only with what can be **proven** from the code or from existing
documentation.

The result is not a product. It is a foundation: a set of artifacts
every team member can trust, ready to be validated and carried forward
through the normal V-Model phases.

**Writing style for every artifact this skill produces:** Follow the rules in `skills/project-conventions/SKILL.md` under "Writing style for every artifact". Zero em dashes of any form. No Unicode em dash (U+2014), no en dash (U+2013), no double-hyphen substitute. No AI vocabulary, no negative parallelisms, no rule-of-three padding. Every reverse-engineered ADR, every FEATURE description, every anticipated Epic, the BA draft sections you fill from sources, and every backlog entry is written in that style. Before you save an artifact, scan it for U+2014 and U+2013 and fix any hit.


## MANDATORY: FIX/IMP statt Chores, depends-on als Graph-Kante (2026-04-21)

**Chore-Begriff und FIX/IMP-Knoten entfallen.** Jede Arbeit ausserhalb
eines Features ist entweder:

- **FIX-NNN** (Bug-/Issue-Followup) unter
 `docs/context/fixes/FIX-{NNN}-{slug}.md`
- **IMPROVEMENT / IMP-NNN** (technische oder andersartige Aenderung, die
 kein eigenes Feature ist) unter
 `docs/context/improvements/IMP-{NNN}-{slug}.md`

**Pflicht-Frontmatter fuer FIX und IMP:**

```yaml
feature: FEATURE-NNN # Pflicht: zu welchem Feature gehoert das?
epic: EPIC-NNN # Pflicht: in welchem Epic lebt das?
phase: Released|Building|Planned|Candidates
status: Planned|Active|Done|Waiting|Deferred
depends-on: [FEATURE-..., ADR-..., FIX-..., IMP-...] # optional
```

FIX und IMP ohne `feature:` und `epic:` sind invalid
(Invarianten N-13, N-14).

**Abhaengigkeiten (depends-on):** Jedes Artefakt (Epic, Feature, ADR,
FIX, IMP) darf im Frontmatter `depends-on: [ID, ID, ...]` fuehren. Der
resultierende Graph ist azyklisch (E-11). Zielen mit IDs auf existierende
Artefakte (E-10). Details: graph-invariants.md Abschnitt
"Abhaengigkeiten und Implementierungsreihenfolge".

## MANDATORY: Lesbare deutsche Epic-Statements und HMW

Epic-Hypothesis-Statements werden als **ganze deutsche Saetze**
formuliert. Keine eingestreuten Template-Platzhalter wie `FOR`, `WHO`,
`THE`, `IS A`, `THAT`, `UNLIKE`, `OUR SOLUTION`. Der Kern bleibt
(Persona / Problem / Loesung / Differenzierung), aber als lesbarer
Prosa-Absatz.

**Alt (Template-Rest, nicht mehr erlaubt):**

> FOR **Enterprise-Entwicklungsteams (P1)**
> WHO **mit driftenden Artefakten arbeiten** ...

**Neu (deutscher Satz):**

> Fuer Enterprise-Entwicklungsteams, die mit driftenden Artefakten
> zwischen Code, Wiki, Backlog und Roadmap arbeiten, liefert dieses
> Epic ein Capability-Bundle aus Cross-Artifact-Lesen, Rollen-
> Uebersetzung, Content-Creation und Forward-Inferenz. Es unterscheidet
> sich von Cursor oder Claude Code dadurch, dass die Richtung Code-zu-
> Fachsprache ist, nicht umgekehrt.

HMW-Ueberschriften und HMW-Fragen werden ebenfalls durchgehend auf
Deutsch formuliert ("Wie koennen wir ..." statt "How might we ...").

## MANDATORY: Umlaute und /humanizer

- Alle vom Skill erzeugten Dokumente verwenden korrekte deutsche
 Umlaute: `ae -> ae`, `oe -> oe`, `ue -> ue`, `ss -> ss` bzw.
 `ae/oe/ue/ss` nicht zulaessig, stattdessen `ä/ö/ü/ß`.
- /humanizer-Regeln werden IMMER angewendet: keine Em-Dashes, keine
 AI-Vokabular-Woerter (landscape, nuanced, delve, leverage, crucial,
 robust, seamless, holistic, foster, ensuring, highlighting,
 underscoring, etc.), keine negativen Parallelismen, aktive Stimme,
 keine Rule-of-Three-Paddings.


## Core philosophy

**Backward walk, evidence only.** Code tells you what exists. It does
not tell you whether it solves the right problem. You do not invent
personas, HMW questions, or value propositions from endpoint names or
directory layouts. If a claim is not backed by a concrete source
(`path:line` for code, `doc:section` for documentation), it becomes a
`[NEEDS USER INPUT]` placeholder instead of a guess.

**Draft, not ground truth.** Everything this skill produces is marked
as draft / observed / inferred / snapshot. The next skill (`/business-analyse`)
validates each claim with the user and promotes the status to
`Validated` or `Accepted` one section at a time.

**Forward again from the validated state.** After reverse engineering,
the user goes through `/business-analyse` → `/requirements-engineering`
→ `/architecture` (if refactoring) → `/coding`. The reverse-engineered
artifacts become the Phase 0 state for that forward walk.

## What you create

- `_devprocess/requirements/handoff/plan-context.md`. Tech stack and
 codebase snapshot, ready for `/coding`.
- `_devprocess/architecture/ADR-{XXX}-{slug}.md`. One per observable
 architecture decision, `Status: Inferred from codebase`.
- `_devprocess/architecture/arc42.md`. Structural snapshot,
 `Status: Reverse-engineered snapshot`.
- `_devprocess/requirements/epics/EPIC-{NNN}-{slug}.md`. One or more
 **anticipated** Epics that group observed capabilities by theme.
 Even when the business motivation is not yet described, the epic
 gives the features a frame (domain, user group, module). Status:
 `Anticipated (not yet validated)`. `/business-analyse` and
 `/requirements-engineering` later refine, split, merge, or rename
 these epics.
- `_devprocess/requirements/features/FEATURE-{EPIC}-{NNN}-{slug}.md`.
 One per observable user-facing capability, `Status: Observed (not
 validated)`, nested under its anticipated Epic's number.
- `_devprocess/analysis/BA-{PROJECT}.md`. Evidence-based draft,
 `Status: Draft (reverse-engineered, awaiting validation in /business-analyse)`.
- Append entries to `_devprocess/context/10_backlog.md`. TODOs, FIXMEs,
 observed gaps, tech debt, undocumented dependencies.

## What you do NOT create

- Code changes, refactorings, or new tests
- **Validated** Epics with Hypothesis Statements, Business Outcomes,
 or HMW questions. This skill only writes **Anticipated Epics**
 (thematic groupings of observed capabilities) with
 `Status: Anticipated`. The strategic content comes from
 `/business-analyse` and `/requirements-engineering` later.
- Success Criteria or User Stories on the FEATURE inventory (those
 come from `/requirements-engineering` after `/business-analyse`)
- Personas, HMW questions, or value propositions that are not
 explicitly stated in the existing documentation

## Anti-hallucination rules

These rules are non-negotiable. Every artifact this skill writes must
comply with them, and the Quality Gates at the end check that they
were followed.

1. **Source per claim.** Every non-placeholder sentence you write
 must carry a `Source:` line. Format:
 - For code: `Source: src/api/auth/handlers.ts:42-58`
 - For docs: `Source: README.md § "Getting Started"`
 - For config: `Source: package.json "dependencies.prisma"`

2. **No source → placeholder, not a guess.** If you cannot find a
 concrete source for a section, you write:
 ```
 [NEEDS USER INPUT. No evidence found in {searched sources}.
 /business-analyse will fill this in.]
 ```
 You do not write a "reasonable assumption" in its place.

3. **No persona from code structure.** You never infer personas from
 route names, directory names, or endpoint signatures. Endpoints
 are technical facts, not user research. Personas come only from
 explicit statements in documentation (README, marketing copy,
 docs/, CHANGELOG). If docs mention no user types, the persona
 section is a placeholder.

4. **No HMW question without an explicit problem statement.** If the
 existing documentation nowhere states the problem the product
 solves, the HMW section is a placeholder.

5. **Status markers everywhere.** Every file this skill writes carries
 a status marker in its frontmatter or header. No silent documents.

6. **One decision per ADR.** You do not bundle multiple decisions into
 one ADR to make the output look tidier. If you observe five
 decisions, you write five ADRs.

## Workflow

You walk backwards through the V, one phase at a time. Each phase
produces one or more artifacts before you move up to the next.

### Phase -1: Pre-check for existing workflow artifacts (binding)

**Added 2026-04-20 after a real project run revealed that two
parallel workflows (Superpowers and V-Model reverse-engineering) had
produced overlapping artifacts in the same project.** Before any
scan, probe the project for existing workflow residues. Greenfield
projects skip this phase; brownfield with prior tooling does not.

Check these locations and patterns:

- `docs/adr/`, `docs/architecture/ADR-*.md`, `_devprocess/architecture/ADR-*.md`
- `docs/superpowers/`, `docs/plans/`, `docs/specs/`, `_devprocess/implementation/plans/`
- `docs/requirements/`, `docs/analysis/`
- README, CONTRIBUTING, or CLAUDE.md references to workflow skills,
 DIA, MADR, arc42
- Multiple ADR-format styles in the same directory (MADR vs custom)
- Multiple numbering series (ADR-001..037 alongside 037..045 without
 prefix)

If ANY of these are found, stop before producing new artifacts and
ask the user a single `AskUserQuestion` (per the User Interaction
Protocol, one-at-a-time with Pro/Con):

> "I found existing workflow artifacts under {paths}. How should we
> proceed? (a) consolidate them into the V-Model format before I
> reverse-engineer the rest, (b) keep them untouched and produce new
> artifacts alongside (flagged as separate source), (c) replace them
> with reverse-engineered versions (destructive)."

Only after the decision is recorded do you proceed with Phase 0.

**Numbering collision protocol.** If two ADR series coexist, the
consolidation must decide which numbers win. Rule of thumb: the
series with the higher count of external references in source code,
commits, and backlog wins. Renumber the smaller series with a clear
note in the renumbered ADR header ("Before 2026-04-20 this ran as
ADR-037; renumbered to ADR-046 because Superpowers series used 037").

**Dedup protocol.** If two files describe the same decision or
feature (different language, different format, same topic), merge
under the newer structure and add a "Previous variants" note that
lists the sources. Do not silently delete.

### Phase 0: Scope and codebase scan (5-10 min)

Ask the user which scope applies, same tiers as `/business-analyse`:

```
What is the scope of this reverse-engineering run?

A) Simple Test / single-feature onboarding
 -> Scan the affected module, produce minimal artifacts
 -> Timeframe: 30-60 min

B) Proof of Concept / small repo
 -> Full tech-stack extraction, 3-8 ADRs, 5-15 features, BA draft
 -> Timeframe: 1-3 h

C) Minimum Viable Product / full project onboarding
 -> Full arc42 snapshot, 8+ ADRs, 15+ features, full BA draft,
 complete backlog seed
 -> Timeframe: 3-8 h
```

Then scan the codebase structure and list:

- Package / build manifests (`package.json`, `pyproject.toml`,
 `Cargo.toml`, `go.mod`, `pom.xml`, `Gemfile`)
- Top-level directories and their apparent purpose
- Entry points (`main.*`, `app.*`, `index.*`, `src/index.*`)
- Test directories and test runner config
- CI config (`.github/workflows/*`, `.gitlab-ci.yml`, etc.)
- Lint/format config, tsconfig/pyproject, etc.
- Existing documentation (`README.md`, `docs/`, `CHANGELOG.md`,
 `CONTRIBUTING.md`, `ARCHITECTURE.md`)

Report this as a Codebase Map before proceeding. This is the
inventory you will draw sources from for the rest of the walk.

### Phase 1: Tech stack → plan-context.md

Extract the concrete tech stack from the manifests and entry points.
For each layer, record what is there and cite the source:

```
## Tech Stack

- **Runtime:** Node.js (package.json "engines.node": ">=20")
- **Language:** TypeScript 5.4 (tsconfig.json, package.json devDeps)
- **Framework:** Next.js 14 App Router (package.json "next": "14.x")
- **Database:** PostgreSQL via Prisma (prisma/schema.prisma, "provider = postgres")
- **Auth:** NextAuth (package.json "next-auth": "5.x")
- **Testing:** Vitest + Playwright (vitest.config.ts, e2e/)
```

Write the result into `_devprocess/requirements/handoff/plan-context.md`
using the same structure the `/architecture` skill produces, with the
header:

```yaml
---
status: Snapshot from existing code
source: /reverse-engineering on {date}
---
```

The `Codebase Layout`, `Conventions`, and `Existing Patterns` sections
of `plan-context.md` are filled from the scan in Phase 0.

### Phase 2: Architecture reverse engineering → ADRs + arc42

Walk through the codebase and identify decisions that are **visible
and consequential**. For each, write one ADR in MADR format with:

- `Status: Inferred from codebase` in the frontmatter
- `Context:` what you see in the code that implies this decision was
 made (with source)
- `Decision:` the observable choice
- `Alternatives considered:` leave as `[NEEDS USER INPUT, not visible
 in code]` unless the alternatives are mentioned in a comment or doc
- `Consequences:` only the ones you can see (e.g. lock-in, operational
 implications that are visible in CI config)
- `Source:` footer with all files/lines that support the decision

Typical decisions to look for:

- Database engine and ORM choice
- API style (REST vs GraphQL vs RPC) and framework
- Frontend framework and state management
- Auth and session strategy
- Deployment target (serverless, container, VM)
- Package manager and monorepo tooling
- Observability stack
- Testing strategy (unit only vs unit + integration vs e2e)

Write ADRs to `_devprocess/architecture/ADR-{XXX}-{slug}.md`, numbered
in the order you discovered them.

Then produce `_devprocess/architecture/arc42.md` as a **snapshot**.
Fill only the sections you can back with sources:

- **§1 Introduction and Goals:** copy from README/docs if present,
 otherwise placeholder
- **§2 Architecture Constraints:** from package.json engines, CI
 targets, license file
- **§3 System Scope and Context:** from entry points + external
 integrations you can see in config
- **§4 Solution Strategy:** reference the inferred ADRs
- **§5 Building Block View:** from top-level directories + module
 boundaries you can observe
- **§6 Runtime View:** placeholder unless explicit docs exist
- **§7 Deployment View:** from CI config and Dockerfile/k8s manifests
 if present
- **§8 Crosscutting:** from config (auth, logging, error handling)
- **§9-12:** placeholders unless evidence exists

Header of arc42:

```yaml
---
status: Reverse-engineered snapshot
source: /reverse-engineering on {date}
---
```

### Phase 3: Functional reverse engineering → Anticipated Epics + FEATURE inventory

Identify observable user-facing capabilities. A feature is anything
the system lets a user (or an API consumer) do. Sources:

- Routes / controllers / CLI commands / public API endpoints
- Rendered pages / navigation entries
- Public exports if the project is a library
- Test descriptions (`describe('user can ...')`, `it('admin should ...')`)

**Step 3a: Anticipated Epics.** Before writing FEATURE files, group
the observable capabilities into 1-N thematic clusters (e.g. by
domain, module, user group). For each cluster, write an Epic
placeholder at `_devprocess/requirements/epics/EPIC-{NNN}-{slug}.md`
from `EPIC-TEMPLATE.md` with:

```yaml
---
status: Anticipated (not yet validated)
source: /reverse-engineering on {date}
needs-validation: true
---

# EPIC-{NNN}: {thematic name, e.g. "User and access management"}

> **Status**: Anticipated. Derived from observed capabilities,
> not from a validated business motivation. `/business-analyse`
> refines or replaces the Hypothesis Statement and outcomes.

## Anticipated Scope

{1-2 sentences: which observed capabilities this epic groups, and why}

## Evidence

- {module or directory, short description}
- {route or API surface}
- {test file that describes this capability cluster}
```

When no obvious clusters exist, create a single catch-all
`EPIC-001-observed-capabilities.md`. Split later.

**Step 3b: FEATURE files.** For each observable capability, write
`_devprocess/requirements/features/FEATURE-{EPIC}-{NNN}-{slug}.md`
using the existing `FEATURE-TEMPLATE.md` but with reduced scope.
`{EPIC}` is the 3-digit number of the anticipated Epic the feature
belongs to, `{NNN}` is the local counter inside that Epic.

```yaml
---
status: Observed (not validated)
source: /reverse-engineering on {date}
---

# FEATURE-{EPIC}-{NNN}: {short name}

## Feature Description

{What the code does, in 2-3 sentences.}

Source: {file paths and line ranges that implement this feature}

## Benefits Hypothesis

[NEEDS USER INPUT. /requirements-engineering will define this
after /business-analyse has validated the WHY.]

## User Stories

[NEEDS USER INPUT]

## Success Criteria

[NEEDS USER INPUT]

## Technical NFRs

{Any non-functional constraints visible in code: rate limits, timeout
settings, retry policies, auth requirements.}

Source: {config or middleware locations}
```

Keep FEATURE names short and capability-focused ("User login",
"Project export", "Admin user management"). Do not lump multiple
capabilities into one feature.

**Step 3c: Observable Success Criteria (added 2026-04-20).**

Previously RE left every SC as a pure `[AWAITING RE]` placeholder.
That produced features the consistency-check could not anchor. The
updated rule: RE writes one SC entry per observable capability, with
the Target field split:

- **Capability line** comes from what the code does. Example:
 "Nutzer kann eine vergangene Unterhaltung erneut oeffnen". This is
 derivable from routes, handlers, or tests.
- **Target** stays `[AWAITING BA]` unless the code itself declares
 a deterministic target (timeout constants, rate limits, explicit
 performance assertions in tests). In that case the observed target
 goes in with `Source:` line; a business-target reserved cell stays
 `[AWAITING BA]` next to it.
- **Measurement** follows the same rule: observable measurement
 from code/tests, otherwise placeholder.

The resulting SC table looks like:

```
| ID | Kriterium (observable) | Target | Messung |
| ----- | ------------------------------------------ | ------------------ | -------------------------- |
| SC-01 | Nutzer kann eine vergangene Unterhaltung | [AWAITING BA] | Pilot-Interview oder NPS |
| | erneut oeffnen | | |
| SC-02 | Startup-Abbruch wenn Sandbox nach 30s | 30s (hart codiert) | Integration-Test |
| | nicht bereit | Source: src/main/. | src/tests/.../timeout.test |
| | | index.ts:1088 | |
```

Every SC line that has no observable Target gets `[AWAITING BA]`.
The consistency-check's invariant N-4 is satisfied (every feature has
at least one SC), and the RE-Handoff can honestly claim the Feature
inventory is mapped against code, even when business targets are
still open.

When `/business-analyse` or `/requirements-engineering` later runs,
it fills the `[AWAITING BA]` placeholders with validated business
targets. Observable targets remain as-is unless the user explicitly
revises them.

### Phase 4: Business reverse engineering → BA draft

This is the most constrained phase. Read:

- `README.md` for intro, use cases, motivation
- `docs/` or `documentation/` content
- `package.json` / `pyproject.toml` `description`, `keywords`, `author`
- `CHANGELOG.md` for historical goals and removed features
- Landing-page copy if the repo contains one
- Issue/PR templates if they describe target users
- Contributing guides
- Marketing text in any comments or top-of-file docstrings

Build `_devprocess/analysis/BA-{PROJECT}.md` from the `BA-TEMPLATE.md`
but with every section following the evidence rule:

```yaml
---
status: Draft (reverse-engineered, awaiting validation in /business-analyse)
created-by: /reverse-engineering
needs-validation: true
---
```

For each section of the BA template:

- **Project purpose / scope:** fill from README intro if present,
 otherwise placeholder.
- **Primary persona:** fill ONLY if the docs explicitly name a user
 type. Quote the exact phrase. If no user type is named, placeholder.
- **Secondary personas:** same rule.
- **Problem statement:** from README motivation / "Why this exists"
 sections. Otherwise placeholder.
- **How-Might-We question:** only if the docs contain an explicit
 problem statement you can frame as HMW. Otherwise placeholder.
- **Value proposition:** from README or marketing copy. Otherwise
 placeholder.
- **Jobs to be Done:** only if the docs mention concrete user jobs.
- **Idea Potential, Pricing, Competitors:** placeholders unless
 explicitly documented.
- **Critical hypotheses:** placeholder unless the docs mention
 assumptions the team was testing.

Every non-placeholder sentence carries a `Source:` line.

When you finish, count:

- `filled-from-sources`: how many sections are evidence-backed
- `needs-user-input`: how many sections are placeholders

Include both counts in the BA header so `/business-analyse` knows
how much work remains.

### Phase 5: Backlog extraction → 10_backlog.md

Scan for:

- `TODO`, `FIXME`, `HACK`, `XXX` comments in code
- Failing or skipped tests (`.skip`, `xit`, `pytest.mark.skip`)
- Undocumented environment variables (referenced in code but missing
 from `.env.example` or README)
- Missing test coverage on observable features (Phase 3 features
 without matching test files)
- Outdated dependencies (if a lockfile and package.json disagree, or
 if major versions are pinned to old releases)
- Missing CI steps (e.g. no security scan, no type-check, no linter)

Append each finding as a row to `_devprocess/context/10_backlog.md`
following the binding format in
`skills/requirements-engineering/templates/BACKLOG-TEMPLATE.md`.
Reverse-engineered findings go into the **Standalone Items** section
(no Epic yet, to be reassigned during BA/RE) with:

- `Status = Planned`
- `Prio = P2` (default, the team reprioritises during BA/RE)
- `Source = REV`
- `Evidence = path:line` or short description
- `Typ = Chore` (or `Security` for audit findings, `Bug-Followup` for
 failing or skipped tests)

If this skill seeds the backlog file itself, copy the template
headers (Dashboard, Legende, Standalone Items, Traceability) first
and update the dashboard counts after all rows are written.

**Phase-Schema for the backlog (added 2026-04-20 after a real run).**
Brownfield projects often sit in a hybrid state where some features
are fully implemented, others are in progress, and others exist only
as ideas. A binary Done/Planned status does not capture that.
Introduce three Phase categories in the backlog Dashboard and Legende:

- `Released` - feature is **completely** implemented and verified
 against the codebase. Status=Done alone is not sufficient; the
 Phase=Released claim requires all Success Criteria to be traceable in
 code. Partial implementation belongs in `Building`, not `Released`.
- `Building` - in progress or ready to start. Scope, acceptance
 criteria, and dependencies are clear.
- `Planned` - anticipated but not ready. Needs refinement (analysis,
 target group, scope, or architecture). Each Candidates item carries a
 `needs refinement: {reason}` marker in its Notes column.

Phase and Status are orthogonal: an Epic can be partially Released
(for FEATURE-A) and partially Planned (for FEATURE-B) at the same
time. Phase describes the lifecycle assignment, Status describes the
progress indicator.

Reverse-engineered items default to `Phase = Building` (code exists,
awaiting validation) unless Phase 7 (Codebase-Verification) upgrades
them to `Released` or downgrades them to `Planned` based on code
evidence.

### Phase 6: Handoff Ritual (moved, see below)

### Phase 7: Codebase-Verification Gate (added 2026-04-20)

Before the Handoff Ritual runs, every FEATURE-spec and every ADR
from Phases 2-3 gets an explicit verification against the codebase.
This is the gate that lifts claims from "we wrote it down" to "we
checked it compiles with reality."

**Mechanism.** For each FEATURE-spec and each ADR, append a section
`## Codebase-Verifikation ({date})` with this content:

```
## Codebase-Verifikation ({date})

**Phase:** {Released | Building | Planned | Candidates}

**Refinement-Bedarf:** {none | reason if Candidates or Planned}

**Verifikations-Befund:**
- Source-Pfade geprueft: {n/m existieren}
- Success-Criteria stichprobe (Features) oder Kern-Decision (ADRs):
 {n/m belegt}
- Drift-Findings: {keine | "Doc: X / Code: Y / Einschaetzung: ..."}

**Backlog-Vorschlag:** {none | concrete FIX/IMP text}
```

**Parallelisation.** For large projects (20+ FEATUREs, 30+ ADRs),
split the verification into 3-6 concurrent agents with non-
overlapping file slices (e.g. FEATURE-001..007, FEATURE-008..015,
FEATURE-016..021; ADR-001..015, ADR-016..030, ADR-031..046). Each
agent reads its slice, verifies against the code, and writes the
verification section directly. At the end, consolidate the Phase
counts into the Backlog Dashboard and add drift-specific BL-items
where the verification surfaced issues.

**Backlog drift items.** Every Drift-Finding that cannot be fixed
with a one-line doc edit becomes a new Backlog entry. Typical drift
patterns:

- Source paths or line numbers outdated (Chore, Building).
- SCs marked `AWAITING RE` (Chore, Building).
- UI disabled in code but active in doc (Bug-Followup, Planned if
 PO-decision needed).
- Architecture decision describes X, code implements Y (Chore to
 update the ADR, or Refactor if code should be changed).
- BA says "separate vorhaben", code shows full implementation: flag
 as Planned with `needs refinement: Scope-Entscheidung` and
 escalate to the PO via the User Interaction Protocol.

The gate is non-destructive. It does not rewrite artifacts, it
attaches verification evidence. After the gate, the Backlog
Dashboard shows real Phase counts and the Handoff Ritual reports
honest numbers.

### Phase 8: Graph-Konsistenz-Check (added 2026-04-20)

Nach Phase 7 (Codebase-Verifikation pro Artefakt) folgt Phase 8:
der Graph-weite Konsistenz-Check. Phase 7 fragt "stimmt dieses
Feature mit dem Code ueberein?" Phase 8 fragt "ist der Artefakt-
Graph als Ganzes konsistent?"

**Mechanismus.** RE ruft `/consistency-check` im Mode A (syntaktisch,
kostenlos). Der Skill pruft alle Invarianten aus
`skills/project-conventions/references/graph-invariants.md` und
liefert:

- Eine **Graph-Health-Sektion** im Backlog mit Invarianten-Status.
- **Automatische FIX/IMPs** fuer jede gefundene Luecke
 (`Source = CONSISTENCY-CHECK`).
- Eine Konsole-Summary fuer den Handoff Ritual.

**Optional Mode A+B.** Bei Projekten mit bereits gueltiger BA, die
semantische Konsistenz pruefen wollen (Feature-ADR-Coherence,
BA-Feature-Anker), ruft RE `/consistency-check --deep` auf. Dies
kostet Agent-Zeit und sollte nur bei MVP-Scope gemacht werden.

**Gueltig vor Phase 8:** Phase 0-7 alle durch. Phase 8 darf nicht
im Zwischenstand laufen; sonst sind alle Luecken falsch (weil
Artefakte noch nicht alle geschrieben sind).

**Output-Integration.** Die Handoff-Ritual-Zusammenfassung enthaelt
die Graph-Health-Zahlen. Wenn der Check kritische Luecken findet
(Dead-Links, Orphan-Features ohne Epic), weist der Handoff den User
explizit darauf hin, bevor `/business-analyse` startet.

### Phase 6: Handoff Ritual

The handoff follows the standard 3-part pattern.

**Part 1: Artifact report**

```
Reverse Engineering complete for {PROJECT}

Scope: {Simple / PoC / MVP}
Tech stack: {summary from plan-context.md}

Artifacts produced:
- plan-context.md (Snapshot)
- {N} ADRs (Inferred)
- arc42.md (Snapshot, {M}/12 sections filled)
- {N} FEATURE-*.md (Observed)
- BA-{PROJECT}.md (Draft, {filled}/{total} sections
 evidence-backed, {placeholder} open)
- {N} new backlog entries (FIX-NNN oder IMP-NNN, P2)

Sources walked:
- {N} code files scanned
- {N} documentation files read
```

**Part 2: Handoff context entry in `30_handoffs.md`**

Append:

- **Scope**: Simple / PoC / MVP
- **What was reverse-engineered**: list of artifact counts
- **Evidence coverage**: how many BA sections need user input
- **Risks / gaps**: explicit list of placeholders the team must fill
- **Recommended next phase**: always `/business-analyse`

**Part 3: Transition question**

Ask the user exactly this:

> "Technical context is captured. I also built an evidence-based BA
> draft, but it is **not validated**. Every claim in the BA comes
> from existing docs, and {N} sections are marked `[NEEDS USER INPUT]`
> because no source was found. The code is a good technical foundation,
> but it does not tell us whether the product solves the right
> problem.
>
> Next step: `/business-analyse`. It will walk through the draft
> section by section, confirm the evidence-backed claims, and fill
> the placeholders with you.
>
> Shall I start `/business-analyse` now, or do you want to review the
> reverse-engineered artifacts first?"

On agreement (`yes`, `go`, `next`, `weiter`) or when running inside
`/v-model-workflow`: start `/business-analyse`. It will detect the
draft BA and enter Validation Mode automatically.

On rejection: pause and wait. The artifacts stay in `_devprocess/`
and the user can resume any time.

## Quality gates

Before you run the Handoff Ritual, verify:

1. **Every non-placeholder sentence has a `Source:` line.** Grep the
 written files for sentences without attribution and fix them.
2. **Every file has a status marker.** `plan-context.md`, `arc42.md`,
 every ADR, every FEATURE, and the BA draft all carry an explicit
 status in the frontmatter or header.
3. **No invented personas.** If the BA personas section has content,
 the content must quote or cite the documentation source. If it
 does not, replace it with `[NEEDS USER INPUT]`.
4. **No invented HMW.** Same rule as personas.
5. **FEATURE count matches observable capabilities.** If the code has
 12 routes and you produced 4 features, you under-counted. If you
 produced 30, you over-fragmented.
6. **Backlog is non-empty for anything but a pristine codebase.** If
 the backlog has zero entries after reverse-engineering a real
 project, you missed the TODO/FIXME scan.
7. **No format or numbering conflicts.** (added 2026-04-20) If
 multiple ADR formats coexist in `docs/adr/` (e.g. MADR vs simple
 German headers), flag and normalise. If multiple ADR numbering
 series coexist (ADR-001..037 alongside 037..045 without prefix),
 resolve the collision per Phase -1 before running the Handoff
 Ritual.
8. **Codebase-Verifikation present on every FEATURE and ADR.** (added
 2026-04-20) Phase 7 adds a `## Codebase-Verifikation ({date})`
 section to every FEATURE-spec and every ADR with an explicit
 Phase (Released / Building / Planned / Candidates), source-path check, and
 drift-findings list.
9. **Backlog Phase-counts reflect Phase 7 results.** (added
 2026-04-20) Dashboard has four counters (Released, Building,
 Planned, Candidates) and drift-findings from Phase 7 appear as
 backlog rows.

If any gate fails, you fix it before running the Handoff Ritual.
The user will not catch silent hallucinations. The gates are your
responsibility.

## When to use which phase depth

- **Simple Test:** Phases 0-2 only, skip BA draft (Phase 4), output
 is plan-context + 1-3 ADRs. Use when the user is onboarding one
 small feature into the workflow.
- **PoC:** Phases 0-4, skip full arc42 (keep the §1-5 skeleton), skip
 exhaustive backlog scan. Output is the core artifact set.
- **MVP / full onboarding:** All phases, full rigor.

Match depth to scope. Do not over-produce for a small target; do not
under-produce for a full onboarding.

## Project structure

This skill follows the conventions from `/project-conventions`. The
default paths are `_devprocess/…`. However, many real projects use
`docs/…` as the root for internal documentation (public-vs-internal
is then handled per file via `.gitignore` and stripping). **Check
which convention the project already uses before writing.**
(added 2026-04-20 after a real run.)

Detection rules:

- If `docs/adr/` or `docs/architecture/` exists: use `docs/` as root.
- If `docs/analysis/BA-*.md` exists: the project follows the
 `docs/`-based convention for internal docs.
- If `_devprocess/` exists: use `_devprocess/` (the canonical path).
- If neither exists and the project has a CLAUDE.md that references
 either, follow the CLAUDE.md hint.
- If nothing is present, default to `_devprocess/` as per
 `/project-conventions`.

Ensure the structure exists before writing:

```bash
# Replace {ROOT} with either _devprocess or docs based on detection above.
mkdir -p {ROOT}/{analysis,requirements/{epics,features,handoff},architecture,adr,context,implementation/plans}
touch {ROOT}/context/30_handoffs.md
```

`adr/` is the canonical location for ADR files. If the project
already puts them under `architecture/ADR-*.md`, consolidate into
`adr/` during Phase -1 before producing new ADRs, to avoid mixed
paths.

For `{ROOT}/context/10_backlog.md`, do not create an empty file.
Seed it from
`skills/requirements-engineering/templates/BACKLOG-TEMPLATE.md`
so the first RE write already follows the binding format. Include
the three Phase counters (Released / Building / Planned / Candidates) in the
Dashboard per Phase 5's schema update.

## Keywords

reverse engineering, existing project, legacy codebase, brownfield,
onboard existing, import code, we already have code, existing app,
legacy import, codebase snapshot, reverse engineer, extract artifacts,
bestehendes Projekt, existierender Code, Legacy-Projekt, Code-Import
