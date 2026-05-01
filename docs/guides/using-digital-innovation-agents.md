---
title: Using Digital Innovation Agents
description: The orientation skill that loads automatically on session start. Introduces the V-Model skill set, entry points, and opt-out behaviour.
---

# Using Digital Innovation Agents

`using-digital-innovation-agents` is the orientation skill. It
loads **automatically at session start** via the SessionStart hook
and gives the agent a brief introduction to the workflow on every
new session. You do not invoke it manually.

The skill exists for two reasons:

- **Discoverability.** A new user types nothing special and the
  agent already knows there is a V-Model available, what the
  entry points are, and how to opt out.
- **Boundary safety.** The skill makes the workflow advisory.
  Without it, the agent might push the workflow even when the
  user just wants a quick edit. With it, the agent asks first
  and respects opt-out language.

## What the agent learns at session start

### The skill catalog

The agent learns it has access to thirteen skills, grouped into
guide, brownfield entry, V-Model phase skills, and
foundation skills. The full list is in
[Commands](../reference/commands).

### When to invoke which skill

| User context | Suggested entry |
|---|---|
| Starting something new, problem space unclear | `/dia-guide` |
| Existing codebase, no V-Model artifacts | `/reverse-engineering`, then `/business-analysis` for the WHY |
| Existing DIA project on v1 or v2 | `/dia-migration` |
| Clear problem, no solution yet | `/business-analysis` |
| Features defined, no architecture | `/architecture` |
| Ready to implement | `/coding` |
| A bug surfaced outside an active cycle | `/coding` (bug-capture entry) |

These are **suggestions**, not rules. The user is in charge.

### Language adaptation

Skill content is written in English so it is portable. The agent
**always responds in the user's language**. German user, German
reply. Spanish user, Spanish reply. Skill instructions stay
English internally; user-facing messages adapt automatically.

### Artifact locations

Project artifacts live under `_devprocess/`:

- `_devprocess/analysis/` for BA, EXPLORE, RESEARCH, AUDIT,
  EPIC-NN-ba (flat, no subfolders except `sources/`)
- `_devprocess/requirements/` for epics, features, fixes,
  improvements, handoff
- `_devprocess/architecture/` for ADRs and arc42
- `_devprocess/rules/` for stable rule sets (technical, design,
  domain)
- `_devprocess/implementation/plans/` for PLAN-NN files
- `_devprocess/context/` for `BACKLOG.md` (single source of truth
  for state), `HANDOFFS.md`, `METRICS.md`
- `src/ARCHITECTURE.map` for the wayfinder root
- `src/{module}/README.md` for module wayfinders

See [Artifacts](../reference/artifacts) for the full directory
tree.

## Opt-out behaviour

The skill set is **advisory**. The user can leave the workflow at
any time, and the agent respects that immediately.

### Leaving a `/dia-guide` loop mid-cycle

User says "stop", "exit", "I want to do something else", "let's
pause this", or asks an unrelated question:

- The agent exits the workflow immediately.
- No "are you sure?" pushback.
- Answers the next question directly, without invoking any
  V-Model skill.
- Workflow state stays in `_devprocess/` and in the git
  phase-done tags. The user can resume later by re-invoking
  `/dia-guide`.

### Temporarily disabling

User says "ignore V-Model today", "I just want a quick fix", "no
skills needed for this", "just help me with X without the
workflow":

- The agent does **not** invoke any skill, even when the task
  matches a skill description ("fix this bug" would normally
  match `/coding`).
- Plain mode, like any normal Claude Code session without the
  plugin.
- The agent does not remind the user that the skills exist or
  suggest re-enabling.
- The opt-out stays in effect until the user explicitly ends it
  or a new session starts.

### Permanently disabling

In the Claude Code CLI:

```
/plugin disable digital-innovation-agents
```

This removes the SessionStart hook entirely. The skill mentions
this command only when the user asks how to disable permanently.

## User Interaction Protocol

The orientation skill teaches every phase skill the same dialog
rules:

1. **One question per turn.** Never batch decisions.
2. **Use `AskUserQuestion` for choices.** Free-form prose only
   for quick factual confirmations.
3. **Each option carries an explicit Pro and Con line.** The
   user sees both sides at a glance.
4. **Mark the recommended option as the first entry** with
   "(Recommended)". If the rationale is not obvious from the
   Pros / Cons, the agent adds a one-line "Empfehlung: ...
   weil ..." sentence before the question.
5. **No "dealer's choice" framing.** If the agent has no
   preference, it says so explicitly.

These rules bind across every phase skill, regardless of project
language.

## Principles

- **Living documents.** Every phase writes back into its source
  artifacts so documentation reflects the current state. State
  goes through the backlog row first.
- **Tech-agnostic success criteria.** No OAuth, REST, or
  PostgreSQL in Success Criteria. Technology details belong in
  Technical NFRs.
- **Quality gates.** Each skill verifies its own output before
  handoff. `/consistency-check` Mode A runs at every phase
  boundary.
- **User in control.** No autonomous generation, always propose
  and confirm.
- **Advisory, not enforcing.** If the user doesn't want the
  workflow, the agent doesn't force it.

## Scope adaptation

The workflow adapts to project scope:

- **Simple Test / Feature** (hours to 1 to 2 days): minimal
  exploration, skip validation, focus on definition of done.
- **Proof of Concept** (1 to 4 weeks): shortened exploration,
  full ideation, hypothesis-driven validation.
- **Minimum Viable Product** (2 to 6 months): full exploration,
  full ideation, complete market assessment.

`/business-analysis` asks which scope applies at the start and
calibrates depth accordingly.

## Read the skill file

[`skills/using-digital-innovation-agents/SKILL.md`](https://github.com/pssah4/digital-innovation-agents/blob/main/skills/using-digital-innovation-agents/SKILL.md)
on GitHub.

## See also

- [V-Model workflow guide](./dia-guide): the guide
  the orientation skill points to first
- [Commands reference](../reference/commands): every slash-command
  in one table
- [Installation tutorial](../tutorials/installation): how to
  install the plugin so the SessionStart hook fires
