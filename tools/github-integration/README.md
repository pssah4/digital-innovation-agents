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

## Subcommands

| Subcommand           | When called by skills                                                       |
|----------------------|-----------------------------------------------------------------------------|
| `create-issue`       | First entry-skill invocation on a new backlog item                          |
| `tag-phase`          | End of every Handoff Ritual (BA, RE, Arch, Code, Test, Audit)               |
| `open-draft-pr`      | After the first commit on the item branch (typically end of Phase 0)        |
| `ready-for-review`   | After all required phase tags are set (Closing Handoff)                     |
| `status`             | `/dia-guide` post-phase audit, or user query                                |

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
python3 tools/github-integration/flow.py ready-for-review --item FEAT-04-09 --with-audit

# Anytime: where do we stand?
python3 tools/github-integration/flow.py status --item FEAT-04-09
```

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
| `feat-04-09/audit-done`          | Audit report written, findings filed                   |
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
           '*/test-done', '*/audit-done', '*/ready-for-review']
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
