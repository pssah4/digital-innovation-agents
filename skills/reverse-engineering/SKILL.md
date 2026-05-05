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

## MANDATORY Pre-Phase 0: Branch check (multi-item exception)

Reverse-engineering bootstraps the entire backlog at once: 20+
artefacts can land in a single run. Branching per-item would force
the user to juggle 20 branches before any work is done. Therefore
RE is the exception to the per-item branching rule:

- All reverse-engineered artefacts land on
  `feature/reverse-engineer-<repo-name>`.
- Per-item branches kick in AFTER RE merges, when downstream skills
  (`/coding`, etc.) work on individual items.

Branch check at start:

- If on `main` / `master` / `dev`: refuse, AskUserQuestion to create
  `feature/reverse-engineer-<repo-name>` and switch.
- If on the expected branch: silent continue.
- If on another branch: AskUserQuestion -- switch to expected, or
  rename the current branch to the expected name.

GitHub integration: RE does not create per-item issues during
Phase 0-7. The `/dia-guide` post-RE handoff is responsible
for that, after the user has triaged which reverse-engineered
items are real backlog candidates.

Phase tag: RE does NOT set per-item phase tags during its run.
After RE completes and the user has triaged the backlog seed,
`/dia-guide` runs a one-shot pass that creates GitHub
issues and tags `<item-id>/reverse-engineered` for every promoted
item. This signals downstream skills that the item came from RE
(useful for "go back and validate this with the user" workflows).

State stored in `.git/dia-active-skill`. Full rules:
`skills/project-conventions/references/team-workflow.md`,
`skills/project-conventions/references/branch-protection.md`.

## MANDATORY Phase 0: Artifact triage

Reverse engineering scans existing code to produce artifacts. Every
artifact this skill creates lands in one of these categories:

- **FEATURE** (observed capability with user-facing surface)
- **ADR** (decision inferred from code patterns or external docs)
- **IMP** (technical debt or improvement candidate surfaced by the
  scan)
- **FIX** (bug or drift surfaced by the scan)

The skill assigns each artifact to its category before writing.
Frontmatter `feature:` and `epic:` are mandatory for FIX and IMP.

## MANDATORY: Backlog as single source of truth

Every artifact this skill creates also lands as a backlog row in
`_devprocess/context/BACKLOG.md`. Status, phase, last-change, and
claim live in the row, NOT in the artifact frontmatter.

**Defaults for reverse-engineered artifacts:**

- Feature observed in code: status Planned, phase Building (or
  Released if there is evidence the capability is shipped to users)
- ADR inferred: status Proposed, phase Building
- BA draft: status `Draft (Reverse-Engineered)`, validation pending

**Sync chain (binding order):**

1. Create the backlog row
2. Create the artifact body
3. Run `/consistency-check` mode A at the end of the skill phase

## MANDATORY: Wayfinder generation as primary output

`/reverse-engineering` produces the wayfinder layer as a primary
output, not an afterthought:

- `src/ARCHITECTURE.map` populated with one row per identified
  entry-point file. Template:
  `skills/architecture/templates/ARCHITECTURE-MAP-TEMPLATE.md`.
- JSDoc headers in every entry-point file. Template:
  `skills/architecture/templates/JSDOC-HEADER-TEMPLATE.md`.
- Module READMEs for every directory under `src/` that owns
  substance (more than 3 source files or any cross-module API).
  Template: `skills/architecture/templates/MODULE-README-TEMPLATE.md`.

This is the most token-efficient form of project context and the
basis on which the agent orients itself in subsequent phases.

## MANDATORY: Rules layer seed

`/reverse-engineering` seeds `_devprocess/rules/` with the patterns
the codebase actually follows:

- `_devprocess/rules/technical.md`: stack (detected from
  package.json, pyproject.toml, etc.), build commands, test setup,
  conventions visible in 10+ files.
- `_devprocess/rules/design.md` (if UI surface exists): design
  tokens, component patterns observed in the codebase.
- `_devprocess/rules/domain.md`: glossary entries derived from class
  and module names, business rules surfaced by validations or
  invariants in code.

Hard cap: 500 lines total across all rule files.


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


## MANDATORY: FIX/IMP, depends-on as a graph edge

**Chores are not a separate node type.** Every piece of work outside
of a Feature is either:

- **FIX-{ee}-{ff}-{nn}** (bug or issue follow-up) at
  `_devprocess/requirements/fixes/FIX-{ee}-{ff}-{nn}-{slug}.md`
- **IMPROVEMENT / IMP-{ee}-{ff}-{nn}** (technical or other change that is not a
  feature) at
  `_devprocess/requirements/improvements/IMP-{ee}-{ff}-{nn}-{slug}.md`

**Required frontmatter for FIX and IMP:**

```yaml
id: FIX-{ee}-{ff}-{nn}
feature: FEAT-{ee}-{ff}    # mandatory
epic: EPIC-{nn}                    # mandatory
adr-refs: []
plan-refs: []
depends-on: []
created: {YYYY-MM-DD}
```

FIX and IMP without `feature:` and `epic:` are invalid. Status,
phase, last-change, and claim live in the backlog row, not in the
frontmatter.

**Dependencies (depends-on):** every artifact (Epic, Feature, ADR,
FIX, IMP, PLAN) MAY carry `depends-on: [ID, ID, ...]` in the
frontmatter. The resulting graph is acyclic. Targets must be
existing artifact IDs.

## MANDATORY: Hypothesis statements as full prose

Epic hypothesis statements (in the BA draft this skill writes) are
written as full prose paragraphs in the user's working language. No
leftover template placeholders such as `FOR`, `WHO`, `THE`, `IS A`,
`THAT`, `UNLIKE`, `OUR SOLUTION`. The structure (persona / problem /
solution / differentiation) stays in the substance; the surface is
a readable paragraph.

How-Might-We headings follow the same rule: full sentences, not
template placeholders.

## MANDATORY: Writing style and humanizer rules

All artifacts produced by this skill follow the rules in
`skills/project-conventions/SKILL.md` under "Writing style for every
artifact". Zero em dashes (U+2014, U+2013, double-hyphen substitute).
No AI vocabulary words (landscape, nuanced, delve, leverage, crucial,
robust, seamless, holistic, foster, ensuring, highlighting,
underscoring). No negative parallelisms ("not X but Y"). Active
voice by default. Sentence case in headings. No rule-of-three padding.

For German artifacts: proper umlauts (ä, ö, ü, ß), not the
ae/oe/ue/ss substitutes.


## Core philosophy

**Backward walk, evidence only.** Code tells you what exists. It does
not tell you whether it solves the right problem. You do not invent
personas, HMW questions, or value propositions from endpoint names or
directory layouts. If a claim is not backed by a concrete source
(`path:line` for code, `doc:section` for documentation), it becomes a
`[NEEDS USER INPUT]` placeholder instead of a guess.

**Draft, not ground truth.** Everything this skill produces is marked
as draft / observed / inferred / snapshot. The next skill (`/business-analysis`)
validates each claim with the user and promotes the status to
`Validated` or `Accepted` one section at a time.

**Forward again from the validated state.** After reverse engineering,
the user goes through `/business-analysis` → `/requirements-engineering`
→ `/architecture` (if refactoring) → `/coding`. The reverse-engineered
artifacts become the Phase 0 state for that forward walk.

## What you create

- `_devprocess/requirements/handoff/plan-context.md`. Tech stack and
 codebase snapshot, ready for `/coding`.
- `_devprocess/architecture/ADR-{XXX}-{slug}.md`. One per observable
 architecture decision, `Status: Inferred from codebase`.
- `_devprocess/architecture/arc42.md`. Structural snapshot,
 `Status: Reverse-engineered snapshot`.
- `_devprocess/requirements/epics/EPIC-{nn}-{slug}.md`. One or more
 **anticipated** Epics that group observed capabilities by theme.
 Even when the business motivation is not yet described, the epic
 gives the features a frame (domain, user group, module). Status:
 `Anticipated (not yet validated)`. `/business-analysis` and
 `/requirements-engineering` later refine, split, merge, or rename
 these epics.
- `_devprocess/requirements/features/FEAT-{ee}-{ff}-{slug}.md`.
 One per observable user-facing capability, `Status: Observed (not
 validated)`, nested under its anticipated Epic's number.
- `_devprocess/analysis/BA-{PROJECT}.md`. Evidence-based Project-BA
 draft (singleton, product layer),
 `Status: Draft (reverse-engineered, awaiting validation in /business-analysis)`.
 Item-BAs (`BA-EPIC-*.md`, `BA-FEAT-*.md`, ...) are NOT created by
 this skill. They are the responsibility of `/business-analysis`
 once the user starts working on a specific item.
- Append entries to `_devprocess/context/BACKLOG.md`. TODOs, FIXMEs,
 observed gaps, tech debt, undocumented dependencies.

## What you do NOT create

- Code changes, refactorings, or new tests
- **Validated** Epics with Hypothesis Statements, Business Outcomes,
 or HMW questions. This skill only writes **Anticipated Epics**
 (thematic groupings of observed capabilities) with
 `Status: Anticipated`. The strategic content comes from
 `/business-analysis` and `/requirements-engineering` later.
- Success Criteria or User Stories on the FEATURE inventory (those
 come from `/requirements-engineering` after `/business-analysis`)
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
 /business-analysis will fill this in.]
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
- Multiple numbering series (ADR-01..037 alongside 037..045 without
 prefix)
- **DIA v1 patterns** (added 2026-04-30): `FEATURE-NNNN`-style
 filenames (4-digit), `EPIC-NNN` / `ADR-NNN` (3-digit), `status:`
 / `phase:` fields in YAML frontmatter, `> **Status**: ...` lines
 in artifact bodies, `_devprocess/context/fixes/` (instead of
 `requirements/fixes/`), `_devprocess/context/20_bugs.md`,
 numeric-prefixed `10_backlog.md` / `30_handoffs.md` /
 `40_metrics.md`, any `archive/` folder under `_devprocess/`.

If ANY of these are found, stop before producing new artifacts and
ask the user a single `AskUserQuestion` (per the User Interaction
Protocol, one-at-a-time with Pro/Con):

> "I found existing workflow artifacts under {paths}. How should we
> proceed? (a) normalize them to current DIA conventions first
> (Phase -1.5 runs the migration scripts), then reverse-engineer the
> gaps from code, (b) keep them untouched and produce new artifacts
> alongside (flagged as separate source), (c) replace them with
> reverse-engineered versions (destructive)."

Recommendation: (a) for DIA v1 patterns or any partial DIA-style
artefacts. (b) for parallel non-DIA workflows the team wants to
preserve. (c) only when the user explicitly confirms the existing
artefacts are obsolete.

Only after the decision is recorded do you proceed with Phase -1.5
(if normalization was chosen) or Phase 0 (otherwise).

### Phase -1.5: Migration of pre-existing artefacts (added 2026-04-30)

Skipped unless Phase -1 found DIA-style artefacts and the user chose
option (a). Runs the shared migration scripts under `tools/migration/`
in the DIA repo, the same scripts `/dia-migration` orchestrates.

Sequence (each script idempotent, run with confirmation gates only
between major write phases):

1. `tools/migration/detect_state.py` -- inventory v1/v2/mixed signals.
2. `tools/migration/strip_frontmatter_status.py` -- pull `status:` /
   `phase:` / `last_updated:` out of artefact YAML frontmatter.
3. `tools/migration/strip_body_status.py` -- pull `> **Status**: ...`
   lines out of artefact bodies.
4. `tools/migration/migrate_naming.py` -- rename ID schemas
   (`FEATURE-NNNN` -> `FEAT-EE-FF`, `EPIC-NNN` -> `EPIC-NN`, etc.)
   and rewrite cross-references.
5. `tools/migration/flatten_analysis.py` -- collapse `analysis/` to
   the four canonical prefixes (BA, EXPLORE, RESEARCH, AUDIT).
6. `tools/migration/build_backlog.py` -- regenerate
   `_devprocess/context/BACKLOG.md` from the (now-clean) artefact set.
7. `tools/migration/migrate_skill_names.py` -- rewrite legacy skill
   names in CLAUDE.md / README / inline scripts.

After Phase -1.5, the repo's existing artefacts conform to current
DIA conventions. Phase 0 then proceeds with the code-walk to fill
the gaps that the existing artefacts do not cover.

The intent: `/dia-migration` and `/reverse-engineering` share the
canonical migration mechanics. `/dia-migration` runs them with full
phase-by-phase user confirmation (because the user explicitly
invoked migration). `/reverse-engineering` runs them as a
preparatory pass with one consolidated confirmation, because the
user's primary intent was the code-walk.

**Numbering collision protocol.** If two ADR series coexist, the
consolidation must decide which numbers win. Rule of thumb: the
series with the higher count of external references in source code,
commits, and backlog wins. Renumber the smaller series with a clear
note in the renumbered ADR header ("Before 2026-04-20 this ran as
ADR-37; renumbered to ADR-46 because Superpowers series used 037").

**Dedup protocol.** If two files describe the same decision or
feature (different language, different format, same topic), merge
under the newer structure and add a "Previous variants" note that
lists the sources. Do not silently delete.

### Phase 0: Scope and codebase scan (5-10 min)

Ask the user which scope applies, same tiers as `/business-analysis`:

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
placeholder at `_devprocess/requirements/epics/EPIC-{nn}-{slug}.md`
from `EPIC-TEMPLATE.md` with:

```yaml
---
status: Anticipated (not yet validated)
source: /reverse-engineering on {date}
needs-validation: true
---

# EPIC-{nn}: {thematic name, e.g. "User and access management"}

> **Status**: Anticipated. Derived from observed capabilities,
> not from a validated business motivation. `/business-analysis`
> refines or replaces the Hypothesis Statement and outcomes.

## Anticipated Scope

{1-2 sentences: which observed capabilities this epic groups, and why}

## Evidence

- {module or directory, short description}
- {route or API surface}
- {test file that describes this capability cluster}
```

When no obvious clusters exist, create a single catch-all
`EPIC-01-observed-capabilities.md`. Split later.

**Step 3b: FEATURE files.** For each observable capability, write
`_devprocess/requirements/features/FEAT-{ee}-{ff}-{slug}.md`
using the existing `FEATURE-TEMPLATE.md` but with reduced scope.
`{EPIC}` is the 2-digit number of the anticipated Epic the feature
belongs to, `{NNN}` is the local counter inside that Epic.

```yaml
---
status: Observed (not validated)
source: /reverse-engineering on {date}
---

# FEAT-{ee}-{ff}: {short name}

## Feature Description

{What the code does, in 2-3 sentences.}

Source: {file paths and line ranges that implement this feature}

## Benefits Hypothesis

[NEEDS USER INPUT. /requirements-engineering will define this
after /business-analysis has validated the WHY.]

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

When `/business-analysis` or `/requirements-engineering` later runs,
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
status: Draft (reverse-engineered, awaiting validation in /business-analysis)
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

Include both counts in the BA header so `/business-analysis` knows
how much work remains.

### Phase 5: Backlog extraction → BACKLOG.md

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

Append each finding as a row to `_devprocess/context/BACKLOG.md`
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
overlapping file slices (e.g. FEAT-NN-NN..NN, FEAT-NN-NN..NN,
FEAT-NN-NN..NN; ADR-01..015, ADR-16..030, ADR-31..046). Each
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
explizit darauf hin, bevor `/business-analysis` startet.

### Phase 9: Parallel-branch alignment (advisory, added 2026-05-05)

Reverse-engineering allocates fresh ids while walking the code
(EPIC-NN, FEAT-EE-FF, plus FIX/IMP from TODO/FIXME extraction). If
the brownfield repo has unmerged feature branches that already
carry their own ids, those branches will collide with the freshly
inventoried state once the maintainer tries to merge them.

This phase does **not** modify other branches. It enumerates them
and reports which ones would need a renumber-before-merge step.

Steps:

1. Enumerate other branches:
   ```bash
   git for-each-ref --format='%(refname:short)' refs/heads/ \
     | grep -Ev '^(main|master|dev|<reverse-engineering-branch>)$'
   ```
2. For each branch, check for collisions against the reverse-
   engineering branch (read-only, no checkout needed if the script
   uses `--source-ref`):
   ```bash
   for B in <list>; do
     python3 tools/renumber-for-merge.py \
       --target <reverse-engineering-branch> \
       --source-ref "$B" \
       --list-conflicts
   done
   ```
3. Aggregate the JSON outputs into a final report block in
   `_devprocess/context/HANDOFFS.md`:
   ```
   ## reverse-engineering {YYYY-MM-DD} -- parallel-branch alignment
   Branches with id collisions vs the reverse-engineered state:
   - feature/foo: epic 1, feat 2, fix 0, imp 0
   - feature/bar: epic 0, feat 1, fix 1, imp 0
   To align before merging, run on each branch:
     bash scripts/merge-to-dev.sh <branch> <reverse-engineering-branch>
   ```
4. The maintainer decides per branch (renumber, rebase, abandon).
   The skill does not switch branches automatically beyond the
   read-only `git ls-tree` calls inside the script.

If no parallel branches exist, the phase prints "No parallel
branches found" and returns. Reverse-engineering proceeds to the
Handoff Ritual either way.

### Phase 6: Handoff Ritual

The handoff follows the standard 4-part pattern (artifact report,
handoff context, phase-end commit, transition question).

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
- {N} new backlog entries (FIX-{ee}-{ff}-{nn} oder IMP-{ee}-{ff}-{nn}, P2)

Sources walked:
- {N} code files scanned
- {N} documentation files read
```

**Part 2: Handoff context entry in `HANDOFFS.md`**

Append:

- **Scope**: Simple / PoC / MVP
- **What was reverse-engineered**: list of artifact counts
- **Evidence coverage**: how many BA sections need user input
- **Risks / gaps**: explicit list of placeholders the team must fill
- **Recommended next phase**: always `/business-analysis`

**Part 3: Phase-end commit**

Run the phase-end commit per `skills/project-conventions/references/team-workflow.md`
section "Phase-end commit (binding)". The block fires the binding
branch-and-item check, stages every artefact this phase produced
(plan-context, ADRs, arc42, FEATURE specs, BA draft, BACKLOG
seed), commits with the canonical message, sets the phase tag, and
opens a draft PR if one does not exist yet.

Reverse-engineering uses a single feature branch
`feature/reverse-engineer-<repo-name>` (per the RE exception in
team-workflow.md), so the commit-boundary check expects that branch
rather than a per-item branch.

Canonical commit message for RE-engineering:

```
chore(reverse): <repo-name> reverse-engineering complete

<one-line summary: N FEATUREs, M ADRs, BA draft, K backlog entries>

Refs: <repo-name>
```

After the commit lands, run:

```
python3 tools/github-integration/flow.py tag-phase --item <repo-name> --phase reverse
```

Skip the commit silently if the working tree has no changes.

**Part 4: Transition question**

Ask the user exactly this:

> "Technical context is captured. I also built an evidence-based BA
> draft, but it is **not validated**. Every claim in the BA comes
> from existing docs, and {N} sections are marked `[NEEDS USER INPUT]`
> because no source was found. The code is a good technical foundation,
> but it does not tell us whether the product solves the right
> problem.
>
> Next step: `/business-analysis`. It will walk through the draft
> section by section, confirm the evidence-backed claims, and fill
> the placeholders with you.
>
> Shall I start `/business-analysis` now, or do you want to review the
> reverse-engineered artifacts first?"

On agreement (`yes`, `go`, `next`, `weiter`) or when running inside
`/dia-guide`: start `/business-analysis`. It will detect the
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
 series coexist (ADR-01..037 alongside 037..045 without prefix),
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
touch {ROOT}/context/HANDOFFS.md
```

`adr/` is the canonical location for ADR files. If the project
already puts them under `architecture/ADR-*.md`, consolidate into
`adr/` during Phase -1 before producing new ADRs, to avoid mixed
paths.

For `{ROOT}/context/BACKLOG.md`, do not create an empty file.
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
