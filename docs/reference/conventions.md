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
| Epic | `EPIC-{XXX}-{slug}.md` | `EPIC-001-ai-agent-core.md` |
| Feature | `FEATURE-{XXX}-{slug}.md` | `FEATURE-042-semantic-search.md` |
| ADR | `ADR-{XXX}-{slug}.md` | `ADR-003-embedding-provider.md` |
| Security Audit | `AUDIT-{PROJECT}-{YYYY-MM-DD}.md` | `AUDIT-obsilo-2026-03-22.md` |
| Handoff (RE -> Arch) | `architect-handoff.md` | Fixed name |
| Handoff (Arch -> Code) | `plan-context.md` | Fixed name |
| Backlog | `10_backlog.md` | Fixed name |
| Bug log | `20_bugs.md` | Fixed name (FIX-NN entries) |
| Handoffs log | `30_handoffs.md` | Fixed name (append-only) |

**Rules:**

- 3-digit numbers with leading zeros (`001`, `042`, not `1`, `42`)
- kebab-case slugs (`ai-agent-core`, not `aiAgentCore`)
- No spaces, no umlauts in filenames
- Dates as `YYYY-MM-DD`

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
