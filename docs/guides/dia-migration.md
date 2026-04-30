# DIA Migration

`/dia-migration` brings any repo up to current Digital Innovation Agents
conventions. It handles three starting states:

- **DIA v1** projects whose artifacts use the old patterns
  (`FEATURE-NNNN`, `ADR-NNN`, status fields in frontmatter, `fixes/`
  under `context/`, `archive/` folders, `20_bugs.md`).
- **Older V-Model variants** with similar layout but inconsistent
  prefixes or per-cycle handoffs.
- **Brownfield repos** without a `_devprocess/` directory yet. In that
  case `/dia-migration` defers to `/reverse-engineering` for the
  artifact bootstrap, then runs its own normalisation passes.

Idempotent: running it again on a clean v2 repo performs the consistency
check and exits without changes.

## When to use it

- "Migrate this project to DIA v2"
- "Upgrade my V-Model setup"
- "Restructure the backlog as single source of truth"
- "Clean up artifact frontmatter status drift"
- "Convert FEATURE-NNNN to FEAT-NN-NN"

## What it does

Seven phases, each independently re-runnable:

| Phase | What |
|-------|------|
| 0 | Detection and plan |
| 1 | Foundation: `_devprocess/rules/`, `src/ARCHITECTURE.map`, directory layout |
| 2 | Bulk frontmatter and body status cleanup |
| 3 | Filename migration to v2 ID schemas (`FEAT-NN-NN`, `FIX-NN-NN-NN`, `ADR-NN`, ...) |
| 4 | `analysis/` flattening to four prefixes (BA, EXPLORE, RESEARCH, AUDIT) |
| 5 | Backlog regeneration as single source of truth |
| 6 | Skill name updates (`/business-analyse` -> `/business-analysis`, `/v-model-workflow` -> `/dia-orchestrator`) |
| 7 | Consistency check (`/consistency-check` mode A with auto-fix) |

## Safety

- Refuses to run on `main`, `master`, or `dev`. Use a feature branch.
- Source code under `src/` is not edited (only `src/ARCHITECTURE.map`
  and module READMEs are added). JSDoc headers in `.ts`/`.js` files
  are proposed but not auto-written.
- Deletes are listed before execution; the user confirms.
- The previous backlog is preserved as `BACKLOG.md.preMigration` for
  one-step rollback.
- Each phase commits separately, so any phase can be rolled back via
  `git reset --hard HEAD`.

## Tools

The skill ships seven Python scripts under `skills/dia-migration/tools/`.
They run independently of the skill prose (you can invoke them by hand
on a CI runner if you want):

- `detect_state.py` -- Phase 0 inventory (JSON report on stdout)
- `strip_frontmatter_status.py` -- Phase 2a
- `strip_body_status.py` -- Phase 2b
- `migrate_naming.py` -- Phase 3 (renames plus reference replacement)
- `flatten_analysis.py` -- Phase 4
- `build_backlog.py` -- Phase 5 (regenerates `BACKLOG.md`)
- `migrate_skill_names.py` -- Phase 6

All scripts:

- Take the project root as the first argument (default: `cwd`)
- Are idempotent
- Exit non-zero on errors so the orchestrating skill can stop the pipeline

## Typical run

```
git checkout -b feature/dia-migration
# Tell the agent in your tool: "migrate this project to DIA v2"
# Or run /dia-migration directly
```

The skill walks you through the seven phases, asking before deletes
and overwrites. At the end you have a clean v2 repo on a feature
branch, ready to merge once you have reviewed the commits.
