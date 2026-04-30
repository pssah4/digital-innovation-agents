# Branch protection -- shared check for entry skills

Every skill that begins new work or writes new artefacts MUST verify
the user is not on a protected branch before the first write. This
prevents accidental commits on `main`, `master`, or `dev` and makes
sure feature work is reviewable and revertable as a single PR.

The check is invariant across skills. It happens once, at the very
start of the skill, before Phase 0 / Phase -1 / any artefact write.

## Skills that MUST run this check

- `/reverse-engineering` -- before Phase -1
- `/business-analysis` -- before Phase 0
- `/requirements-engineering` -- before any FEATURE write
- `/architecture` -- before any ADR write
- `/coding` -- before any code or artefact edit
- `/testing` -- before any test write
- `/security-audit` -- before any AUDIT report write
- `/dia-migration` -- before any migration step
- `/release` -- this skill is the exception. It MUST run on `dev` /
  `main` and skips the check.

## The check

Pseudo-flow:

```
current_branch = git rev-parse --abbrev-ref HEAD
protected = ["main", "master", "dev"]   # configurable
if current_branch in protected:
    AskUserQuestion (one question, with Pro/Con):
        "You are on protected branch '{current_branch}'. New work
         should land on a dedicated feature branch so it stays
         reviewable and revertable as a single PR. How to proceed?"
        Options:
          A) Create feature branch '{suggested_slug}' and switch
             Pro: Safe default, keeps history clean
             Con: One extra step
          B) Stay on '{current_branch}' (advanced, requires confirmation)
             Pro: Sometimes correct (hot-fix on main, doc-only on dev)
             Con: Loses PR review, risks force-push conflicts
          C) Custom branch name
             Pro: User picks the name explicitly
             Con: Slightly more typing
        Recommendation: A in 95% of cases. B only when the user
        explicitly knows the work is a tiny commit that should land
        on the protected branch directly.
```

## Slug suggestion heuristics

The recommended slug for option A is derived from the user's
request, not generated blindly:

- For `/reverse-engineering`: `feature/reverse-engineer-<repo-name>`
- For `/business-analysis` (new BA): `feature/ba-<short-topic>`
- For `/business-analysis` (validation): `feature/ba-validate-<existing-BA-slug>`
- For `/requirements-engineering`: `feature/re-<feature-or-epic-slug>`
- For `/architecture`: `feature/arch-<adr-or-feature-slug>`
- For `/coding`: `feature/<feature-slug>` (mirrors the FEATURE ID)
- For `/testing`: `feature/test-<feature-or-area>`
- For `/security-audit`: `feature/audit-<YYYY-MM-DD>`
- For `/dia-migration`: `feature/dia-migration-v{version}`

All slugs:

- lower-case, hyphen-separated
- start with `feature/`, `fix/`, or `chore/` per project convention
- max 50 characters

## Non-interactive contexts

If the skill runs inside a non-interactive context (CI, scripted
agent run with no `AskUserQuestion` tool available), it MUST exit
with a clear error rather than write on the protected branch.

## Defense in depth

The pre-commit hook (`tools/git-hooks/pre-commit`, installed via
`tools/install-git-hooks.sh`) blocks commits on protected branches
as a backstop. This skill-side check exists because the user
should be asked BEFORE the work begins, not after their first
commit attempt fails.

## Override mechanism

Two override paths exist for valid edge cases:

- **Per-commit:** `git commit --no-verify` (bypasses the pre-commit
  hook for that single commit only).
- **Per-project:** `git config dia.protected-branches "main master"`
  (removes `dev` from the protected list, e.g. when the project
  uses `dev` as its work branch).

Skills MUST NOT bypass the question via these overrides
automatically. The user must explicitly trigger them.
