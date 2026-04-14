---
name: project-conventions
description: >
  Defines project structure, naming conventions, and way of working for all
  projects. Referenced by other skills to ensure consistent directory
  structures, file names, and documentation standards. Use this skill when
  the user mentions "project setup", "project structure", "conventions",
  "init", "initialize project", "directory structure", or similar. Also
  automatically relevant when starting a new project.
disable-model-invocation: false
---

# Project Structure & Conventions

This skill defines the binding standards for directory structures, file
names, and ways of working. All other skills (BA, RE, Architecture, Coding,
Testing, Security Audit) follow these conventions.

## Codebase-Awareness -- Core Principle

All skills operate in the context of the existing codebase, never in a
vacuum. Read `references/codebase-awareness.md` for the complete rules.

Summary: Before any work, read existing code, recognize patterns, understand
dependencies, check reference implementations. The project's `CLAUDE.md`
takes PRECEDENCE over generic skill instructions.

## Directory Structure

Every project has this base structure. Not all directories are created
upfront -- they emerge during the V-Model workflow.

Read `references/directory-structure.md` for the full reference.

### Short overview

```
{project}/
  _devprocess/                    -- Internal knowledge archive (not public)
    analysis/                     -- Business Analysis & Security Audits
    requirements/                 -- Epics, Features, handoff documents
    architecture/                 -- ADRs, arc42
    context/                      -- Backlog, bugs, handoffs, status docs
  src/                            -- Source code
  docs/                           -- Public documentation (English)
  scripts/                        -- Build/Deploy/Utility scripts
  memory/                         -- MEMORY.md + reference files
  .claude/                        -- Claude Code configuration
    skills/                       -- Project-specific skills (optional)
  CLAUDE.md                       -- Project-specific context
```

## File Name Conventions

Read `references/naming-conventions.md` for the full reference.

### Short overview

| Artifact | Pattern | Example |
|----------|---------|---------|
| Business Analysis | `BA-{PROJECT}.md` | `BA-obsilo.md` |
| Exploration Board | `EXPLORE-{PROJECT}.md` | `EXPLORE-obsilo.md` |
| Epic | `EPIC-{NNN}-{slug}.md` | `EPIC-001-ai-agent-core.md` |
| Feature | `FEATURE-{EPIC}-{NNN}-{slug}.md` | `FEATURE-001-001-semantic-search.md` |
| ADR | `ADR-{NNN}-{slug}.md` | `ADR-003-embedding-provider.md` |
| Security Audit | `AUDIT-{PROJECT}-{YYYY-MM-DD}.md` | `AUDIT-obsilo-2026-03-22.md` |
| Handoff (RE->Arch) | `architect-handoff.md` | Fixed name |
| Handoff (Arch->Code) | `plan-context.md` | Fixed name |
| Backlog | `10_backlog.md` | Fixed name |
| Bug log | `20_bugs.md` | Fixed name (FIX-NN entries) |
| Handoffs log | `30_handoffs.md` | Fixed name (append-only) |

Rules: 3-digit numbers, kebab-case slugs, no spaces, no umlauts in file names.

**Epic-scoped feature numbering:** Features are numbered within their
epic, not globally. The format is `FEATURE-{EPIC}-{NNN}-{slug}.md`
where `EPIC` is the 3-digit epic number (identical to the number in
the epic's filename) and `NNN` is the 3-digit feature counter local
to that epic. Examples:

- EPIC-001 -> FEATURE-001-001, FEATURE-001-002, FEATURE-001-003, ...
- EPIC-002 -> FEATURE-002-001, FEATURE-002-002, ...
- EPIC-013 -> FEATURE-013-001, FEATURE-013-002, ...

This keeps epic and feature traceable via the filename alone, makes
parallel epic work conflict-free (two epics can each start at
FEATURE-{EPIC}-001), and keeps alphabetical sort order stable.

### The `_devprocess/context/` files

Three living documents live side-by-side under `_devprocess/context/`:

- **`10_backlog.md`** -- the project backlog and **single source of
  truth for the project state**. Follows the binding template at
  `skills/requirements-engineering/templates/BACKLOG-TEMPLATE.md`.
  Entries for features, chores, security findings, and deferred items,
  grouped by Epic with a dashboard on top. MUST be updated after every
  status-changing action (new entry, status transition, priority or
  epic change, implementation done). Every agent that touches the
  project state also touches this file.
- **`20_bugs.md`** -- the bug log. Populated by the `/coding` skill's
  debugging protocol (see `skills/coding/SKILL.md` Phase 3c). Each entry
  uses a `FIX-NN` ID with priority (P0/P1/P2), causal chain, and (after
  resolution) commit SHA and regression-test status.
- **`30_handoffs.md`** -- the phase handoffs log. Append-only. Each phase
  skill writes one entry at the end of its run with: artifacts produced,
  handoff context (open questions, assumptions, risks), and next phase.
  Used by the next skill to pick up context without re-reading all artifacts.

The numbering (`10_`, `20_`, `30_`) leaves room for future additions
without renumbering.

## Language Conventions

| Context | Language |
|---------|----------|
| Conversation with user | User's language (agent adapts automatically) |
| Commit messages | English, conventional prefixes (feat/fix/chore/docs/refactor) |
| Private documentation (`_devprocess/`) | Match user's language (agent decides) |
| Public documentation (`docs/`, `README`) | English |
| Code, identifiers, variables | English |
| Skill files (`SKILL.md`) | English (user language adapts in dialog) |

**Note:** Skills are written in English so they are portable across
languages, but when a skill runs and talks to the user, the agent switches
to the user's language. See `skills/using-digital-innovation-agents/SKILL.md`.

## Feature Lifecycle

Every feature goes through:

```
1. BACKLOG          -- Entry in _devprocess/context/10_backlog.md
2. FEATURE-SPEC     -- Write spec BEFORE implementation
3. PLAN             -- Plan-Mode: create implementation plan
4. IMPLEMENTATION   -- Code, build+deploy after each step
5. SPEC UPDATE      -- Feature-spec becomes reference doc
6. BACKLOG UPDATE   -- Immediately after implementation
```

## Plan Structure

Every non-trivial plan has:

1. **Context** -- Diagnostic, not descriptive. Root-cause analysis
2. **Changes** -- Per file one subsection, BEFORE/AFTER code blocks
3. **File summary** -- Table (File | Change | Risk)
4. **Not affected** -- Explicit list of UNCHANGED files (blast radius)
5. **Verification** -- Acceptance criteria, build always step 1

## Git Workflow

- Dual-remote: private (origin, all branches) + public (only main)
- Branch flow: `feature/*` -> `dev` -> `main` -> `public/main`
- Safe-merge: merges to dev via `scripts/merge-to-dev.sh`
- Commits: conventional prefixes, Co-Authored-By Claude
- Two-stage stripping for public (dev tooling, then internal docs)

## Debugging Conventions

Bugs as causal chains:
```
Problem: [observable behavior]
Root Cause: [why it happens]
Chain: step 1 -> step 2 -> ... -> error
```

Bug IDs: `FIX-NN` (P0 = immediate, P1 = short-term, P2 = medium-term).
Security findings: `H-N` / `M-N` / `L-N` (High/Medium/Low).

All bugs discovered during `/coding` land in `_devprocess/context/20_bugs.md`
with the full causal chain and priority.

## Memory Conventions

- `CLAUDE.md` (global `~/.claude/`): HOW we work (cross-project)
- `CLAUDE.md` (project-root): project-specific context
- `memory/MEMORY.md`: key facts, short references (< 200 lines)
- Detailed references: separate files, linked from MEMORY.md
- Update existing entries instead of creating new ones
- Actively delete outdated entries

## Initializing a Project

When setting up a new project, create this base structure:

```bash
mkdir -p _devprocess/{analysis/security,requirements/{epics,features,handoff},architecture,context}
mkdir -p src docs scripts memory
```

And create the initial files:
- `_devprocess/context/10_backlog.md` -- seeded from
  `skills/requirements-engineering/templates/BACKLOG-TEMPLATE.md`
  with the project name filled in and empty dashboard counts
- `_devprocess/context/20_bugs.md` (empty bug log)
- `_devprocess/context/30_handoffs.md` (empty handoffs log)
- `CLAUDE.md` (project context template)
- `memory/MEMORY.md` (empty memory template)

## Keywords
Project structure, conventions, init, project setup, directory structure,
naming conventions, coding standards, way of working
