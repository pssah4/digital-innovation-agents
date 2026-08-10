# Handoff ritual formats for /coding

## Part 1: Artifact report format

```
Produced / updated:
- src/{files}: {summary}
- _devprocess/implementation/plans/PLAN-*.md: {status updates, SHAs}
- _devprocess/requirements/features/FEAT-*.md: {substance updates}
- _devprocess/architecture/ADR-*.md: {status and implementation notes}
- _devprocess/requirements/handoff/plan-context.md: {ref updates if any}
- _devprocess/requirements/fixes/FIX-*.md: {new or updated FIX specs}
- _devprocess/context/BACKLOG.md: {new/resolved items, including FIX rows}
```

## Part 3: Phase-end commit format

Canonical commit message for CODING (full contract:
`skills/project-conventions/references/team-workflow.md#phase-end-commit-binding`):

```
<feat|fix>(code): <ITEM-ID> coding complete

<one-line summary of what shipped>
<open concerns / assumptions for testing as short bullets>

Refs: <ITEM-ID>[, ADR-NN, PLAN-NN, FIX-...]
DIA-Phase: code-done
DIA-Handoff: <ITEM-ID> -> testing
DIA-Triage: <ITEM-ID> <feature|imp|fix|adr>
```

Use `feat` for new FEATURE work, `fix` for FIX work, `chore` for IMP
work. Long coding phases produce multiple intermediate commits per
task; only the final phase-end commit gets the `<id>/code-done` tag
and the DIA trailers. Skip the commit silently if the working tree
has no changes.

After the commit lands:

```
python3 tools/github-integration/flow.py tag-phase --item <ID> --phase code
python3 tools/github-integration/flow.py sync-status --item <ID>
```

`sync-status` mirrors the BACKLOG Status column to the GitHub issue
and project (and the GitHub Assignee back into the BACKLOG Claim
column). It is a no-op outside `mode = "github-sync"`.

## Part 4: Transition question wording

> "Implementation is complete. Recommended next: `/testing` -- input
> from the new code plus the updated FEATURE specs.
>
> Shall I start `/testing` now, or would you like to review first?"

On agreement ("yes" / "go" / "next") or when running inside
`/dia-guide`: start `/testing` and pass the handoff context. On
rejection: pause and wait for user instruction.
