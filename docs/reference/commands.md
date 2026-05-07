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

## Activation

| Command | When to use |
|---|---|
| `/dia-setup` | First call in any new project. Writes `.dia/config.toml` with one of three modes (`off`, `git-only`, `github-sync`) and manages anchor blocks in agent files (`CLAUDE.md`, `AGENTS.md`, `GEMINI.md`, `.cursorrules`, `.github/copilot-instructions.md`, `.windsurfrules`). Re-run any time to change the mode or remove the anchors. |

See [dia-setup guide](../guides/dia-setup) and [Three modes](../concepts/three-modes).

## Guide and entry points

| Command | When to use |
|---|---|
| `/dia-guide` | Starting a new project, running the full cycle, or resuming an interrupted workflow. Drives phase transitions, mandatory phase-boundary consistency checks, GitHub flow.py integration, and ends with the Closing Handoff. |
| `/reverse-engineering` | Brownfield entry. Walks the V backwards over an existing codebase. Produces wayfinder, ADRs, arc42, FEAT inventory, backlog seed, evidence-based BA draft. Every claim sourced. |
| `/dia-migration` | Existing DIA users upgrading between versions (v1 -> v2 -> v3). Renames `FEATURE-NNNN` to `FEAT-EE-FF`, flattens analysis, regenerates the backlog, runs graph-health. Stage 5b migrates the BACKLOG status vocabulary to the GitHub-aligned set. Idempotent, branch-safe. |

See [V-Model workflow guide](../guides/dia-guide),
[Reverse Engineering guide](../guides/reverse-engineering), and
[DIA Migration guide](../guides/dia-migration).

## Phase skills (in V-Model order)

| Phase | Command | Purpose |
|---|---|---|
| 1 | `/business-analysis` | Exploration, Ideation, Validation. Produces the Project-BA `BA-{PROJECT}.md` (singleton, optional but recommended) plus one Item-BA per backlog item that needs discovery depth: `BA-EPIC-{nn}-{slug}.md` (mandatory before EPIC), `BA-FEAT-{ee}-{ff}-{slug}.md` (mandatory before FEAT), `BA-IMP-*.md` and `BA-FIX-*.md` (optional). All BAs live flat in `_devprocess/analysis/` and feed the EPIC/FEAT/IMP/FIX artefact via `ba-ref:` in the artefact frontmatter. |
| 2 | `/requirements-engineering` | Transforms BA into Epics, `FEAT-{ee}-{ff}` features, tech-agnostic Success Criteria, hypothesis statements as full prose. |
| 3 | `/architecture` | Creates ADRs (MADR) with the abstraction rule, arc42, `plan-context.md`. Maintains the wayfinder layer. |
| 4 | `/coding` | Critical review, PLAN-NN persistence with coverage gate, bug-capture entry, writeback to backlog and wayfinder. Bugs land as `FIX-{ee}-{ff}-{nn}` rows plus detail files. |
| 5 | `/testing` | Unit and integration tests with AAA, FIRST principles, coverage targets, fix-loop. |
| 6 | `/security-audit` | OWASP Top 10 + LLM Top 10 + SAST + SCA + Zero Trust. Two modes: per-item audit, periodic full-codebase audit on a `feature/audit-{date}` branch. |

Each phase skill ends with a **4-part Handoff Ritual**: artifact
report, handoff context appended to `HANDOFFS.md`, phase-end commit
(canonical `{type}({phase}): {ITEM-ID} {phase} complete`) plus
`tag-phase` followed by `sync-status`, transition question.

## flow.py subcommands (mode-aware GitHub integration)

`tools/github-integration/flow.py` is the team-collaboration driver.
It reads `.dia/config.toml` and skips GitHub-touching subcommands
when the mode is not `github-sync`. Skills call it during the
Handoff Ritual; you can also invoke it directly.

| Subcommand | What it does | Mode requirement |
|---|---|---|
| `create-issue --item ID` | Create a GitHub issue for the backlog item, add `gh project item-add` if `[github] project_number` is set in `.dia/config.toml` | `github-sync` |
| `tag-phase --item ID --phase PHASE` | Set the local annotated git tag `<id-lower>/<phase>-done`. Phases: `ba`, `re`, `arch`, `code`, `test`, `sec`, `ready-for-review`. Legacy `audit` accepted as alias for `sec` | `git-only` or `github-sync` |
| `sync-status --item ID` | Mirror BACKLOG Status to the GitHub issue state and the configured Project Status field; pull GitHub Assignee back into the BACKLOG Claim column. Clears Claim on `Done` or when no Assignee is set | `github-sync` |
| `promote-to-epic --item EPIC-NN [--rename-branch]` | After RE: rename the parent issue to `EPIC-NN: {title}`, create one sub-issue per FEAT and IMP under the EPIC, write a `## Sub-Issues` tasklist into the parent body, optionally rename the feature branch to `feature/epic-NN-<slug>` | `github-sync` |
| `open-draft-pr --item ID` | Open a draft PR against the configured `source_branch` (default `develop`) | `github-sync` |
| `ready-for-review --item ID [--with-sec]` | Verify the required phase tags are set (`code-done`, `test-done`, optionally `sec-done`); flip the draft PR to ready. Legacy `--with-audit` accepted as alias for `--with-sec` | `github-sync` |
| `validate-fix --item FIX-EE-FF-NN` | Hotfix-scoped consistency check: BACKLOG row exists with refs to parent FEAT, at least one commit on the branch cites the FIX-id, no orphan `FIXME(stub):` references the id, GitHub issue exists in `github-sync` | always |
| `status --item ID` | Print branch, phase tags, and GitHub issue state for the item | `git-only` or `github-sync` |

`validate-fix` always runs the local checks; the GitHub-side
issue check is gated on `github-sync`.

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
