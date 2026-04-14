---
title: V-Model workflow
description: The orchestrator that guides projects through all 7 V-Model phases, with phase transitions and Release Closure.
---

# V-Model workflow

`/v-model-workflow` is the orchestrator. It drives projects through
all 7 V-Model phases, manages the handoffs between phase skills, and
ends with Phase 7 Release Closure.

## When to use the orchestrator

Use `/v-model-workflow` when:

- You are starting a new project and do not know which phase to begin with
- You want the full cycle without manually invoking each phase skill
- You are unsure where you are in the V-Model and need an orientation
- You want automatic phase transitions (the orchestrator asks before
  each transition, but defaults to "yes" when you agree)

Invoke a phase skill directly when:

- You know exactly which phase you need (for example, `/coding` because
  everything upstream is done)
- You want to iterate on one phase multiple times without moving on
- You are resuming a project mid-workflow

Both modes produce the same artifacts. The orchestrator just reduces
friction by handling transitions for you.

## The 7 phases

```
Phase 1: /business-analyse          Problem exploration, ideation, validation
Phase 2: /requirements-engineering  Epics, Features, Success Criteria
Phase 3: /architecture              ADRs, arc42, plan-context.md
Phase 4: /coding                    Critical review, implementation, writeback
Phase 5: /testing                   Integration tests, fix-loop
Phase 6: /security-audit            OWASP, SAST, SCA
Phase 7: Release Closure            Finalization, release notes, CHANGELOG
```

Phase 1 starts on the left side of the V (design), descends to Phase 4
(implementation) at the bottom, then climbs the right side through
Phase 5 and 6 (verification), and ends with Phase 7 (release closure).

## Orchestrated phase transitions

Every phase skill ends with a mandatory Handoff Ritual in 3 parts:

1. **Artifact report**: what was produced, with file paths
2. **Handoff context**: appended to `_devprocess/context/30_handoffs.md`
   with open questions, assumptions, and next-phase inputs
3. **Transition question**: "Start `/<next-skill>` now, or review first?"

When running inside `/v-model-workflow`, the orchestrator reads the
handoff context and launches the next skill automatically. Every
transition needs either an implicit "yes" (you say "go", "next",
"continue") or an explicit approval. You can always opt out: "stop",
"I want to check first", or simply asking an unrelated question
pauses the workflow.

No endless loops. The orchestrator respects user control at every step.

## When to invoke `/v-model-workflow` directly

Type `/v-model-workflow` when you want to enter the workflow at a
specific phase. The orchestrator asks:

```
V-Model Workflow: where are you?

A) Starting from scratch             -> /business-analyse
B) Problem clear, need requirements  -> /requirements-engineering
C) Requirements exist, need arch     -> /architecture
D) Architecture ready                -> /coding
E) Implementation done               -> /testing
F) Tests passed                      -> /security-audit
G) Audit done                        -> Phase 7 Release Closure
H) Unsure                            -> short orientation interview
```

Pick the option matching your state. The orchestrator picks up where
you are and drives the remainder of the cycle.

## Opt-out

The workflow is advisory, not enforcing. You can:

- **Leave the loop**: at any handoff, say "stop" or ask something
  unrelated. The workflow pauses immediately. No "are you sure?"
  pushback.
- **Temporarily disable the skills**: say "ignore the V-Model today"
  or "just help me with X without the workflow". The agent works in
  plain mode without invoking any phase skill.
- **Permanently disable**: `/plugin disable digital-innovation-agents`
  removes the SessionStart hook entirely.

The workflow state is preserved in `_devprocess/`. You can resume
later by re-invoking `/v-model-workflow`.

## Phase 7: Release Closure

Phase 7 is the final phase that closes the cycle. The orchestrator
runs 5 steps automatically:

1. **Final artifact synchronization** across all phases: BA, Features,
   ADRs, arc42, plan-context all reflect the actual implemented state
2. **Generate release notes** from implemented features, fixed bugs
   (`20_bugs.md`), security findings, breaking changes
3. **Update CHANGELOG**: move `[Unreleased]` to `[{version}] - {date}`,
   decide semver bump (patch/minor/major)
4. **Backlog cleanup**: open bugs referenced, future ideas captured
5. **Closing report** to the user with a full cycle summary

The result is a release-ready state with documentation that matches
the code.

## Read the skill file

Want to see the exact instructions the agent follows?
[`skills/v-model-workflow/SKILL.md`](https://github.com/pssah4/digital-innovation-agents/blob/main/skills/v-model-workflow/SKILL.md)
on GitHub.

## What's next

- [Business Analysis guide](./business-analyse): Phase 1 detail
- [Coding guide](./coding): Phase 4 detail, the heart of the system
- [V-Model concept](../concepts/v-model): why this shape?
- [Handoff Rituals concept](../concepts/handoff-rituals): how transitions work
