---
title: Handoff Rituals
description: The mandatory 3-part ritual every phase skill runs at the end to ensure structured phase transitions.
---

# Handoff Rituals

Every V-Model phase skill runs a 3-part Handoff Ritual at the end of
its phase. This is the mechanism that keeps phase transitions
structured without introducing heavy gates or approval bureaucracy.

## The three parts

### Part 1: Artifact report

The skill lists every artifact it produced or updated, with full paths:

```
Produced / updated:
- _devprocess/analysis/BA-project.md: full Business Analysis
- _devprocess/analysis/EXPLORE-project.md: Exploration Board (PoC)
- Key output: How-Might-We question, 2 Personas
```

This gives the user (and the next phase skill) an immediate overview
of what was done.

### Part 2: Handoff context

The skill appends a new entry to `_devprocess/context/30_handoffs.md`
with content that is not obvious from the artifacts alone:

- Open decisions that were deferred
- Assumptions that were made but not confirmed
- Risks or concerns worth flagging
- Dependencies on other phases or external systems

Example entry in `30_handoffs.md`:

```markdown
## 2026-04-14 14:30, business-analyse -> requirements-engineering

**Scope:** PoC

**Produced:**
- _devprocess/analysis/BA-retrospectives.md
- _devprocess/analysis/EXPLORE-retrospectives.md

**Handoff context:**
- HMW: "How might we help distributed product teams run retros that
  surface root causes, so action items actually ship?"
- 2 Personas identified, Persona A (Product Manager) is primary
- Critical hypothesis: "async format does not kill group dynamics",
  must be validated in PoC
- Assumption: Slack integration is possible. Architect please verify.
```

The next phase skill reads this entry to pick up context.

### Part 3: Transition question

The skill asks the user an explicit question:

> "Business Analysis is complete. The next step in the V-Model is
> `/requirements-engineering`.
>
> Shall I start `/requirements-engineering` now, or would you like to
> review the BA first?"

**On agreement** ("yes", "go", "next") or when running inside
`/v-model-workflow`: the orchestrator launches the next skill and
passes the handoff context.

**On rejection** ("no", "stop", "I want to check first"): the skill
pauses and waits. The workflow state is preserved in `_devprocess/`
so the user can resume later.

## Why 3 parts, not a gate?

A gate is a pass/fail mechanism that blocks progress. Gates sound
good in theory but duplicate the quality checks already inside each
skill. For example, `/business-analyse` already runs quality gates on
its Exploration Board before handoff. An extra outer gate adds
bureaucracy without adding rigor.

A handoff ritual is different. It is a deliberate, structured transfer
of context. The ritual ensures:

- Nothing is lost between phases (artifact report)
- The next phase knows what is important and what is unknown (handoff context)
- The user is in control at every transition (explicit question)

It is verbose enough to be structured, but lightweight enough not to
slow the workflow down.

## The `30_handoffs.md` log

`_devprocess/context/30_handoffs.md` is an append-only log of every
phase transition in the project. Each entry has:

- Timestamp and phase transition (for example, `architecture -> coding`)
- Artifacts produced or updated with full paths
- Handoff context (free-form prose: open questions, risks, assumptions)

The log is never rewritten or cleaned up. It is a historical record.
The next phase skill reads the latest entry. Older entries stay for
audit and "how did we get here?" investigations.

## Integration with the orchestrator

When `/v-model-workflow` runs, the orchestrator reads the handoff
context after each ritual and uses it as input for the next phase.
When a skill runs directly (without the orchestrator), the ritual
still runs, and the next skill finds the context in `30_handoffs.md`
when it is eventually invoked.

Both paths end up with the same artifacts and the same traceability.

## Rules for skills

Every phase skill (`/business-analyse`, `/requirements-engineering`,
`/architecture`, `/coding`, `/testing`, `/security-audit`) implements
this ritual at the end. The ritual is mandatory. The skill does not
consider itself complete until the ritual has run.

This is documented in `skills/<skill>/SKILL.md` under a section titled
"Handoff Ritual (mandatory at end of phase)".

## See also

- [V-Model workflow guide](../guides/v-model-workflow): the orchestrator
- [Artifacts reference](../reference/artifacts): including `30_handoffs.md`
- [V-Model concept](./v-model): the cycle the rituals serve
