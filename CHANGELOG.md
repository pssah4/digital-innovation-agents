# Changelog

All notable changes to digital-innovation-agents are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

Work toward v2.0.0. See branch `main`.

### Added

- Claude Code plugin manifest (`.claude-plugin/plugin.json`)
- Claude Code plugin marketplace (`.claude-plugin/marketplace.json`) as `pssah4-skills`
- Cursor plugin manifest (`.cursor-plugin/plugin.json`)
- Codex install instructions (`.codex/INSTALL.md`, symlink-based)
- OpenCode plugin (`.opencode/plugins/digital-innovation-agents.js` + `INSTALL.md`)
- Gemini CLI extension (`gemini-extension.json` + `GEMINI.md`)
- SessionStart hook for Claude Code, Cursor, Copilot CLI (`hooks/hooks.json`,
  `hooks/hooks-cursor.json`, `hooks/session-start`, `hooks/run-hook.cmd`)
- Bootstrap skill `using-digital-innovation-agents` with advisory entry-points
  overview and explicit opt-out instructions (leave workflow, temporarily
  disable, permanently disable via `/plugin disable`)
- `CLAUDE.md` at repo root + `AGENTS.md` symlink (Codex convention)
- README with installation sections for Claude Code, Cursor, GitHub Copilot
  CLI, Codex, OpenCode, Gemini CLI, and GitHub Copilot Chat
- Auto-detect in `install-skills.sh` for v1 (`claude-code-skills/`) and v2
  (`skills/`) directory layout

### Changed

- Skills directory renamed from `claude-code-skills/` to `skills/` (Claude
  Code plugin convention). v1.0.0 tag remains unchanged with the old layout.
- `install-skills.sh` moved from `claude-code-skills/` to `scripts/`
- README installation section rewritten to cover all 7 supported platforms
- README file structure diagram updated to reflect v2 layout
- Removed obsolete "Migration notes: Copilot to Claude Code" section
  (both platforms are now supported in parallel)

### Note

v1.0.0 remains installable via `./scripts/install-skills.sh --version v1.0.0`
as a legacy snapshot. It is not available through the plugin marketplace.

## [1.0.0] - 2026-04-13

### Stabilization Release

First tagged release. Captures the V-Model Classic workflow as a frozen
reference point before the v2 restructuring begins.

### Features

- 8 Claude Code skills covering the full V-Model cycle:
  `project-conventions`, `business-analyse`, `requirements-engineering`,
  `architecture`, `coding`, `testing`, `security-audit`, `v-model-workflow`
- 3 innovation phases in `business-analyse`: Exploration, Ideation, Validation
- 20+ innovation methods with probing techniques (5-Why, Future Projection,
  Perspective Shift, Emotional Level, Analogy Trigger)
- Tech-agnostic success criteria enforcement in `requirements-engineering`
  with a forbidden-terms list
- Living documents pattern in `coding` skill (ADR/Feature writeback during
  and after implementation)
- OWASP Top 10 and OWASP LLM Top 10 coverage in `security-audit`
- GitHub Copilot agents mirror under `.github/` for non-Claude-Code users
- Shell-based installer: `./install-skills.sh`

### Support Policy

**v1.0.0 is frozen.** No further releases will be made on the v1 line.
Users requiring new features should use v2 (main branch). v1 remains
available as an unmaintained stable snapshot, installable via:

    ./install-skills.sh --version v1.0.0

[unreleased]: https://github.com/pssah4/digital-innovation-agents/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/pssah4/digital-innovation-agents/releases/tag/v1.0.0
