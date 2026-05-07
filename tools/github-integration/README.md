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

- `off`: every subcommand is a no-op with a clear message.
- `git-only`: GitHub-only subcommands (`create-issue`,
  `update-issue`, `open-draft-pr`, `ready-for-review`,
  `sync-status`, `promote-to-epic`) are no-ops. `tag-phase` and
  `status` work locally so phase-end commits keep their tags.
- `github-sync`: full behaviour. Issues, PRs, project field, tasklist
  rollups all sync.

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
| `validate-fix`       | After a hotfix lands; hotfix-scoped consistency check                      |

All subcommands take `--item <ID>` (e.g. `--item FEAT-04-09`) and
are idempotent.

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
```

## sync-status: backlog Status mirrored to GitHub

After the stage-3 migration, BACKLOG and GitHub Projects share one
status vocabulary: `Backlog`, `Ready`, `In Progress`, `In Review`,
`Done`. `sync-status` mirrors the BACKLOG Status column to:

- the GitHub issue state: `Done` closes the issue, every other
  status reopens it
- the configured GitHub Project Status field: same value, no
  translation
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
  --item EPIC-NN [--parent-issue 42] [--rename-branch]
```

Steps:

1. Renames the parent issue title to `EPIC-NN: <title>`. Adds the
   `epic` label.
2. Creates sub-issues for every `FEAT-NN-*` and `IMP-NN-*-*` row in
   the BACKLOG (skips already-existing ones).
3. Writes a `## Sub-Issues` tasklist into the parent body so GitHub
   tracks the rollup automatically.
4. With `--rename-branch`: renames the current feature branch to
   `feature/epic-NN-<slug>`. No-op if it already matches.

Idempotent. Safe to re-run.

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
