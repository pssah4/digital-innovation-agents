---
title: Versioning Policy
description: What counts as a breaking, additive, or cosmetic change to the Digital Innovation Agents skill set.
---

# Versioning Policy

This project follows [Semantic Versioning](https://semver.org/): the
public version is `MAJOR.MINOR.PATCH`. For a skill set, "public API"
means more than code. It includes skill names, command names, the
artifact contract, and the shape of the frontmatter.

## What counts as the public surface

| Surface | Example | Why it matters |
| --- | --- | --- |
| Skill names (directory names) | `/business-analyse`, `/architecture` | Users type these; install scripts pin these |
| Skill `name` in frontmatter | `name: business-analyse` | Platforms route by this |
| Produced artifact paths | `_devprocess/01_business-analysis/BA-*.md` | Downstream skills read these |
| Template filenames | `EPIC-TEMPLATE.md`, `FEATURE-TEMPLATE.md` | Users fork these into projects |
| Plugin manifest schema | `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json` | Plugin marketplaces parse these |
| CLI surface of `scripts/install-skills.sh` | flag names, exit codes | Users script around these |

Everything else -- internal prose, wording of a `description`,
references/ layout, commit messages -- is not part of the public
surface. Change it freely.

## Change classes

### MAJOR -- breaking

Bump `MAJOR` when existing users have to change something. Examples:

- Rename or remove a skill (`/business-analyse` -> `/discovery`)
- Rename or remove a command (`/v-model-workflow` -> `/v-workflow`)
- Change the required frontmatter shape (rename `description` -> `summary`)
- Move or rename a produced artifact (`BA-{PROJECT}.md` -> `business-analysis.md`)
- Remove a template
- Remove a CLI flag or change its semantics
- Change the installation target directory
- Drop support for a platform (Cursor, Codex, Gemini, Copilot, OpenCode)

A MAJOR bump requires a migration note in `CHANGELOG.md` with
before/after examples.

### MINOR -- additive

Bump `MINOR` when behaviour expands but nothing existing breaks.
Examples:

- Add a new skill
- Add a new command
- Add a new optional frontmatter field (e.g. `depends_on`)
- Add a new CLI flag with a safe default
- Add a new template file
- Add a new platform manifest
- Add a new artifact that nothing currently relies on

### PATCH -- cosmetic or internal

Bump `PATCH` for changes users are unlikely to notice. Examples:

- Rewrite of a skill `description` that preserves triggers
- Typo fixes, grammar, markdown formatting
- Expand a reference or template body without changing its name
- Internal refactor of scripts, CI, hooks
- Docs-only changes under `docs/`
- New CI job, updated linter config

## Ambiguous cases

**"I reworded the description to trigger better."** PATCH if the new
wording is a superset of the old triggers (same keywords plus some
extras). MINOR if it removes triggers users might have learned to rely
on. MAJOR if you also renamed the skill.

**"I moved content from `SKILL.md` to `references/`."** PATCH. The
referenced file paths are not part of the public surface.

**"I added a new optional frontmatter field."** MINOR. Existing skills
that do not use it keep working.

**"I tightened the validator and existing skills now fail."** MAJOR if
the validator is part of CI and blocks merges; PATCH if it only warns.
Either way, call it out in the PR.

**"I added a step to the v-model-workflow orchestrator."** MINOR if
the new step is optional or auto-detected; MAJOR if it changes the
order of existing steps or requires new input.

## Release cadence

This project does not pre-commit to a release cadence. Releases happen
when there is either (a) a batch of additive or cosmetic changes worth
tagging, or (b) a single breaking change that needs a clean boundary.

Pre-release markers (`-rc1`, `-beta.1`) are welcome for breaking
changes -- they let early adopters test before the boundary moves.

## The `CHANGELOG.md` contract

Every PR that touches the public surface should add an entry to
`CHANGELOG.md` under `## Unreleased`. Each release moves that block
under a dated heading.

Entry format:

```markdown
### Breaking
- Renamed `/business-analyse` to `/discovery`
  (migration: update any scripts that call `/business-analyse`)

### Added
- New `depends_on` frontmatter field on skills

### Changed
- `install-skills.sh` now asks for confirmation before overwrite

### Fixed
- ...
```

Short over lyrical. One line per change, with a parenthetical migration
note when relevant.
