---
title: Project Conventions
description: Directory structure, file naming, language rules, and feature lifecycle shared by all V-Model skills.
---

# Project Conventions

`/project-conventions` is the foundational skill that defines the
structure every other skill follows. It is referenced (not invoked)
by the other phase skills.

## Directory structure

```
{project}/
  _devprocess/              Internal knowledge archive (not public)
    analysis/               Business Analysis + Security Audits
    requirements/           Epics, Features, handoff documents
    architecture/           ADRs, arc42
    context/                Backlog, bugs, handoffs
  src/                      Source code
  docs/                     Public documentation
  scripts/                  Build/deploy utility scripts
  memory/                   MEMORY.md + reference files
  CLAUDE.md                 Project-specific context
```

## File naming

| Artifact | Pattern |
|---|---|
| Business Analysis | `BA-{PROJECT}.md` |
| Epic | `EPIC-{NNN}-{slug}.md` |
| Feature | `FEATURE-{EPIC}-{NNN}-{slug}.md` (epic-local, e.g. `FEATURE-001-001-...`) |
| ADR | `ADR-{NNN}-{slug}.md` |
| Security Audit | `AUDIT-{PROJECT}-{YYYY-MM-DD}.md` |
| Backlog | `BACKLOG.md` |
| Bug log | `20_bugs.md` |
| Handoffs log | `HANDOFFS.md` |

Rules: 3-digit numbers, kebab-case slugs, no spaces, no umlauts in
filenames. Features are numbered inside their parent epic, not
globally: `FEATURE-{EPIC}-{NNN}` where `{ee}` is the 2-digit epic
number identical to the parent epic's filename number. Example:
EPIC-001 owns FEATURE-001-001, FEATURE-001-002, ...; EPIC-013 owns
FEATURE-013-001, ...

## The `_devprocess/context/` files

- **`BACKLOG.md`**: living backlog and **single source of truth
  for the project state**. Follows the binding format at
  [`skills/requirements-engineering/templates/BACKLOG-TEMPLATE.md`](https://github.com/pssah4/digital-innovation-agents/blob/main/skills/requirements-engineering/templates/BACKLOG-TEMPLATE.md)
  with a dashboard on top, entries grouped by Epic, standalone items
  for epic-free findings, and a reference list of open bugs from
  `20_bugs.md`. Every phase skill that changes project state updates
  this file in the same edit pass
- **`20_bugs.md`**: FIX-NN bug log, written by `/coding` Phase 3c
  (Debugging Protocol)
- **`HANDOFFS.md`**: append-only phase handoffs log, written by
  each phase skill at the end of its run

## Language rules

- **Skill instructions**: English (for portability)
- **User dialog**: the agent responds in the user's language
- **Commit messages**: English, conventional prefixes
- **Public documentation**: English
- **Code, identifiers, variables**: English

## Read the skill file

[`skills/project-conventions/SKILL.md`](https://github.com/pssah4/digital-innovation-agents/blob/main/skills/project-conventions/SKILL.md) on GitHub.
