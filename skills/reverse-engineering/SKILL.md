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

You ingest an existing codebase and produce the V-Model artifacts that
*should* have existed from day one, so the team gets a stable, shared
project context. You walk the V backwards — Coding → Architecture →
Requirements → Business Analysis — and fill each level only with what
can be **proven** from the code or from existing documentation.

The result is not a product. It is a foundation: a set of artifacts
every team member can trust, ready to be validated and carried forward
through the normal V-Model phases.

## Core philosophy

**Backward walk, evidence only.** Code tells you what exists. It does
not tell you whether it solves the right problem. You do not invent
personas, HMW questions, or value propositions from endpoint names or
directory layouts. If a claim is not backed by a concrete source
(`path:line` for code, `doc:section` for documentation), it becomes a
`[NEEDS USER INPUT]` placeholder — not a guess.

**Draft, not ground truth.** Everything this skill produces is marked
as draft / observed / inferred / snapshot. The next skill (`/business-analyse`)
validates each claim with the user and promotes the status to
`Validated` or `Accepted` one section at a time.

**Forward again from the validated state.** After reverse engineering,
the user goes through `/business-analyse` → `/requirements-engineering`
→ `/architecture` (if refactoring) → `/coding`. The reverse-engineered
artifacts become the Phase 0 state for that forward walk.

## What you create

- `_devprocess/requirements/handoff/plan-context.md` — Tech stack and
  codebase snapshot, ready for `/coding`
- `_devprocess/architecture/ADR-{XXX}-{slug}.md` — one per observable
  architecture decision, `Status: Inferred from codebase`
- `_devprocess/architecture/arc42.md` — structural snapshot,
  `Status: Reverse-engineered snapshot`
- `_devprocess/requirements/features/FEATURE-{XXX}-{slug}.md` — one per
  observable user-facing capability, `Status: Observed (not validated)`
- `_devprocess/analysis/BA-{PROJECT}.md` — evidence-based draft,
  `Status: Draft (reverse-engineered, awaiting validation in /business-analyse)`
- Append entries to `_devprocess/context/10_backlog.md` — TODOs, FIXMEs,
  observed gaps, tech debt, undocumented dependencies

## What you do NOT create

- Code changes, refactorings, or new tests
- Epics (strategic grouping comes after BA validation)
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
   [NEEDS USER INPUT — no evidence found in {searched sources}.
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
- `Alternatives considered:` leave as `[NEEDS USER INPUT — not visible
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

### Phase 3: Functional reverse engineering → FEATURE inventory

Identify observable user-facing capabilities. A feature is anything
the system lets a user (or an API consumer) do. Sources:

- Routes / controllers / CLI commands / public API endpoints
- Rendered pages / navigation entries
- Public exports if the project is a library
- Test descriptions (`describe('user can ...')`, `it('admin should ...')`)

For each feature, write `_devprocess/requirements/features/FEATURE-{XXX}-{slug}.md`
using the existing `FEATURE-TEMPLATE.md` but with a reduced scope:

```yaml
---
status: Observed (not validated)
source: /reverse-engineering on {date}
---

# FEATURE-{XXX}: {short name}

## Feature Description

{What the code does, in 2-3 sentences.}

Source: {file paths and line ranges that implement this feature}

## Benefits Hypothesis

[NEEDS USER INPUT — /requirements-engineering will define this
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

### Phase 4: Business reverse engineering → BA draft

This is the most constrained phase. Read:

- `README.md` — especially intro, use cases, motivation
- `docs/` or `documentation/` content
- `package.json` / `pyproject.toml` `description`, `keywords`, `author`
- `CHANGELOG.md` — historical goals and removed features
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

Append each finding as an entry to `_devprocess/context/10_backlog.md`
with priority `P2` by default (the team will reprioritise during BA/RE):

```
### BL-{NNN}: {short title}
Priority: P2
Source: /reverse-engineering on {date}
Evidence: {path:line or description}
Notes: {1-2 sentences}
```

### Phase 6: Handoff Ritual

The handoff follows the standard 3-part pattern.

**Part 1: Artifact report**

```
Reverse Engineering complete for {PROJECT}

Scope: {Simple / PoC / MVP}
Tech stack: {summary from plan-context.md}

Artifacts produced:
- plan-context.md                          (Snapshot)
- {N} ADRs                                 (Inferred)
- arc42.md                                 (Snapshot, {M}/12 sections filled)
- {N} FEATURE-*.md                         (Observed)
- BA-{PROJECT}.md                          (Draft, {filled}/{total} sections
                                            evidence-backed, {placeholder} open)
- {N} new backlog entries                  (BL-NNN, P2)

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

> "Technical context is captured. I built an evidence-based BA draft
> too — but it is **not validated**. Every claim in the BA comes
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
   every ADR, every FEATURE, the BA draft — all carry an explicit
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

If any gate fails, you fix it before running the Handoff Ritual.
The user will not catch silent hallucinations — the gates are your
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

This skill follows the conventions from `/project-conventions`. It
writes to the same `_devprocess/` paths the forward skills use, with
status markers distinguishing reverse-engineered from validated
artifacts. Ensure the structure exists before writing:

```bash
mkdir -p _devprocess/{analysis,requirements/{features,handoff},architecture,context}
touch _devprocess/context/10_backlog.md _devprocess/context/30_handoffs.md
```

## Keywords

reverse engineering, existing project, legacy codebase, brownfield,
onboard existing, import code, we already have code, existing app,
legacy import, codebase snapshot, reverse engineer, extract artifacts,
bestehendes Projekt, existierender Code, Legacy-Projekt, Code-Import
