---
title: Commands
description: Complete list of commands that Digital Innovation Agents provides.
---

# Commands

All commands work the same way across Claude Code, Cursor, Codex,
OpenCode, Gemini CLI, and GitHub Copilot. Type `/` in your coding tool
to see autocomplete suggestions.

## Orchestrator

| Command | When to use |
|---|---|
| `/v-model-workflow` | Starting a new project, running the full cycle, or resuming an interrupted workflow. The orchestrator drives phase transitions and ends with Phase 7 Release Closure. |

See [V-Model workflow guide](../guides/v-model-workflow).

## Phase skills (in V-Model order)

| Phase | Command | Purpose |
|---|---|---|
| 1 | `/business-analyse` | Exploration, Ideation, Validation. Produces `BA-{PROJECT}.md` and the HMW question. |
| 2 | `/requirements-engineering` | Transforms BA into Epics, Features, tech-agnostic Success Criteria. |
| 3 | `/architecture` | Creates ADRs (MADR), arc42, `plan-context.md`. |
| 4 | `/coding` | Critical review, implementation briefing with 5 sub-phase patterns, writeback to artifacts. |
| 5 | `/testing` | Integration tests, unit-test gaps, fix-loop. |
| 6 | `/security-audit` | OWASP Top 10 + LLM Top 10 + SAST + SCA + Zero Trust. |

Each phase skill ends with a **3-part Handoff Ritual** (artifact report,
handoff context appended to `30_handoffs.md`, transition question).

## Foundation skill

| Command | When to use |
|---|---|
| `/project-conventions` | Initializing a new project or checking directory / naming conventions. Referenced by all other skills. |

## Bootstrap skill

The `using-digital-innovation-agents` skill is loaded automatically at
session start via the SessionStart hook. You don't invoke it manually --
it provides the agent with an orientation of the workflow on every new
session.

## Opt-out language

The workflow is advisory. To leave mid-cycle or disable temporarily:

| User says | Effect |
|---|---|
| "stop" / "exit" / "I want to do something else" | Exit the current workflow loop, answer unrelated questions in plain mode |
| "ignore the V-Model today" / "just help me with X" | Temporarily disable the skills for this session |
| `/plugin disable digital-innovation-agents` | Permanently disable the plugin (standard Claude Code plugin management) |

See [Installation tutorial](../tutorials/installation) for initial setup
and [Troubleshooting](./troubleshooting) for common issues.
