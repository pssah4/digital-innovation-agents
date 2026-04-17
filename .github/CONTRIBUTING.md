# Contributing to Digital Innovation Agents

Thanks for your interest in improving this project. This document outlines
how to contribute changes to the skills, docs, hooks, or CI.

## Ways to contribute

- **Report an issue** — bugs, unclear docs, missing platform support
- **Improve an existing skill** — tighter prose, better examples, fixed
  references
- **Add a new skill or phase artifact** — discuss first via an issue to avoid
  duplicated work
- **Docs** — VitePress pages under `docs/`, README, CHANGELOG
- **Tooling** — install script, hooks, CI

## Getting started

```bash
git clone https://github.com/pssah4/digital-innovation-agents.git
cd digital-innovation-agents
npm install         # VitePress docs
npm run docs:dev    # local docs at http://localhost:5173
```

The skills themselves are plain Markdown with YAML frontmatter and need no
build step — edit them directly under `skills/<phase>/SKILL.md`.

## Skill structure

Every skill lives in its own directory:

```
skills/<phase>/
├── SKILL.md          # required — frontmatter + body
├── references/       # optional — deep-dive material loaded on demand
└── templates/        # optional — artifact scaffolds
```

`SKILL.md` requires frontmatter with at least `name` and `description`.
`description` is the selector the model uses to decide when to invoke the
skill — keep it specific and trigger-rich.

```markdown
---
name: business-analyse
description: Use when the problem space is unclear …
---
```

Run the validator before opening a PR:

```bash
bash scripts/validate-skills.sh
```

CI runs the same validator plus link checks, JSON syntax validation, and
shellcheck on every PR.

## Commit messages

Follow the existing style visible in `git log`:

- `skills: …` — changes under `skills/`
- `docs: …` — docs, README, CHANGELOG
- `feat: …` — new capability
- `fix: …` — bugfix
- `chore(ci|deps): …` — tooling, dependencies

Keep subjects short, lowercase, imperative. Body explains the *why* when the
subject is not self-evident.

## Pull requests

1. Fork and create a topic branch off `main`.
2. Make your changes — small, focused PRs review faster than big ones.
3. Run local checks: `npm run docs:build`, `bash scripts/validate-skills.sh`.
4. Fill in the PR template (summary, scope, test plan).
5. Link related issues.

A maintainer will review. Expect discussion — skills are user-facing prose,
and wording matters.

## Scope boundaries

- **Stay focused.** Unrelated refactors belong in their own PR.
- **Respect `_devprocess/`.** User-project artifacts never land in this
  repo.
- **Advisory, not enforcing.** Skills should guide, not block, user
  workflows.

## Code of conduct

Be respectful, assume good intent, prefer concrete feedback over blanket
criticism. Harassment is not tolerated.

## License

By contributing, you agree that your contributions will be licensed under
the [MIT License](../LICENSE).
