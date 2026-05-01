# tools/migration/

Project-agnostic migration scripts that bring an existing repo to
current DIA conventions. Used by both:

- `/reverse-engineering` (during Phase -1, when brownfield onboarding
  detects pre-existing DIA-style artefacts that need normalization
  before the code-walk fills the gaps)
- `/dia-migration` (as a convenience wrapper for users who already
  have DIA artefacts and want to upgrade between DIA versions without
  running the full reverse-engineering walk)

The scripts are also directly callable via `python3 tools/migration/<script>.py`
without invoking a skill.

## Scripts

| Script                          | Phase | Purpose                                                  |
|---------------------------------|-------|----------------------------------------------------------|
| `detect_state.py`               | 0     | Inventory the repo, classify v1/v2/mixed/brownfield. JSON output. |
| `strip_frontmatter_status.py`   | 2a    | Remove `status:`, `phase:`, `last_updated:` from YAML frontmatter. |
| `strip_body_status.py`          | 2b    | Remove `**Status:**` / `> **Status**: ...` lines from artifact bodies. |
| `migrate_naming.py`             | 3     | Rename `FEATURE-NNNN` -> `FEAT-EE-FF`, `EPIC-NNN` -> `EPIC-NN`, etc. |
| `flatten_analysis.py`           | 4     | Flatten `analysis/` to four prefixes: BA, EXPLORE, RESEARCH, AUDIT. |
| `build_backlog.py`              | 5     | Regenerate `_devprocess/context/BACKLOG.md` from all artefacts. |
| `migrate_skill_names.py`        | 6     | Rewrite legacy skill names: `/business-analyse` -> `/business-analysis`, `/v-model-workflow` -> `/dia-guide`. |

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
   should run on a feature branch like `feature/dia-migration` so the
   work is reviewable and revertable as a single PR.

The `/reverse-engineering` and `/dia-migration` skills enforce both
checks before invoking these scripts.

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
