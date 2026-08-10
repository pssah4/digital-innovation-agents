---
name: dia-bootstrap
description: Bootstrap context for the Digital Innovation Agents V-Model workflow. Auto-loaded at session start by the SessionStart hook (unless mode = off). Carries the entry-point catalog, the helper-script path resolution rule, the activation contract, and opt-out behaviour. The user does not invoke this skill manually.
---

# DIA Bootstrap

You have access to a structured V-Model workflow for AI-augmented
innovation and development, from business concept through requirements,
architecture, implementation, testing, and security audit.

## Helper script paths (binding for every phase skill)

Plugin helper scripts (`tools/github-integration/flow.py`,
`tools/dia-setup/anchor.py`, `tools/migration/*`,
`tools/consistency-check.py`, `scripts/*`) live in the plugin bundle,
NOT in the user project. Resolve every `tools/...` and `scripts/...`
path in skill text against the plugin root, in this priority:

1. `$DIA_PLUGIN_ROOT` (preferred; printed by the SessionStart hook)
2. `$CLAUDE_PLUGIN_ROOT` (Claude Code)
3. `$CURSOR_PLUGIN_ROOT` (Cursor)
4. Working directory (last resort, plugin checkout only)

Example: `python3 tools/github-integration/flow.py ...` expands to
`python3 "$DIA_PLUGIN_ROOT/tools/github-integration/flow.py" ...`.
If no variable resolves, surface a clear error and link the
[installation tutorial](https://pssah4.github.io/digital-innovation-agents/tutorials/installation).
Do not guess.

## Activation

No `.dia/config.toml` yet? Run `/dia-setup` first. It asks for the
mode (`off`: hooks silent, skills advisory only; `git-only`: local
commits, tags, merge scripts; `github-sync`: backlog mirrored to
GitHub issues via flow.py) and the profile (below), then writes the
config and the anchor blocks. Re-run `/dia-setup` any time.

## Profiles

`profile` in `.dia/config.toml` controls how much of the V-Model is
binding. A missing field means `full`.

- **`full`**: every phase skill is binding as written.
- **`lean`**: only durable decisions and stable navigation are
  binding: rules consolidated in AGENTS.md (CLAUDE.md stays a
  pointer), `_devprocess/SYSTEM-MAP.md` for code navigation, post-hoc
  ADRs (`kind: post-hoc`) behind `decisions/README.md` as a router
  table, and backlog state (GitHub Issues in `github-sync`, a thin
  BACKLOG.md in `git-only`). All other phase skills stay available as
  advisory tools; no gate blocks, no BA/FEATURE artifacts are
  required, handoffs reduce to phase-end commits with DIA trailers.
  Guiding rule in lean: never document what code, tests, git, PRs, or
  issues already carry.

## Entry points

- `/dia-setup` -- activation, mode/profile change, deactivation
- `/dia-guide` -- orientation and next-step recommendation (explicit
  user command)
- `/dia-realign` -- brownfield entry AND version upgrades: walks an
  existing codebase backwards into V-Model artifacts, migrates legacy
  DIA conventions
- `/business-analysis` -- problem exploration, ideation, validation
- `/requirements-engineering` -- epics, features, success criteria
- `/architecture` -- decisions (ADR), rules, navigation, plan-context
- `/coding` -- context handoff, critical review, implementation
- `/testing` -- unit and integration tests with fix-loop
- `/security-audit` -- OWASP, SAST, SCA, supply chain, Zero Trust
- `/consistency-check` -- artifact graph check (explicit user command;
  runs automatically only via the pre-commit hook and before release)
- `/project-conventions` -- structure and naming standards

These are suggestions, not rules. The user is in charge.

## Language in dialog

Skill content is English for portability. In dialog, always respond
in the user's language; artifacts follow the artifact-language rule
in `skills/project-conventions/references/canonical-specs.md`.

## Artifact locations

All project artifacts live under `_devprocess/` (full map:
`skills/project-conventions/references/directory-structure.md`).
State lives in `_devprocess/context/BACKLOG.md`; phase transitions
live in DIA commit trailers.

## Opting out

The skill set is advisory. If the user says "stop", "exit", asks an
unrelated question, or opts out ("no skills for this", "ignore
V-Model today"): exit the workflow immediately, answer directly, do
not push back, do not suggest re-enabling. State is preserved under
`_devprocess/`; `/dia-guide` resumes later. Permanent disable:
`/plugin disable digital-innovation-agents` (mention only if asked).

## Principles

- Living documents: every phase writes back into its source artifacts
- Tech-agnostic success criteria; technology belongs in NFRs
- Quality gates: each skill verifies its own output before handoff
- User in control: propose and confirm, never generate autonomously
- Advisory, not enforcing

## User Interaction Protocol (binding)

One question per turn. Use `AskUserQuestion`. Every option carries
`+ Pro:` and `- Con:` lines. Recommended option first, labelled
"(Recommended)". No dealer's-choice framing. Full protocol:
`skills/project-conventions/references/user-interaction-protocol.md`.
