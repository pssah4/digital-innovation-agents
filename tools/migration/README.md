# tools/migration/

Project-agnostic migration scripts that bring an existing repo to
current DIA conventions. Orchestrated by `/dia-realign` (the merged
successor of the retired `/reverse-engineering` and `/dia-migration`
skills): `detect_state.py` picks the mode, Mode B runs the scripts
as its script pass, and the reverse walk uses them to normalize any
pre-existing DIA-style artefacts before the code walk fills the gaps.

The scripts are also directly callable via `python3 tools/migration/<script>.py`
without invoking a skill.

## Scripts

| Script                          | Phase | Purpose                                                  |
|---------------------------------|-------|----------------------------------------------------------|
| `detect_state.py`               | 0     | Inventory the repo, classify v1/v2/mixed/brownfield. JSON output. |
| `strip_frontmatter_status.py`   | 2a    | Remove `status:`, `phase:`, `last_updated:` from YAML frontmatter. |
| `strip_body_status.py`          | 2b    | Remove `**Status:**` / `> **Status**: ...` lines from artifact bodies. |
| `migrate_naming.py`             | 3     | Rename `FEATURE-NNNN` -> `FEAT-EE-FF`, `EPIC-NNN` -> `EPIC-NN`, normalise Item-BA filenames (`BA-EPIC-NN`, `BA-FEAT-EE-FF`, `BA-IMP-EE-FF-NN`, `BA-FIX-EE-FF-NN`), warn on legacy generic `BA-NNN-{slug}.md` that needs manual triage. |
| `flatten_analysis.py`           | 4     | Flatten `analysis/` to four prefixes (BA, EXPLORE, RESEARCH, AUDIT). Move legacy mini-BAs `_devprocess/requirements/epics/EPIC-NN-ba.md` to `_devprocess/analysis/BA-EPIC-NN-{slug}.md`. |
| `build_backlog.py`              | 5     | Regenerate `_devprocess/context/BACKLOG.md` from all artefacts. Restore `ba-ref:` in EPIC/FEAT/IMP/FIX frontmatter when a matching Item-BA exists in `analysis/`. |
| `migrate_status_vocabulary.py`  | 5b    | Map legacy BACKLOG Status values to the GitHub-aligned vocabulary (`Planned` -> `Ready` etc.). |
| `migrate_skill_names.py`        | 6     | Rewrite legacy skill names: `/business-analyse` -> `/business-analysis`, `/v-model-workflow` -> `/dia-guide`, `/reverse-engineering` and `/dia-migration` -> `/dia-realign`. |
| `shrink_artifacts_v3.py`        | 6b    | Align existing artefacts with the shrunk v3.6 templates. Dry-run by default, `--apply` to write. |

All scripts:

- Auto-detect the repo root via `git rev-parse --show-toplevel`, or
  accept a `project_root` argument as override.
- Are idempotent. Running on an already-migrated repo is a no-op.
- Print a summary at the end (files changed, refs updated).
- Exit non-zero on any error so the caller can stop the pipeline.

## Pre-flight requirements

These scripts modify artefact files. Before running, verify:

1. The working tree is clean (`git status --short` returns nothing).
2. The current branch is **not** `main`, `master`, or `dev`. Migration
   should run on a dedicated branch like `chore/dia-realign-<date>`
   so the work is reviewable and revertable as a single PR.

The `/dia-realign` skill enforces both checks before invoking these
scripts.

## Direct invocation

```bash
# Phase 0: detect what state the repo is in
python3 tools/migration/detect_state.py

# Phase 2: strip status duplicates (frontmatter + body)
python3 tools/migration/strip_frontmatter_status.py
python3 tools/migration/strip_body_status.py

# Phase 5: regenerate the backlog
python3 tools/migration/build_backlog.py
```

The skills run them in order with confirmation gates between phases.
