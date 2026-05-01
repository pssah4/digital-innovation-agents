---
title: DIA Migration
description: Bring any repo up to v3 conventions. Handles legacy DIA v1 / v2 projects, older V-Model variants, and brownfield repos.
---

# DIA Migration

`/dia-migration` brings any repo up to current Digital Innovation
Agents conventions. It handles three starting states:

- **DIA v1 / v2 projects** whose artifacts use older patterns
  (`FEATURE-NNNN`, `EPIC-NNN`, `ADR-NNN`, status fields in
  frontmatter, `fixes/` under `context/`, `archive/` folders,
  `20_bugs.md`, `analysis/security/` subfolder).
- **Older V-Model variants** with similar layout but inconsistent
  prefixes or per-cycle handoffs.
- **Brownfield repos** without a `_devprocess/` directory yet. In
  that case `/dia-migration` defers to `/reverse-engineering` for
  the artifact bootstrap, then runs its own normalisation passes.

Idempotent: running it again on a clean v3 repo performs the
consistency check and exits without changes.

## When to use it

- "Migrate this project to DIA v3"
- "Upgrade my V-Model setup"
- "Restructure the backlog as single source of truth"
- "Clean up artifact frontmatter status drift"
- "Convert FEATURE-NNNN to FEAT-EE-FF"
- "Move audit reports out of analysis/security/ subfolder"

## Pre-Phase 0: branch and item check

Mandatory before any work. The skill refuses to run on `main`,
`master`, or `dev`. It expects a dedicated migration branch:

```
chore/dia-migration-{YYYY-MM-DD}
```

The migration is treated as one item with a single backlog row. Phase
commits and the `tag-phase` mechanism work the same way as in normal
phase skills.

## What it does

Eight phases, each independently re-runnable:

| Phase | What |
|---|---|
| 0 | Detection and migration plan |
| -1.5 | Brownfield handover: defer to `/reverse-engineering` if no `_devprocess/` exists |
| 1 | Foundation: `_devprocess/rules/`, `src/ARCHITECTURE.map`, full directory layout |
| 2 | Bulk frontmatter and body status cleanup (status moves from frontmatter to backlog row) |
| 3 | Filename migration to v3 ID schemas (`FEAT-{ee}-{ff}`, `FIX-{ee}-{ff}-{nn}`, `IMP-{ee}-{ff}-{nn}`, `EPIC-{nn}`, `ADR-{nn}`, `PLAN-{nn}`) |
| 4 | `analysis/` flattening to four prefixes (BA, EXPLORE, RESEARCH, AUDIT). The `analysis/security/` subfolder is removed; audit reports move flat into `analysis/` |
| 5 | Backlog regeneration as single source of truth, with rows reflecting the three-layer model |
| 6 | Skill name updates (`/business-analyse` -> `/business-analysis`, `/v-model-workflow` -> `/dia-guide`) |
| 7 | Consistency check (`/consistency-check` Mode A with auto-fix) |

## Safety

- Refuses to run on `main`, `master`, or `dev`. Use a dedicated
  `chore/dia-migration-{YYYY-MM-DD}` branch.
- Source code under `src/` is not edited (only
  `src/ARCHITECTURE.map` and module READMEs are added). JSDoc /
  docstring headers are proposed but not auto-written.
- Deletes are listed before execution; the user confirms.
- The previous backlog is preserved as `BACKLOG.md.preMigration`
  for one-step rollback.
- Each phase commits separately, so any phase can be rolled back
  via `git reset --hard HEAD`.

## Shared tools

Phase scripts live under `tools/migration/`, shared between
`/dia-migration` and `/reverse-engineering` (which uses them as
sub-routines after its initial inventory). They run independently
of the skill prose (you can invoke them by hand on a CI runner):

- `detect_state.py`: Phase 0 inventory (JSON report on stdout)
- `strip_frontmatter_status.py`: Phase 2a
- `strip_body_status.py`: Phase 2b
- `migrate_naming.py`: Phase 3 (renames plus reference replacement,
  including `FEATURE-{EPIC}-{NNN}` -> `FEAT-{ee}-{ff}` and 3-digit
  -> 2-digit counters)
- `flatten_analysis.py`: Phase 4 (removes `analysis/security/`,
  consolidates into flat `analysis/`)
- `build_backlog.py`: Phase 5 (regenerates `BACKLOG.md` from the
  template, reflecting the three-layer model)
- `migrate_skill_names.py`: Phase 6

All scripts:

- Take the project root as the first argument (default: `cwd`)
- Are idempotent
- Exit non-zero on errors so the orchestrating skill can stop the
  pipeline

## Typical run

```bash
git checkout -b chore/dia-migration-2026-04-30
```

In your coding tool, tell the agent: "migrate this project to DIA
v3". Or run `/dia-migration` directly.

The skill walks you through the eight phases, asking before deletes
and overwrites. At the end you have a clean v3 repo on a dedicated
branch, ready to merge once you have reviewed the commits.

## Brownfield projects

For repos with code but no `_devprocess/` artifacts yet, use
[`/reverse-engineering`](./reverse-engineering) instead. It walks
the V backwards from code to BA, fills every artifact with
evidence, and absorbs the same migration mechanics for any
pre-existing partial artifacts. `/dia-migration` is the **upgrade**
entry; `/reverse-engineering` is the **bootstrap** entry.

## Read the skill file

[`skills/dia-migration/SKILL.md`](https://github.com/pssah4/digital-innovation-agents/blob/main/skills/dia-migration/SKILL.md)
on GitHub.
