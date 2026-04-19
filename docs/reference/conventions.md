---
title: Conventions
description: Naming rules, language conventions, commit style, and git workflow.
---

# Conventions

## File naming

| Artifact | Pattern | Example |
|---|---|---|
| Business Analysis | `BA-{PROJECT}.md` | `BA-obsilo.md` |
| Exploration Board | `EXPLORE-{PROJECT}.md` | `EXPLORE-obsilo.md` |
| Epic | `EPIC-{NNN}-{slug}.md` | `EPIC-001-ai-agent-core.md` |
| Feature | `FEATURE-{EPIC}-{NNN}-{slug}.md` | `FEATURE-001-001-semantic-search.md`, `FEATURE-013-002-reindex-job.md` |
| ADR | `ADR-{NNN}-{slug}.md` | `ADR-003-embedding-provider.md` |
| Security Audit | `AUDIT-{PROJECT}-{YYYY-MM-DD}.md` | `AUDIT-obsilo-2026-03-22.md` |
| Handoff (RE -> Arch) | `architect-handoff.md` | Fixed name |
| Handoff (Arch -> Code) | `plan-context.md` | Fixed name |
| Backlog | `10_backlog.md` | Fixed name |
| Bug log | `20_bugs.md` | Fixed name (FIX-NN entries) |
| Handoffs log | `30_handoffs.md` | Fixed name (append-only) |
| Signal layer | `40_metrics.md` | Fixed name (per METRICS-TEMPLATE.md) |

**Rules:**

- 3-digit numbers with leading zeros for Epics and ADRs
  (`001`, `042`, not `1`, `42`)
- Features are epic-scoped: `FEATURE-{EPIC}-{NNN}-{slug}.md`, where
  `EPIC` is the 3-digit parent epic number (identical to the epic's
  filename number) and `NNN` is the 3-digit feature counter local to
  that epic. Example: EPIC-001 gets FEATURE-001-001, FEATURE-001-002,
  ...; EPIC-013 gets FEATURE-013-001, ... The 3-digit-on-both-sides
  format keeps alphabetical sort order stable.
- kebab-case slugs (`ai-agent-core`, not `aiAgentCore`)
- No spaces, no umlauts in filenames
- Dates as `YYYY-MM-DD`
- Backlog follows the binding template at
  `skills/requirements-engineering/templates/BACKLOG-TEMPLATE.md` and
  is the single source of truth for project state

## Language

| Context | Language |
|---|---|
| Conversation with user | User's language (agent adapts automatically) |
| Commit messages | English, conventional prefixes |
| Private documentation (`_devprocess/`) | Matches user's language |
| Public documentation (`docs/`, README) | English |
| Code, identifiers, variables | English |
| Skill files (`SKILL.md`) | English |

The skill files are written in English so they are portable across
language contexts. The agent automatically switches to the user's
language in dialog.

## Bug IDs

- `FIX-NN`: bug ID with priority `P0` (immediate), `P1` (short-term), or `P2` (medium-term)
- Example: `FIX-042 (P1)`: Empty array causes null pointer in feature parser

Every bug found during `/coding` lands in `_devprocess/context/20_bugs.md`
with a causal chain (Problem, Root Cause, Chain of steps leading to
the error).

## Pair IDs (concurrent agent coordination)

When multiple human-agent pairs work the same backlog, each pair
identifies itself with a pair-id in the `Claim` column of
`10_backlog.md`:

- Format: `{human-handle}-{model}`
- Examples: `seb-opus-4-7`, `marie-sonnet-4-6`, `tom-codex`
- Claim cell value: `{pair-id} @ {YYYY-MM-DD}`, for example
  `seb-opus-4-7 @ 2026-04-19`
- Phase skills claim a row at start, release on phase end or `Status: Done`

The backlog itself is the lock. There is no central lock service.

## Security finding IDs

- `H-N` / `M-N` / `L-N`: High / Medium / Low severity
- Example: `H-3`: XSS vulnerability in user-controlled HTML rendering

## Commit style

Conventional commits with `Co-Authored-By Claude`:

```
feat: add X
fix: resolve Y
chore: prepare Z
docs: update readme
refactor: restructure W
```

Example from this repo:

```
feat: v2 skill content - handoff rituals, coding patterns, release closure

Phase 3 of the v2 rollout. The skill content is upgraded from v1
classic to v2, introducing mandatory handoff rituals, five task-level
patterns in /coding, ...

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
```

## Git workflow

- **Dual-remote**: private (origin, all branches) + public (only main)
- **Branch flow**: `feature/*` -> `dev` -> `main` -> `public/main`
- **Safe-merge**: merges to `dev` via `scripts/merge-to-dev.sh` (when available)
- **No interactive git commands**: no `git rebase -i`, no `git add -i`
- **Never amend published commits** without explicit user consent
- **Two-stage stripping** for public distribution: dev tooling first,
  then internal docs

## Plan structure

Every non-trivial plan follows the same structure:

1. **Context**: diagnostic, not descriptive. Root-cause analysis.
2. **Changes**: one subsection per file, BEFORE / AFTER code blocks
3. **File summary**: table (File | Change | Risk)
4. **Not affected**: explicit list of unchanged files (blast radius)
5. **Verification**: acceptance criteria, build always step 1

## See also

- [Artifacts](./artifacts): directory structure
- [Project Conventions guide](../guides/project-conventions)
