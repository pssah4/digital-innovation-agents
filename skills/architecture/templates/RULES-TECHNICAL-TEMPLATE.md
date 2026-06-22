<!-- See skills/architecture/SKILL.md for how to fill. Cap: 45 lines. -->

# Technical rules for {project-name}

Stable truths only. Module-specific details belong in module READMEs;
decisions belong in ADRs. See
skills/project-conventions/SKILL.md#canonical-specs (Writing style,
Three-layer model boundaries).

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

## Wayfinder

For "where does X live?": `grep "<concept>" src/ARCHITECTURE.map`, then
the entry-point's JSDoc header. This file is for stable rules, not
navigation.

<!-- Optional sections (add only when they carry decision content):
     ## Test patterns, ## Code quality. See skills/architecture/SKILL.md. -->
