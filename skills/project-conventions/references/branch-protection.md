# Branch protection -- shared check for entry skills

Every skill that begins new work MUST verify the current branch is
right for THIS work before the first artefact write. The check
fires once per skill invocation (at the very start, before Phase 0
or Phase -1), not before every commit.

The question is broader than "are you on main/master/dev". A user
might be on `feature/yesterday-thing` and start a completely
different topic; that mixes concerns into one PR and makes review
harder. The check asks, regardless of branch type:

> "Is the current branch the right place for the new work, or
> should we create a new feature branch?"

## Skills that MUST run this check

- `/reverse-engineering` -- before Phase -1
- `/business-analysis` -- before Phase 0
- `/requirements-engineering` -- before any FEATURE write
- `/architecture` -- before any ADR write
- `/coding` -- before any code or artefact edit
- `/testing` -- before any test write
- `/security-audit` -- before any AUDIT report write
- `/dia-migration` -- before any migration step
- `/release` -- exception: this skill MUST run on `dev` / `main`,
  skips the check

The check fires once per skill invocation. If the user already
answered for this session (the skill is mid-workflow and the user
is on the branch they confirmed earlier), the check stays silent.

## The check

Pseudo-flow at skill start:

```
current_branch  = git rev-parse --abbrev-ref HEAD
recent_commits  = git log -3 --format='%s' on current_branch
work_topic      = the user's described topic for THIS skill invocation
suggested_slug  = derive from work_topic (see heuristics below)

case current_branch:
    # Case 1: on a protected branch -> always block
    main | master | dev:
        AskUserQuestion (Pro/Con):
            "You are on protected branch '{current_branch}'. New
             work needs a dedicated branch."
            A) Create '{suggested_slug}' and switch (recommended)
            B) Custom branch name
            C) Abort

    # Case 2: on a feature/* branch -> ask whether it fits
    feature/* | fix/* | chore/*:
        AskUserQuestion (Pro/Con):
            "You are on '{current_branch}'. Recent commits:
             {recent_commits}. The new work is '{work_topic}'. Is
             this branch right for it, or should we create a new
             feature branch?"
            A) Continue on '{current_branch}'
               Pro: fewer branches, work stays bundled
               Con: only correct if the topic is the same
            B) Create new branch '{suggested_slug}' (recommended if topics differ)
               Pro: clean PR per topic, easier review and revert
               Con: one extra branch to track
            C) Switch to an existing branch (list other feature branches)
            D) Custom branch name
```

The skill picks the recommendation based on a heuristic:

- **Recommend A (continue)** when the branch name slug is a substring
  of the work topic, OR the last commit subject describes a related
  topic.
- **Recommend B (new branch)** when the branch name has no overlap
  with the work topic, OR the last commit is older than 7 days.
- **Recommend C (switch)** is offered when the user has another
  feature branch whose name overlaps with the work topic.

When unclear, recommend B and let the user override. Default
posture: clean per-topic branches.

## Slug suggestion heuristics

The recommended slug is derived from the user's request, not
generated blindly:

- For `/reverse-engineering`: `feature/reverse-engineer-<repo-name>`
- For `/business-analysis` (new BA): `feature/ba-<short-topic>`
- For `/business-analysis` (validation): `feature/ba-validate-<existing-BA-slug>`
- For `/requirements-engineering`: `feature/re-<feature-or-epic-slug>`
- For `/architecture`: `feature/arch-<adr-or-feature-slug>`
- For `/coding`: `feature/<feature-slug>` (mirrors the FEATURE ID)
- For `/testing`: `feature/test-<feature-or-area>`
- For `/security-audit`: `feature/audit-<YYYY-MM-DD>`
- For `/dia-migration`: `feature/dia-migration-v<version>`

All slugs:

- lower-case, hyphen-separated
- start with `feature/`, `fix/`, or `chore/` per project convention
- max 50 characters

## Once-per-session contract

The check fires only once per skill invocation. After the user has
answered, the skill stores the confirmed branch name and proceeds.
If the user re-runs the same skill mid-flow (e.g. after a context
swap), the skill detects the same active branch and does not
re-ask.

Implementation hint: the skill writes a tiny marker file at
`.git/dia-active-skill` containing
`{skill_name}|{branch}|{started_at}` when the user confirms. Future
invocations check this file. The marker is removed at skill end.
If the marker exists but the user is on a different branch, the
skill asks again (the user switched mid-flow).

## Non-interactive contexts

If the skill runs inside a non-interactive context (CI, scripted
agent run with no `AskUserQuestion` tool available), it MUST exit
with a clear error rather than write on an unconfirmed branch.

## Defense in depth

The pre-commit hook (`tools/git-hooks/pre-commit`, installed via
`tools/install-git-hooks.sh`) is the safety net for the obvious
case: it refuses commits on `main` / `master` / `dev` regardless of
context, and offers an interactive feature-branch creation. It
cannot detect "wrong feature branch for new work" because it has no
notion of work topic. The skill-side check covers that case.

## Override mechanism

Two override paths exist for valid edge cases:

- **Per-commit:** `git commit --no-verify` (bypasses the pre-commit
  hook for a single commit only).
- **Per-project:** `git config dia.protected-branches "main master"`
  (removes `dev` from the protected list when the project uses
  `dev` as its primary work branch).

Skills MUST NOT bypass the question via these overrides
automatically. The user must explicitly trigger them.
