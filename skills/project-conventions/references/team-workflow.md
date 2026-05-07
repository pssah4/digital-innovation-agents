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

### Source of truth split (binding)

Status and Claim are mirrored between BACKLOG.md and GitHub, but
each has a single source of truth:

- **Status**: BACKLOG.md is canonical. `flow.py sync-status` writes
  to GitHub (issue state, project Status field). The reverse is not
  performed: a status edit on GitHub does not flow back into the
  backlog.
- **Claim**: GitHub Assignee is canonical. `flow.py sync-status`
  reads the Assignee and writes it into the BACKLOG `Claim` column
  as `{login} @ {YYYY-MM-DD}`. The reverse is not performed: a
  Claim edited only in BACKLOG.md is not pushed to GitHub.

This asymmetry is deliberate: skills write to BACKLOG.md as part
of their Handoff Ritual; team members assign themselves on the
GitHub UI. Each side touches the format that fits its workflow,
the sync mirrors them.

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
  `phase:coding`, `phase:testing`, `phase:sec`, `phase:review`

The phase label is updated by the guide when phase tags are
set (see below). Only one phase label at a time.

### GitHub Projects board

A single GitHub Project per repo, with a Status field that maps
1:1 to the BACKLOG Status column (see below). Items are mirrored
by `flow.py sync-status --item <ID>`, called from the Handoff
Ritual at every phase end. `flow.py tag-phase --phase <X>` updates
the issue's phase label and ticks its checklist via
`update_issue_after_tag`. The DIA agent does not touch the GitHub
API outside these two paths.

Recommended project Status field setup. The status vocabulary
matches the BACKLOG.md Status column 1:1 so `flow.py sync-status`
mirrors directly without translation.

| Status        | Card lands here when                                   |
|---------------|---------------------------------------------------------|
| Backlog       | Issue created or item parked / blocked                 |
| Ready         | Item prioritized in directions and ready to claim      |
| In Progress   | Someone claimed the item and is actively working on it |
| In Review     | Draft PR flipped to ready, review pending              |
| Done          | PR merged, item shipped                                |

The phase fields (BA, RE, Architecture, Coding, Testing, Audit) are
labels driven by the per-phase tag, not separate status columns.
Phase labels and Status are orthogonal: an item in `In Progress`
can carry any of the `phase:*` labels.

## Phase tags: agent-set, GitHub-readable

Every V-Model phase ends with a Handoff Ritual. As part of that
ritual, the skill sets a git tag pointing at the last commit of
that phase. Tags are annotated (not lightweight), carry a one-line
message describing what the phase delivered, and are pushed with
the next push.

### "Phase" disambiguation (binding terminology)

The word "Phase" carries two meanings in DIA, and they are NOT the
same:

- **Phase tag** (this section). A git tag of the form
  `<item-id-lower>/<phase>-done` set at the end of each V-Model
  phase. Used by `/dia-guide` and `flow.py` to know which phases
  are complete for a given item. Examples: `feat-04-09/ba-done`,
  `feat-04-09/code-done`.
- **Phase column in `BACKLOG.md`**. A separate column with values
  `Released`, `Building`, `Planned`, `Candidates` describing the
  epic-level temporal stage of the item. Independent from the phase
  tags.

When a document says "Phase: Building", it refers to the BACKLOG
column. When it says "Phase tag" or "phase-done tag", it refers to
the git tag. Phase tags do not change the BACKLOG Phase column.

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
| `feat-04-09/sec-done`            | `/security-audit`              | Audit report written, findings filed (legacy `audit-done` still accepted) |
| `feat-04-09/ready-for-review`    | `/dia-guide`            | All required phases complete, draft PR -> ready |

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

## Phase-end commit (binding)

Every phase ends with a commit before the phase tag is set. Without a
commit, the tag has nothing to point at and the next phase starts on
top of an unrecorded working tree. Earlier versions of this contract
left the commit implicit; the result observed in the field was multi-
phase work landing in a single end-of-cycle commit (BA, RE, and code
all in one), which made phase tags meaningless and broke the per-phase
rollback path.

### When the commit fires

The Handoff Ritual of every phase skill (`/business-analysis`,
`/requirements-engineering`, `/architecture`, `/coding`, `/testing`,
`/security-audit`, `/reverse-engineering`) runs the commit between
Part 2 (Handoff context) and the phase-tag step.

Triggers:

1. **End of phase** -- the skill's Handoff Ritual hits the commit step.
2. **Mid-phase user request** -- the user says "commit jetzt" / "commit
   now". The skill runs the same commit block, scoped to whatever is
   currently in the working tree, and continues the phase afterwards.

### What gets committed

The skill stages every artefact it produced or modified during the
phase. If the working tree is empty (no changes), the commit step is
skipped silently and the phase ends without a tag. The guide's
post-phase consistency check then surfaces "phase {x} produced no
artefacts" so the user can decide whether the phase actually ran.

### Branch check at the commit boundary

The commit boundary is the authoritative trigger for the branch / item
mapping. The Pre-Phase 0 check at skill start is advisory; the commit
step is binding:

```
0. If there is no prior commit on the current branch for this item
   (i.e. this is the first phase-end commit), or the current branch
   is `main` / `master` / `dev`:
   - AskUserQuestion: create `<expected-branch>` and switch, or pick a
     custom name. On `main` / `master` / `dev` the question blocks; the
     pre-commit hook would refuse the commit anyway.
1. Stage the artefacts produced this phase.
2. Run `git commit` with the canonical message (see below).
3. Run `flow.py tag-phase --item <ID> --phase <phase>`.
4. If no draft PR exists yet, run `flow.py open-draft-pr --item <ID>`.
5. Push the branch (and tag) when a remote is configured. Skip silently
   in solo mode.
```

The skill does NOT bypass the branch question via the
`.git/dia-active-skill` marker: the marker proves the skill-start
check ran, but the commit step asks again if the branch is wrong for
the item, because users edit branches mid-flow more often than mid-
skill.

### Commit message

```
<conventional-prefix>(<phase>): <ITEM-ID> <phase> complete

<one-line summary of what the phase delivered>

Refs: <ITEM-ID>[, <other ids touched>]
```

Conventional prefixes per phase: `chore` (BA, RE, ARCH, AUDIT, RE-ENG),
`feat` or `fix` (CODING, depending on the artefact category from
triage), `test` (TESTING). Examples:

- `chore(ba): BL-001 BA complete`
- `chore(re): EPIC-04 RE complete`
- `chore(arch): FEAT-04-09 ARCH complete`
- `feat(code): FEAT-04-09 coding complete`
- `test: FEAT-04-09 testing complete`
- `chore(audit): AUDIT-MDM-MAKE-2026-04-30 audit complete`

The `Refs:` line is mandatory. Multiple IDs are comma-separated. This
is what `git log --grep="FEAT-04-09"` keys off later.

### Mid-phase commits

Long phases (RE producing many features, coding spanning days) MAY
produce multiple intermediate commits. Each intermediate commit
follows the same message template but uses a sub-phase noun, e.g.

```
chore(re): EPIC-04 features 04-01 to 04-04 drafted

Refs: EPIC-04, FEAT-04-01, FEAT-04-02, FEAT-04-03, FEAT-04-04
```

The phase tag `<id>/<phase>-done` is set ONLY by the final phase-end
commit, not by intermediate commits.

### Solo mode

When `gh` or the GitHub remote is missing, the commit and the local
tag still run. `flow.py open-draft-pr` is a no-op in solo mode. The
phase still ends with a real commit on the right branch.

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
guide runs the feature-complete handoff:

1. Verifies all required phase tags exist.
2. Asks the user via `AskUserQuestion`:
   "Item `<ID>` is feature-complete. All required phases (coding,
    testing{, audit}) have done-tags. Mark the PR ready for review?"
3. On yes:
   - Tags `<id>/ready-for-review`.
   - Calls `gh pr ready` to flip the draft to ready.
   - Posts a final comment summarising the deliverables.
   - Suggests next step (request review, plan release, etc.).

## Guide: post-phase audit (read-only)

`/dia-guide` is the navigation layer, not an orchestrator. It is
invoked **explicitly** by the user when orientation is needed
("where do I start", "what comes next"). It does not run silently
after every phase, does not set tags, does not auto-fix drift,
and does not call other skills. Each phase skill is autonomous
and owns its own Handoff Ritual (commit, tag-phase, sync-status).

When invoked, the guide reads the current project state and
**reports** rather than fixes:

1. **Branch:** is the current branch on an item-branch (per the
   schema above)? If not, surface a warning naming the expected
   pattern.
2. **Phase tag:** did the just-finished phase set its
   `<id>/<phase>-done` tag (or `<id>/ready-for-review` for the
   release-readiness marker)? If missing, name the responsible
   phase skill so the user can re-run its Handoff Ritual.
3. **Backlog row:** does the BACKLOG row's Status reflect the
   phase progress? Discrepancies indicate the phase skill's
   handoff ritual did not write the row before the phase-end
   commit.
4. **GitHub issue:** does the issue exist and carry the right
   phase label and ticked checklist? (`flow.py status --item <ID>`
   provides the snapshot.)
5. **Next-phase suggestion:** what is the natural next phase for
   this item? Surface as plain text, the user invokes the skill
   themselves.

The guide owns two narrow CRUD moments at workflow boundaries
that no single phase skill covers (item-start branch creation
when the user enters at A/B/C, post-`/reverse-engineering` item
promotion). Everything else is read-only.

The guide is the consistency layer that prevents drift
between Git tags, BACKLOG.md, GitHub issues, and project cards.
Skills focus on producing artefacts; the guide ensures the
state across systems matches.

## Pre-Phase 0 in entry skills: advisory branch-and-issue check

Every entry skill starts with this check. It is advisory: it surfaces
a mismatch early so the user can fix it before the skill produces
artefacts, but it does NOT block the skill if the user wants to draft
artefacts on the current branch first. The binding gate is the phase-
end commit (see "Phase-end commit (binding)" above), which re-asks
the branch question and refuses to commit on a wrong branch.

```
1. Identify the active backlog item.
   - Parse from user prompt ("work on FEAT-04-09").
   - If unclear, AskUserQuestion: which item are we working on?
   - For genuinely new items: create the BACKLOG row first, then
     proceed.

2. Compute the expected branch name from the item.

3. Compare to current branch:
   - Match -> silent continue.
   - Current branch is main/master/dev -> AskUserQuestion (advisory):
     create `<expected-branch>` and switch now, or draft on the
     current branch and decide at the phase-end commit. On
     `main`/`master`/`dev` strongly recommend switching now because
     the pre-commit hook will refuse the commit later anyway.
   - Current branch is a different item-branch -> AskUserQuestion
     (advisory): switch to the right item-branch (or create it), or
     draft here and resolve at the phase-end commit.
   - Current branch matches loosely (typo, slug variation) ->
     AskUserQuestion: continue here or rename the branch.

4. If GitHub issue does not exist for the item:
   call flow.py create-issue.

5. Draft PR is opened at the FIRST phase-end commit on the branch,
   not at skill start. The Pre-Phase 0 check therefore does not call
   flow.py open-draft-pr. The phase-end commit step does.

6. Write `.git/dia-active-skill` with item ID, branch, skill name,
   timestamp. Subsequent skill invocations read this file and stay
   silent if everything matches.
```

The advisory framing matters because the commit-time check is the one
that actually prevents drift. Keeping the skill-start check binding
caused two failure modes in the field: (a) users answered "weiter
hier" and the skill kept writing on `main`, then no commit ran, so the
artefacts ended up tracked on the wrong branch silently; (b) the
`.git/dia-active-skill` marker stayed valid across phase changes, so
later phases never re-asked even when the item had moved on.

## Override and exceptions

- **Solo project, no GitHub:** the skill detects the absence of `gh`
  binary or a GitHub remote and silently skips the GitHub-integration
  steps. Phase tags still get set as local git tags. Local-only
  workflow stays intact.

- **Hot-fix on dev (rare):** the user can override the branch check
  with explicit confirmation. The pre-commit hook still asks; only
  `--no-verify` skips it. The guide will flag the unusual
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
