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

RE bootstraps the entire backlog in one run, so it is the exception
to the per-item branching rule. All RE artefacts land on
`feature/reverse-engineer-<repo-name>`. Per-item branches kick in
AFTER RE merges.

Branch check at start:

- On `main` / `master` / `dev`: refuse; AskUserQuestion to create
  the RE branch and switch.
- On expected branch: silent continue.
- On another branch: AskUserQuestion -- switch or rename.

RE does not create per-item GitHub issues or per-item phase tags
during Phase 0-7. After RE, `/dia-guide` runs the one-shot pass
that creates issues and tags `<item-id>/reverse-engineered`.

State in `.git/dia-active-skill`. Full rules:
`skills/project-conventions/references/team-workflow.md` and
`branch-protection.md`.

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

**Defaults for reverse-engineered artifacts.** The BACKLOG
`Status` column uses the GitHub-aligned vocabulary
(`Backlog | Ready | In Progress | In Review | Done`). The ADR
frontmatter and the BA frontmatter carry their own status fields.

| Item | BACKLOG Status default | Frontmatter status | BACKLOG Phase |
|---|---|---|---|
| Feature observed in code (shipped) | `Done` | (none) | `Released` |
| Feature observed in code (partial) | `In Progress` | (none) | `Building` |
| ADR inferred | `In Progress` | `Proposed` (ADR / MADR) | `Building` |
| BA draft | `Backlog` | `Draft (Reverse-Engineered)` | (n/a) |

Reverse-engineered features marked `Done` go straight to phase
`Released` so the post-RE BA validation walk picks them up
correctly.

**Sync chain (binding order):**

1. Create the backlog row
2. Create the artifact body
3. Run `/consistency-check` mode A at the end of the skill phase

## MANDATORY: Wayfinder + rules layer as primary outputs

Wayfinder (templates under `skills/architecture/templates/`):

- `src/ARCHITECTURE.map`: one row per entry-point file.
- JSDoc headers in every entry-point file.
- Module READMEs for every `src/` directory with more than 3 source
  files or any cross-module API.

Rules layer at `_devprocess/rules/` (hard cap 500 lines total):

- `technical.md`: stack (from manifests), build commands, test setup,
  conventions visible in 10+ files.
- `design.md` (if UI surface exists): tokens, component patterns.
- `domain.md`: glossary from class/module names, invariants in code.


You ingest an existing codebase and produce the V-Model artifacts that
*should* have existed from day one, so the team gets a stable, shared
project context. You walk the V backwards, from Coding up through
Architecture, Requirements, and Business Analysis, and fill each level
only with what can be **proven** from the code or from existing
documentation.

The result is not a product. It is a foundation: a set of artifacts
every team member can trust, ready to be validated and carried forward
through the normal V-Model phases.

**Writing style.** See `skills/project-conventions/SKILL.md#canonical-specs` (Writing style). Applies to every artifact this skill produces.

**Three-layer model and frontmatter spec.** See `skills/project-conventions/SKILL.md#canonical-specs` (Three-layer model boundaries, Frontmatter spec). Status, phase, last-change, and claim live in the backlog row, not in artifact frontmatter.


## MANDATORY: FIX/IMP and depends-on

Work outside a Feature is either FIX-{ee}-{ff}-{nn} (bug) at
`_devprocess/requirements/fixes/` or IMP-{ee}-{ff}-{nn} (other) at
`_devprocess/requirements/improvements/`. Both require frontmatter
`feature:` and `epic:`. Frontmatter spec: see canonical specs link
above.

Any artifact MAY carry `depends-on: [ID, ID, ...]` in frontmatter.
The resulting graph is acyclic; targets must be existing IDs.

## MANDATORY: Hypothesis statements as full prose

Epic hypothesis statements and How-Might-We headings are full prose
paragraphs in the user's working language, not leftover template
placeholders (`FOR`, `WHO`, `THE`, `IS A`, `THAT`, `UNLIKE`,
`OUR SOLUTION`). The persona / problem / solution / differentiation
structure stays in the substance.

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
 **anticipated** Epics grouping observed capabilities by theme
 (`Status: Anticipated (not yet validated)`). `/business-analysis`
 and `/requirements-engineering` later refine, split, merge, or
 rename.
- `_devprocess/requirements/features/FEAT-{ee}-{ff}-{slug}.md`. One
 per observable user-facing capability
 (`Status: Observed (not validated)`), nested under its Epic.
- `_devprocess/analysis/BA-{PROJECT}.md`. Project-BA draft only
 (singleton). Item-BAs are created by `/business-analysis`.
- Append entries to `_devprocess/context/BACKLOG.md` (TODOs,
 FIXMEs, gaps, tech debt, undocumented dependencies).

## What you do NOT create

- Code changes, refactorings, or new tests
- Validated Epics (Hypothesis, Outcomes, HMW). RE writes only
 **Anticipated Epics**; strategic content comes from
 `/business-analysis` and `/requirements-engineering`.
- Success Criteria or User Stories beyond the observable ones
 (`/requirements-engineering` fills the rest after BA validation).
- Personas, HMW questions, or value props that are not explicit in
 existing documentation.

## Anti-hallucination rules

These rules are non-negotiable. Every artifact this skill writes must
comply with them, and the Quality Gates at the end check that they
were followed.

1. **Source per claim block.** Every claim block (paragraph or table
 row) carries a `Source:` line. Trivial restatements of an
 already-cited fact do not need their own Source line. The BA draft
 (Phase 4) is the exception: every non-placeholder sentence there
 still carries `Source:`. Format:
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

5. **Provenance marker on every file.** Each file carries a
 `source: /reverse-engineering on {date}` marker in its frontmatter
 (BA/ADR additionally keep their own status field; the BACKLOG row
 owns lifecycle status per the three-layer model).

6. **One decision per ADR (with tight-coupling exception).** Default
 to one decision per ADR. Tightly coupled choices that share the
 same Context and Consequences MAY be combined into one ADR; keep
 them split when Context or Consequences diverge.

## Workflow

You walk backwards through the V, one phase at a time. Each phase
produces one or more artifacts before you move up to the next.

### Phase -1: Pre-check for existing workflow artifacts (binding)

Probe the project for existing workflow residues before any scan.
Greenfield projects skip this phase.

Signals to check:

- ADR or plan dirs under `docs/` or `_devprocess/`
- README, CONTRIBUTING, CLAUDE.md references to DIA / MADR / arc42
- Multiple ADR formats or numbering series in the same directory
- DIA v1 patterns: `FEATURE-NNNN` (4-digit), `EPIC-NNN`/`ADR-NNN`
  (3-digit), `status:`/`phase:` in YAML, `> **Status**: ...` lines,
  `_devprocess/context/fixes/`, `_devprocess/context/20_bugs.md`,
  numeric-prefixed `10_backlog.md`, any `archive/` folder

If any signal hits, stop and ask the user via `AskUserQuestion`:

> "Existing workflow artifacts under {paths}. Proceed how?
> (a) normalize to current DIA conventions first (Phase -1.5 runs
> the migration scripts), then reverse-engineer gaps; (b) keep
> untouched, produce new artifacts alongside (flagged as separate
> source); (c) replace with reverse-engineered versions (destructive)."

Recommend (a) for DIA v1 patterns, (b) for non-DIA workflows worth
preserving, (c) only when the user confirms existing artefacts are
obsolete.

### Phase -1.5: Migration of pre-existing artefacts

Runs only if Phase -1 chose option (a). Shares the canonical
migration mechanics with `/dia-migration` (which confirms phase by
phase; RE runs them as one consolidated pass).

Sequence (each script idempotent):

1. `tools/migration/detect_state.py` -- inventory v1/v2/mixed signals.
2. `strip_frontmatter_status.py` -- pull `status:` / `phase:` /
   `last_updated:` out of YAML.
3. `strip_body_status.py` -- pull `> **Status**: ...` lines.
4. `migrate_naming.py` -- rename ID schemas, rewrite cross-refs.
5. `flatten_analysis.py` -- collapse `analysis/` to the four
   canonical prefixes (BA, EXPLORE, RESEARCH, AUDIT).
6. `build_backlog.py` -- regenerate `BACKLOG.md`.
7. `migrate_skill_names.py` -- rewrite legacy skill names in
   CLAUDE.md / README / inline scripts.

**Numbering collisions.** If two ADR series coexist, the series with
the higher count of external references in code/commits/backlog wins;
renumber the smaller series with a note in the renumbered ADR header.

**Dedup.** Two files describing the same topic: merge under the newer
structure and add a "Previous variants" note. No silent deletes.

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
One `Sources:` line per Tech Stack block is sufficient (not per row):

```
## Tech Stack

- **Runtime:** Node.js >=20
- **Language:** TypeScript 5.4
- **Framework:** Next.js 14 App Router
- **Database:** PostgreSQL via Prisma
- **Auth:** NextAuth 5.x
- **Testing:** Vitest + Playwright

Sources: package.json, tsconfig.json, prisma/schema.prisma, vitest.config.ts, e2e/
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

**When to write an ADR.** Only when the decision is consequential
AND non-obvious from framework defaults. Skip the rest.

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

**Step 3c: Observable Success Criteria.** Write one SC per
observable capability with three columns:

- **Capability line** derived from routes/handlers/tests.
- **Target** is `[AWAITING BA]` unless the code itself declares a
 deterministic target (timeout constants, rate limits, perf
 assertions); then the observed target goes in with `Source:`.
- **Measurement** follows the same rule.

Example table:

```
| ID | Kriterium (observable) | Target | Messung |
| ----- | ----------------------- | ------------------ | -------------------------- |
| SC-01 | Nutzer kann Unterhaltung erneut oeffnen | [AWAITING BA] | Pilot-Interview |
| SC-02 | Startup-Abbruch wenn Sandbox nach 30s nicht bereit | 30s (Source: src/main/index.ts:1088) | Integration-Test |
```

This satisfies invariant N-4 (every feature has at least one SC).
`/business-analysis` later fills `[AWAITING BA]` with validated
business targets.

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

- `Status = Backlog`
- `Prio = P2` (default, the team reprioritises during BA/RE)
- `Source = REV`
- `Evidence = path:line` or short description
- `Typ = Chore` (or `Security` for audit findings, `Bug-Followup` for
 failing or skipped tests)
- `Notes` carries `needs verification: code-vs-doc` for every REV
 finding. Phase 7 clears this marker (it sets the finding to `Done`
 if the target turns out to be already satisfied, or removes the
 marker once it has confirmed the gap is real).

**Title column = bare title only.** The ID lives in column 1;
`flow.py` builds the GitHub issue title as `<id>: <title>`, so a
prefix in the Title cell duplicates the ID.

**Verify before filing.** Read the code AND the doc the finding
points at; drop the finding if the target is already satisfied
(timeout table already in arc42 §6, CI scan step already exists,
env var already in `.env.example` / README). Survivors still get
`needs verification: code-vs-doc` so Phase 7 re-checks them.

If this skill seeds the backlog file, copy the template headers
(Dashboard, Legende, Standalone Items, Traceability) first and
update dashboard counts after all rows are written.

**Phase-Schema for the backlog.** Phase is orthogonal to Status:

- `Released` - fully implemented; all SCs traceable in code.
 Partial implementation belongs in `Building`, not `Released`.
- `Building` - in progress or ready to start; scope clear.
- `Planned` - anticipated, needs refinement (each Candidates item
 carries `needs refinement: {reason}` in Notes).

Reverse-engineered items default to `Phase = Building` (code exists,
awaiting validation). Phase 7 promotes to `Released` or demotes to
`Planned` based on code evidence.

### Phase 6: Handoff Ritual (moved, see below)

### Phase 7: Codebase-Verification Gate (added 2026-04-20)

Before the Handoff Ritual runs, every FEATURE-spec and every ADR
from Phases 2-3 gets an explicit verification against the codebase.
This is the gate that lifts claims from "we wrote it down" to "we
checked it compiles with reality."

**Mechanism.** For each FEATURE-spec and each ADR, decide the
verification footer based on outcome:

- **Green Released item, no drift:** append a single line
 `Codebase-Verifikation {date}: Released, no drift`.
- **Drift found OR Phase != Released:** append the full block:

```
## Codebase-Verifikation ({date})

**Phase:** {Released | Building | Planned | Candidates}

**Refinement-Bedarf:** {none | reason if Candidates or Planned}

**Verifikations-Befund:**
- Source-Pfade geprueft: {n/m existieren}
- Success-Criteria stichprobe (Features) oder Kern-Decision (ADRs):
 {n/m belegt}
- Drift-Findings: {"Doc: X / Code: Y / Einschaetzung: ..."}

**Backlog-Vorschlag:** {none | concrete FIX/IMP text}
```

**Parallelisation.** For large projects (20+ FEATUREs, 30+ ADRs),
split verification into 3-6 concurrent agents with non-overlapping
file slices. Each agent verifies its slice and writes the
verification section directly. Consolidate Phase counts into the
Backlog Dashboard at the end.

**Backlog drift items.** Every drift finding that cannot be fixed
with a one-line doc edit becomes a new Backlog entry. Common drift:
outdated paths/line numbers, SCs marked `AWAITING RE`, UI disabled
in code but active in doc, ADR describes X / code implements Y, BA
says "separate" / code shows full implementation.

**Verify the Phase-5 findings too.** For each Standalone row with
`Source = REV` (carrying `needs verification: code-vs-doc`):

- Target already satisfied -> `Status = Done`, `Phase = Released`,
 remove the marker, add `verified {date}: already present in <ref>`.
- Gap confirmed -> remove only the marker; leave `Status = Backlog`.
- Cannot decide -> keep marker, append `needs refinement: {reason}`,
 escalate via User Interaction Protocol.

Do not let a finding reach GitHub while it still carries
`needs verification: code-vs-doc`; the marker signals Phase 7 has
not run.

### Phase 8: Graph-Konsistenz-Check

Phase 7 asks "matches this feature the code?". Phase 8 asks "is the
artefact graph as a whole consistent?". Run
`/consistency-check` mode A (syntactic, cheap). Output:

- Graph-Health section in BACKLOG with invariant status.
- Auto-filed FIX/IMPs for each gap (`Source = CONSISTENCY-CHECK`).
- Console summary for the Handoff Ritual.

Run `/consistency-check --deep` only at MVP scope with a valid BA
(checks Feature-ADR coherence and BA-Feature anchors).

**Precondition:** Phases 0-7 must be done. Running Phase 8 early
gives false gaps.

### Phase 9: Parallel-branch alignment (advisory)

RE allocates fresh ids; existing unmerged branches may collide. This
phase enumerates them and reports renumber needs without modifying
other branches.

Steps:

1. List other branches:
   ```bash
   git for-each-ref --format='%(refname:short)' refs/heads/ \
     | grep -Ev '^(main|master|dev|<re-branch>)$'
   ```
2. Per branch, check collisions read-only:
   ```bash
   python3 tools/renumber-for-merge.py \
     --target <re-branch> --source-ref "$B" --list-conflicts
   ```
3. Aggregate into `_devprocess/context/HANDOFFS.md`:
   ```
   ## reverse-engineering {YYYY-MM-DD} -- parallel-branch alignment
   Branches with id collisions:
   - feature/foo: epic 1, feat 2, fix 0, imp 0
   To align: bash scripts/merge-to-dev.sh <branch> <re-branch>
   ```
4. Maintainer decides per branch (renumber / rebase / abandon).

If no parallel branches exist, print "No parallel branches found"
and proceed.

### Phase 6: Handoff Ritual

Standard 4-part pattern: artifact report, handoff context, phase-end
commit, transition question.

**Part 1: Artifact report** -- counts per artifact type
(plan-context, ADRs, arc42 sections filled, FEATURE specs, BA draft
with filled/placeholder counts, new backlog entries) plus sources
walked (files scanned / docs read).

**Part 2: HANDOFFS.md entry** -- scope (Simple/PoC/MVP), what was
reverse-engineered, evidence coverage, risks/gaps, recommended next
phase (always `/business-analysis`).

**Part 3: Phase-end commit** -- per
`skills/project-conventions/references/team-workflow.md`
("Phase-end commit (binding)"). Stages every produced artefact,
commits, sets the phase tag, opens a draft PR. RE uses the single
branch `feature/reverse-engineer-<repo-name>`. Canonical message:

```
chore(reverse): <repo-name> reverse-engineering complete

<one-line summary: N FEATUREs, M ADRs, BA draft, K backlog entries>

Refs: <repo-name>
```

After the commit:
`python3 tools/github-integration/flow.py tag-phase --item <repo-name> --phase reverse`.
Skip silently if working tree is clean.

**Part 4: Transition question**

> "Technical context is captured. I also built an evidence-based BA
> draft, but it is **not validated**. {N} sections are marked
> `[NEEDS USER INPUT]`. Next step: `/business-analysis`. Start now,
> or review the reverse-engineered artifacts first?"

On agreement or when running inside `/dia-guide`: start
`/business-analysis` (Validation Mode auto-detects the draft BA).
On rejection: pause; artifacts stay in `_devprocess/`.

## Quality gates

Before the Handoff Ritual, verify:

1. **Source per claim block.** Grep written files for unattributed
 claim blocks. BA draft additionally needs per-sentence sources.
2. **Status marker on every file.** plan-context, arc42, every ADR,
 every FEATURE, the BA draft.
3. **No invented personas.** BA persona content must quote/cite a
 doc source, otherwise `[NEEDS USER INPUT]`.
4. **No invented HMW.** Same rule.
5. **FEATURE count matches observable capabilities.** 12 routes ->
 not 4 features and not 30.
6. **Backlog non-empty** for any non-pristine codebase (else you
 missed the TODO/FIXME scan).
7. **No format or numbering conflicts.** Resolve coexisting ADR
 formats or numbering series during Phase -1.
8. **Codebase-Verifikation present** on every FEATURE and ADR per
 Phase 7 (either the one-liner or the full block).
9. **Backlog Phase-counts reflect Phase 7 results.** Dashboard has
 Released / Building / Planned / Candidates counters; drift
 findings appear as rows.

Fix any failed gate before running the Handoff Ritual.

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

Follows `/project-conventions`. Detect the root before writing:

- `docs/adr/` or `docs/architecture/` exists -> `docs/` root.
- `_devprocess/` exists -> `_devprocess/` (canonical).
- CLAUDE.md hints either way -> follow the hint.
- Nothing present -> default `_devprocess/`.

Ensure structure exists before writing:

```bash
mkdir -p {ROOT}/{analysis,requirements/{epics,features,handoff},architecture,adr,context,implementation/plans}
touch {ROOT}/context/HANDOFFS.md
```

`adr/` is canonical for ADRs; consolidate `architecture/ADR-*.md`
into `adr/` during Phase -1.

Seed `{ROOT}/context/BACKLOG.md` from
`skills/requirements-engineering/templates/BACKLOG-TEMPLATE.md`
with the four Phase counters (Released / Building / Planned /
Candidates) in the Dashboard.

## Keywords

reverse engineering, existing project, legacy codebase, brownfield,
onboard existing, import code, we already have code, existing app,
legacy import, codebase snapshot, reverse engineer, extract artifacts,
bestehendes Projekt, existierender Code, Legacy-Projekt, Code-Import
