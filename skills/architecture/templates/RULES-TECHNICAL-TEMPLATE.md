<!--
Instructions for the agent: produce this file as
`_devprocess/rules/technical.md`. Write the prose in the user's working
language. Keep keywords (Stack, Build, Test, Lint, etc.) in English so
the file greps consistently across projects.

Hard cap: 150 lines. Only what an agent MUST know to write correct
code in this project. Module-specific details go into module READMEs,
not here. Architecture decisions go into ADRs, not here.

If the file grows beyond 150 lines, the rule is too detailed and
belongs in code (linter rule, type constraint, test) or in an ADR.
-->

# Technical rules for {project-name}

> Max 150 lines. Stable truths only. Edits happen during /architecture
> and /coding when a rule changes meaning. Updates flow back through
> the writeback loop, not by drift.

## Stack

- Language: {e.g. TypeScript strict}
- Framework: {e.g. Electron + React 18}
- Database: {e.g. better-sqlite3}
- Build: {e.g. Vite 7}
- Tests: {e.g. Vitest}
- Lint: {e.g. ESLint + Prettier}

## Commands

```bash
{cmd:dev}        # Dev server / watch mode
{cmd:build}      # Production build
{cmd:test}       # Run tests
{cmd:lint}       # Linting
{cmd:typecheck}  # Type-check
```

## Conventions

- {one rule, e.g. "Functional components and hooks only."}
- {one rule, e.g. "Named exports, PascalCase for components."}
- {one rule, e.g. "Conventional Commits: feat:, fix:, refactor:, chore:."}

## Code quality

- Fix errors at the root, do not silence them with eslint-disable.
- For unfamiliar APIs: read the docs, do not guess.
- No silent data loss (DROP COLUMN, schema rewrites, etc.) without
  explicit user approval.

## Test patterns

- {one rule, e.g. "Integration tests primary, unit tests secondary."}
- {one rule, e.g. "Mocks: only external services, never internal modules."}
- {one rule, e.g. "Coverage threshold: 30% lines, 35% functions."}

## Wayfinder

For "where does X live?" questions: `grep "<concept>" src/ARCHITECTURE.map`
first, then the entry-point's JSDoc header. This file is for stable
rules, not navigation.
