# Changelog

All notable changes to digital-innovation-agents are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [2.2.1] - 2026-04-19

Patch release. Documentation update for v2.2.0 features and a new
standalone PULSE page that frames the team operating model on top of
the V-Model workflow. Two skills (`v-model-workflow`, `security-audit`)
flipped from `disable-model-invocation: true` to `false` with sharper
descriptions so the slash menu surfaces them and auto-invocation only
fires on explicit triggers.

### Added (docs)

- **PULSE page** (`docs/pulse.md`). Standalone framework page describing
  the team operating model: four manifesto values, three nested tempos
  (execution / coordination / product), the shared context layer linking
  to every V-Model artifact, the conscious filter, communication
  channels, roles as hats, and the PULSE-V-Model relationship.
  Includes an "Open conversations" section that records substantive
  LinkedIn challenges and the replies, with links to the v2.2.0
  features that closed the gaps each commenter named.
- **PULSE in top-level nav** (`docs/.vitepress/config.mts`).

### Changed (docs)

- `docs/reference/artifacts.md`: `40_metrics.md` added to the directory
  tree, "three context files" expanded to "four context files" with the
  signal-layer description and the Claim column on backlog rows. Project
  initialisation snippet copies `METRICS-TEMPLATE.md` too.
- `docs/reference/conventions.md`: `40_metrics.md` added to the file-name
  table, new "Pair IDs (concurrent agent coordination)" section with the
  `{human-handle}-{model}` format and Claim cell convention.
- `docs/concepts/handoff-rituals.md`: new section "Dialog handoffs, not
  blockers" describing the Questions/Answers tables in `architect-handoff.md`
  and `plan-context.md`, the agent-agent self-answer path, and the
  `AskUserQuestion` fallback for the residue.
- `docs/concepts/living-documents.md`: `40_metrics.md` added to the
  writeback table.
- `docs/guides/business-analyse.md`: new "Phase 8: Post-Release Review"
  section describing how Critical Hypotheses get classified against
  real usage evidence and how the phase is queued via the `release-to-ba`
  handoff entry.

### Changed (skills)

- `skills/v-model-workflow/SKILL.md` and `skills/security-audit/SKILL.md`:
  `disable-model-invocation` flipped to `false` so both skills appear in
  the `/` slash menu. Descriptions tightened with explicit TRIGGER ONLY
  / DO NOT trigger lists so auto-invocation does not fire on generic
  mentions of "workflow" or "security".

## [2.2.0] - 2026-04-19

Minor release. Closes the forward-bias gap in the V-Model workflow
identified by LinkedIn comments on the PULSE article. The workflow
now has return channels at every handoff, cross-phase feedback
triggers, a lightweight signal layer, a post-release BA review, a
claim protocol for concurrent human-agent pairs, explicit
documentation of iteration, and SHA-pinned GitHub Actions for
supply-chain hardening.

### Added (workflow)

- **Signal layer** (FEATURE-001-001). New artifact
  `_devprocess/context/40_metrics.md`, seeded from
  `skills/v-model-workflow/templates/METRICS-TEMPLATE.md`. Five
  tables: cycle time per FEATURE, drift count (plan-context.md vs.
  real code), BA hypothesis validation status, phase transition
  counts, cross-phase trigger counts. Append-additive, no rows ever
  deleted. Writes happen inside existing phase actions: `/coding`
  Phase 2d (drift count during codebase reconciliation), `/coding`
  Final synchronization step 5 (cycle time, transitions, triggers),
  `/business-analyse` Phase 8 (hypothesis status). No separate
  metrics-collection ceremony.
- **Dialog handoffs, not blockers** (FEATURE-001-002). Both handoff
  documents (`architect-handoff.md` and `plan-context.md`) carry a
  `## Dialog` section with Questions and Answers tables. Receiving
  skills scan for pending entries on session start, attempt to
  self-answer from existing artifacts (agent-agent path), and
  surface the unresolvable residue to the user in a single
  `AskUserQuestion` (agent-human path). Pending entries never block
  unrelated work. New template
  `skills/requirements-engineering/templates/ARCHITECT-HANDOFF-TEMPLATE.md`.
- **Cross-phase feedback triggers** (FEATURE-001-003). Two new
  binding triggers that complete the decision-graph pattern
  alongside the existing mid-course bug trigger. Mid-course design
  discovery in `/coding` amends or supersedes an ADR when the code
  proves the design wrong. Mid-course requirements discovery in
  `/architecture` routes a gap or contradiction back to
  `/requirements-engineering` with local blocking (only the
  affected ADR waits, others continue with `blocked-by` dependency
  cite).
- **BA as living document after release** (FEATURE-001-004). New
  `/business-analyse` Phase 8: Post-Release Review. Walks each
  Critical Hypothesis, classifies per real usage evidence as
  `Confirmed by usage`, `Contradicted by usage`, or `Inconclusive`.
  Contradictions trigger backlog entries. Queued automatically by
  `/v-model-workflow` Phase 7 Step 6 via a `release-to-ba` handoff
  entry.
- **Concurrent-agent coordination** (FEATURE-001-005). Backlog rows
  gain a `Claim` column with format `{pair-id} @ {YYYY-MM-DD}`.
  Phase skills claim on start and release on phase end or
  `Status: Done`. Claim conflict surfaces via `AskUserQuestion`
  with four options (ask release, take over, different item,
  split). No central lock service, the backlog itself is the lock.
  Pair-id convention: `{human-handle}-{model}`.
- **V-Model as decision graph** (FEATURE-001-006). New section in
  `skills/v-model-workflow/SKILL.md` and in `docs/concepts/v-model.md`
  that names the three cross-phase triggers and explicitly says the
  forward walk is the default, not the only path. Closes the PULSE
  comment #6 critique that the V looks like waterfall.

### Added (security)

- **SHA-pinned GitHub Actions** (FEATURE-002-001, Issue #9 Gap 1).
  Every third-party action in `.github/workflows/deploy-docs.yml`
  pinned to a 40-char commit SHA with the human-readable version as
  trailing comment. New `.github/dependabot.yml` enables weekly
  bumps for `github-actions` and `npm`. Dependabot updates both SHA
  and comment together.

### Added (planning)

- `_devprocess/plans/v2.2.0-plan.md`. Seven FEATURE specs,
  sequencing rationale (smallest-risk first), acceptance criteria.
  Dog-foods the V-Model planning conventions on the project's own
  improvements.

### Changed

- `project-conventions/SKILL.md` Feature Lifecycle extended with
  CLAIM and RELEASE CLAIM steps. Directory structure reference
  includes `40_metrics.md`.
- `v-model-workflow/SKILL.md` Phase 7 Release Closure Step 6 writes
  the `release-to-ba` handoff entry that queues the BA review.
- `coding/SKILL.md` Phase 1 scans plan-context.md for pending
  Dialog entries. Phase 2d (new) writes the drift-count row.
  Final synchronization step 5 (new) writes cycle time and phase
  transition rows.
- `architecture/SKILL.md` Phase 1a (new) scans architect-handoff.md
  for pending Dialog entries and tries to self-answer.
- `requirements-engineering/SKILL.md` references the new
  ARCHITECT-HANDOFF-TEMPLATE.
- `business-analyse/SKILL.md` adds Phase 8 (Post-Release Review).

### Not in this release

- Issue #9 Gap 2 (cosign release signing). Waits for a key-management
  decision.
- Issue #9 Gap 3 (`SHA256SUMS` publishing). Sequenced with Gap 2.
- UX/Design as an optional V-Model phase. Waiting for Claude Design
  availability and validation.

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
