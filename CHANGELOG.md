# Changelog

All notable changes to digital-innovation-agents are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [2.1.0] - 2026-04-19

Minor release. Brownfield entry point, method-proposal protocol across
BA and RE, binding User Interaction Protocol, mid-course bug trigger in
`/coding`, canonical writing style for every artifact, and a complete
VitePress landing-page overhaul with a handcrafted V-Model SVG.

### Added (Skills)

- New `/reverse-engineering` skill as the brownfield entry point into
  the V-Model workflow. Walks the V backwards over an existing
  codebase and produces `plan-context.md`, ADRs (`Status: Inferred`),
  an arc42 snapshot, a FEATURE inventory (`Status: Observed`), a seed
  of backlog entries, and an evidence-based BA draft (`Status: Draft`)
  with strict anti-hallucination rules: every claim carries a
  `Source:` reference, placeholders replace guesses, personas are
  never invented from code structure.
- `/business-analyse` Phase 0 (Existing BA Detection) preflight. When
  a draft BA exists, the skill enters Validation Mode and walks
  section by section, confirming evidence-backed claims and filling
  `[NEEDS USER INPUT]` placeholders via the normal interview. On
  success it promotes the BA from `Status: Draft` to `Status: Validated`.
- `/v-model-workflow` entry option A0 for brownfield projects, plus a
  new "Reverse Engineering -> Business Analysis" transition that
  always routes through `/business-analyse` to validate the WHY
  before the forward walk resumes.
- Explicit method-proposal protocol in `/business-analyse` and
  `/requirements-engineering`: when user answers go generic or
  sections lack evidence, the skill stops the interview and proposes
  the matching method from `skills/business-analyse/references/innovation-methods.md`,
  always linked to its user-facing docs card.
- Mid-course bug discovery trigger in `/coding`: when a new bug
  surfaces during implementation, the flow pauses, routes through
  BUG-NNN / FEATURE-NNNN / ADR-amendment triage, writes a root-cause
  analysis, adds a backlog entry BEFORE the fix, and cites both items
  in the commit message (`Refs: FEATURE-0507, BUG-018`).
- Per-commit backlog writeback gate in `/coding`: the backlog MUST
  reflect the post-implementation state before every commit that
  references a FEATURE-NNNN or BUG-NNN. Stricter than end-of-phase
  writeback to prevent drift across long phases.
- Binding User Interaction Protocol in `/using-digital-innovation-agents`
  and `/v-model-workflow`: one question per turn, use
  `AskUserQuestion`, every option carries a labelled Pro and Con, the
  recommended option is the first entry with "(Recommended)", no
  dealer's choice framing.
- Canonical "Writing style for every artifact" guide in
  `/project-conventions`. Zero em dashes (U+2014), no en dashes
  (U+2013), no double-hyphen substitute, no AI vocabulary, no
  negative parallelisms, no rule-of-three padding, sentence-case
  headings, active voice, grep-before-save rule. Every phase-skill
  now carries a pointer block to this canonical section.

### Added (Documentation)

- VitePress landing page overhaul: handcrafted V-Model SVG with six
  clickable phase boxes (Business Analysis, Requirements Engineering,
  Architecture, Coding, Testing, Security Audit), method pills above
  each phase, artifact cards below, handoff arrows between phases,
  dashed loops for test fix / security fix / living-documents
  writeback. Three-zone palette with petrol/pink/indigo gradient.
- Method-catalog pages for Discovery, Ideation, and Validation under
  `docs/reference/methods-*.md`, each with a user-facing card for
  every method referenced by the BA and RE skills.
- Dedicated reverse-engineering guide with an expanded methodology
  chapter.
- About page with Sebastian Hanke bio and Buy Me A Coffee sponsorship;
  refreshed README and Security Audit section in the landing diagram.

### Changed

- Templates de-em-dashed throughout (`BA-TEMPLATE.md`,
  `EXPLORATION-BOARD.md`, `BACKLOG-TEMPLATE.md`, `EPIC-TEMPLATE.md`,
  `FEATURE-TEMPLATE.md`, `AUDIT-TEMPLATE.md`). Prose uses commas,
  periods, parentheses, or colons instead of em dashes.
- Bash command permissions in `.claude/settings.json` expanded for
  the reverse-engineering and documentation workflows.

### Fixed

- SVG layout across multiple iterations: phase alignment, orthogonal
  fix loops, writeback arrows, two-line phase labels, clickable
  navigation to guides.

## [2.0.0] - 2026-04-14

Major release: multi-platform plugin distribution, v2 skill content,
mandatory Handoff Rituals, Phase 7 Release Closure, VitePress docs
site, full English translation.

### Added (Phase 1, VitePress Docs Site)

- VitePress-based documentation site under `docs/`, built with
  `vitepress-plugin-mermaid` for V-Model and traceability diagrams
- GitHub Pages deployment via `.github/workflows/deploy-docs.yml`
- Landing page (`docs/index.md`) with hero section and feature tiles
- Tutorials: installation (all 7 platforms), first-business-analysis,
  full-v-model-run
- Guides: one per skill. v-model-workflow, business-analyse, and
  coding as full guides; the other 5 as structured intros linking
  back to `skills/*/SKILL.md` as source of truth
- Reference: commands, artifacts (`_devprocess/` layout), conventions,
  troubleshooting
- Concepts: The V-Model (with Mermaid diagram), Living Documents,
  Tech-agnostic Requirements, Handoff Rituals, Verification Gates
- About page with Sebastian Hanke bio and Buy Me A Coffee sponsorship
- Imprint page (minimal placeholder)
- Release notes: v1.0.0 Classic, v2.0.0 (placeholder to be finalized
  at v2.0.0 tag)
- Root `package.json` with VitePress + Mermaid dev dependencies
- `.gitignore` updated for `node_modules/`, `docs/.vitepress/cache/`,
  `docs/.vitepress/dist/`

### Added (Phase 3, v2 Content)

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
- `project-conventions/SKILL.md`: filename table extended with
  `20_bugs.md` and `30_handoffs.md` entries; new "The `_devprocess/context/`
  files" section explains the three living logs.
- `business-analyse/SKILL.md` and `requirements-engineering/SKILL.md`
  (already English): existing "Handoff" section replaced by the new
  3-part Handoff Ritual.

### Added (Phase 2, Multi-Platform Plugin Infrastructure)

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

[unreleased]: https://github.com/pssah4/digital-innovation-agents/compare/v2.0.0...HEAD
[2.0.0]: https://github.com/pssah4/digital-innovation-agents/releases/tag/v2.0.0
[1.0.0]: https://github.com/pssah4/digital-innovation-agents/releases/tag/v1.0.0
