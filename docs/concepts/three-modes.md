---
title: Three modes
description: How DIA runs in your project. The three activation modes off, git-only, and github-sync, what each does, and which to pick.
---

# Three modes: off, git-only, github-sync

DIA does not assume that every project wants the full GitHub
collaboration layer. The plugin runs in one of three modes, set
once during `/dia-setup` and changed any time by re-running the
same skill. The mode is a single line in `.dia/config.toml`.

## What each mode does

| Aspect | `off` | `git-only` | `github-sync` |
|---|---|---|---|
| SessionStart hook injects the bootstrap skill into every session | no | yes | yes |
| Anchor block in `CLAUDE.md`, `AGENTS.md`, `GEMINI.md`, `.cursorrules`, `.github/copilot-instructions.md`, `.windsurfrules` | no | yes | yes |
| `/dia-guide` available (manual invocation) | yes | yes | yes |
| Phase skills available (`/business-analysis` ... `/security-audit`) | yes | yes | yes |
| BACKLOG.md, FEAT specs, ADRs, plans get written | yes | yes | yes |
| `flow.py tag-phase` sets the local phase tag | no | yes | yes |
| `flow.py status` reports on tags and branch | no | yes | yes |
| `flow.py create-issue`, `open-draft-pr`, `sync-status`, `promote-to-epic` | no | no | yes |
| `flow.py validate-fix` (local checks always run, GitHub-issue check only in github-sync) | local-only | local-only | full |
| GitHub issue created per backlog item | no | no | yes |
| Sub-issues + tasklist on the parent EPIC | no | no | yes |
| GitHub Project Status field mirrored from BACKLOG | no | no | yes |
| Claim column populated from GitHub Assignee | no | no | yes |
| Local git hooks (`pre-commit`, `pre-merge-commit`) | independent | independent | independent |
| `scripts/merge-to-dev.sh` | independent | independent | independent |

## End-to-end run in `github-sync` (what really happens)

When `mode = "github-sync"` is active, the workflow runs through
without manual intervention beyond the standard skill prompts.
This table maps each step to the visible side-effect on GitHub.

| Step | Skill or script | Effect (in `github-sync`) |
|---|---|---|
| Session start | SessionStart hook | Bootstrap skill is injected; the agent learns the skill catalog and `DIA_PLUGIN_ROOT` |
| Item start (entry A/B/C) | `/dia-guide` | New feature branch from the configured `source_branch` (default `develop`) |
| First skill writes a backlog row | the phase skill | `flow.py create-issue --item <ID>` creates the GitHub issue, plus `gh project item-add` if `project_number` is set |
| Each phase Handoff Ritual ends | the phase skill | `flow.py tag-phase --phase <X>` (annotated tag, issue label updated, checklist ticked, `phase:planned` removed) AND `flow.py sync-status --item <ID>` (mirror BACKLOG Status to issue and Project Status field, pull GitHub Assignee back into BACKLOG Claim, clear Claim on Done or no-assignee) |
| End of `/requirements-engineering` (when EPIC ID becomes known) | `/requirements-engineering` | `flow.py promote-to-epic --item EPIC-NN --rename-branch` rewrites the parent issue title to `EPIC-NN: <title>`, creates a sub-issue per FEAT/IMP, writes a `## Sub-Issues` tasklist into the parent body, renames the feature branch to `feature/epic-NN-<slug>` |
| First commit on the feature branch | `/coding` (or manual) | `flow.py open-draft-pr --item <ID>` opens the draft PR against `source_branch` |
| All required phase tags set | Closing Handoff | `flow.py ready-for-review --item <ID> [--with-sec]` verifies tags exist, flips draft -> ready, sets the `<id>/ready-for-review` tag |
| Hotfix lane closes | `/coding` | `flow.py validate-fix --item FIX-EE-FF-NN` runs all four checks: BACKLOG row with parent-FEAT refs, commit cites the FIX id, no orphan `FIXME(stub):`, GitHub issue exists |
| `scripts/merge-to-dev.sh <branch>` runs | the merge wrapper | `tools/renumber-for-merge.py --plan-out FILE` aligns ids; merge happens; `flow.py apply-renumber --plan FILE` rewrites GitHub issue titles AND parent-body Sub-Issues tasklist according to the renumber map. Plan file is preserved at `.dia/last-renumber-plan.json` on failure for retry. |

The only one-time setup that does not happen automatically in
`github-sync` is the GitHub Project board configuration. `/dia-setup`
asks for `project_number`, `status_field` (default `Status`), and
optional `project_owner` once via `AskUserQuestion`. With
`project_number = 0` the issue itself still syncs; only the project
Status field stays untouched.

## Which mode for which situation

`off` means **the plugin behaves as if it were not installed**. The
hook stays silent, no anchor block lives in your agent files, every
flow.py call is a no-op including the local phase tagging. The
skills are still on disk, so a user who knows the slash commands
can call `/business-analysis` manually, but the agent will not pick
up the V-Model from the project context on its own. Pick `off` when
you have the plugin installed globally but a particular project
should stay neutral, when you want to use a different methodology
for one project, or for sessions where DIA should not interfere.

`git-only` is **the V-Model workflow without GitHub**. The hook
injects the bootstrap, the anchor block in your agent files tells
the coding tool that DIA is active, every phase skill is available
and writes its artifacts, `tag-phase` records phase boundaries as
local annotated git tags, `status` reports on them, the local git
hooks (branch protection, renumber-on-merge) and
`scripts/merge-to-dev.sh` work as usual. What does NOT happen:
issues, PRs, project cards, sync-status, promote-to-epic. Pick
`git-only` when you work solo, when your team already tracks work
elsewhere (Linear, Jira, Notion), or when the repo lives outside
GitHub.

`github-sync` adds **the team-collaboration mirror**. Every backlog
row gets a GitHub issue. After RE, `promote-to-epic` rewrites the
parent issue to `EPIC-NN: {slug}`, creates one sub-issue per FEAT
and IMP under the EPIC, and writes a `## Sub-Issues` tasklist into
the parent body so GitHub auto-rolls up progress. After every
Handoff Ritual, `sync-status` mirrors the BACKLOG Status column to
the GitHub issue state and the GitHub Project Status field, and
pulls the GitHub Assignee back into the BACKLOG Claim column. Pick
`github-sync` when your team uses GitHub Issues and Projects as the
work board.

## Decision flow

- **Plugin installed but you want a particular project untouched**
  -> `off`.
- **Solo work or non-GitHub team**, but you want the V-Model
  agent-led -> `git-only`.
- **Team with GitHub Issues / Projects** -> `github-sync`.

You can change mode any time by running `/dia-setup` again. The
skill picks up the existing `.dia/config.toml`, asks for the new
mode, rewrites the file, and refreshes the anchor blocks. Going
from `github-sync` to `git-only` does not delete the GitHub issues
that already exist; they simply stop being kept in sync.

## What the mode does NOT control

Some pieces of DIA run independently of the mode:

- Local git hooks under `tools/git-hooks/` (branch protection,
  renumber-on-merge). Install or remove them via
  `tools/install-git-hooks.sh` regardless of mode.
- `scripts/merge-to-dev.sh`. The safe-merge wrapper is a shell
  script, not a flow.py call.
- The migration scripts under `tools/migration/`. They are
  invoked by `/dia-migration`, which always runs locally.
- The `/consistency-check` skill, which only touches files inside
  `_devprocess/` and `src/`.

## How the mode is enforced

`flow.py` reads `.dia/config.toml` at the start of every
subcommand. If the action is GitHub-touching and the mode is not
`github-sync`, the script prints a clear `[subcommand] mode=X,
skipping (set mode=github-sync via /dia-setup to enable)` and
exits with status 0. The session-start hook reads the same config
and emits an empty injection JSON when the mode is `off`. Phase
skills delegate to `flow.py` and inherit the mode-awareness from
there, so a phase ritual under `git-only` cleanly separates the
local steps (commit, tag) from the skipped GitHub steps.

## Defaults if `.dia/config.toml` is missing

For backwards compatibility with setups that predate `/dia-setup`,
flow.py defaults to `git-only` when no `.dia/config.toml` exists
and the SessionStart hook uses its legacy injection path. New
projects should always run `/dia-setup` first to make the choice
explicit.
