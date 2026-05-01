# Branch protection -- shared check for entry skills

This document describes two checks for branch correctness:

1. **Skill-start check (advisory)** -- runs at Pre-Phase 0, surfaces
   a mismatch early so the user can switch before producing artefacts.
   Not blocking.
2. **Commit-boundary check (binding)** -- runs at every phase-end
   commit (and every mid-phase commit). Refuses to commit on a wrong
   branch. This is the authoritative gate for the branch / item
   mapping.

The split exists because field experience showed the skill-start
check alone cannot prevent drift: users answer "weiter hier", the
skill keeps writing, and no commit runs until much later, so the
artefacts end up tracked on the wrong branch silently. The commit
boundary is the natural enforcement point because it cannot be
deferred without losing work.

The full team-workflow contract (branch = backlog item, phase tags,
GitHub issue, draft PR, phase-end commit, project cards) lives in
`team-workflow.md`. Read that first; this file is the operational
detail of the two checks.

## Core rule (from team-workflow.md)

One backlog item -> one branch. Branch name is derived from the
item ID:

| Item type | Branch                                     |
|-----------|--------------------------------------------|
| FEAT-EE-FF | `feature/feat-ee-ff-<short-slug>`         |
| EPIC-NN | `feature/epic-nn-<short-slug>`               |
| FIX-EE-FF-NN | `fix/fix-ee-ff-nn-<short-slug>`         |
| IMP-EE-FF-NN | `chore/imp-ee-ff-nn-<short-slug>`       |

Skills do not own branches; backlog items do. Multiple skills (BA,
RE, Arch, Coding, Testing, Audit) all write to the same branch as
the item walks through the V-Model phases.

## Skills that MUST run this check

- `/reverse-engineering` -- before Phase -1 (special: bootstraps
  many items at once, see exception below)
- `/business-analysis` -- before Phase 0
- `/requirements-engineering` -- before any FEATURE write
- `/architecture` -- before any ADR write
- `/coding` -- before any code or artefact edit
- `/testing` -- before any test write
- `/security-audit` -- before any AUDIT report write
- `/dia-migration` -- before any migration step
- `/release` -- exception: this skill runs on `dev` / `main` and
  skips the check.

The check fires once per skill invocation (state in
`.git/dia-active-skill`).

## Skill-start check (advisory)

Pseudo-flow at skill start:

```
work_item       = identify the active backlog item (parse from prompt
                  or AskUserQuestion). For genuinely new items, write
                  the BACKLOG row first.
expected_branch = derive_branch_name(work_item)
current_branch  = git rev-parse --abbrev-ref HEAD

case current_branch:
    expected_branch (exact or close match):
        silent continue.

    main | master | dev:
        AskUserQuestion (Pro/Con per option):
            "You are on protected branch '{current}'. New work for
             {work_item} needs a dedicated branch. The phase-end
             commit will refuse to land on '{current}' anyway."
            A) Create '{expected_branch}' and switch now (recommended)
            B) Draft here, decide at phase-end commit
            C) Custom branch name

    other feature/*, fix/*, chore/*:
        AskUserQuestion (Pro/Con per option):
            "You are on '{current}'. New work targets '{work_item}'.
             Switch to its branch?"
            A) Switch to '{expected_branch}' (creates it if missing,
               recommended)
            B) Draft here and resolve at the phase-end commit
            C) Custom branch name

    case loose match (typo, slug variation):
        AskUserQuestion: continue here, or rename to canonical name.
```

The skill-start check is advisory: choosing option B does not block
the skill. The phase-end commit will re-ask before any artefact is
recorded in git history.

## Commit-boundary check (binding)

Pseudo-flow at every commit step (phase-end commit and any mid-phase
commit):

```
work_item       = the active backlog item carried by the skill
                  (read from .git/dia-active-skill).
expected_branch = derive_branch_name(work_item)
current_branch  = git rev-parse --abbrev-ref HEAD
prior_commits   = git rev-list --count HEAD ^merge-base-with-trunk

case current_branch:
    expected_branch:
        proceed with commit.

    main | master | dev:
        BLOCK. AskUserQuestion (no Continue option):
            "Cannot commit phase artefacts on protected branch
             '{current}'. New work for {work_item} needs a dedicated
             branch."
            A) Create '{expected_branch}' from current HEAD and
               switch (carries the working tree along)
            B) Custom branch name
            C) Abort the commit step (skill ends without a tag)

    other feature/*, fix/*, chore/*:
        AskUserQuestion:
            "About to record {work_item} artefacts on '{current}',
             which is the branch for a different item. Switch to
             '{expected_branch}' before committing?"
            A) Switch to '{expected_branch}', carry the working
               tree, then commit (recommended)
            B) Commit here and re-tag the BACKLOG row's branch
               (only when the user knows the items belong together,
               e.g. nested epic work)
            C) Abort the commit step
```

The commit-boundary check ignores the `.git/dia-active-skill` marker
for branch correctness. The marker proves the skill-start check ran
once; it does not prove the user stayed on the right branch since.
Users edit branches mid-flow more often than mid-skill, so the
marker is unreliable as the sole gate.

The recommendation always derives from the item-to-branch mapping,
not from heuristics about the current branch's age or topic
overlap. The model is deterministic: one item, one branch name,
one PR.

## Once-per-session contract

The check fires only once per skill invocation. After the user has
answered, the skill writes to `.git/dia-active-skill`:

```
{skill_name}|{item_id}|{branch}|{started_at_iso}
```

Future skill invocations read this file and skip the question if
all four fields still match. If the user has switched branch or
item mid-flow, the marker mismatches and the question fires again.

The marker is removed at skill end.

## Exception: /reverse-engineering

`/reverse-engineering` bootstraps an entire backlog at once
(potentially 20+ items). Branching per-item would force the user to
juggle 20 branches before any work is done. The exception:

- `/reverse-engineering` runs on a single feature branch
  `feature/reverse-engineer-<repo-name>`.
- All artefacts produced (FEATURE specs, ADRs, BA draft, backlog
  rows) land in that one branch.
- After RE handoff, the per-item branching kicks in: `/coding` for
  FEAT-04-09 creates `feature/feat-04-09-...` from the
  reverse-engineering merge base.

This exception is documented in `team-workflow.md` and applies only
to RE.

## Slug heuristics

When the skill creates the branch, it derives the short slug from
the item title (BACKLOG.md row, second column). Rules:

- Lower-case
- ASCII-only (umlauts to ae/oe/ue/ss for shell-friendliness)
- Hyphen-separated
- Drop articles ("the", "a", "der", "die"), drop "and" / "und"
- Max 4 words
- Append at most 30 characters after the item id

Example:
- BACKLOG: `FEAT-04-09 | OpenAI-kompatible Streaming Tool-Call Robustheit`
- Slug: `openai-streaming-toolcall`
- Branch: `feature/feat-04-09-openai-streaming-toolcall`

If the slug derivation produces a confusing result, the skill
offers two options in the AskUserQuestion (the auto-slug and a
custom-slug input).

## Non-interactive contexts

If the skill runs without a TTY or without `AskUserQuestion` (CI,
scripted agent), it MUST exit with a clear error rather than write
on an unconfirmed branch. The error message names the expected
branch and the command the user can run manually.

## Defense in depth

The pre-commit hook (`tools/git-hooks/pre-commit`, installed via
`tools/install-git-hooks.sh`) refuses commits on protected branches
(`main`, `master`, `dev`) regardless of skill context. It is the
backstop for the most-obvious mistake. It cannot detect "wrong
feature branch for this item" because it does not know the active
item; that is the skill-side check's job.

## Override mechanism

- **Per-commit:** `git commit --no-verify` (bypasses the pre-commit
  hook for a single commit).
- **Per-project:** `git config dia.protected-branches "main master"`
  (removes `dev` from the protected list; useful when a project
  uses `dev` as its primary work branch).
- **Per-project workflow:** `git config dia.workflow trunk-based`
  (disables per-item branching entirely; all work happens on
  `main`, isolation lives in feature flags). See team-workflow.md
  for the trunk-based variant.

Skills MUST NOT bypass the question via these overrides
automatically. The user must explicitly trigger them.
