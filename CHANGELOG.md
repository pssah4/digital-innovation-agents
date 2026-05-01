# Changelog

All notable changes to digital-innovation-agents are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added: team workflow -- branch=item, phase tags, GitHub integration (2026-04-30)

Codifies how a backlog item flows through Git + GitHub when teams
collaborate. Replaces the earlier "branch per skill" idea with a
team-friendlier "branch per backlog item" model.

**Core invariant: branch = backlog item.** One branch lives for the
entire lifecycle of one backlog item (FEAT, FIX, IMP, EPIC). All
V-Model phases for that item write into the same branch. The branch
ends when its PR merges to `dev`.

Branch naming derived from item id:
- FEAT: `feature/feat-ee-ff-<slug>`
- EPIC: `feature/epic-nn-<slug>`
- FIX:  `fix/fix-ee-ff-nn-<slug>`
- IMP:  `chore/imp-ee-ff-nn-<slug>`

**Phase tags as GitHub-readable progress markers.** Every V-Model
phase ends with the skill setting an annotated git tag
`<item-id-lower>/<phase>-done` (ba-done, re-done, arch-done,
code-done, test-done, audit-done, ready-for-review). Tags are
agent-set so the user does not need to remember the schema; tags are
GitHub-readable so a Project board or Action can move cards.

**Skill-triggered GitHub integration.** New driver
`tools/github-integration/flow.py` with subcommands:
- `create-issue` -- one issue per backlog item, written by the first
  skill that touches the item. Issue body has a phase checklist; the
  agent ticks it as tags are set.
- `tag-phase` -- creates the annotated tag, updates the issue
  checklist, updates the `phase:*` label.
- `open-draft-pr` -- opens a draft PR for the item branch after the
  first commit.
- `ready-for-review` -- verifies required phase tags exist, tags
  `<id>/ready-for-review`, flips the draft PR to ready.
- `status` -- machine-readable summary of where an item stands
  (orchestrator uses this for the post-phase check).

The backlog truth stays in `BACKLOG.md`. GitHub is the team-
collaboration view on top. If `gh` is missing or no GitHub remote is
configured, the script enters local-only mode -- only git tags get
set, the rest is no-op.

**Orchestrator role expanded.** `/dia-orchestrator` now runs a
post-phase consistency check after every entry-skill ends:
1. Branch check (current branch is an item-branch)
2. Tag check (just-finished phase tagged correctly)
3. Backlog check (status reflects phase progress)
4. Issue check (GitHub issue exists, label correct, checklist ticked)
5. Next-phase suggestion via AskUserQuestion

Plus a feature-complete handoff before `/release`: verifies all
required `<id>/*-done` tags, asks via AskUserQuestion whether to
mark the PR ready for review, calls `flow.py ready-for-review`, then
hands off to `/release`.

**Reverse-engineering exception.** RE bootstraps the entire backlog
at once and runs on a single branch
`feature/reverse-engineer-<repo-name>`. Per-item branches start AFTER
RE merges, when downstream skills (`/coding`, etc.) work on
individual items.

Updated:
- `skills/project-conventions/references/team-workflow.md` (new, canonical)
- `skills/project-conventions/references/branch-protection.md` (rewritten to reference team-workflow.md)
- `tools/github-integration/flow.py` (new, ~360 LOC)
- `tools/github-integration/README.md` (new)
- All 7 entry skills' Pre-Phase 0 sections rewritten for the new model
- `skills/dia-orchestrator/SKILL.md` -- post-phase consistency check + feature-complete handoff

### Added: branch protection (2026-04-30)

Two-layer defense against committing new work on the wrong branch.

**Layer 1: pre-commit hook.** Refuses commits on protected branches
(default: `main`, `master`, `dev`) and offers to create a feature
branch interactively. Configurable per project via
`git config dia.protected-branches "<space-separated-list>"`. This
covers the obvious case (commit on dev/main).

**Layer 2: skill-side check.** Every entry skill (reverse-engineering,
business-analysis, requirements-engineering, architecture, coding,
testing, security-audit) now starts with a "MANDATORY Pre-Phase 0:
Branch protection" check that fires ONCE per skill invocation,
regardless of branch type. The check is broader than "are you on
main/dev" -- it also catches the case where the user is on
`feature/yesterday-thing` and starts a different topic, which would
otherwise mix concerns into one PR.

Behaviour:

- On `main` / `master` / `dev`: always refuse, ask via
  `AskUserQuestion` to create a feature branch.
- On a `feature/*` / `fix/*` / `chore/*` branch: ask whether the
  branch fits THIS work, with options continue / new branch / switch
  to existing / custom. Recommendation derives from slug overlap and
  recency of last commit on the branch.

The check stays silent for the rest of the skill invocation
(state in `.git/dia-active-skill`).

Shared contract: `skills/project-conventions/references/branch-protection.md`
documents slug heuristics per skill, recommendation logic, the
once-per-session contract, and override mechanisms.

### Changed: tools/migration/ replaces skills/dia-migration/tools/ (2026-04-30)

The migration scripts move to the top-level `tools/migration/`
directory so both `/dia-migration` and `/reverse-engineering` can
share them. Previously the scripts lived under
`skills/dia-migration/tools/` and only that one skill could call
them.

`/reverse-engineering` now has a Phase -1.5 (between Phase -1
detection and Phase 0 scope) that runs the migration scripts when
DIA-style artefacts are detected in the brownfield repo. This
makes brownfield onboarding into DIA a single-skill operation: the
user runs `/reverse-engineering`, and any pre-existing partial
artefacts get normalised before the code-walk fills the gaps.

`/dia-migration` is now positioned as a convenience wrapper for
existing DIA users upgrading between DIA versions, not a brownfield
onboarding skill. The description and body make this boundary
explicit. For brownfield, the answer is `/reverse-engineering`.

### Added: tools/ directory with project-agnostic Mode A driver and pre-commit hook (2026-04-30)

New `tools/` directory containing the syntactic consistency-check
driver and a pre-commit hook template that any DIA-conformant project
can install. The script auto-detects the repo root via `git`,
expects the standard DIA artefact layout, and accepts an optional
`dia.config.json` for project-specific overrides.

- `tools/consistency-check.py` -- Mode A driver. Checks: dead links,
  ADR abstraction violations (no code paths in core sections), and
  backlog completeness. Auto-fixes Status/Phase frontmatter and body
  duplicates. Writes findings to `.git/consistency-check.last-run.json`.
- `tools/git-hooks/pre-commit` -- pre-commit hook. Runs Mode A with
  `--fix`. On remaining findings prompts the user (y/N) whether to
  launch the interactive Mode C fix-loop in Claude Code. Bypassable
  via `git commit --no-verify`.
- `tools/install-git-hooks.sh` -- installer. Run from the target
  project's repo root: `bash <DIA-checkout>/tools/install-git-hooks.sh`.
  Copies the script to `.git/hooks-data/` and the hook to
  `.git/hooks/pre-commit`.

This codifies the "drift safeguards" architecture: structure is the
specification (BACKLOG.md as single source for status, ARCHITECTURE.map
for code paths), and the syntactic check enforces it on every commit.

### Added: Mode C interactive fix-loop in consistency-check skill (2026-04-30)

The consistency-check skill now defines a third mode for guided fix
workflows. Triggered by `/consistency-check --fix-interactive` or
when the pre-commit hook leaves non-auto-fixable findings, Mode C
walks each finding with the user via `AskUserQuestion`, presenting:

- Two to four concrete fix options with one-line `Pro:`/`Con:` blocks.
- A `Skip` option that defers without losing the finding.
- A `Custom` option for free-text override.
- A clear recommendation per finding, derived from project state.

A Trust-Mode batch option ("mach wie du denkst, ich akzeptiere alle
fixes") delegates all decisions to the agent, with audit-log output
at the end. Escalations happen when fixes touch shared infrastructure
or would delete substance.

The loop is resumable: findings persist in
`.git/consistency-check.last-run.json` across Claude Code sessions.

### Changed: BACKLOG.md / HANDOFFS.md / METRICS.md (BREAKING)

The three context meta-files in `_devprocess/context/` are renamed
from numeric prefixes to capital sentinel filenames:

- `10_backlog.md` -> `BACKLOG.md`
- `30_handoffs.md` -> `HANDOFFS.md`
- `40_metrics.md` -> `METRICS.md`

Capitalization signals "meta-file, not artefact". Numeric prefixes
imposed an ordering that has no semantic meaning (the three files
play distinct roles, none of them sequential).

Migration: the `dia-migration` skill v2 will perform the rename
automatically. Manual migration: `git mv` the three files, then
`grep`-and-replace references across the repo.

### Added: /dia-migration skill (2026-04-30)

New skill `/dia-migration` that brings legacy DIA v1 projects, older
V-Model variants, or brownfield repos up to current DIA v2
conventions. Idempotent and branch-safe; refuses to run on
`main`/`master`/`dev`. Source code under `src/` is not auto-edited
(only `src/ARCHITECTURE.map` and module READMEs are added).

Seven phases, each committed separately:

1. Detection and plan
2. Foundation (`_devprocess/rules/`, `src/ARCHITECTURE.map`,
   directory layout, `20_bugs.md` removal)
3. Bulk status cleanup (frontmatter `status:`/`phase:`/`last_updated:`
   plus body `**Status:**` headers)
4. Filename migration (`FEATURE-NNNN` -> `FEAT-NN-NN`, `EPIC-NNN` ->
   `EPIC-NN`, `ADR-NNN` -> `ADR-NN`, `FIX-EEFF-NN` -> `FIX-NN-NN-NN`,
   etc.)
5. Analysis flattening to four prefixes (BA, EXPLORE, RESEARCH, AUDIT)
6. Backlog regeneration as single source of truth (previous backlog
   preserved as `BACKLOG.md.preMigration`)
7. Skill name updates (`/business-analyse` -> `/business-analysis`,
   `/v-model-workflow` -> `/dia-orchestrator`)
8. Consistency check (`/consistency-check` mode A with auto-fix)

Ships seven executable Python scripts under
`skills/dia-migration/tools/`: `detect_state.py`,
`strip_frontmatter_status.py`, `strip_body_status.py`,
`migrate_naming.py`, `flatten_analysis.py`, `build_backlog.py`,
`migrate_skill_names.py`. All idempotent.

Cross-references added in `README.md` (skill table plus quick-start
entry-points), `AGENTS.md` (orientation block), `.codex/INSTALL.md`,
`.opencode/INSTALL.md`, `scripts/install-skills.sh` (skill array
plus usage block), `docs/.vitepress/config.mts` (sidebar Migration
section), and a new doc page at `docs/guides/dia-migration.md`.

### Added (drift-resistance refactor, 2026-04-30)

Drift-resistance refactor based on a 2026-04-29 audit of one V-Model
project (24% drift across 110 sampled claims, concentrated on status
fields, key-files lists, and quantitative claims). The refactor
introduces three orthogonal mechanics that extend the V-Model without
replacing it.

#### New three-layer documentation model

Documented in `skills/project-conventions/SKILL.md` under
"Three-layer documentation model":

- **Wayfinder layer**: `src/ARCHITECTURE.map` plus JSDoc headers in
  entry-point files plus optional module READMEs. The only place
  current code paths live.
- **Rule sets**: `_devprocess/rules/technical.md` (max 150 lines),
  `design.md` (max 100 lines, optional), `domain.md` (max 100 lines).
  Stable truths only, hard cap 500 lines total.
- **Backlog as single source of truth**:
  `_devprocess/context/BACKLOG.md` carries status, phase, claim,
  and the relation graph for every artifact. Status fields move out
  of artifact frontmatter entirely.
- **Detail artifacts**: BA, Epics, Features, Plans, Fixes, ADR
  detail. Audit trail of the engineering process. Substance only,
  no current code paths in core sections.

#### New templates

- `skills/architecture/templates/ARCHITECTURE-MAP-TEMPLATE.md`
  (wayfinder lookup table)
- `skills/architecture/templates/JSDOC-HEADER-TEMPLATE.md`
  (5-line entry-point header)
- `skills/architecture/templates/MODULE-README-TEMPLATE.md`
  (module-level wayfinder)
- `skills/architecture/templates/RULES-TECHNICAL-TEMPLATE.md`
- `skills/architecture/templates/RULES-DESIGN-TEMPLATE.md`
- `skills/architecture/templates/RULES-DOMAIN-TEMPLATE.md`
- `skills/coding/templates/FIX-TEMPLATE.md`
- `skills/coding/templates/IMP-TEMPLATE.md`

#### Updated templates (status field removed from frontmatter)

- `skills/architecture/templates/ADR-TEMPLATE.md`: ADR abstraction
  rule introduced (no code paths in core sections), optional
  `## Implementation Notes` appendix allowed to go stale.
- `skills/requirements-engineering/templates/FEATURE-TEMPLATE.md`:
  status field removed from frontmatter; `## How It Works` and
  `## Key Files` sections removed; optional `## Code Pointer`
  appendix references ARCHITECTURE.map concept names instead of file
  paths.
- `skills/coding/templates/PLAN-TEMPLATE.md`: explicit Coverage Gate
  table; status moved to backlog row.
- `skills/requirements-engineering/templates/BACKLOG-TEMPLATE.md`:
  Refs column carries the relation graph; row format extended with
  Phase, Last change, Refs columns; vocabulary section unified.

#### Updated skills (English-only instructions, backlog-first writeback)

All MANDATORY blocks converted from German to English in
`/business-analysis`, `/requirements-engineering`, `/architecture`,
`/coding`, `/testing`, `/consistency-check`, `/dia-orchestrator`,
`/reverse-engineering`. Skill instructions are now English; artifact
output continues to follow the user's working language.

- **`/architecture`**: ADR abstraction rule (no code paths in core
  sections), ADR consolidation duty (cap at ~30 thematic ADRs),
  rule-set maintenance, wayfinder generation as mandatory output.
- **`/coding`**: backlog-first writeback (backlog row updated BEFORE
  artifact body), wayfinder maintenance (ARCHITECTURE.map + JSDoc
  headers + module READMEs land in the same commit as the code),
  status synchronization on Done, FIX/IMP at canonical
  `_devprocess/context/{fixes,improvements}/` paths.
- **`/testing`**: hard verify-gate language ("0 failures, 0 errors,
  coverage not regressed"), backlog-first artifact updates.
- **`/consistency-check`**: 8 quick-check items including new
  invariants (backlog completeness E-12, backlog-as-single-source
  N-15, ADR abstraction A-1, wayfinder paths E-13). 6 deep-check
  items including spec-code coherence, rule-set drift, orphan
  artifacts, ADR duplication, map completeness, backlog graph
  render. Auto-fix mode now removes duplicate `status:`/`phase:`
  fields from artifact frontmatter.
- **`/dia-orchestrator`**: plan-gate at /architecture-to-/coding
  transition is binding; consistency-check at phase boundaries is
  binding. Project structure setup includes `_devprocess/rules/`
  and `src/ARCHITECTURE.map`.
- **`/reverse-engineering`**: wayfinder generation
  (ARCHITECTURE.map plus JSDoc headers plus module READMEs) is
  mandatory primary output. Rules layer seeded from observed code
  patterns.

#### Path standardization

All references to `docs/context/...` paths corrected to
`_devprocess/context/...` across skills and reference files.

#### Migration notes

Projects on the previous convention (status in frontmatter) keep
working; the new auto-fix mode of `/consistency-check` migrates
them on the next run. Existing artifacts carrying both
frontmatter and backlog status get their frontmatter cleaned and
the backlog row preserved as the source of truth.

## [2.4.0] - 2026-04-20

Minor release. Adds `/consistency-check` as a first-class graph-health
skill and rolls a mandatory Phase/Status frontmatter convention across
five V-Model skills. `/business-analysis` gets a three-level BA
hierarchy (Project-BA / Epic-BA / Feature-BA) with inheritance rules
that keep downstream artifacts compact. `/coding` and
`/reverse-engineering` grow binding mid-course triggers that prevent
drift between code and spec. `/dia-orchestrator` replaces the static
entry-point question with a hybrid detection that scans the project,
runs a graph-health check, and recommends the next phase.

### Added (skills)

- **`/consistency-check`** (`skills/consistency-check/SKILL.md`). New
  skill that validates the V-Model artifact graph in two modes. Mode
  A is syntactic (links, IDs, refs, frontmatter, backlog-artifact
  sync) and runs at the end of every phase skill. Mode B is semantic
  (content-level consistency via agent) and runs before release or
  on explicit request. Returns a Graph-Health snapshot used by the
  orchestrator to diagnose the next entry point.
- **Phase/Status frontmatter convention** across `architecture`,
  `coding`, `requirements-engineering`, `reverse-engineering`, and
  `dia-orchestrator`. Every Feature, Epic, and ADR carries `phase:`
  and `status:` in frontmatter; the backlog row stays in sync on
  every change. Enum values and sync chain live in
  `skills/project-conventions/references/graph-invariants.md`
  (new reference file).
- **BA hierarchy** in `/business-analysis`. Project-BA
  (`_devprocess/analysis/BA-{project}.md`) is the single source of
  truth for personas, value dimensions, strategic KPIs, and product-
  wide risk. Epic-BA (`requirements/epics/EPIC-{nn}-ba.md`, max 80
  lines) references Project-BA IDs; Epic-KPIs must map to a
  Project-BA KPI via frontmatter `project-kpi-ref:`. Feature-BA is
  rare, only when a feature activates a new persona or owns its own
  hypotheses. New template
  `skills/business-analysis/templates/EPIC-BA-TEMPLATE.md`.
- **Mid-course capability discovery trigger** in `/coding`. New user-
  facing capability (route, handler, command, Sidebar entry, settings
  tab, CLI flag, public API endpoint) pauses the coding flow, runs a
  short dialog (persona, JTBD, expected outcome), writes a FEATURE-
  spec draft and a BA-Nachtrag before the code lands, and closes
  with a `/consistency-check` run. Prevents orphan-code drift.
- **Phase -1 pre-check for existing workflow residues** in
  `/reverse-engineering`. Brownfield projects with prior tooling
  (parallel ADR series, Superpowers artifacts, multiple numbering
  styles) get a decision dialog before any scan starts: consolidate,
  keep alongside, or replace. Includes a numbering-collision
  protocol and a dedup protocol.
- **Observable Success Criteria** in `/reverse-engineering`. SC
  entries get split into an observable capability line derived from
  code and tests, and a `[AWAITING BA]` target placeholder where the
  code has no deterministic target. Replaces the previous pure
  placeholder pattern so the consistency-check can anchor every
  Feature.
- **Hybrid entry-point detection** in `/dia-orchestrator`. The
  orchestrator scans the project, runs `/consistency-check` Mode A,
  and recommends the likely entry phase from the Graph-Health
  snapshot. The user sees the recommendation plus manual
  alternatives via `AskUserQuestion` and keeps the override. On
  phase start, consistency gaps relevant to that phase get surfaced.

### Added (tools)

- **Graph visualisation** under `skills/dia-orchestrator/tools/`:
  `graph-viewer.html` (browser-side viewer for the artifact graph),
  `parse-graph.py` (scans the project and emits graph data), and
  `open-graph.sh` (one-shot runner).

### Not in this release

- Docs guides (`docs/guides/*.md`) do not yet describe the new
  consistency-check skill, BA hierarchy, or hybrid entry-point
  detection. Deferred to a follow-up patch release once the skill
  behaviour is validated in real projects.

## [2.3.0] - 2026-04-20

Minor release. Promotes plan persistence to a first-class artifact of
the `/coding` phase. Every non-trivial implementation run now leaves a
`PLAN-{nn}-{slug}.md` file behind in `_devprocess/implementation/plans/`,
protected by a Plan Coverage Gate that checks Success Criterion
coverage, ADR alignment, codebase anchoring, and verification gates
before any code is written. The plan body stays free-form so the
skill inherits improvements in the coding agent's native planning mode
instead of freezing a fixed schema. `/dia-orchestrator` updated to
route implementation through the persisted plan and to surface
mid-course requirements discovery from `/coding` as well as
`/architecture`.

### Added (skills)

- **`skills/coding/templates/PLAN-TEMPLATE.md`**. New template for
  persisted plan files. Prescribes only the traceability wrapper
  (frontmatter with id / status / date / feature-refs / adr-refs /
  bug-refs / pair-id, a Change Log section, and an Implementation
  Notes section). The plan body belongs to the coding agent; the
  skill never reshapes it.

### Changed (skills)

- `skills/coding/SKILL.md`: new Phase 3a "Plan persistence" describing
  the PLAN-{nn} file flow, a four-item Plan Coverage Gate (SC coverage,
  ADR alignment, codebase anchoring, verification gates), and a
  writeback loop that re-runs the gate whenever a source artifact
  changes while a plan is Active. Adds source-artifact reading
  instruction for prior and active plans. Explicit guidance for
  Mid-course requirements discovery during coding (amend the FEATURE
  in place, re-run the Coverage Gate).
- `skills/dia-orchestrator/SKILL.md`: implementation step now persists
  a PLAN-{nn} file and hands off to the Default agent with the plan as
  source of truth; mid-course deviations append to the plan's Change
  Log. Cycle diagram updated to include the PLAN step. `_devprocess`
  scaffold includes `implementation/plans/`.

### Not in this release

- Docs guides (`docs/guides/coding.md`, `docs/guides/dia-orchestrator.md`)
  do not yet describe plan persistence or the Coverage Gate. Deferred
  to a follow-up patch release once the skill behaviour is validated
  in real projects.

## [2.2.1] - 2026-04-19

Patch release. Documentation update for v2.2.0 features and a new
standalone PULSE page that frames the team operating model on top of
the V-Model workflow. Two skills (`dia-orchestrator`, `security-audit`)
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

- `docs/reference/artifacts.md`: `METRICS.md` added to the directory
  tree, "three context files" expanded to "four context files" with the
  signal-layer description and the Claim column on backlog rows. Project
  initialisation snippet copies `METRICS-TEMPLATE.md` too.
- `docs/reference/conventions.md`: `METRICS.md` added to the file-name
  table, new "Pair IDs (concurrent agent coordination)" section with the
  `{human-handle}-{model}` format and Claim cell convention.
- `docs/concepts/handoff-rituals.md`: new section "Dialog handoffs, not
  blockers" describing the Questions/Answers tables in `architect-handoff.md`
  and `plan-context.md`, the agent-agent self-answer path, and the
  `AskUserQuestion` fallback for the residue.
- `docs/concepts/living-documents.md`: `METRICS.md` added to the
  writeback table.
- `docs/guides/business-analysis.md`: new "Phase 8: Post-Release Review"
  section describing how Critical Hypotheses get classified against
  real usage evidence and how the phase is queued via the `release-to-ba`
  handoff entry.

### Changed (skills)

- `skills/dia-orchestrator/SKILL.md` and `skills/security-audit/SKILL.md`:
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

- **Signal layer** (FEAT-01-01). New artifact
  `_devprocess/context/METRICS.md`, seeded from
  `skills/dia-orchestrator/templates/METRICS-TEMPLATE.md`. Five
  tables: cycle time per FEATURE, drift count (plan-context.md vs.
  real code), BA hypothesis validation status, phase transition
  counts, cross-phase trigger counts. Append-additive, no rows ever
  deleted. Writes happen inside existing phase actions: `/coding`
  Phase 2d (drift count during codebase reconciliation), `/coding`
  Final synchronization step 5 (cycle time, transitions, triggers),
  `/business-analysis` Phase 8 (hypothesis status). No separate
  metrics-collection ceremony.
- **Dialog handoffs, not blockers** (FEAT-01-02). Both handoff
  documents (`architect-handoff.md` and `plan-context.md`) carry a
  `## Dialog` section with Questions and Answers tables. Receiving
  skills scan for pending entries on session start, attempt to
  self-answer from existing artifacts (agent-agent path), and
  surface the unresolvable residue to the user in a single
  `AskUserQuestion` (agent-human path). Pending entries never block
  unrelated work. New template
  `skills/requirements-engineering/templates/ARCHITECT-HANDOFF-TEMPLATE.md`.
- **Cross-phase feedback triggers** (FEAT-01-03). Two new
  binding triggers that complete the decision-graph pattern
  alongside the existing mid-course bug trigger. Mid-course design
  discovery in `/coding` amends or supersedes an ADR when the code
  proves the design wrong. Mid-course requirements discovery in
  `/architecture` routes a gap or contradiction back to
  `/requirements-engineering` with local blocking (only the
  affected ADR waits, others continue with `blocked-by` dependency
  cite).
- **BA as living document after release** (FEAT-01-004). New
  `/business-analysis` Phase 8: Post-Release Review. Walks each
  Critical Hypothesis, classifies per real usage evidence as
  `Confirmed by usage`, `Contradicted by usage`, or `Inconclusive`.
  Contradictions trigger backlog entries. Queued automatically by
  `/dia-orchestrator` Phase 7 Step 6 via a `release-to-ba` handoff
  entry.
- **Concurrent-agent coordination** (FEAT-01-005). Backlog rows
  gain a `Claim` column with format `{pair-id} @ {YYYY-MM-DD}`.
  Phase skills claim on start and release on phase end or
  `Status: Done`. Claim conflict surfaces via `AskUserQuestion`
  with four options (ask release, take over, different item,
  split). No central lock service, the backlog itself is the lock.
  Pair-id convention: `{human-handle}-{model}`.
- **V-Model as decision graph** (FEAT-01-006). New section in
  `skills/dia-orchestrator/SKILL.md` and in `docs/concepts/v-model.md`
  that names the three cross-phase triggers and explicitly says the
  forward walk is the default, not the only path. Closes the PULSE
  comment #6 critique that the V looks like waterfall.

### Added (security)

- **SHA-pinned GitHub Actions** (FEAT-02-01, Issue #9 Gap 1).
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
  includes `METRICS.md`.
- `dia-orchestrator/SKILL.md` Phase 7 Release Closure Step 6 writes
  the `release-to-ba` handoff entry that queues the BA review.
- `coding/SKILL.md` Phase 1 scans plan-context.md for pending
  Dialog entries. Phase 2d (new) writes the drift-count row.
  Final synchronization step 5 (new) writes cycle time and phase
  transition rows.
- `architecture/SKILL.md` Phase 1a (new) scans architect-handoff.md
  for pending Dialog entries and tries to self-answer.
- `requirements-engineering/SKILL.md` references the new
  ARCHITECT-HANDOFF-TEMPLATE.
- `business-analysis/SKILL.md` adds Phase 8 (Post-Release Review).

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
- `/business-analysis` Phase 0 (Existing BA Detection) preflight. When
  a draft BA exists, the skill enters Validation Mode and walks
  section by section, confirming evidence-backed claims and filling
  `[NEEDS USER INPUT]` placeholders via the normal interview. On
  success it promotes the BA from `Status: Draft` to `Status: Validated`.
- `/dia-orchestrator` entry option A0 for brownfield projects, plus a
  new "Reverse Engineering -> Business Analysis" transition that
  always routes through `/business-analysis` to validate the WHY
  before the forward walk resumes.
- Explicit method-proposal protocol in `/business-analysis` and
  `/requirements-engineering`: when user answers go generic or
  sections lack evidence, the skill stops the interview and proposes
  the matching method from `skills/business-analysis/references/innovation-methods.md`,
  always linked to its user-facing docs card.
- Mid-course bug discovery trigger in `/coding`: when a new bug
  surfaces during implementation, the flow pauses, routes through
  BUG-NNN / FEAT-NN-NN / ADR-amendment triage, writes a root-cause
  analysis, adds a backlog entry BEFORE the fix, and cites both items
  in the commit message (`Refs: FEAT-05-07, BUG-018`).
- Per-commit backlog writeback gate in `/coding`: the backlog MUST
  reflect the post-implementation state before every commit that
  references a FEAT-NN-NN or BUG-NNN. Stricter than end-of-phase
  writeback to prevent drift across long phases.
- Binding User Interaction Protocol in `/using-digital-innovation-agents`
  and `/dia-orchestrator`: one question per turn, use
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
- Guides: one per skill. dia-orchestrator, business-analysis, and
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
- **`/dia-orchestrator` skill**: new "Orchestrated Phase Transitions"
  section driving phase handoffs actively, and a new **Phase 7: Release
  Closure** that finalizes artifacts, generates release notes, updates
  CHANGELOG, and cleans the backlog.
- **All 6 phase skills** (business-analysis, requirements-engineering,
  architecture, coding, testing, security-audit): mandatory 3-part
  Handoff Ritual at end of phase -- Artifact report, Handoff context
  (appended to `HANDOFFS.md`), Explicit transition question.
- **`_devprocess/context/20_bugs.md`**: new file convention for the
  FIX-NN-NN-NN bug log, maintained by `/coding` Phase 3c.
- **`_devprocess/context/HANDOFFS.md`**: new file convention for the
  append-only phase handoffs log, written by each phase skill.
- **`using-digital-innovation-agents`**: new "Language in dialog" section
  -- skill content is English, user-facing dialog adapts to user's
  language automatically.

### Changed (Phase 3)

- All 6 German skill files translated to English for portability and
  consistency with `plugin.json`, README, CHANGELOG: `coding`, `testing`,
  `architecture`, `security-audit`, `dia-orchestrator`, `project-conventions`.
- `project-conventions/SKILL.md`: filename table extended with
  `20_bugs.md` and `HANDOFFS.md` entries; new "The `_devprocess/context/`
  files" section explains the three living logs.
- `business-analysis/SKILL.md` and `requirements-engineering/SKILL.md`
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
  `project-conventions`, `business-analysis`, `requirements-engineering`,
  `architecture`, `coding`, `testing`, `security-audit`, `dia-orchestrator`
- 3 innovation phases in `business-analysis`: Exploration, Ideation, Validation
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
