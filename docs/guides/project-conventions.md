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
| Epic | `EPIC-{XXX}-{slug}.md` |
| Feature | `FEATURE-{XXX}-{slug}.md` |
| ADR | `ADR-{XXX}-{slug}.md` |
| Security Audit | `AUDIT-{PROJECT}-{YYYY-MM-DD}.md` |
| Backlog | `10_backlog.md` |
| Bug log | `20_bugs.md` |
| Handoffs log | `30_handoffs.md` |

Rules: 3-digit numbers, kebab-case slugs, no spaces, no umlauts in
filenames.

## The `_devprocess/context/` files

- **`10_backlog.md`**: living backlog, maintained by `/requirements-engineering`
  and updated at the end of every V-Model cycle
- **`20_bugs.md`**: FIX-NN bug log, written by `/coding` Phase 3c
  (Debugging Protocol)
- **`30_handoffs.md`**: append-only phase handoffs log, written by
  each phase skill at the end of its run

## Language rules

- **Skill instructions**: English (for portability)
- **User dialog**: the agent responds in the user's language
- **Commit messages**: English, conventional prefixes
- **Public documentation**: English
- **Code, identifiers, variables**: English

## Source

Full skill content in
[`skills/project-conventions/SKILL.md`](https://github.com/pssah4/digital-innovation-agents/blob/main/skills/project-conventions/SKILL.md).
