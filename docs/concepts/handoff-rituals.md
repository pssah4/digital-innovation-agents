---
title: Handoff Rituals
description: The mandatory 4-part ritual every phase skill runs at the end to ensure structured phase transitions.
---

# Handoff Rituals

Every V-Model phase skill runs a 4-part Handoff Ritual at the end of
its phase. This is the mechanism that keeps phase transitions
structured without introducing heavy gates or approval bureaucracy.

## The four parts

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

The skill appends a new entry to `_devprocess/context/HANDOFFS.md`
with content that is not obvious from the artifacts alone:

- Open decisions that were deferred
- Assumptions that were made but not confirmed
- Risks or concerns worth flagging
- Dependencies on other phases or external systems

Example entry in `HANDOFFS.md`:

```markdown
## 2026-04-14 14:30, business-analysis -> requirements-engineering

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

### Part 3: Phase-end commit and tag

Every phase ends with a canonical commit and a phase-done tag:

```bash
git add -A
git commit -m "chore(ba): EPIC-01 BA complete

Refs: EPIC-01

Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>"

python tools/github-integration/flow.py tag-phase --phase ba
```

The commit type matches the phase (`chore(ba)`, `feat(re)`,
`chore(arch)`, `feat(code)`, `test`, `chore(sec)`). The
`tag-phase` call attaches a `<ITEM-ID>/<phase>-done` tag, for
example `EPIC-01/ba-done`. Phase-done tags are how the guide
detects that a phase has completed for an item.

### Part 4: Transition question

The skill asks the user an explicit question:

> "Business Analysis is complete. The next step in the V-Model is
> `/requirements-engineering`.
>
> Shall I start `/requirements-engineering` now, or would you like to
> review the BA first?"

**On agreement** ("yes", "go", "next") or when running inside
`/dia-guide`: the guide launches the next skill and
passes the handoff context.

**On rejection** ("no", "stop", "I want to check first"): the skill
pauses and waits. The workflow state is preserved in `_devprocess/`
so the user can resume later.

## Why 4 parts, not a gate?

A gate is a pass/fail mechanism that blocks progress. Gates sound
good in theory but duplicate the quality checks already inside each
skill. For example, `/business-analysis` already runs quality gates on
its Exploration Board before handoff. An extra outer gate adds
bureaucracy without adding rigor.

A handoff ritual is different. It is a deliberate, structured transfer
of context. The ritual ensures:

- Nothing is lost between phases (artifact report)
- The next phase knows what is important and what is unknown (handoff context)
- The phase boundary is detectable from git history alone (phase-end commit and tag)
- The user is in control at every transition (explicit question)

It is verbose enough to be structured, but lightweight enough not to
slow the workflow down.

After every ritual, the guide runs `/consistency-check` Mode A
on the changed artifacts. Drift caught at the boundary is cheap. Drift
discovered three phases later is expensive.

## Dialog handoffs, not blockers

Both inter-phase handoff documents (`architect-handoff.md` and
`plan-context.md`) carry a `## Dialog` section with a Questions table
and an Answers table. The receiving skill scans the Questions table
on session start and tries the agent-agent path first: it self-answers
from existing artifacts (BA, ADRs, FEATURE specs, codebase). What it
cannot resolve from artifacts gets bundled into a single
`AskUserQuestion` for the user.

Pending dialog entries never block unrelated work. Only the affected
ADR or feature waits. Other work continues with a `blocked-by` note
that cites the open question.

This pattern keeps phase transitions structured without forcing every
question through a meeting or a Slack thread. The handoff document is
the conversation transcript, and the next session reads it on start.

The seed format for both documents lives in
[`skills/requirements-engineering/templates/ARCHITECT-HANDOFF-TEMPLATE.md`](https://github.com/pssah4/digital-innovation-agents/blob/main/skills/requirements-engineering/templates/ARCHITECT-HANDOFF-TEMPLATE.md).

## The `HANDOFFS.md` log

`_devprocess/context/HANDOFFS.md` is an append-only log of every
phase transition in the project. Each entry has:

- Timestamp and phase transition (for example, `architecture -> coding`)
- Artifacts produced or updated with full paths
- Handoff context (free-form prose: open questions, risks, assumptions)

The log is never rewritten or cleaned up. It is a historical record.
The next phase skill reads the latest entry. Older entries stay for
audit and "how did we get here?" investigations.

## Integration with the guide

When `/dia-guide` runs, the guide reads the handoff
context after each ritual and uses it as input for the next phase.
When a skill runs directly (without the guide), the ritual
still runs, and the next skill finds the context in `HANDOFFS.md`
when it is eventually invoked.

Both paths end up with the same artifacts and the same traceability.

## Rules for skills

Every phase skill (`/business-analysis`, `/requirements-engineering`,
`/architecture`, `/coding`, `/testing`, `/security-audit`) implements
this ritual at the end. The ritual is mandatory. The skill does not
consider itself complete until the ritual has run.

This is documented in `skills/<skill>/SKILL.md` under a section titled
"Handoff Ritual (mandatory at end of phase)".

## See also

- [V-Model workflow guide](../guides/dia-guide): the guide
- [Artifacts reference](../reference/artifacts): including `HANDOFFS.md`
- [V-Model concept](./v-model): the cycle the rituals serve
