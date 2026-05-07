---
title: Hotfix lane
description: Fast path for trivial bug fixes. Five criteria, fix-now-document-after, four consistency mechanisms, validate-fix gate.
---

# Hotfix lane

Not every bug deserves the full backlog-row-first capture flow.
When the fix is obviously local and small, demanding a FIX-Row,
detail file, branch, and (in `github-sync` mode) GitHub issue
before the fix runs adds friction without adding visibility. The
hotfix lane lets `/coding` fix immediately and then create the
artifacts right after, so the work is still visible in the
backlog and on the team board.

## Five criteria (all must hold)

The hotfix lane is allowed only when **all five** apply:

1. The fix touches at most three files.
2. No new feature, no new dependency.
3. No breaking change to a public API or interface.
4. The fix takes under 15 minutes.
5. An existing FEAT covers the affected functionality, so the
   FIX has a clear parent to attach to.

If any single criterion fails, fall back to the standard
bug-capture flow: write the FIX-Row first, then implement.

## The flow

When all five criteria hold:

1. **Fix immediately.** `/coding` analyses, fixes, and runs the
   relevant tests in place. No FIX-Row yet.
2. **Document right after the fix lands locally.** Mandatory:
   - Write the BACKLOG row for the FIX (status `Ready` or
     `In Progress` depending on whether the commit already exists,
     phase `Building`, Source `BUG`, Refs the parent FEAT).
   - Create the FIX detail file under
     `_devprocess/requirements/fixes/FIX-{ee}-{ff}-{nn}-{slug}.md`.
   - Commit with the canonical message
     `fix: FIX-{ee}-{ff}-{nn} <short description>` and the
     standard `Refs:` trailer.
   - When `mode = "github-sync"`: create the matching GitHub
     issue (`gh issue create --title "FIX-{ee}-{ff}-{nn}: {slug}"
     --label "fix,hotfix"`), then run
     `python3 tools/github-integration/flow.py sync-status --item
     FIX-{ee}-{ff}-{nn}`.
   - **Always** (in any mode) close with
     `python3 tools/github-integration/flow.py validate-fix --item
     FIX-{ee}-{ff}-{nn}`.
3. **Acknowledge** in chat: list the modified files, the FIX-ID,
   the issue URL (if created), and the validate-fix verdict.

The hotfix lane does NOT suspend the regression-test cycle (Phase
4b in `/coding`). If the bug is non-trivial enough to need a
regression test, write it; the 15-minute budget includes the
test.

## Four consistency mechanisms

The hotfix lane skips the V-Model phases, but it does not skip
consistency. Four mechanisms keep the lane safe:

1. **FIX-Row in `BACKLOG.md` (mandatory, even retroactively).**
   Every fix gets a row with full id `FIX-{ee}-{ff}-{nn}`, either
   before the fix (standard lane) or right after (hotfix lane).
   The row is the anchor that `/consistency-check` mode A uses to
   find and validate the fix.
2. **Commit cites the FIX-id.** The commit subject and `Refs:`
   trailer both name the FIX, the parent FEAT, and any other
   affected artifact:
   ```
   fix: FIX-05-02-01 button click handler null check

   Refs: FIX-05-02-01, FEAT-05-02
   ```
   Git history and BACKLOG.md stay synchronized through the cite.
3. **Deferred-stub marker (bidirectional binding).** If the fix
   leaves a temporary stub, `/consistency-check` mode A enforces
   the link in both directions:
   - code marker `// FIXME(stub): <reason> -- see FIX-05-02-01`
   - the FIX row points back at the stub via the Notes column

   A missing pair triggers `stub-without-fix-row` or
   `fix-without-stub-evidence`.
4. **Regression-test cycle (3 runs).** Hotfixes still run the
   Phase 4b cycle: write the test, the test passes, revert the
   fix, the test fails, restore the fix, the test passes again.
   The FIX detail file gets a `## Regression test` entry that
   confirms the cycle.

## Closing the consistency gap with `validate-fix`

`/consistency-check` mode A normally fires at the end of every
phase. Hotfixes have no phase boundary, so the check has no
automatic trigger. To close the gap, the hotfix flow ends with
`flow.py validate-fix --item FIX-{ee}-{ff}-{nn}`. The subcommand
performs a hotfix-scoped mode-A check:

- FIX row exists in BACKLOG.md with the correct id and references
  the parent FEAT in the Refs column
- at least one commit on the current branch cites the FIX id in
  the subject or `Refs:` trailer
- no `FIXME(stub):` referencing this FIX-id is present in the
  codebase without a matching FIX row
- in `mode = "github-sync"`: the matching GitHub issue exists

The validate-fix call is part of the hotfix lane's mandatory
post-fix steps; it is not optional.

## Anti-misuse signal

The directions meeting reviews the share of hotfix-lane FIX
items per iteration. If hotfixes account for more than 30% of an
iteration's work, the lane is being misused as a process bypass
and the backlog gets a quality-debt item: either the fixes are
larger than the criteria allow (file the IMP), or the codebase
needs structural fixes that prevent the recurring small bugs
(file the EPIC).

## See also

- `skills/coding/SKILL.md` for the operational steps the agent
  takes when running the lane
- [Coding guide](../guides/coding) for the surrounding
  bug-capture flow and Plan Coverage Gate
- [Verification gates](./verification-gates) for the regression
  test 3-run cycle in detail
- [Commands reference](../reference/commands) for `validate-fix`
