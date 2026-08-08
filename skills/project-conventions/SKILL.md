---
name: project-conventions
description: >
  Defines project structure, naming conventions, and way of working for
  all projects; other skills link here for the canonical specs. Use when
  the user mentions "project setup", "project structure", "conventions",
  "init", "initialize project", "directory structure", or starts a new
  project.
disable-model-invocation: false
---

# Project structure and conventions

This skill defines the binding standards for directory structures, file
names, and ways of working. All other skills (BA, RE, Architecture,
Coding, Testing, Security Audit) follow these conventions. Details live
in `references/`; load a reference file only when the task touches its
area.

## Codebase-awareness (core principle)

All skills operate in the context of the existing codebase, never in a
vacuum. Read `references/codebase-awareness.md` for the complete rules.
Summary: before any work, read existing code, recognize patterns,
understand dependencies, check reference implementations. The project's
`CLAUDE.md` takes PRECEDENCE over generic skill instructions.

## Canonical Specs (single home; other skills link here)

Index. Full detail: `references/canonical-specs.md`. Phase skills and
templates never restate these specs; they link here.

1. **Reader budget.** Every artifact scannable in under two minutes,
   enforced as per-artifact line caps in the single source
   `references/artifact-caps.json` (read at runtime by
   `/consistency-check`; never mirror the values). Exceeding a cap
   needs a one-line `## Reasoned exception` block at the top of the
   file, added only with justification, never routinely.
   ARCHITECTURE-MAP, MODULE-README, JSDOC-HEADER and RULES-* carry
   their caps in their template comments.
2. **Frontmatter spec.** Identity and relations only; `status`,
   `phase`, `author`, `claim` are forbidden (N-15). Empty refs are
   omitted, never stubbed. Full key list in the reference.
3. **Backlog vocabulary.** Binding column order, GitHub-aligned status
   values, phase tags `<id>/<phase>-done`, DIA commit trailers
   (`DIA-Phase`, `DIA-Handoff`, `DIA-Triage`), ID schema, Claim and
   Refs column formats. Full vocabulary in the reference.
4. **Writing style.** Zero em/en dashes, no AI vocabulary, active
   voice, sentence case in headings. Blacklist and pre-save scan:
   `references/writing-style.md` (single home, also used by
   `/humanizer`).
5. **Activation Path format.** Fixed `## Activation Path` section in
   every FEATURE spec, parsed by N-18. Exact format in the reference.
6. **Priority / Effort legend.** P0-P3 and XS-XL definitions in the
   reference. XL at FEAT scope means: split first.
7. **Three-layer model.** Wayfinder / rule sets / backlog / detail
   artifacts with binding boundaries, the ADR abstraction rule (A-1)
   and the ADR/FEATURE/PLAN separation:
   `references/three-layer-model.md`.
8. **Section policy.** Sections are emitted only when they carry
   decision content; optional sections live in template comments, not
   as `TBD` placeholders.

## Backlog as single source of truth

State lives in the BACKLOG row, never in artifact frontmatter. The row
exists before the artifact and changes before the body. Lifecycle and
sync chain: `references/backlog-sot.md`.

## Directory structure

Full reference: `references/directory-structure.md`.

```
{project}/
  _devprocess/                    -- Internal knowledge archive (not public)
    analysis/                     -- Flat: BA-, EXPLORE-, AUDIT-, RESEARCH- (sources/ for user files)
    requirements/                 -- Epics, features, fixes, improvements, handoff
    architecture/                 -- ADRs, arc42
    rules/                        -- Stable rule sets (full profile), max 500 lines total
    implementation/plans/         -- PLAN files
    context/                      -- BACKLOG.md, BACKLOG-HISTORY.md, METRICS.md
  src/                            -- Source code + ARCHITECTURE.map + module READMEs
  docs/                           -- Public documentation (English)
  scripts/  memory/  .claude/     -- Tooling, memory, Claude config
  CLAUDE.md                       -- Project-specific context
```

## File name conventions

Full reference: `references/naming-conventions.md`. Rules: 2-digit
counters, kebab-case slugs, no spaces, no umlauts in file names.
Features are numbered within their epic (`FEAT-{ee}-{ff}-{slug}.md`),
which keeps parallel epic work conflict-free and sort order stable.

## Language conventions

| Context | Language |
|---------|----------|
| Conversation with user | User's language |
| Commit messages | English, conventional prefixes |
| Private documentation (`_devprocess/`) | Match the user's chat language |
| Public documentation (`docs/`, `README`) | English |
| Code, identifiers, skill files | English |

Artifact-language rule (binding, incl. the one clarifying question on
ambiguity): `references/canonical-specs.md#artifact-language-binding`.

## Plan structure

Every non-trivial plan has: 1. Context (diagnostic, root cause),
2. Changes (per file, BEFORE/AFTER), 3. File summary table,
4. Not affected (blast radius), 5. Verification (build is step 1).

## Git workflow

- Dual-remote: private (origin, all branches) + public (only main)
- Branch flow: `feature/*` -> `dev` -> `main` -> `public/main`
- Safe-merge: merges to dev via `scripts/merge-to-dev.sh`
- Commits: conventional prefixes, Co-Authored-By Claude, DIA trailers
  on phase-end commits (see canonical spec 3)
- Two-stage stripping for public (dev tooling, then internal docs)

## Initializing a project

Base structure, initial files, and the full `mkdir` block:
`references/canonical-specs.md#initializing-a-project`. In the lean
profile, rules consolidate into AGENTS.md instead of
`_devprocess/rules/`; see `skills/dia-setup/SKILL.md`.

## Keywords

Project structure, conventions, init, project setup, directory
structure, naming conventions, coding standards, way of working
