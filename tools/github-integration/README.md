# tools/github-integration/

Team-workflow driver: keeps GitHub issues, project cards, draft PRs,
and git tags in sync with the BACKLOG.md truth as a backlog item
walks through the V-Model phases.

The skills call this script via `flow.py <subcommand>`. The user can
also call it directly when a manual override is needed.

The integration is **skill-triggered**: the BACKLOG.md remains the
single source of truth, GitHub is the team-collaboration view on
top.

## Prerequisites

- `gh` CLI installed (`brew install gh`, then `gh auth login`).
- A GitHub remote configured for the repo (`git remote -v` shows
  origin).
- Optional: a GitHub Project named "DIA workflow" linked to the repo,
  with columns matching the V-Model phases. The script does not
  require the project to exist; if absent, only issues / PRs / tags
  are managed.

If `gh` is not installed or no GitHub remote is configured, the
script enters **local-only mode**: it sets git tags but skips all
GitHub API calls. Switching to GitHub later is non-destructive --
re-run `create-issue` and tags will sync.

## Mode awareness

flow.py reads `.dia/config.toml` (managed by `/dia-setup`) and
respects the `mode` setting:

- `off`: GitHub-only subcommands (`create-issue`, `open-draft-pr`,
  `ready-for-review`, `sync-status`, `promote-to-epic`,
  `initial-sync`, `apply-renumber`) are no-ops. `tag-phase` and
  `status` are also no-ops in `off` per the three-modes contract.
  Exceptions: `validate-fix` runs its local checks (BACKLOG row,
  commit cite, FIXME stub markers) in every mode; `preflight` is
  read-only and runs in every mode (it warns when the mode is not
  `github-sync`).
- `git-only`: GitHub-only subcommands stay no-ops. `tag-phase` and
  `status` work locally so phase-end commits keep their tags.
  `validate-fix` runs the local checks; the GitHub-issue check is
  skipped. `preflight` runs.
- `github-sync`: full behaviour. Issues, PRs, project field,
  tasklist rollups, `initial-sync` bulk onboarding, `validate-fix`
  GitHub-issue check, and the post-merge `apply-renumber` all sync.

If `.dia/config.toml` is missing, the script falls back to
`git-only` for backwards compatibility with setups created before
stage 1.

## Subcommands

| Subcommand           | When called by skills                                                       |
|----------------------|-----------------------------------------------------------------------------|
| `create-issue`       | First entry-skill invocation on a new backlog item                          |
| `tag-phase`          | End of every Handoff Ritual (BA, RE, Arch, Code, Test, Audit)               |
| `open-draft-pr`      | After the first commit on the item branch (typically end of Phase 0)        |
| `ready-for-review`   | After all required phase tags are set (Closing Handoff)                     |
| `status`             | `/dia-guide` post-phase audit, or user query                                |
| `sync-status`        | After every Handoff Ritual; mirrors backlog Status to issue / project      |
| `promote-to-epic`    | After RE finishes for a new EPIC; renames parent, creates sub-issues       |
| `preflight`          | Before a bulk sync; read-only checks (project reachable, labels, vocab, ...) |
| `initial-sync`       | Once after `/reverse-engineering` or `/dia-migration`; bulk-onboard the backlog |
| `validate-fix`       | After a hotfix lands; hotfix-scoped consistency check                      |

Most subcommands take `--item <ID>` (e.g. `--item FEAT-04-09`) and
are idempotent. `preflight` and `initial-sync` operate on the whole
backlog and take no `--item`.

## Quick reference

```bash
# Once per new backlog item
python3 tools/github-integration/flow.py create-issue --item FEAT-04-09

# After every phase ends
python3 tools/github-integration/flow.py tag-phase --item FEAT-04-09 --phase ba
python3 tools/github-integration/flow.py tag-phase --item FEAT-04-09 --phase re
python3 tools/github-integration/flow.py tag-phase --item FEAT-04-09 --phase arch
python3 tools/github-integration/flow.py tag-phase --item FEAT-04-09 --phase code
python3 tools/github-integration/flow.py tag-phase --item FEAT-04-09 --phase test

# After the first commit
python3 tools/github-integration/flow.py open-draft-pr --item FEAT-04-09

# After all required phases
python3 tools/github-integration/flow.py ready-for-review --item FEAT-04-09 --with-sec

# Anytime: where do we stand?
python3 tools/github-integration/flow.py status --item FEAT-04-09

# After every handoff ritual: mirror backlog status and claim
python3 tools/github-integration/flow.py sync-status --item FEAT-04-09

# Once per new EPIC after RE: rename parent, create sub-issues
python3 tools/github-integration/flow.py promote-to-epic \
  --item EPIC-04 --rename-branch

# Before a bulk sync of a migrated / reverse-engineered backlog
python3 tools/github-integration/flow.py preflight

# Bulk-onboard the whole backlog onto GitHub (runs preflight first)
python3 tools/github-integration/flow.py initial-sync --dry-run   # preview
python3 tools/github-integration/flow.py initial-sync             # execute
```

## sync-status: backlog Status mirrored to GitHub

After the stage-3 migration, BACKLOG and GitHub Projects share one
status vocabulary: `Backlog`, `Ready`, `In Progress`, `In Review`,
`Done`. `sync-status` mirrors the BACKLOG Status column to:

- the GitHub issue state: `Done` closes the issue, every other
  status reopens it
- the configured GitHub Project Status field: same value, matched
  case-insensitively against the project's option names so a
  backlog `In Progress` lands on GitHub's built-in `In progress`.
  When the project field cannot be set, `sync-status` prints the
  precise reason (`reason=option_missing`, `reason=item_list_failed`,
  ...) instead of a blanket "not configured", so a rate-limited or
  mis-scoped run is not mistaken for an unconfigured one.
- the BACKLOG Claim column: `sync-status` reads the GitHub
  Assignee and writes `{login} @ {YYYY-MM-DD}` back. When the
  status is `Done` or no assignee is set, the Claim column is
  cleared.

For projects that did not yet run
`tools/migration/migrate_status_vocabulary.py`, a legacy
translation table resolves the old DIA values:

| Legacy BACKLOG status | GitHub status |
|---|---|
| `Planned`  | `Ready`       |
| `Active`   | `In Progress` |
| `Review`   | `In Review`   |
| `Waiting`  | `Backlog`     |
| `Deferred` | `Backlog`     |

The legacy mapping disappears as soon as the migration runs.

## Project-level configuration

`sync-status` updates the issue and, optionally, a status field on a
GitHub Project. Configure the project in `.dia/config.toml`:

```toml
[github]
project_number = 7
status_field = "Status"
```

Without a `project_number`, only the issue state (open / closed) is
mirrored. With it, `sync-status` resolves the project owner from the
repo, looks up the field id, and sets the single-select option.

## validate-fix

Hotfix-scoped consistency check. Hotfixes skip the V-Model phases,
so `/consistency-check` mode A has no automatic trigger for them.
`validate-fix` performs the minimum check the standard flow would
have done. Run after the hotfix commit lands and (in github-sync
mode) the issue is created.

```
python3 tools/github-integration/flow.py validate-fix --item FIX-NN-NN-NN
```

Checks:

1. The FIX row exists in `BACKLOG.md` with correct id and references
   the parent FEAT in the Refs column.
2. At least one commit on the current branch cites the FIX id in
   the subject or `Refs:` trailer.
3. No `FIXME(stub):` referencing this FIX id exists in the codebase
   without the matching BACKLOG row.
4. In `mode = "github-sync"`: a GitHub issue exists for the FIX id.

Output is JSON with `ok: true|false` and a `findings` list. Exit
code is non-zero if any finding fires.

## promote-to-epic

Run after `/requirements-engineering` has produced an EPIC and one
or more FEATs / IMPs.

```
python3 tools/github-integration/flow.py promote-to-epic \
  --item EPIC-NN [--parent-issue 42] [--rename-branch] \
  [--no-sync-bodies] [--dry-run]
```

Steps:

1. Renames the parent issue title to `EPIC-NN: <title>`. Adds the
   `epic` label and puts the epic on the configured project board.
2. Mirrors the epic body from `_devprocess/requirements/epics/EPIC-NN-*.md`
   (default; `--no-sync-bodies` skips it). A detail file that is still
   a reverse-engineering skeleton is replaced by a short stub instead
   of pushing placeholder content, with a warning.
3. Creates sub-issues for every `FEAT-NN-*`, `FIX-NN-*-*` and
   `IMP-NN-*-*` row in the BACKLOG (skips already-existing ones), then
   links them as real GitHub sub-issues. The freshly created issue
   number is used directly, so a lagging search index never drops a
   new sub-issue from the rollup.
4. Refreshes a `## Sub-Issues` tasklist inside
   `<!-- DIA:sub-issues -->` / `<!-- /DIA:sub-issues -->` markers at
   the end of the parent body. Content outside the markers (the epic
   description) is preserved verbatim, so a re-run can never leave the
   epic body with only the tasklist.
5. Mirrors the BACKLOG Status to the project board for the epic and
   every sub-item (one project scan via the per-run cache, not one per
   item).
6. With `--rename-branch`: renames the current feature branch to
   `feature/epic-NN-<slug>`. No-op if it already matches.

`--dry-run` prints what would happen using read-only lookups only.
Idempotent. Safe to re-run.

## preflight

Read-only validation to run before a bulk sync (after
`/reverse-engineering` or `/dia-migration` leaves a backlog with
dozens of items). Makes no changes.

```
python3 tools/github-integration/flow.py preflight [--strict]
```

Checks:

- `gh` reachable, a GitHub remote is configured, and the workflow
  mode is `github-sync`.
- The configured GitHub Project is reachable (`gh project view`),
  including the `gh auth refresh -s project` scope hint.
- The project Status field exists and has an option for every
  BACKLOG status the backlog uses (case-insensitive: `In Progress`
  matches GitHub's built-in `In progress`).
- The repo labels `gh issue create` needs (`epic`, `phase:planned`,
  the type and priority labels) exist, with `gh label create`
  fix-it lines for any that are missing.
- The BACKLOG Title column carries no doubled id prefix.
- A small sample (<= 5) of items that already link an issue: backlog
  status vs. issue open/closed state.
- The GraphQL rate budget against a rough estimate of a full sync.

Exit code is 1 on blockers (missing labels, project unreachable,
unmapped status, no Status field). Warnings alone exit 0 unless
`--strict`.

## initial-sync

Bulk-onboard an existing backlog onto GitHub in one resumable pass.
flow.py is otherwise built for the incremental Handoff Ritual (one
item per phase transition); `initial-sync` is the path for a backlog
that never went through that ritual.

```
python3 tools/github-integration/flow.py initial-sync [--dry-run] [--skip-preflight]
```

What it does:

1. Runs `preflight`; aborts on blockers unless `--skip-preflight`.
2. For each EPIC: creates the epic issue if it does not exist, then
   runs `promote-to-epic` (sub-issues created and linked, bodies
   mirrored, status synced).
3. For each standalone FEAT / FIX / IMP (one whose epic number has no
   `EPIC-NN` row): `create-issue` then `sync-status`.

`--dry-run` prints the full plan without touching GitHub. Idempotent
and resumable: a re-run skips items that already have an issue. The
per-run project caches keep the cost to a couple of project scans
rather than one per item.

## Tag schema

```
<item-id-lower>/<phase>-done
```

| Tag                              | Phase                                                  |
|----------------------------------|--------------------------------------------------------|
| `feat-04-09/ba-done`             | BA validated, backlog row updated                      |
| `feat-04-09/re-done`             | FEATURE spec and success criteria                      |
| `feat-04-09/arch-done`           | ADRs, arc42, plan-context                              |
| `feat-04-09/code-done`           | Implementation committed, build green                  |
| `feat-04-09/test-done`           | Tests added, coverage check passed                     |
| `feat-04-09/sec-done`            | Audit report written, findings filed (legacy `audit-done` still accepted) |
| `feat-04-09/ready-for-review`    | All required phases complete, draft -> ready           |

Tags are **annotated** (not lightweight), so they carry a one-line
message and survive `git tag --list -n`.

## GitHub Projects automation (optional)

If the repo has a GitHub Project board with columns matching the
phases, a tiny GitHub Actions workflow can move cards based on tag
events:

```yaml
# .github/workflows/dia-card-sync.yml
name: DIA card sync
on:
  push:
    tags: ['*/ba-done', '*/re-done', '*/arch-done', '*/code-done',
           '*/test-done', '*/sec-done', '*/ready-for-review']
jobs:
  move-card:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: |
          # Parse tag, find issue from item id, move project card
          # ... project-specific automation here
```

Skills do not depend on this Action being present; they only set the
tag. If the Action is missing, cards must be moved manually -- but
the rest of the workflow (issue update, label, draft PR) still
works because that is handled by `flow.py` directly.

## Why this design

- **Backlog stays authoritative.** GitHub is a view, not the source.
  This avoids the failure mode where Project board state diverges
  from backlog state because they were edited from different sides.
- **Tags are agent-set.** The user does not need to remember tag
  names or schemas. The skill knows which phase just ended and which
  tag to write.
- **Local-only mode degrades gracefully.** Solo project, no GitHub?
  Tags still get set, the workflow still works.
- **Idempotent everywhere.** Re-running any subcommand on an
  already-current state is a no-op. Safe in retry loops.
