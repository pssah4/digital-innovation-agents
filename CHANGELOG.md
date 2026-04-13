# Changelog

All notable changes to digital-innovation-agents are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

Work toward v2.0.0. See branch `main`.

### Added (Phase 3 -- v2 Content)

- **`/coding` skill**: five new sub-phases that brief the Default Claude
  Code agent with precise guidelines -- 3a Task-breakdown guidelines,
  3b optional TDD mode, 3c Debugging protocol with 4-phase root-cause
  process and "architecture alarm" after 3+ failed fixes, 4a Verification
  gate before completion, 4b Regression test cycle for bug fixes.
  Phase 1 (Load context), Phase 2 (Critical review), Phase 4 (Final
  synchronization) remain unchanged as the v1 differentiators.
- **`/testing` skill**: new section "Role alongside TDD" clarifying that
  Integration tests are the primary focus, unit-test gaps secondary, and
  coverage check tertiary. Fallback mode remains for runs where TDD was
  not active.
- **`/v-model-workflow` skill**: new "Orchestrated Phase Transitions"
  section driving phase handoffs actively, and a new **Phase 7: Release
  Closure** that finalizes artifacts, generates release notes, updates
  CHANGELOG, and cleans the backlog.
- **All 6 phase skills** (business-analyse, requirements-engineering,
  architecture, coding, testing, security-audit): mandatory 3-part
  Handoff Ritual at end of phase -- Artifact report, Handoff context
  (appended to `30_handoffs.md`), Explicit transition question.
- **`_devprocess/context/20_bugs.md`**: new file convention for the
  FIX-NN bug log, maintained by `/coding` Phase 3c.
- **`_devprocess/context/30_handoffs.md`**: new file convention for the
  append-only phase handoffs log, written by each phase skill.
- **`using-digital-innovation-agents`**: new "Language in dialog" section
  -- skill content is English, user-facing dialog adapts to user's
  language automatically.

### Changed (Phase 3)

- All 6 German skill files translated to English for portability and
  consistency with `plugin.json`, README, CHANGELOG: `coding`, `testing`,
  `architecture`, `security-audit`, `v-model-workflow`, `project-conventions`.
- `project-conventions/SKILL.md`: dateinamen table extended with
  `20_bugs.md` and `30_handoffs.md` entries; new "The `_devprocess/context/`
  files" section explains the three living logs.
- `business-analyse/SKILL.md` and `requirements-engineering/SKILL.md`
  (already English): existing "Handoff" section replaced by the new
  3-part Handoff Ritual.

### Added (Phase 2 -- Multi-Platform Plugin Infrastructure)

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
