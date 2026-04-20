---
id: PLAN-{NNN}
title: {short plan title}
status: Draft
date: {YYYY-MM-DD}
feature-refs: []
adr-refs: []
bug-refs: []
supersedes: null
superseded-by: null
pair-id: {human-handle}-{model-slug}
---

# PLAN-{NNN}: {title}

<!--
The frontmatter above + the three sections at the bottom (Change Log,
Implementation Notes) are the ONLY parts this template prescribes. They
carry the traceability signal the V-Model needs.

Everything between here and "## Change Log" is the plan BODY. The body
belongs to the coding agent that created it. For Claude Code: paste the
agent's plan verbatim. Do not reshape it. If Claude Code ships a better
planning format next month, we inherit the improvement for free.

If an agent with weaker planning produces the plan, see the guidance
at the bottom of this template for a minimal structure fallback.
-->

## {Section name chosen by the agent}

...plan body, as produced by the coding agent...

<!--
===================================================================
Below this line: required sections for traceability. Do not remove.
===================================================================
-->

## Change Log

Append-only. Each mid-course deviation appends an entry. Never rewrite
past entries.

### {YYYY-MM-DD}: Plan created

Initial version.

## Implementation Notes

Filled when the plan reaches Status: Implemented or Superseded.

- Per-task commit SHAs (short form) or "Not executed because ..."
- Deviations summary from the original plan
- Test count delta (new / adjusted / removed)
- Cycle time: first-commit -> last-commit

---

## Fallback guidance (only if the coding agent did not produce a plan)

If you are a human or a coding agent without a native planning mode,
use this minimal structure for the plan body:

1. **Context** -- one paragraph diagnosing why this plan is needed,
   referencing the FEATURE / ADR / plan-context.md sections it
   realizes.
2. **Scope** -- in / out bullets.
3. **Tasks** -- ordered list; each task names the file paths touched
   and the verification step (test, build, smoke).
4. **Verification** -- how you know the plan is done. At minimum a
   build command and the acceptance criteria from the FEATURE spec.

No fixed template beyond this. More structure is welcome if the
situation asks for it.
