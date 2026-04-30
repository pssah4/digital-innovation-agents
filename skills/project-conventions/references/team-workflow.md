# Team workflow: branch, GitHub issue, phase tags, draft PR

This document is the canonical reference for how a backlog item
flows through the V-Model phases when a team uses Git, GitHub, and
the DIA skill set together. Every entry skill MUST follow this
contract; every CHANGELOG entry that touches the workflow MUST
reference this file.

## Core invariant: branch = backlog item

One branch lives for the entire lifecycle of one backlog item
(FEAT, FIX, IMP, EPIC). All V-Model phases for that item -- BA,
RE, Architecture, Coding, Testing, Security-Audit, Release -- write
into the same branch. The branch ends when its PR merges to `dev`.

The branch is NOT keyed on the skill. Skills are activities; the
backlog item is the deliverable. Multiple skills, one branch.

### Branch naming

| Item type | Pattern | Example |
|-----------|---------|---------|
| FEAT | `feature/<item-id-lower>-<short-slug>` | `feature/feat-04-09-openai-streaming` |
| EPIC | `feature/<item-id-lower>-<short-slug>` | `feature/epic-03-context-memory` |
| FIX | `fix/<item-id-lower>-<short-slug>` | `fix/fix-12-04-01-copilot-embedding` |
| IMP | `chore/<item-id-lower>-<short-slug>` | `chore/imp-08-02-03-better-logging` |

The item-id is lower-cased (`feat-04-09`, not `FEAT-04-09`) so the
branch name is shell-friendly and grep-friendly.

## GitHub integration: issue per item, project card auto-managed

The backlog truth lives in `_devprocess/context/BACKLOG.md` (in the
repo). GitHub is the team-collaboration layer on top: every backlog
item gets a GitHub issue, a project card, and eventually a PR.

### Issue creation

Triggered by the first skill that touches a NEW backlog item
(typically `/business-analysis` for a feature idea, `/coding` for
a mid-cycle FIX, etc.). The skill calls
`tools/github-integration/flow.py create-issue --item <ID>`
which:

1. Reads the backlog row for `<ID>` from `BACKLOG.md`.
2. Calls `gh issue create` with title, body, and labels derived
   from the row.
3. Writes the resulting `#NNN` back into the backlog row's
   `Issue` column.
4. Returns the issue URL for the skill to display.

If the issue already exists for that item, the script is a no-op
and just returns the existing URL.

### Issue body template

```
**Backlog item:** [FEAT-04-09](_devprocess/context/BACKLOG.md#feat-04-09)
**Type:** Feature
**Epic:** EPIC-04 -- Providers, Web & Localization
**Priority:** P1

## Description
{from BACKLOG row "Title" + first paragraph of FEATURE spec}

## V-Model phases (auto-tracked)
- [ ] BA -- business-analysis
- [ ] RE -- requirements-engineering
- [ ] Architecture
- [ ] Coding
- [ ] Testing
- [ ] Security-Audit
- [ ] Ready for review

The DIA agent updates this checklist as phase tags are set.
Source of truth: `BACKLOG.md`. PR: TBD.
```

### Labels

Auto-applied per item type and priority:

- Type: `feature`, `fix`, `improvement`, `epic`
- Priority: `p0`, `p1`, `p2`
- Phase: `phase:planned`, `phase:ba`, `phase:re`, `phase:arch`,
  `phase:coding`, `phase:testing`, `phase:audit`, `phase:review`

The phase label is updated by the orchestrator when phase tags are
set (see below). Only one phase label at a time.

### GitHub Projects board

A single "DIA workflow" project per repo, with columns matching the
phases. Cards move via GitHub Actions triggered by phase tags or by
`flow.py update-issue --phase X`. The DIA agent does not touch the
GitHub API for project cards directly; it sets git tags and the
GitHub-side automation moves the card.

Recommended project column setup:

| Column         | Card lands here when               |
|----------------|------------------------------------|
| Planned        | Issue created                      |
| BA             | tag `<id>/ba-done` set             |
| RE             | tag `<id>/re-done` set             |
| Architecture   | tag `<id>/arch-done` set           |
| Coding         | tag `<id>/code-done` set           |
| Testing        | tag `<id>/test-done` set           |
| Audit          | tag `<id>/audit-done` set          |
| Review         | tag `<id>/ready-for-review` set    |
| Done           | PR merged                          |

## Phase tags: agent-set, GitHub-readable

Every V-Model phase ends with a Handoff Ritual. As part of that
ritual, the skill sets a git tag pointing at the last commit of
that phase. Tags are annotated (not lightweight), carry a one-line
message describing what the phase delivered, and are pushed with
the next push.

### Tag schema

```
<item-id-lower>/<phase>-done
```

| Tag                              | Set by                         | Meaning |
|----------------------------------|--------------------------------|---------|
| `feat-04-09/ba-done`             | `/business-analysis`           | BA validated, backlog row updated |
| `feat-04-09/re-done`             | `/requirements-engineering`    | FEATURE spec written, success criteria set |
| `feat-04-09/arch-done`           | `/architecture`                | ADRs / arc42 updates / plan-context handed to coding |
| `feat-04-09/code-done`           | `/coding`                      | Implementation committed, build green |
| `feat-04-09/test-done`           | `/testing`                     | Tests added, coverage check passed |
| `feat-04-09/audit-done`          | `/security-audit`              | Audit report written, findings filed |
| `feat-04-09/ready-for-review`    | `/dia-orchestrator`            | All required phases complete, draft PR -> ready |

### Setting tags

The skill's Handoff Ritual calls
`tools/github-integration/flow.py tag-phase --item <ID> --phase <phase>`
which:

1. Verifies the current branch matches the item.
2. Creates an annotated tag with the canonical message.
3. Updates the issue's checklist (one phase ticked).
4. Updates the issue's `phase:*` label.
5. Pushes the tag (only when the user is online; if not, queues for
   the next push).

Tags are agent-set, not user-set. This keeps the workflow
consistent: the user does not need to remember tag names. The skill
prompts the user for confirmation before tagging if the Handoff
Ritual ends with a non-trivial decision.

## Draft PR per item

Opened by `/business-analysis` (for new features) or
`/coding` (for FIX / IMP) when the item enters the Building phase.

The PR is a Draft until `<id>/ready-for-review` is tagged. While
draft, it serves as a living view of the work in progress: the
`gh pr` command shows the diff, the issue link, and the phase
checklist, so the rest of the team can see what is being built
even before review starts.

### Mark-ready-for-review trigger

After `/coding`, `/testing`, and (if required by the item type)
`/security-audit` have all set their `<id>/*-done` tags, the
orchestrator runs the feature-complete handoff:

1. Verifies all required phase tags exist.
2. Asks the user via `AskUserQuestion`:
   "Item `<ID>` is feature-complete. All required phases (coding,
    testing{, audit}) have done-tags. Mark the PR ready for review?"
3. On yes:
   - Tags `<id>/ready-for-review`.
   - Calls `gh pr ready` to flip the draft to ready.
   - Posts a final comment summarising the deliverables.
   - Suggests next step (request review, plan release, etc.).

## Orchestrator: post-phase consistency check

`/dia-orchestrator` is the conductor. After every entry-skill
finishes a phase, the orchestrator gets invoked (silently or
explicitly) and runs:

1. **Branch check:** is the current branch on an item-branch (per
   the schema above)?
2. **Tag check:** does the just-finished phase have its tag set?
   If not, set it now.
3. **Backlog check:** does the BACKLOG row's status reflect the
   phase progress?
4. **Issue check:** is the GitHub issue's checklist in sync with
   the tags?
5. **Next-phase suggestion:** what is the natural next phase for
   this item? Surface it as `AskUserQuestion`:
   "Phase `<X>` complete for `<ID>`. Recommended next: `/{skill}`.
    Continue now, pause, or pick a different next step?"

The orchestrator is the consistency layer that prevents drift
between Git tags, BACKLOG.md, GitHub issues, and project cards.
Skills focus on producing artefacts; the orchestrator ensures the
state across systems matches.

## Pre-Phase 0 in entry skills: branch-and-issue check

Every entry skill starts with this check:

```
1. Identify the active backlog item.
   - Parse from user prompt ("work on FEAT-04-09").
   - If unclear, AskUserQuestion: which item are we working on?
   - For genuinely new items: create the BACKLOG row first, then
     proceed.

2. Compute the expected branch name from the item.

3. Compare to current branch:
   - Match -> silent continue.
   - Current branch is main/master/dev -> AskUserQuestion: create
     `<expected-branch>` and switch.
   - Current branch is a different item-branch -> AskUserQuestion:
     switch to the right item-branch (or create it).
   - Current branch matches loosely (typo, slug variation) ->
     AskUserQuestion: continue here or rename the branch.

4. If GitHub issue does not exist for the item:
   call flow.py create-issue.

5. If draft PR does not exist for the branch:
   call flow.py open-draft-pr (only after the first commit on the
   branch; for the very first skill on a brand-new branch, the
   draft PR is opened at the end of Phase 0).

6. Write `.git/dia-active-skill` with item ID, branch, skill name,
   timestamp. Subsequent skill invocations read this file and stay
   silent if everything matches.
```

## Override and exceptions

- **Solo project, no GitHub:** the skill detects the absence of `gh`
  binary or a GitHub remote and silently skips the GitHub-integration
  steps. Phase tags still get set as local git tags. Local-only
  workflow stays intact.

- **Hot-fix on dev (rare):** the user can override the branch check
  with explicit confirmation. The pre-commit hook still asks; only
  `--no-verify` skips it. The orchestrator will flag the unusual
  state and remind the user that the hot-fix needs follow-up
  documentation.

- **Trunk-based development teams:** can disable the per-item
  branching by setting `git config dia.workflow trunk-based`. In
  that mode, all DIA artefact writes happen on `main`, the per-item
  isolation lives in feature flags rather than branches. Phase
  tags still apply. Not the default.

## What this replaces

This contract supersedes the earlier "branch per skill" model
(`feature/ba-...`, `feature/re-...`, `feature/arch-...`). Multiple
PRs per item produce review fatigue and merge conflicts. Branch =
item is the simpler, team-friendlier model.
