---
name: dia-realign
description: >
 One entry point for repos that predate current DIA conventions:
 brownfield onboarding (existing codebase, legacy code, reverse
 engineer, we already have code) and legacy DIA upgrades (migrate
 v1/v2, upgrade DIA, FEATURE to FEAT, restructure backlog). Detects
 repo state, then runs a reverse walk, a script pass, or a gap walk.
disable-model-invocation: false
---

# DIA realign

Successor of the retired `/reverse-engineering` and `/dia-migration`
skills. You bring a repo that predates current DIA conventions in
line with them: reverse-engineer V-Model artifacts from the code,
migrate legacy DIA artifacts with the scripts under
`tools/migration/`, or both.

**Writing style, three-layer model, frontmatter spec.** See
`skills/project-conventions/SKILL.md#canonical-specs`; binding for
every artifact this skill produces. Status, phase, last-change, and
claim live in the backlog row, not in artifact frontmatter.

## MANDATORY mode selection (first step)

Run `python3 tools/migration/detect_state.py` and pick the mode from
the JSON report:

| Detection result | Mode |
|---|---|
| No `_devprocess/` (recommendation `brownfield-call-dia-realign-first`) | **A: full reverse walk** |
| Legacy DIA signals: old IDs, `HANDOFFS.md`, v1/v2 layout (recommendation `run-full-migration`) | **B: script pass, then gap walk** |
| Current artifacts (recommendation `v2-clean-no-migration-needed`) | **C: gap walk and deprecations only** |
| `empty-repo` | Not this skill. Greenfield starts at `/business-analysis`. |

Confirm the detected mode with the user before writing anything.
Mixed states resolve toward B: the script pass is idempotent.

## MANDATORY Pre-Phase 0: branch check

Standard ritual, full rules in
`skills/project-conventions/references/team-workflow.md`: Mode A runs
on `feature/realign-<repo-name>` (multi-item exception: one branch
bootstraps the whole backlog, per-item branches start AFTER merge);
Modes B and C run on `chore/dia-realign-<YYYY-MM-DD>`. Refuse on
`main` / `master` / `dev` (AskUserQuestion to create and switch), no
per-item issues or phase tags during the walk, write
`.git/dia-active-skill` so subsequent invocations stay silent.

## MANDATORY Phase 0: artifact triage

Every artifact this skill creates lands in one of four categories
before writing: **FEATURE** (observed capability), **ADR** (decision
inferred from code or docs), **IMP** (improvement candidate), **FIX**
(bug or drift surfaced by the scan). Frontmatter `feature:` and
`epic:` are mandatory for FIX and IMP. A `DIA-Triage` trailer on a
prior commit for an item answers the category question for that item.

## Anti-hallucination rules (binding)

**Core rule: every claim is sourced (`path:line` for code,
`doc:section` for documentation); nothing is invented.** Code tells
you what exists, not whether it solves the right problem. The gates
at the end check compliance.

1. **Source per claim block.** Every claim block (paragraph or table
   row) carries a `Source:` line. Formats:
   `Source: src/api/auth/handlers.ts:42-58`,
   `Source: README.md § "Getting Started"`,
   `Source: package.json "dependencies.prisma"`. The BA draft is
   stricter: every non-placeholder sentence carries `Source:`.
2. **No source means placeholder, not a guess.** Write
   `[NEEDS USER INPUT. No evidence found in {searched sources}.
   /business-analysis will fill this in.]` instead of a "reasonable
   assumption".
3. **No persona from code structure.** Routes, directories, and
   endpoint signatures are technical facts, not user research.
   Personas come only from explicit statements in documentation.
4. **No HMW question without an explicit problem statement** in the
   existing documentation.
5. **Provenance marker on every file:** `source: /dia-realign on
   {date}` in frontmatter. Realign artifacts additionally carry the
   tolerated draft markers from the defaults table below
   (`Anticipated | Observed | Inferred | Draft (reverse-engineered`,
   preserved by `/consistency-check` per N-10/N-11 until validation);
   the BACKLOG row owns lifecycle status.
6. **One decision per ADR.** Tightly coupled choices sharing Context
   and Consequences MAY combine; split when either diverges.

Everything produced is draft, observed, inferred, or snapshot.
`/business-analysis` validates claim by claim afterwards; the
realigned artifacts are the Phase 0 state for the forward walk.

## MANDATORY: backlog as single source of truth

Every artifact also lands as a row in
`_devprocess/context/BACKLOG.md`. Sync chain (binding order): 1.
backlog row, 2. artifact body, 3. explicit `/consistency-check` mode
A at the end of the run. Defaults for reverse-engineered artifacts:

| Item | BACKLOG Status | Frontmatter status | BACKLOG Phase |
|---|---|---|---|
| Epic anticipated | `Backlog` | `Anticipated (not yet validated)` | `Planned` |
| Feature observed (shipped) | `Done` | `Observed (not validated)` | `Released` |
| Feature observed (partial) | `In Progress` | `Observed (not validated)` | `Building` |
| ADR inferred | `In Progress` | `Inferred from codebase` | `Building` |
| BA draft | `Backlog` | `Draft (reverse-engineered)` | (n/a) |
| Scan finding (Phase A6) | `Backlog` | (none) | `Building` |

Any artifact MAY carry `depends-on: [ID, ...]` (acyclic, existing
targets). Hypothesis statements and HMW headings are full prose,
never leftover template placeholders.

## Mode A: full reverse walk

Walk the V backwards, one phase at a time. Detail formats for every
artifact: `references/artifact-formats.md` (binding).

### Phase A1: scope and codebase scan

Ask the scope tier (same tiers as `/business-analysis`): **Simple
Test** (single module, minimal artifacts, 30-60 min), **PoC** (full
stack extraction, 3-8 ADRs, 5-15 features, BA draft, 1-3 h), **MVP**
(full arc42-REFERENCE, 8+ ADRs, 15+ features, complete backlog
seed, 3-8 h). Then scan and report a Codebase Map: manifests,
top-level directories, entry points, test setup, CI config, lint
config, existing documentation. This inventory is the source pool
for the rest of the walk.

### Phase A2: wayfinder, rules layer, plan-context

Primary outputs, templates under `skills/architecture/templates/`:

- `src/ARCHITECTURE.map` (one row per entry-point file), JSDoc
  headers in entry-point files, module READMEs for `src/` dirs with
  more than 3 source files or a cross-module API.
- `_devprocess/rules/` (hard cap 500 lines total): `technical.md`
  (stack from manifests, build commands, conventions visible in 10+
  files), `design.md` (only with UI surface), `domain.md` (glossary
  from class/module names, invariants in code). In the lean profile
  (`profile = "lean"` in `.dia/config.toml`) seed
  `_devprocess/SYSTEM-MAP.md` and `decisions/README.md` instead.
- `_devprocess/requirements/handoff/plan-context.md` from
  `plan-context-TEMPLATE.md`: a pure reference index, cap 20 lines.
  It names where decisions live; stack facts go into
  `rules/technical.md`, never into plan-context.

### Phase A3: ADRs and arc42 snapshot

Identify decisions that are **visible and consequential AND
non-obvious from framework defaults**; skip the rest. One ADR per
decision from `ADR-TEMPLATE.md` with `kind: post-hoc` (Context,
Decision, Consequences, Sources; Considered Options omitted). Code
paths that embody the decision go into `## Sources`. Frontmatter
status `Proposed` plus the provenance marker. Write to
`_devprocess/architecture/ADR-{nn}-{slug}.md`.

Then produce `_devprocess/architecture/arc42-REFERENCE.md` from
`arc42-REFERENCE-TEMPLATE.md` (post-code, cap-exempt). Fill only
sections you can back with sources; omit sections without substance.
Do NOT write arc42-CONSTRAINTS (that is a pre-code artifact; a
later `/architecture` run creates it when new work starts).

### Phase A4: anticipated epics, FEATURE inventory, observable SCs

Sources for capabilities: routes, controllers, CLI commands, public
API, rendered pages, public exports, test descriptions.

- **A4a Anticipated Epics.** Group capabilities into thematic
  clusters; one `EPIC-{nn}-{slug}.md` per cluster with
  `status: Anticipated (not yet validated)` and an Evidence list.
  No obvious clusters: single `EPIC-01-observed-capabilities.md`.
- **A4b FEATURE files.** One `FEAT-{ee}-{ff}-{slug}.md` per
  observable capability, `Status: Observed` in the backlog sense,
  description sourced, Benefits Hypothesis / User Stories / Success
  Criteria as `[NEEDS USER INPUT]`. Short capability names; never
  lump capabilities.
- **A4c Observable Success Criteria.** One SC per capability;
  Target and Measurement are `[AWAITING BA]` unless the code
  declares a deterministic target (timeouts, rate limits, perf
  assertions), then the observed value goes in with `Source:`.
  Satisfies invariant N-4 (every feature has at least one SC).

### Phase A5: BA draft

The most constrained phase. Read README, docs/, manifest
description/keywords, CHANGELOG, landing copy, issue/PR templates,
contributing guides. Build `_devprocess/analysis/BA-{PROJECT}.md`
from the 40-line `BA-TEMPLATE.md` (five questions). Each section is
either evidence-backed (every sentence with `Source:`) or a
`[NEEDS USER INPUT]` placeholder. Count `filled-from-sources` and
`needs-user-input` in the header so `/business-analysis` knows the
remaining work. Long-form sections (BA-EXTENDED) only on request.

### Phase A6: backlog seed

Scan for TODO/FIXME/HACK/XXX, skipped tests, undocumented env vars,
missing test coverage on observed features, outdated dependencies,
missing CI steps. **Verify before filing:** read code AND doc the
finding points at; drop findings whose target is already satisfied.
Each survivor becomes a Standalone Items row: `Status = Backlog`,
`Prio = P2`, `Source = REV`, `Evidence = path:line`, `Typ = Chore`
(or `Security` / `Bug-Followup`), `Notes = anticipated; needs
verification: code-vs-doc`. Title column carries the bare title
only (the ID lives in column 1). If the skill seeds the backlog
file, copy the template headers from
`skills/requirements-engineering/templates/BACKLOG-TEMPLATE.md`
first and update dashboard counts after all rows. Phase mapping:
`Released` (fully implemented), `Building` (partial or awaiting
validation, the default for realigned items), `Planned`
(anticipated, needs refinement).

## Mode B: script pass, then gap walk

Brings an existing DIA repo to current conventions, then fills gaps.

### Migration scripts (tools/migration/)

| Script | Step | Purpose |
|---|---|---|
| `detect_state.py` | 0 | Inventory the repo, classify v1/v2/mixed/brownfield. JSON output. |
| `strip_frontmatter_status.py` | 2a | Remove `status:` / `phase:` / `last_updated:` from YAML frontmatter. |
| `strip_body_status.py` | 2b | Remove body-level `**Status:**` / `> **Status**:` lines. |
| `migrate_naming.py` | 3 | Rename ID schemas (FEATURE-NNNN to FEAT-EE-FF, EPIC-NNN to EPIC-NN, ADR/PLAN leading zeros, Item-BA filenames), rewrite cross-refs. |
| `flatten_analysis.py` | 4 | Flatten `analysis/` to four prefixes (BA, EXPLORE, RESEARCH, AUDIT) plus `sources/`; move legacy mini-BAs. |
| `build_backlog.py` | 5 | Regenerate `BACKLOG.md` from artifact scan; restore `ba-ref:`; previous version saved as `BACKLOG.md.preMigration`. |
| `migrate_status_vocabulary.py` | 5b | Map legacy Status values to the GitHub-aligned vocabulary. |
| `migrate_skill_names.py` | 6 | Rewrite legacy skill names to current ones (includes the two predecessors of this skill). |
| `shrink_artifacts_v3.py` | 6b | Align existing artifacts with the shrunk v3.6 templates; dry-run default, `--apply` to write. |

All scripts accept the project root as argument, print a summary,
are idempotent, and exit non-zero on error so the pipeline stops.

### Safety contract

1. Branch check first (see Pre-Phase 0); dirty tree stops the run
   (commit or stash first).
2. **Dry-run first** where the script supports it; otherwise show
   the plan (rename list, delete list, backlog preview) and get
   confirmation via AskUserQuestion before executing.
3. **Backup before overwrite:** `build_backlog.py` writes
   `BACKLOG.md.preMigration`; per-step commits
   (`chore(dia-realign): step N -- summary`) keep every step
   reversible via `git reset --hard HEAD`.
4. Source code is touched only for `src/ARCHITECTURE.map` and
   optional module READMEs; JSDoc headers are proposed, not
   auto-written. Files outside `_devprocess/` and `src/` stay
   untouched. Deletes are listed before execution.
5. Migration sets no V-Model phase tags and creates no per-item
   issues; the run merges as a single chore PR.

### Step sequence

Each step is one script call plus confirmation; each is
independently re-runnable and commits on success.

0. `detect_state.py`: present the one-page plan, get confirmation.
1. Foundation (no script): seed `_devprocess/rules/` and
   `src/ARCHITECTURE.map` from `skills/architecture/templates/`,
   create `requirements/{epics,features,fixes,improvements,handoff}/`,
   move `context/fixes|improvements/` under `requirements/`. Lean
   profile: SYSTEM-MAP and DECISIONS-README templates instead of
   the rules files.
2. `strip_frontmatter_status.py`, then `strip_body_status.py`:
   status truth moves to the backlog.
3. `migrate_naming.py`: show the rename plan, then execute (file
   renames, then global ref rewrite). Numbering collisions: the
   series with more external references wins, the smaller one is
   renumbered with a header note. Duplicate topics merge under the
   newer structure with a "Previous variants" note; no silent
   deletes.
4. `flatten_analysis.py`: show the move list, then execute.
5. `build_backlog.py`: show the backlog preview, confirm overwrite.
   Then `migrate_status_vocabulary.py` (edits only the Status
   column).
6. `migrate_skill_names.py`, then `shrink_artifacts_v3.py all`.
7. Explicit `/consistency-check` mode A with `--fix` for safe drift
   types; human-triage findings become `BL-NNN` rows with
   `Source = CONSISTENCY-CHECK`.
8. **Gap walk:** compare the migrated artifact set against the Mode
   A output list and run only the missing phases (typically A2
   wayfinder/rules, A4c observable SCs, A5 BA draft). Apply the
   Mode C deprecation offers.

### Failure modes and rollback

A failing script exits non-zero; the skill stops before the next
step. `git reset --hard HEAD` undoes the failed step (previous
steps are committed); re-running `/dia-realign` re-detects state
and resumes at the first dirty step. Backlog-only rollback: restore
`BACKLOG.md.preMigration` over `BACKLOG.md`.

## Mode C: gap walk and deprecations

For repos whose artifacts are already current. Run the gap walk
(Mode B step 8) for anything missing, then make the deprecation
offers. **Offers only, never forced**; each via AskUserQuestion with
a "keep as is" option.

- **HANDOFFS.md.** Phase transitions are DIA commit trailers now
  (`DIA-Phase`, `DIA-Handoff`, `DIA-Triage`; spec:
  `skills/project-conventions/references/canonical-specs.md`,
  "Phase-end commit trailers"). Offer: prepend a deprecation header
  ("retired, replaced by DIA commit trailers, kept as audit trail")
  and optionally move the file to
  `_devprocess/context/archive/HANDOFFS-legacy.md`. Never rewrite
  or delete its entries.
- **Long-form legacy artifacts.** Pre-v4 long BAs, monolithic
  `arc42.md` files, and prose-style `plan-context.md` files count
  as "legacy format, valid". No forced migration; offer the split
  (BA to 40-line core plus BA-EXTENDED, arc42 to CONSTRAINTS plus
  REFERENCE, plan-context to the 20-line ref index) only when the
  user asks for it or actively reworks the artifact.

## MANDATORY: codebase verification gate

The anti-fabrication anchor. Before the handoff ritual, every
FEATURE spec and every ADR produced in Mode A (and every artifact
the gap walk touched) gets an explicit verification against the
codebase. This lifts claims from "we wrote it down" to "we checked
it against reality".

Per FEATURE and ADR, append a verification footer:

- **Released, no drift:** single line
  `Codebase-Verifikation {date}: Released, no drift`.
- **Drift found OR phase not Released:** full block:

```
## Codebase-Verifikation ({date})

**Phase:** {Released | Building | Planned | Candidates}
**Refinement-Bedarf:** {none | reason}
**Verifikations-Befund:**
- Source-Pfade geprueft: {n/m existieren}
- Success-Criteria-Stichprobe (Features) oder Kern-Decision (ADRs): {n/m belegt}
- Drift-Findings: {"Doc: X / Code: Y / Einschaetzung: ..."}
**Backlog-Vorschlag:** {none | concrete FIX/IMP text}
```

Large projects (20+ FEATUREs, 30+ ADRs): split into 3-6 concurrent
agents with non-overlapping file slices; consolidate phase counts
into the Backlog Dashboard. Every drift finding that is not a
one-line doc edit becomes a backlog row.

**Verify the Phase A6 findings too.** Per Standalone row with
`Source = REV` and the `needs verification: code-vs-doc` marker:
target already satisfied means `Status = Done`, `Phase = Released`,
marker removed, note `verified {date}: already present in <ref>`;
gap confirmed means marker removed, `Status = Backlog` stays;
undecidable means marker stays plus `needs refinement: {reason}`,
escalate. No finding reaches GitHub while it still carries the
marker.

## Derivability table: what is NOT documented

Facts that a canonical carrier already holds are never restated in
realign artifacts; the artifact points at the carrier instead.

| Fact class | Canonical carrier | In realign artifacts |
|---|---|---|
| Stack versions, dependencies | manifests (`package.json`, ...) | pointer from `rules/technical.md` |
| Current file paths, entry points | `src/ARCHITECTURE.map` | pointer only |
| Directory tree | the repo itself | never repeated (also not in arc42) |
| Status, phase, claim | BACKLOG row | never in frontmatter or body |
| History, authorship | git log / PRs | never |
| Behavior under test | test files | referenced as SC evidence |

## Closing sequence and handoff ritual

1. **Quality gates.** Source per claim block (BA per sentence);
   provenance marker on every file; no invented personas or HMW;
   FEATURE count matches observable capabilities (12 routes is
   neither 4 nor 30 features); backlog non-empty for any
   non-pristine codebase; no coexisting numbering series;
   Codebase-Verifikation present on every FEATURE and ADR; backlog
   phase counts reflect the gate results. Fix failures first.
2. **Graph check.** Explicit `/consistency-check` mode A (the
   pre-commit hook covers day-to-day; this run is one of the
   mandated explicit invocations). `--deep` only at MVP scope with
   a valid BA.
3. **Parallel-branch alignment (advisory).** Per other branch run
   `python3 tools/renumber-for-merge.py --target <realign-branch>
   --source-ref <branch> --list-conflicts`; report id collisions
   in the console and the BACKLOG Notes. Report only; never modify
   other branches.
4. **Artifact report.** Counts per artifact type (plan-context,
   ADRs, arc42 sections, FEATUREs, BA draft with
   filled/placeholder counts, backlog rows) plus sources walked.
   Mode B adds files renamed, refs updated, status fields cleaned.
5. **Phase-end commit with DIA trailers** (per
   `skills/project-conventions/references/team-workflow.md`,
   "Phase-end commit (binding)"). Canonical message:

```
chore(realign): <repo-name> realign complete

<N FEATUREs, M ADRs, BA draft, K backlog rows>

Refs: <repo-name>
DIA-Handoff: <repo-name> -> business-analysis
```

   Realign is not a V-phase, so the commit carries no `DIA-Phase`
   trailer and sets no phase tag; item-level tags
   (`<id-lower>/realigned`) are set later by `/dia-guide` during the
   item promotion. Skip silently on a clean
   tree.
6. **Transition question.**

> "Technical context is captured. The BA draft is evidence-based
> but NOT validated; {N} sections are `[NEEDS USER INPUT]`. Next:
> `/dia-guide` runs the post-realign item promotion (issues, tags),
> then `/business-analysis` validates the draft. Start now, or
> review the artifacts first?"

On agreement: `/dia-guide` for item promotion, then
`/business-analysis` (Validation Mode auto-detects the draft BA).
On rejection: pause; artifacts stay in `_devprocess/`.

## Scope depth

**Simple Test:** A1-A3 only, no BA draft; output is plan-context,
rules seed, 1-3 ADRs. **PoC:** A1-A5, arc42-REFERENCE reduced to
context and solution strategy, no exhaustive backlog scan.
**MVP:** all phases, full rigor. Do not over- or under-produce.

## Project structure

Follows `/project-conventions`. Root detection before writing:
`docs/adr/` or `docs/architecture/` means `docs/` root;
`_devprocess/` is canonical; CLAUDE.md hints win; default
`_devprocess/`. Ensure the standard directory tree exists
(`mkdir -p {ROOT}/{analysis,requirements/{epics,features,fixes,improvements,handoff},architecture,adr,context,implementation/plans}`).
`adr/` is canonical for ADRs; consolidate `architecture/ADR-*.md`
into `adr/` during the script pass. Do not create `HANDOFFS.md`
(retired; see Mode C).

## Keywords

realign, reverse engineering, existing project, legacy codebase,
brownfield, onboard existing, we already have code, extract
artifacts, DIA migration, upgrade DIA, migrate v1, migrate v2,
restructure backlog, FEATURE to FEAT, status drift cleanup,
bestehendes Projekt, existierender Code, Legacy-Projekt
