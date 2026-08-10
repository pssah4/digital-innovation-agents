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
- _devprocess/analysis/BA-project.md: Business Analysis record
- _devprocess/analysis/EXPLORE-project.md: Exploration Board (PoC)
- Key output: How-Might-We question, 2 Personas
```

This gives the user (and the next phase skill) an immediate overview
of what was done.

### Part 2: Phase-end commit with DIA trailers

Every phase ends with a canonical commit before the phase tag is
set. The commit carries machine-readable trailers, and the handoff
context (open decisions, unconfirmed assumptions, risks,
dependencies) goes into the commit body as short bullets:

```bash
git add -A
git commit -m "chore(ba): EPIC-01 BA complete

- Critical hypothesis: async format does not kill group dynamics
- Assumption: Slack integration is possible. Architect please verify.

Refs: EPIC-01
DIA-Phase: ba-done
DIA-Handoff: EPIC-01 -> requirements-engineering

Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>"

python tools/github-integration/flow.py tag-phase --phase ba
```

The three `DIA-*` trailers are the phase-transition record:

- `DIA-Phase: <phase>-done` mirrors the phase-tag vocabulary
  (`ba|re|arch|plan|code|test|sec`-done).
- `DIA-Handoff: <ITEM-ID> -> <next-skill>` names the item and the
  recommended next skill.
- `DIA-Triage: <ITEM-ID> <kind>` (only on the commit where triage
  happened) carries the item kind (`feature|imp|fix|adr`). A skill
  that finds a `DIA-Triage` trailer for its item skips its Phase-0
  triage question.

The commit type matches the phase (`chore(ba)`, `chore(re)`,
`chore(arch)`, `feat(code)`, `test`, `chore(audit)`). The
`tag-phase` call attaches a `<ITEM-ID>/<phase>-done` tag, for
example `EPIC-01/ba-done`. Phase-done tags and trailers are how the
guide detects that a phase has completed for an item.

### Part 3: Transition question

The skill asks the user an explicit question:

> "Business Analysis is complete. The next step in the V-Model is
> `/requirements-engineering`.
>
> Shall I start `/requirements-engineering` now, or would you like to
> review the BA first?"

**On agreement** ("yes", "go", "next"): the skill starts the next
phase skill and passes the handoff context.

**On rejection** ("no", "stop", "I want to check first"): the skill
pauses and waits. The workflow state is preserved in `_devprocess/`
and git history, so the user can resume later.

## Why a ritual, not a gate?

A gate is a pass/fail mechanism that blocks progress. Gates sound
good in theory but duplicate the quality checks already inside each
skill. For example, `/business-analysis` already runs quality gates on
its Exploration Board before handoff. An extra outer gate adds
bureaucracy without adding rigor.

A handoff ritual is different. It is a deliberate, structured transfer
of context. The ritual ensures:

- Nothing is lost between phases (artifact report)
- The next phase knows what is important and what is unknown (commit body and trailers)
- The phase boundary is detectable from git history alone (phase-end commit, trailers, and tag)
- The user is in control at every transition (explicit question)

It is verbose enough to be structured, but lightweight enough not to
slow the workflow down.

Between phase boundaries, the pre-commit hook enforces the
drift-critical graph invariants automatically. The full
[`/consistency-check`](../guides/consistency-check) run is an
explicit command; it is mandatory once per cycle before release
(security-audit Step 7 / Closing Handoff).

## Dialog handoffs, not blockers

Both inter-phase handoff documents (`architect-handoff.md` and
`plan-context.md`) carry structured questions for the receiving
skill. The receiving skill tries the agent-agent path first: it
self-answers from existing artifacts (BA, ADRs, FEATURE specs,
codebase). What it cannot resolve from artifacts gets bundled into a
single `AskUserQuestion` for the user. Coder questions travel via
BACKLOG-row notes or PR comments.

Pending questions never block unrelated work. Only the affected
ADR or feature waits. Other work continues with a `blocked-by` note
that cites the open question.

The seed format for the architect handoff lives in
[`skills/requirements-engineering/templates/ARCHITECT-HANDOFF-TEMPLATE.md`](https://github.com/pssah4/digital-innovation-agents/blob/main/skills/requirements-engineering/templates/ARCHITECT-HANDOFF-TEMPLATE.md).

## The trailer record replaces HANDOFFS.md

Earlier DIA versions appended every phase transition to an
append-only `_devprocess/context/HANDOFFS.md` log. Since v4, the
phase-end commit trailers ARE the transition record. The advantages:

- The record cannot drift from the commit it describes; they are the
  same object.
- It is machine-readable with plain git:
  `git log --format='%(trailers:key=DIA-Handoff,valueonly)'`.
- No extra file to keep in sync, no merge conflicts on a hot
  append-only log.

The canonical trailer spec lives in
[`skills/project-conventions/references/canonical-specs.md`](https://github.com/pssah4/digital-innovation-agents/blob/main/skills/project-conventions/references/canonical-specs.md)
under "Phase-end commit trailers".

**Legacy note:** existing `HANDOFFS.md` files stay untouched and are
skipped by tooling. [`/dia-realign`](../guides/dia-realign) offers a
deprecation header and an optional move to
`_devprocess/context/archive/HANDOFFS-legacy.md`; it never rewrites
or deletes entries.

## Integration with the guide

When `/dia-guide` runs, it reads the latest DIA trailers from git
history and uses them as input for the next-phase recommendation.
When a skill runs directly (without the guide), the ritual still
runs, and the next skill finds the context in the trailers and the
commit body when it is eventually invoked.

Both paths end up with the same artifacts and the same traceability.

## Rules for skills

Every phase skill (`/business-analysis`, `/requirements-engineering`,
`/architecture`, `/coding`, `/testing`, `/security-audit`,
`/dia-realign`) implements this ritual at the end. The ritual is
mandatory. The skill does not consider itself complete until the
ritual has run.

## See also

- [V-Model workflow guide](../guides/dia-guide): the guide
- [Artifacts reference](../reference/artifacts): the full artifact inventory
- [V-Model concept](./v-model): the cycle the rituals serve
