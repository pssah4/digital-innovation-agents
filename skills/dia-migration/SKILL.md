---
name: dia-migration
description: >
 Convenience wrapper for existing DIA users upgrading between DIA
 versions (e.g. v1 -> v2 -> v3). Runs the migration scripts under
 `tools/migration/` in sequence: detect state, strip status
 duplicates, rename IDs (FEATURE-NNNN -> FEAT-EE-FF, EPIC-NNN ->
 EPIC-NN), flatten analysis/, regenerate BACKLOG.md, update
 skill-name references, run `/consistency-check` mode A. Idempotent.
 Use this skill when the user already has DIA artefacts and wants
 to upgrade to current conventions without the full
 reverse-engineering walk. Triggers: "migrate to DIA v2", "migrate
 v1", "upgrade DIA", "convert backlog", "restructure backlog",
 "FEATURE to FEAT". For BROWNFIELD projects (no `_devprocess/` yet,
 only code), use `/reverse-engineering` instead -- it absorbs the
 same migration mechanics for any pre-existing partial artefacts
 and additionally walks the code to fill the gaps.
disable-model-invocation: false
---

# DIA Migration

Convenience wrapper that brings an **existing DIA repo** to current
conventions. Not a brownfield onboarding skill -- for that, use
`/reverse-engineering`, which contains the same migration mechanics
plus a full code-walk for missing artefacts.

Designed for two starting states:

- **DIA v1 -> current**: artefacts use the old patterns
  (FEATURE-NNNN, ADR-NNN, status in frontmatter, fixes under context/,
  archive/ folders, 20_bugs.md, numeric-prefixed context files).
- **Older V-Model variant -> current**: same DIA layout idea but
  inconsistent prefixes or per-cycle handoffs.

For **brownfield without V-Model artefacts** (code exists, no
`_devprocess/` directory): the answer is `/reverse-engineering`.
That skill detects pre-existing partial artefacts, runs the same
migration scripts as Phase -1.5, then walks the code to produce
the missing artefacts. Do not start with `/dia-migration` for
brownfield -- you would only get the migration step without the
artefact-bootstrap from code.

The skill is **idempotent**. Running it on an already-current repo
performs the consistency check and exits without changes.

## Shared tooling

This skill orchestrates the scripts under `tools/migration/` in the
DIA repo:

| Script                          | Phase | Purpose                                                  |
|---------------------------------|-------|----------------------------------------------------------|
| `tools/migration/detect_state.py`         | 0 | Inventory the repo, classify v1/v2/mixed.                |
| `tools/migration/strip_frontmatter_status.py` | 2a | Remove `status:` / `phase:` from YAML frontmatter. |
| `tools/migration/strip_body_status.py`    | 2b | Remove body-level `**Status:**` / `> **Status**:` lines. |
| `tools/migration/migrate_naming.py`       | 3 | Rename ID schemas (FEATURE-NNNN -> FEAT-EE-FF, etc.).  |
| `tools/migration/flatten_analysis.py`     | 4 | Flatten analysis/ to BA / EXPLORE / RESEARCH / AUDIT.    |
| `tools/migration/build_backlog.py`        | 5 | Regenerate BACKLOG.md from artefact scan.                |
| `tools/migration/migrate_skill_names.py`  | 6 | Rewrite `/business-analyse` -> `/business-analysis`,
   `/v-model-workflow` -> `/dia-orchestrator`. |

`/reverse-engineering` reuses the same scripts under Phase -1.5.
Both skills share the canonical implementation; this one wraps it
with a phase-by-phase confirmation loop, the other one runs them
silently as part of the backwards walk.

## Writing style

Every artifact this skill writes follows the rules in
`skills/project-conventions/SKILL.md` under "Writing style for every
artifact". No em dashes, no AI vocabulary, no negative parallelisms,
sentence case in headings.

## When to invoke

User says:

- "migrate this project to DIA v2"
- "upgrade my V-Model setup"
- "restructure the backlog"
- "clean up artifact frontmatter"
- "convert FEATURE-NNNN to FEAT-NN-NN"

Or: another skill (typically `/dia-orchestrator` on first run against
a non-conforming repo) calls `/dia-migration` to bring the structure
in line before continuing.

## Safety contract

The skill operates on a feature branch. It does not push, it does not
touch source code, and it does not delete user-authored content
without explicit confirmation. Concrete rules:

1. Branch check at start. Refuse to run on `main`, `master`, or
   `dev`. The user must create a migration branch first
   (`git checkout -b feature/dia-migration` is the typical name).
2. Source code under `src/` (or the project's code root) is only
   edited to add `src/ARCHITECTURE.map` and optional
   `src/{module}/README.md` files. JSDoc headers in `.ts`/`.js`
   files are NOT auto-written. The skill proposes a list and asks.
3. Files outside `_devprocess/` and `src/` are not touched.
4. Deletes are listed before execution. `archive/` folders, the
   legacy `20_bugs.md`, and superseded handoff files are removed
   only after the user sees the list.
5. If git status is dirty at start, the skill stops and asks the
   user to commit or stash first. Mid-migration commits on a clean
   tree are encouraged so each phase is reversible.

## Phases

The skill walks seven phases. Each phase is independently
re-runnable. If a phase fails, the next one is not started.

### Phase 0: Detection and plan

Inventory the repo and classify it. Outputs a one-page plan for
user review.

- Detect project root convention: `_devprocess/`, `docs/`, or none.
- Scan for old vs. new patterns:
  - filename pattern `FEATURE-NNNN` (4-digit) -> v1
  - filename pattern `FEAT-NN-NN` -> v2
  - presence of `_devprocess/context/fixes/` -> v1
  - presence of `_devprocess/requirements/fixes/` -> v2
  - presence of `_devprocess/context/20_bugs.md` -> v1
  - presence of any `archive/` directory under `_devprocess/` -> v1
  - frontmatter `status:` or `phase:` fields -> v1
  - body-level `**Status:**` headers in artifacts -> v1
- Count each finding.
- Decide migration scope:
  - all v2 patterns, no findings -> exit with green report
  - mixed -> run all phases (each is idempotent)
  - brownfield (no `_devprocess/` and no `docs/`) -> hand off to
    `/reverse-engineering` first, then continue here

The plan is saved as a Markdown report at
`_devprocess/context/HANDOFFS.md` under a new entry
`dia-migration plan {date}` and printed for the user.

### Phase 1: Foundation

Create the layers that DIA v2 requires regardless of starting state.

1. `_devprocess/rules/` with `technical.md` (always),
   `design.md` (only if the project has UI surface), `domain.md`
   (always). Seeded from
   `skills/architecture/templates/RULES-*-TEMPLATE.md`. If files
   already exist, leave them in place but check the line budget
   (max 500 lines total).
2. `src/ARCHITECTURE.map` seeded from
   `skills/architecture/templates/ARCHITECTURE-MAP-TEMPLATE.md`. If
   a map already exists, validate it; otherwise scan `src/` for
   entry-point candidates (large files containing `class`,
   `interface`, `Manager`, `Service`, `Registry`, `Pipeline` in
   their names) and propose initial rows. The user confirms before
   writing.
3. `_devprocess/requirements/{epics,features,fixes,improvements,handoff}/`
   directories. Move existing `_devprocess/context/fixes/` to
   `_devprocess/requirements/fixes/` and same for `improvements/`.
4. `_devprocess/analysis/` flattened: `analysis/security/AUDIT-*`
   moves to `analysis/` root, `archive/` deleted (with the file
   list shown to the user first).
5. `_devprocess/context/20_bugs.md` deleted. The backlog regenerated
   in Phase 5 carries the FIX status.

### Phase 2: Bulk frontmatter and body status cleanup

Every artifact under `_devprocess/requirements/`, `architecture/`,
`implementation/plans/`, `context/fixes/`, `context/improvements/`
gets two passes:

1. **Frontmatter pass**: remove `status:`, `phase:`, `last_updated:`,
   `last-updated:`, `lastUpdated:` lines from the YAML frontmatter.
   Multi-line values are removed entirely.
2. **Body header pass**: in the first 25 lines after the frontmatter,
   remove lines matching `**Status:** X`, `> **Status:** X`,
   `Status: Implemented`, `Status: Akzeptiert`, etc. Also
   `**Last Updated:** ...` and German equivalents.

Run via `tools/migration/strip_frontmatter_status.py` and
`tools/migration/strip_body_status.py` (both live under `tools/migration/` in the DIA repo).

After this phase, the repo's status truth lives ONLY in the backlog.

### Phase 3: Filename migration to DIA v2 ID schemas

Renames artifact files and updates all cross-references in
`.md`-files plus `src/ARCHITECTURE.map`. Idempotent.

| Old pattern              | New pattern                | Notes                                  |
|--------------------------|----------------------------|----------------------------------------|
| `EPIC-NNN-{slug}.md`     | `EPIC-{nn}-{slug}.md`      | strip leading zero, fits in 2 digits   |
| `FEATURE-NNNN-{slug}.md` | `FEAT-{ee}-{ff}-{slug}.md` | prefix change FEATURE -> FEAT, hyphen split |
| `FEATURE-NNN-{slug}.md`  | `FEAT-{ee}-{ff}-{slug}.md` | legacy 3-digit (e.g. FEATURE-400) gets normalized |
| `FIX-{eeff}-{nn}-{slug}.md` | `FIX-{ee}-{ff}-{nn}-{slug}.md` | hyphen split for clarity            |
| `IMP-{eeff}-{nn}-{slug}.md` | `IMP-{ee}-{ff}-{nn}-{slug}.md` | analog                              |
| `ADR-NNN-{slug}.md`      | `ADR-{nn}-{slug}.md`       | strip leading zero                     |
| `PLAN-NNN-{slug}.md`     | `PLAN-{nn}-{slug}.md`      | strip leading zero                     |
| `BA-NNN-{slug}.md`       | `BA-{nn}-{slug}.md`        | strip leading zero                     |
| `EXPLORE-NNN-{slug}.md`  | `EXPLORE-{nn}-{slug}.md`   | strip leading zero                     |
| `RESEARCH-NNN-{slug}.md` | `RESEARCH-{nn}-{slug}.md`  | strip leading zero                     |
| handoff files            | `architect-handoff-FEAT-{ee}-{ff}.md`, `plan-context-FEAT-{ee}-{ff}.md` | per active feature stream |

Run via `tools/migration/migrate_naming.py`. The script does two passes: first
the file renames, then a global text replacement of references using
the rename map. A second sweep catches body references to IDs that
do not have a corresponding file (e.g. an EPIC-023 mentioned in
prose but never created).

When the file count exceeds 99 in any class, the script suggests
extending that class to 3-digit (e.g. `EPIC-100`). The user confirms
before applying. Until then, 2-digit is the default.

The append-only `_devprocess/context/HANDOFFS.md` is exempt from
the body sweep. Historical entries keep their original IDs as
audit-trail records.

### Phase 4: analysis/ flattening to four prefixes

Reduces the analysis/ directory to four prefixes: `BA-`, `EXPLORE-`,
`RESEARCH-`, `AUDIT-`.

- `CODEBASE-NNN`, `DESIGN-NNN`, `SECURITY-NNN`, `SPIKE-NNN`,
  `FINDING-`, `ROOT-CAUSE-`, `GAP-ANALYSE-`, `SOLUTION-PROPOSAL-`,
  `SCAFFOLD-`, `MOBILE-`, `STANDALONE-`, `TEMPLATE-`, `REVIEW-`,
  `ANALYSIS-`, `HANDOFF-` -> renamed to `RESEARCH-NN-{originalprefix-slug}`,
  preserving the old prefix in the slug for traceability.
- `analysis/security/AUDIT-*.md` -> moved to `analysis/AUDIT-*.md`
  (flat).
- `analysis/security/` and `analysis/archive/` directories deleted
  (archive content has typically been replaced by the backlog).
- External content (blog posts, reddit posts) -> moved to
  `_devprocess/articles/` if present.

Run via `tools/migration/flatten_analysis.py`.

### Phase 5: Backlog regeneration

Build `_devprocess/context/BACKLOG.md` from scratch by scanning
all artifacts. The new backlog is the single source of truth for
status, phase, claim, and Refs.

- One row per Feature, Fix, Improvement, ADR, Plan.
- Epics are section headers, not rows.
- Status defaults from heuristics:
  - Features in epics 01-22 (or whatever ranges the user marks as
    "shipped") default to Done/Released.
  - Features in active epics default to Active/Building.
  - ADRs default to Accepted/Released for old ADRs and
    Accepted/Building for new ones (cutoff: numeric ID >=
    `last_shipped_adr + 1`, asked from the user once).
  - PLANs default to Draft/Building.
- The Refs column is populated from frontmatter `epic:`,
  `adr-refs:`, `feature-refs:`, `related:`, `supersedes:`,
  `superseded-by:`.
- A pre-existing `BACKLOG.md` is overwritten only after the
  user confirms (the script saves the previous version under
  `BACKLOG.md.preMigration` for one-step rollback).

Run via `tools/migration/build_backlog.py`. The script is parameterized
through a small YAML config that the user can edit before the run
(epic cutoffs, status overrides for known exceptions).

### Phase 6: Cross-skill rename support

If the repo references the old skill names (`/business-analyse`,
`/v-model-workflow`), this phase rewrites them to the current names
(`/business-analysis`, `/dia-orchestrator`). It also updates skill
folder references in CLAUDE.md, README, and any inline scripts.

This phase is a no-op for repos that already use v2 skill names.

### Phase 7: Consistency check

Runs `/consistency-check` mode A (syntactic) and reports findings.
Auto-fix is applied for the safe drift types:

- Frontmatter `status:` or `phase:` fields lingering anywhere
- Backlog rows missing for an existing artifact (placeholder row
  inserted)
- Dashboard counts vs. computed totals
- Dead links inside `_devprocess/`

Findings that need human triage (orphan ADRs, ADR abstraction
violations, true semantic conflicts) are listed in the final
report and parked as `BL-NNN` rows in the backlog with
`Source = CONSISTENCY-CHECK`.

If the consistency check passes, the skill writes a final entry to
`_devprocess/context/HANDOFFS.md`:

```
## dia-migration {YYYY-MM-DD} -- migration complete

Phases run: 0 (detection), 1 (foundation), 2 (status cleanup),
3 (naming), 4 (analysis flatten), 5 (backlog), 6 (skill renames),
7 (consistency).

Counts after migration:
- Artifacts: {N}
- Backlog rows: {N}
- ADR catalog entries: {N}
- Status drift remaining: 0
- archive/ folders remaining: 0
```

## Tools

The migration scripts live in the DIA repo at `tools/migration/` and are shared with `/reverse-engineering`:

| Script                          | Purpose                                                  |
|---------------------------------|----------------------------------------------------------|
| `tools/migration/detect_state.py`         | Phase 0 detection. Returns a JSON report.                |
| `tools/migration/strip_frontmatter_status.py` | Phase 2a. Removes status fields from YAML frontmatter. |
| `tools/migration/strip_body_status.py`    | Phase 2b. Removes status headers from artifact bodies.   |
| `tools/migration/migrate_naming.py`       | Phase 3. Renames files and updates references.           |
| `tools/migration/flatten_analysis.py`     | Phase 4. Reduces analysis/ to four prefixes.             |
| `tools/migration/build_backlog.py`        | Phase 5. Regenerates the backlog from all artifacts.     |
| `tools/migration/migrate_skill_names.py`  | Phase 6. Updates `/business-analyse` and `/v-model-workflow` references. |

All scripts:

- accept the project root as an argument (default: current working
  directory).
- print a summary at the end (files changed, refs updated).
- are idempotent. Running again finds zero changes if the repo is
  already clean.
- exit with non-zero code on any error so the skill can stop the
  pipeline.

## Workflow when invoked

1. **Pre-flight**: confirm git branch is not main/dev/master and
   working tree is clean (or warn).
2. **Phase 0**: run `detect_state.py`, present the plan to the
   user, get confirmation. Stop if user declines.
3. **Phase 1**: foundation (rules, ARCHITECTURE.map seed, dirs).
   Confirm with user for the ARCHITECTURE.map seed (entry-point
   candidates).
4. **Phase 2**: status cleanup. Two scripts in sequence. Commit
   after.
5. **Phase 3**: naming migration. Show rename plan, ask user, then
   execute. Commit after.
6. **Phase 4**: analysis flattening. Show rename list, confirm,
   execute. Commit after.
7. **Phase 5**: backlog regeneration. Show backlog summary preview,
   confirm overwrite, execute. Commit after.
8. **Phase 6**: skill name updates. Idempotent, commit after.
9. **Phase 7**: consistency check. Run `/consistency-check` mode A
   with `--fix`. Final report.

Each phase ends with a commit message:
`chore(dia-migration): phase N -- {short summary}`.

The user can interrupt between phases. Re-running `/dia-migration`
picks up at the next dirty phase based on the detection output.

## Handoff Ritual

At the end of a successful run:

```
DIA migration complete on branch {branch}.

Summary:
- Phases executed: 7/7
- Files renamed: {N}
- References updated: {N}
- Status fields cleaned: {N}
- archive/ folders removed: {N}
- Backlog rows: {N}

Next steps:
1. Review the migration commits.
2. Merge the branch when satisfied.
3. /dia-orchestrator picks up the project state from here.
```

## Failure modes and rollback

If a phase fails:

1. The script writes its error to stderr and exits non-zero.
2. The skill stops without proceeding to the next phase.
3. The user can `git reset --hard HEAD` to undo the failed phase
   (the previous phases are already committed).
4. Re-running `/dia-migration` re-detects state and resumes at the
   first dirty phase.

For Phase 5 specifically (backlog overwrite), the previous backlog
is preserved as `BACKLOG.md.preMigration`. To roll back the
backlog rewrite without rolling back commits:

```bash
mv _devprocess/context/BACKLOG.md.preMigration \
   _devprocess/context/BACKLOG.md
```

## Keywords

DIA migration, V-Model migration, repo migration, DIA v1, DIA v2,
upgrade conventions, restructure backlog, status drift cleanup,
filename migration, FEATURE to FEAT, EPIC numbering, ADR numbering,
analysis flattening, archive cleanup, brownfield to V-Model.
