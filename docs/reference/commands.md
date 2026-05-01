---
title: Commands
description: Complete list of commands that Digital Innovation Agents provides.
---

# Commands

All commands work the same way across Claude Code (CLI), Cursor,
Codex, OpenCode, Gemini CLI, and GitHub Copilot. Type `/` in your
coding tool to see autocomplete suggestions. The thirteen skills
group into guide, brownfield entries, V-Model phase skills,
and foundation skills.

## Guide and entry points

| Command | When to use |
|---|---|
| `/dia-guide` | Starting a new project, running the full cycle, or resuming an interrupted workflow. Drives phase transitions, mandatory phase-boundary consistency checks, GitHub flow.py integration, and ends with the Closing Handoff. |
| `/reverse-engineering` | Brownfield entry. Walks the V backwards over an existing codebase. Produces wayfinder, ADRs, arc42, FEAT inventory, backlog seed, evidence-based BA draft. Every claim sourced. |
| `/dia-migration` | Existing DIA users upgrading between versions (v1 -> v2 -> v3). Renames `FEATURE-NNNN` to `FEAT-EE-FF`, flattens analysis, regenerates the backlog, runs graph-health. Idempotent, branch-safe. |

See [V-Model workflow guide](../guides/dia-guide),
[Reverse Engineering guide](../guides/reverse-engineering), and
[DIA Migration guide](../guides/dia-migration).

## Phase skills (in V-Model order)

| Phase | Command | Purpose |
|---|---|---|
| 1 | `/business-analysis` | Exploration, Ideation, Validation. Produces `BA-{PROJECT}.md`, optional `EPIC-{nn}-ba.md` per epic, the HMW question. |
| 2 | `/requirements-engineering` | Transforms BA into Epics, `FEAT-{ee}-{ff}` features, tech-agnostic Success Criteria, hypothesis statements as full prose. |
| 3 | `/architecture` | Creates ADRs (MADR) with the abstraction rule, arc42, `plan-context.md`. Maintains the wayfinder layer. |
| 4 | `/coding` | Critical review, PLAN-NN persistence with coverage gate, bug-capture entry, writeback to backlog and wayfinder. Bugs land as `FIX-{ee}-{ff}-{nn}` rows plus detail files. |
| 5 | `/testing` | Unit and integration tests with AAA, FIRST principles, coverage targets, fix-loop. |
| 6 | `/security-audit` | OWASP Top 10 + LLM Top 10 + SAST + SCA + Zero Trust. Two modes: per-item audit, periodic full-codebase audit on a `feature/audit-{date}` branch. |

Each phase skill ends with a **4-part Handoff Ritual**: artifact
report, handoff context appended to `HANDOFFS.md`, phase-end commit
(canonical `{type}({phase}): {ITEM-ID} {phase} complete`) plus
`tag-phase` call, transition question.

## Foundation skills

| Command | When to use |
|---|---|
| `/project-conventions` | Initializing a new project, checking the three-layer documentation model, or verifying directory and naming conventions. Referenced by all other skills. |
| `/consistency-check` | Verifying the V-Model artifact graph at phase boundaries. Mode A (syntactic: links, IDs, refs), Mode B (semantic via agent), Mode C (full). Mandatory at every phase end and before release. |
| `/humanizer` | Stripping AI vocabulary, em dashes, negative parallelisms, and filler from any artifact. Enforces sentence case and active voice. |

## Orientation skill

The `using-digital-innovation-agents` skill loads automatically at
session start via the SessionStart hook. You do not invoke it
manually. It gives the agent a brief orientation of the workflow on
every new session, including entry points and opt-out behaviour.

## Opt-out language

The workflow is advisory. To leave mid-cycle or disable temporarily:

| User says | Effect |
|---|---|
| "stop" / "exit" / "I want to do something else" | Exit the current workflow loop, answer unrelated questions in plain mode |
| "ignore the V-Model today" / "just help me with X" | Temporarily disable the skills for this session |
| `/plugin disable digital-innovation-agents` | Permanently disable the plugin (Claude Code CLI only) |

See [Installation tutorial](../tutorials/installation) for initial setup
and [Troubleshooting](./troubleshooting) for common issues.
