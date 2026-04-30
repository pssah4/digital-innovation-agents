<!--
Instructions for the agent: produce this file as
`_devprocess/implementation/plans/PLAN-{nn}-{slug}.md`. Write the prose
in the user's working language. Keep section names (Change Log,
Implementation Notes, etc.) in English so the file greps consistently
across projects.

The frontmatter and the three sections at the bottom (Coverage Gate,
Change Log, Implementation Notes) are the ONLY parts this template
prescribes. The body belongs to the coding agent that produced the
plan.

Status, phase, last-change, and claim live in the backlog row for
this plan in `_devprocess/context/BACKLOG.md`. The frontmatter
carries identity and relations only.
-->

---
id: PLAN-{nn}
title: {short plan title}
date: {YYYY-MM-DD}
feature-refs: []
adr-refs: []
fix-refs: []
imp-refs: []
supersedes: null
superseded-by: null
pair-id: {human-handle}-{model-slug}
---

# PLAN-{nn}: {title}

<!--
Backlog row carries status (Draft, Active, Done, Superseded), phase,
claim, and commit SHAs. Look it up via:
`grep "PLAN-{nn}" _devprocess/context/BACKLOG.md`.

Below this point: the plan body produced by the coding agent. For
Claude Code, paste the plan-mode output verbatim. Do not reshape it.
If the agent produced no usable plan, see the fallback structure at
the bottom of this template.
-->

## {Section name chosen by the agent}

...plan body, as produced by the coding agent...

<!--
=========================================================
Below this line: required sections for traceability. Do not remove.
=========================================================
-->

## Coverage Gate

> Filled before status flips to Active in the backlog row. Lists which
> Success Criteria mapped to which task, which were deferred, and
> which ADRs got at least one operationalizing task.

- [ ] SC coverage: every SC of every referenced FEATURE is either
      mapped to a task here or marked "Deferred: {reason}"
- [ ] ADR alignment: every ADR in `adr-refs` has at least one task
      that operationalizes its Decision section
- [ ] Codebase anchoring: every task names at least one concrete
      file path (Create / Modify / Test)
- [ ] Verify commands: at least one build command and one test
      command are defined

| FEATURE-SC          | Task in this plan | Status                |
|---------------------|-------------------|-----------------------|
| FEAT-{ee}-{ff} SC-01 | Task {N}    | Mapped / Deferred ... |

| ADR referenced | Task in this plan that operationalizes it |
|----------------|--------------------------------------------|
| ADR-{nn}      | Task {N}                                   |

## Change Log

Append-only. Each mid-course deviation appends an entry. Never rewrite
past entries.

### {YYYY-MM-DD}: Plan created

Initial version.

## Implementation Notes

Filled when the backlog row reaches status Done or Superseded.

- Per-task commit SHAs (short form) or "Not executed because ..."
- Deviations summary from the original plan
- Test count delta (new / adjusted / removed)
- Cycle time: first-commit -> last-commit
- ARCHITECTURE.map / JSDoc-header updates landed in commits: ...

---

## Fallback guidance (only if the coding agent did not produce a plan)

If you are a human or a coding agent without a native planning mode,
use this minimal structure for the plan body:

1. **Context** - one paragraph diagnosing why this plan is needed,
   referencing the FEATURE / ADR / plan-context.md sections it
   realizes.
2. **Scope** - in / out bullets.
3. **Tasks** - ordered list; each task names the file paths touched
   and the verification step (test, build, smoke).
4. **Verification** - how you know the plan is done. At minimum a
   build command and the acceptance criteria from the FEATURE spec.

No fixed template beyond this. More structure is welcome if the
situation asks for it.
