---
title: V-Model workflow guide
description: "The guide that helps users navigate the V-Model: state audit, next-phase recommendation, handoff completeness check, and the Closing Handoff after a successful security audit."
---

# V-Model workflow guide

`/dia-guide` is the navigational layer of DIA. It does not perform
CRUD work on artifacts. It reads project state, audits the last
handoff, recommends the next phase skill, and runs the Closing
Handoff after a successful security audit. Every concrete change
lives in the phase skill the guide dispatches to.

The phase skills (`/business-analysis`, `/requirements-engineering`,
`/architecture`, `/coding`, `/testing`, `/security-audit`) are
autonomous. They run their own triage, their own `/consistency-check`
mode A at phase end, and their own handoff ritual. The guide is the
on-demand orientation layer above them.

## When to use the guide

Use `/dia-guide` when:

- You are starting a new project and do not know which phase to
  begin with
- You want a status read of the current cycle ("where am I?")
- You finished a phase and want a recommendation for the next step
- You are unsure whether the last handoff was complete

Invoke a phase skill directly when:

- You know exactly which phase you need (for example, `/coding`
  because the design is finalised)
- You want to iterate inside one phase
- You are resuming a project mid-workflow without an orientation
  question

Both modes produce the same artifacts. The guide reduces friction
by reading the state and recommending; it does not block direct
phase-skill use.

## What the guide actually does

Three responsibilities, all on demand:

| Responsibility | Trigger | Output |
|---|---|---|
| Orientation interview | "Where do I start?" / "I am lost" | One recommended phase skill, with one or two alternatives, based on the state of `BACKLOG.md`, the latest `HANDOFFS.md` entry, and the current branch |
| Handoff audit | After any phase, on user request | Read of last `HANDOFFS.md` entry; check for required fields (`triage:`, `triage_kind:`, `epic:`, `feature:`); report any gap and name the responsible skill |
| Closing Handoff | After `/security-audit` returns green or yellow | Recommend `/consistency-check` mode B; on Release-Ready: yes, output the closing report and the `release-to-ba` template |

The guide does not write to artifacts. It reads, recommends, and
hands off.

## Phase 0: Artifact triage (delegated)

The artifact triage (FEAT / IMP / FIX / ADR) is owned by every
phase skill at its own entry. The guide does not run the triage; it
checks that the most recent handoff entry carries a `triage:` field
and reports the gap if missing.

Triage details live in [graph-invariants.md, section "Artifact
triage at entry point"](https://github.com/pssah4/digital-innovation-agents/blob/main/skills/project-conventions/references/graph-invariants.md).

## Hybrid entry-point detection

When invoked with an open question ("where do I start?"), the guide
scans project state and proposes an entry point. The user picks
from a clean menu:

```
A0) Continue current item (resume mid-cycle)
A)  Starting from scratch              -> /business-analysis
B)  Problem clear, need requirements   -> /requirements-engineering
C)  Requirements exist, need arch      -> /architecture
D)  Architecture ready                 -> /coding
E)  Implementation done                -> /testing
F)  Tests passed                       -> /security-audit
G)  Audit done                         -> Closing Handoff (consistency-check mode B + optional /release)
H)  Unsure                             -> short orientation interview
I)  Brownfield (existing code)         -> /reverse-engineering
```

The scan reads `BACKLOG.md`, the latest `HANDOFFS.md` entry, and
git phase-done tags. The recommendation is the proposed default;
the user can pick anything.

## The six phases plus Closing Handoff

```
Phase 1: /business-analysis          Problem exploration, ideation, validation
Phase 2: /requirements-engineering   Epics, FEAT-EE-FF, Success Criteria
Phase 3: /architecture               ADRs, arc42, wayfinder, plan-context.md
Phase 4: /coding                     Critical review, PLAN-NN, implementation, writeback
Phase 5: /testing                    Unit + integration tests, fix-loop
Phase 6: /security-audit             OWASP, SAST, SCA, Zero Trust
Closing Handoff (not a phase)        consistency-check mode B + optional release
```

Phase 1 starts on the left side of the V (design), descends to
Phase 4 (implementation) at the bottom, then climbs the right side
through Phase 5 and 6 (verification). The Closing Handoff is a
short orientation output, not a numbered phase.

## V-Model as a decision graph, not a straight path

The forward walk Phase 1 -> 6 is the default. Real projects
discover things mid-flight. Three mid-course triggers can pause a
phase skill and route work back:

- **Mid-course bug discovery** in `/coding`: triage, FIX backlog
  row, fix.
- **Mid-course design discovery** in `/coding`: amend or supersede
  the ADR, update arc42 and the wayfinder, then continue.
- **Mid-course requirements discovery** in `/architecture`: route
  back to `/requirements-engineering` for a FEAT update.
- **Mid-course capability discovery** in `/coding`: capture the
  capability gap as an ADR, route through `/architecture`, then
  continue.

The phase skills handle all four. The guide does not own iteration
logic; it just observes the state and recommends what to do next.

## Phase boundary mechanics (owned by phase skills)

The boundary mechanics live in the phase skills, not in the guide.
The guide only reads their output. Each phase skill runs at its end:

1. **`/consistency-check` mode A** on the changed artifacts:
   syntactic check for dead links, orphan refs, ID mismatches.
2. **4-part Handoff Ritual** (artifact report, handoff context in
   `HANDOFFS.md`, phase-end commit plus `tag-phase`, transition
   question). See [Handoff Rituals](../concepts/handoff-rituals).
3. **Plan-gate** (only at the start of `/coding`): SC coverage map,
   ADR alignment, codebase anchoring, verify commands ready. The
   plan must close every Critical ASR. This gate lives in the
   `/coding` entry block.

If a phase skill detects an issue at boundary, it reports and
pauses. The guide can be invoked next to reread state and
recommend a remediation step.

## GitHub flow.py integration

The phase skills coordinate with GitHub through
`tools/github-integration/flow.py`:

- `flow.py create-issue --item <ITEM-ID>`: create a tracking issue
  on phase entry
- `flow.py tag-phase --phase {ba|re|arch|plan|code|test|sec}`:
  attach a `<ITEM-ID>/<phase>-done` tag at every phase-end commit
- `flow.py ready-for-review`: convert draft PR to ready when the
  cycle reaches the Closing Handoff
- `flow.py claim --pair {pair-id}`: register the pair claim

The guide reads `flow.py status --item <ID>` for its state audit.
The local backlog row remains the source of truth; GitHub mirrors
it.

## Concurrent agent coordination

When multiple human-agent pairs work the same backlog, each pair
identifies itself with a pair-id (`{human-handle}-{model}`, for
example `seb-opus-4-7`) in the `Claim` column of `BACKLOG.md`.
Phase skills claim a row at start and release on phase end or
`Status: Done`. The backlog itself is the lock; there is no
central lock service.

## User Interaction Protocol

The guide follows three rules in user dialog:

1. **One question per turn.** No multi-question lists.
2. **Pro / Con framing for every decision option.** The user sees
   why each option exists and what it costs.
3. **AskUserQuestion for choices.** Free-form prompts only when
   the answer is genuinely open-ended.

## Closing Handoff

The Closing Handoff is a short guide output, not a phase. It fires
after `/security-audit` has produced a non-red verdict and the
fix-loop is closed.

Three steps:

1. **Suggest `/consistency-check` mode B** (semantic). Mode B
   confirms BA Validation is filled, all Feature/ADR statuses are
   final, arc42 reflects the actual decisions, and plan-context
   matches the real tech stack. Mode B returns a Release-Ready
   verdict.
2. **On Release-Ready: yes**: output the closing report (Feature /
   bug / security counts, finalised artifacts) plus the
   `release-to-ba` HANDOFFS template. The user can then run a
   private release skill (the public DIA plugin does not own a
   release mechanism, since release pipelines are project-specific).
3. **On Release-Ready: no**: name the responsible skill and the
   items to fix. Cycle closure resumes after the fix.

The Closing Handoff does not invoke any skill. It is a handoff
text the guide outputs and lets the user decide.

## Opt-out

The workflow is advisory, not enforcing. You can:

- **Leave the loop**: at any handoff, say "stop" or ask something
  unrelated. The workflow pauses immediately.
- **Temporarily disable the skills**: say "ignore the V-Model
  today" or "just help me with X without the workflow".
- **Permanently disable**: `/plugin disable digital-innovation-agents`
  in the Claude Code CLI removes the SessionStart hook entirely.

The workflow state is preserved in `_devprocess/` and in the git
phase-done tags. You can resume later by re-invoking
`/dia-guide`.

## Read the skill file

Want to see the exact instructions the agent follows?
[`skills/dia-guide/SKILL.md`](https://github.com/pssah4/digital-innovation-agents/blob/main/skills/dia-guide/SKILL.md)
on GitHub.

## What's next

- [Business Analysis guide](./business-analysis): Phase 1 detail
- [Coding guide](./coding): Phase 4 detail, the heart of the system
- [V-Model concept](../concepts/v-model): why this shape?
- [Handoff Rituals concept](../concepts/handoff-rituals): how
  transitions work
- [Consistency Check guide](./consistency-check): the boundary
  check that runs at every phase end
- [Three-layer documentation model](../concepts/three-layer-documentation):
  why state lives in the backlog row
- [Drift defense](../concepts/drift-defense): the full catalog of
  drift sources and how each is defended
