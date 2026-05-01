---
title: Project Conventions
description: The three-layer documentation model, directory structure, file naming, language rules, and feature lifecycle shared by all V-Model skills.
---

# Project Conventions

`/project-conventions` is the foundational skill that defines the
structure every other skill follows. It is referenced (not invoked)
by the phase skills, and it owns the three-layer documentation model.

## Codebase awareness, the core principle

All skills operate in the context of the existing codebase, never in
a vacuum. Before any work, the agent reads existing code, recognises
patterns, understands dependencies, checks reference implementations.
The project's `CLAUDE.md` takes **precedence** over generic skill
instructions.

## Three-layer documentation model

Every project organises its V-Model documentation in three layers
plus a fourth group of detail artifacts. Each layer has a different
update cadence, a different owner, and a different audience. Mixing
layers is the dominant source of doc-vs-code drift, so the
boundaries are binding.

| Layer | Purpose | Lives in |
|---|---|---|
| Wayfinder | Concept-to-file lookup, navigational, grep-friendly | `src/ARCHITECTURE.map`, JSDoc / docstring headers, module READMEs |
| Rule sets | Stable truths: stack, conventions, design rules, domain glossary. **Hard cap 500 lines total** | `_devprocess/rules/{technical,design,domain}.md` |
| Backlog | Single source of truth for status of every artifact, plus the relation graph | `_devprocess/context/BACKLOG.md` |
| Detail artifacts | Audit trail of the engineering process: BA, Epics, Features, Plans, Fixes, Improvements, ADRs | `_devprocess/analysis/`, `_devprocess/requirements/`, `_devprocess/architecture/`, `_devprocess/implementation/plans/` |

**Status, phase, last-change, and claim of every artifact live in the
backlog row, not in the artifact frontmatter.** Artifact frontmatter
carries identity (`id`, `title`, `created`) and relations (`epic`,
`adr-refs`, `feature-refs`) only.

**ADR abstraction rule.** ADR core sections (Context, Decision Drivers,
Considered Options, Decision, Consequences) contain no code paths,
file names, line numbers, or method signatures. Code-level hints
belong in the optional `## Implementation Notes` appendix at the
bottom, which is allowed to go stale. The wayfinder is the canonical
source for current paths.

See the full [Three-layer documentation model](../concepts/three-layer-documentation)
concept page for the rationale.

## Directory structure

```
{project}/
  src/
    ARCHITECTURE.map          Wayfinder root: concept | entry-point | adr | how-to-extend
    {module}/README.md        Module wayfinder (one per substantive module)
  _devprocess/                Internal knowledge archive (not public)
    analysis/                 Flat: BA-, EPIC-{nn}-ba-, EXPLORE-, AUDIT-, RESEARCH-
      sources/                User-supplied source files (only subfolder)
    requirements/
      epics/                  EPIC-{nn}-{slug}.md
      features/               FEAT-{ee}-{ff}-{slug}.md (epic-local numbering)
      fixes/                  FIX-{ee}-{ff}-{nn}-{slug}.md (bug detail files)
      improvements/           IMP-{ee}-{ff}-{nn}-{slug}.md
      handoff/                architect-handoff.md, plan-context.md
    architecture/             ADR-{nn}-{slug}.md, arc42.md
    rules/                    Stable rule sets, max 500 lines TOTAL
      technical.md            Stack, conventions, libraries
      design.md               UI rules (only if UI surface)
      domain.md               Domain glossary
    implementation/
      plans/                  PLAN-{nn}-{slug}.md
    context/
      BACKLOG.md              Single source of truth for state
      HANDOFFS.md             Append-only phase log
      METRICS.md              Signal layer (per METRICS-TEMPLATE.md)
  docs/                       Public documentation (English)
  scripts/                    Build / deploy / utility scripts
  memory/                     MEMORY.md + reference files
  .claude/
    skills/                   Project-specific skills (optional)
  CLAUDE.md                   Project-specific context
```

There is no `analysis/security/` subfolder. Audit reports live flat
under `analysis/`. There is no `20_bugs.md` file; bugs are
`FIX-{ee}-{ff}-{nn}` rows in `BACKLOG.md` plus detail files under
`requirements/fixes/`.

## File naming

| Artifact | Pattern | Example |
|---|---|---|
| Business Analysis | `BA-{PROJECT}.md` | `BA-myapp.md` |
| Epic-BA | `EPIC-{nn}-ba.md` | `EPIC-01-ba.md` |
| Epic | `EPIC-{nn}-{slug}.md` | `EPIC-01-ai-agent-core.md` |
| Feature | `FEAT-{ee}-{ff}-{slug}.md` | `FEAT-01-01-semantic-search.md` |
| ADR | `ADR-{nn}-{slug}.md` | `ADR-03-embedding-provider.md` |
| Plan | `PLAN-{nn}-{slug}.md` | `PLAN-04-semantic-search-mvp.md` |
| Fix detail | `FIX-{ee}-{ff}-{nn}-{slug}.md` | `FIX-01-02-03-null-pointer.md` |
| Improvement detail | `IMP-{ee}-{ff}-{nn}-{slug}.md` | `IMP-01-02-01-cache-warmup.md` |
| Security Audit | `AUDIT-{PROJECT}-{YYYY-MM-DD}.md` | `AUDIT-myapp-2026-03-22.md` |
| Backlog | `BACKLOG.md` | Fixed name |
| Handoffs log | `HANDOFFS.md` | Fixed name |
| Signal layer | `METRICS.md` | Fixed name |

Rules:

- **2-digit counters** with leading zeros (`01`, `42`, not `1`, not
  `001`).
- **Epic-scoped feature numbering.** Features are numbered within
  their epic, not globally. The format is
  `FEAT-{ee}-{ff}-{slug}.md`. Example: `EPIC-01` owns
  `FEAT-01-01`, `FEAT-01-02`, ...; `EPIC-13` owns `FEAT-13-01`, ....
- **Fix and Improvement scope to a feature.**
  `FIX-{ee}-{ff}-{nn}` and `IMP-{ee}-{ff}-{nn}` reference the parent
  feature.
- kebab-case slugs, no spaces, no umlauts in filenames, dates as
  `YYYY-MM-DD`.

## The three context files

- **`BACKLOG.md`** is the **single source of truth for project
  state**. Follows the binding format at
  [`skills/requirements-engineering/templates/BACKLOG-TEMPLATE.md`](https://github.com/pssah4/digital-innovation-agents/blob/main/skills/requirements-engineering/templates/BACKLOG-TEMPLATE.md)
  with a dashboard on top and rows grouped by epic. Every phase
  skill that changes project state updates this file in the same
  edit pass, **before** touching the artifact body.
- **`HANDOFFS.md`** is an append-only phase handoffs log, written by
  each phase skill at the end of its run.
- **`METRICS.md`** is the signal layer (cycle time, drift count,
  hypothesis status, phase transitions, cross-phase trigger counts).
  Append-additive, written from inside existing phase actions.

## Reference files

The skill ships four reference files under `references/`:

- [`graph-invariants.md`](https://github.com/pssah4/digital-innovation-agents/blob/main/skills/project-conventions/references/graph-invariants.md):
  the artifact graph rules that `/consistency-check` enforces
- [`team-workflow.md`](https://github.com/pssah4/digital-innovation-agents/blob/main/skills/project-conventions/references/team-workflow.md):
  branch-as-item convention, item branches, claim, GitHub flow.py
  integration
- [`naming-conventions.md`](https://github.com/pssah4/digital-innovation-agents/blob/main/skills/project-conventions/references/naming-conventions.md):
  the full naming rule set
- [`directory-structure.md`](https://github.com/pssah4/digital-innovation-agents/blob/main/skills/project-conventions/references/directory-structure.md):
  the full directory tree
- [`branch-protection.md`](https://github.com/pssah4/digital-innovation-agents/blob/main/skills/project-conventions/references/branch-protection.md):
  branch protection rules
- [`codebase-awareness.md`](https://github.com/pssah4/digital-innovation-agents/blob/main/skills/project-conventions/references/codebase-awareness.md):
  the codebase-awareness principle

## Language rules

- **Skill instructions**: English (for portability)
- **User dialog**: the agent responds in the user's language
- **Commit messages**: English, conventional prefixes
- **Public documentation**: English
- **Private documentation (`_devprocess/`)**: matches user's language
- **Code, identifiers, variables**: English

## Writing-style rules

- No em dashes (U+2014), no en dashes (U+2013). Use periods, commas,
  parentheses, "and", or "but".
- No AI vocabulary: avoid `landscape`, `nuanced`, `delve`, `leverage`,
  `crucial`, `robust`, `seamless`, `holistic`, `foster`, `ensuring`,
  `highlighting`, `underscoring`.
- No negative parallelisms ("not X but Y").
- Active voice, sentence case in headings.

The `/humanizer` skill enforces these rules across every artifact.

## Read the skill file

[`skills/project-conventions/SKILL.md`](https://github.com/pssah4/digital-innovation-agents/blob/main/skills/project-conventions/SKILL.md) on GitHub.

## See also

- [Three-layer documentation model](../concepts/three-layer-documentation):
  the rationale behind the structural rules above
- [Conventions reference](../reference/conventions): every rule in
  one place
- [Artifacts reference](../reference/artifacts): full directory tree
- [Consistency Check guide](./consistency-check): the skill that
  verifies the rules
