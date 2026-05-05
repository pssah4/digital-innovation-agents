---
name: consistency-check
description: >
  Verifies the V-Model artifact graph is intact: BA sections, Epics,
  Features, Success Criteria, ADRs, arc42 sections, PLANs, Backlog,
  Wayfinder rows, and code references. Two modes: syntactic (links,
  IDs, Refs) and semantic (content coherence via an agent). Default
  syntactic at the end of every skill phase. Semantic before release
  or on explicit request. Use this skill when the user mentions
  "consistency check", "graph check", "check references", "dead
  links", "orphan features", "graph-health", or when another V-Model
  skill completes a phase and wants to verify the artifact graph
  before handoff.
disable-model-invocation: false
---

# Consistency Check

This skill treats the V-Model artifacts as a **graph**. Nodes are
artifacts (BA sections, Epics, Features, Success Criteria, ADRs,
arc42 sections, PLANs, Backlog items, Code files). Edges are
references (Epic→Feature, Feature→ADR, Feature→Code via source
paths, BL-Item→Feature, and so on). The check answers one question:
**is the graph complete and consistent, or do we have orphans, dead
links, and semantic drift?**

The skill is called by other skills at the end of each phase, or
directly by the user when a health check is due.

**Writing style:** Every artifact this skill writes follows the
rules in `skills/project-conventions/SKILL.md` under "Writing style".
No em dashes, no AI vocabulary, ASCII for umlauts if the existing
project convention uses ASCII.

## Three modes

- **Mode A (syntactic, default):** fast, no LLM, runs on phase-end
  triggers and pre-commit hooks.
- **Mode B (semantic, on-demand):** agent-based, runs before release
  or on explicit `--deep`.
- **Mode C (interactive fix-loop):** guided fix workflow with
  per-finding `AskUserQuestion`, Pro/Con suggestions, skip and
  custom-message options. Triggered by `--fix-interactive` or after
  a pre-commit hook block.

## Mode reference

### Mode A: Syntactic check (default, fast, no LLM)

Runs on every Phase-End trigger. Uses Grep + filesystem probes
only. Costs near zero.

Checks (8 quick-check items):

1. **Dead links.** Every Markdown link to a project-internal path
   (`_devprocess/...`, `src/...`, `docs/...`) points to an existing
   file.
2. **Backlog completeness.** Every artifact file under
   `_devprocess/requirements/`, `_devprocess/architecture/`,
   `_devprocess/implementation/plans/`, `_devprocess/requirements/fixes/`,
   and `_devprocess/requirements/improvements/` has exactly one row in
   the backlog. No artifact without a row, no row without an
   artifact.
3. **Backlog as single source.** Artifact frontmatter does NOT carry
   `status:` or `phase:` fields. The backlog row is authoritative.
   Frontmatter that duplicates these fields gets flagged.
4. **Spec references valid.** Every Feature references a real Epic
   ID. Every Backlog Refs entry resolves to an existing row or file.
   Every PLAN's `feature-refs`, `adr-refs`, `fix-refs`, and
   `imp-refs` resolve.
5. **ADR references valid.** Every ADR ID listed in a FEATURE's
   `adr-refs`, in arc42 Par. 9 table, in JSDoc headers, or in
   `src/ARCHITECTURE.map` resolves to an existing ADR file.
6. **ADR contradictions.** No two ADRs cover overlapping topics with
   opposing decisions. Heuristic: similar titles or matching
   `triggering-asr` clusters surfaced for human review.
7. **ADR abstraction rule.** No ADR contains code paths
   (`src/...` strings, file basenames, line numbers, method
   signatures) in the core sections (Context, Decision Drivers,
   Considered Options, Decision, Consequences). Code paths in the
   `## Implementation Notes` appendix are exempt.
8. **Backlog graph health.** Every Refs entry in the backlog points
   at an existing row. The graph derived from the Refs columns is
   acyclic (Epic -> Feature -> Plan -> Fix forms a DAG).

## Auto-fix mode

When run with `--fix` (or when called by another skill with
`autofix=true`), the syntactic check repairs the following drift
types automatically, without asking:

- Frontmatter `status:` or `phase:` field present: REMOVE it.
  Backlog row is the single source of truth. The fix lifts the
  current value from the artifact into the backlog row only if no
  row exists yet; otherwise it just removes the duplicate.
- Backlog row missing for an existing artifact file: create the row
  with `status: Planned`, `phase: Building` defaults, place under
  the matching Epic section.
- Artifact file missing for a backlog row: leave the row, flag for
  human triage (the row may be a placeholder or outdated entry).
- Dashboard counts differ from computed totals: rewrite the
  dashboard table.
- ARCHITECTURE.map row points at a missing entry-point file: flag,
  do not auto-delete. Renames may have happened.

The auto-fix report lists what was changed. Items that cannot be
auto-fixed (orphan ADR, dead link, ADR abstraction violation) are
reported and left for the user.

### Mode B: Semantic check (on-demand, agent-based)

Runs on explicit user request or before a release. Uses subagents
to read paired artifacts and judge whether their content remains
consistent. Costs measurable agent-time.

Checks (6 deep-check items):

1. **Spec-code coherence.** For every Feature with status Done in
   the backlog, sample-check whether the Success Criteria
   described in the FEATURE spec are plausibly verifiable in the
   code (sampling, not exhaustive).
2. **Rule-set drift.** Compare `_devprocess/rules/technical.md`
   against the actual project state (linter config, test
   thresholds, framework versions). Surface contradictions for
   human triage.
3. **Orphan artifacts.** Specs without code (FEATURE Done in
   backlog but no entry-point in `src/ARCHITECTURE.map`); code
   without spec (entry-point in `src/ARCHITECTURE.map` with no
   matching FEATURE backlog row).
4. **ADR duplication check.** Two ADRs covering the same topic at
   different abstraction levels are flagged for consolidation.
5. **Map completeness.** Every module under `src/` that owns
   substance has an `ARCHITECTURE.map` entry. Triggers: more than
   3 source files in a directory, or any directory with a
   `README.md`.
6. **Backlog graph render.** Produce a mermaid or JSON graph from
   the backlog Refs columns, surface orphan nodes (no incoming or
   outgoing edges) and status mismatches (e.g. PLAN Done but
   parent FEATURE still In Progress).

Each finding includes file path, row reference, and enough context
to locate the issue. Findings that cannot be auto-fixed become BL
items in the Standalone Items section with `Source = CONSISTENCY-CHECK`.

### Mode C: Interactive fix-loop (on-demand or post-block)

Triggered by `/consistency-check --fix-interactive` or by the
pre-commit hook when Mode A leaves non-auto-fixable findings. The
loop picks up the latest run from
`.git/consistency-check.last-run.json` (Mode A always writes this
file) and walks every finding with the user, one by one.

**Resume contract.** The findings file persists across Claude Code
sessions. If the user exits Claude mid-loop, the next
`/consistency-check --fix-interactive` invocation reads the same
file and continues at the first unresolved finding. Resolved
findings are marked `status: "fixed"` or `status: "skipped"` in the
JSON; the loop never re-asks about them. The file is deleted only
after the loop completes and the user confirms the commit.

**Universal interaction rules (the "never leave the user alone"
contract).** Every step in this loop ends with one
`AskUserQuestion` that satisfies all of:

- One short recommendation sentence ("Empfehlung: A, weil ...").
- Two to four concrete options, each with a one-line `Pro:` and
  one-line `Con:` block.
- A `Skip` option that defers the finding without losing it.
- A `Custom` option ("eigene Anweisung schreiben") so the user can
  always override.
- The recommendation and the option list are derived from the
  current finding plus the project state, not boilerplate.

This rule is invariant. The loop never returns control to the user
without an explicit next-step question. If a step has no decision
left to make (e.g. all findings resolved), the question still asks
about the next workflow step (commit, push, /testing, /release).

**Loop structure (six phases):**

1. **Load.** Read `.git/consistency-check.last-run.json`. If absent
   or empty, run Mode A first and then continue.
2. **Triage.** AskUserQuestion: which strategy (sequential, by
   severity, by class, batch-fix-only, trust-mode auto-approve,
   custom). Recommendation adapts to finding count: sequential up
   to 10, by-severity 11+, trust-mode when the user explicitly
   says "mach wie du denkst" or selects it.

   **Trust mode (auto-approve all):** the user delegates all fix
   decisions to the agent. The loop applies the recommended option
   for every finding without asking, except when:
   - A finding's three options have no clear recommendation
     (recommendation field empty in the suggestion bundle)
   - A fix would touch shared infrastructure (CI configs, hooks,
     governance code) -- always escalate
   - A fix would delete substance (more than just a Status
     duplicate or dead link) -- escalate to confirm

   In trust mode, after every batch of 10 fixes the loop posts
   a one-line progress update so the user sees movement. At the
   end it produces a complete audit log: per-finding the chosen
   option, the resulting diff hunk reference, and any escalations.
3. **Per-finding loop.** For each unresolved finding, AskUserQuestion
   with file:line pointer, finding text, two to four concrete
   fix options with Pro/Con, plus Skip and Custom. Recommendation
   names the option and gives the reason from project state.
4. **Re-check.** Run Mode A again. List remaining findings (Skips
   and any new findings produced by fixes). AskUserQuestion: how
   to handle remaining findings (file as backlog items with
   Source=CONSISTENCY-CHECK, commit anyway via --no-verify, return
   to skips, custom). Recommendation defaults to backlog-filing.
5. **Commit.** Build the commit message from the resolved findings
   list, show it to the user, AskUserQuestion: confirm message,
   edit message, or cancel. Recommendation is "confirm" when the
   message accurately summarizes the fixes.
6. **Follow-up.** AskUserQuestion: what next (push, /coding,
   /testing, /security-audit, /release, custom). Recommendation
   follows the V-Model checklist (after /coding -> /testing,
   after /testing -> /security-audit, before release -> Mode B
   semantic check).

**Fix actions per finding type.** The loop dispatches to specific
fix patterns based on the finding's `type` field:

| Finding type | Auto-fix candidates surfaced as options |
|---|---|
| `dead-link` | Remove, mark planned with FEAT-ref, correct path |
| `adr-abstraction-violation` | Move path to `## Implementation Notes` appendix, move path to `src/ARCHITECTURE.map`, replace path with concept name |
| `orphan-adr` | Mark Superseded with reference, mark Deprecated, link from a feature |
| `orphan-feature` | Assign to existing epic, create new epic, mark Planned |
| `feature-without-sc` | Add `[AWAITING BA]` placeholder, write SC inline, defer |
| `source-path-broken` | Update path, mark feature Planned, remove path entry |
| `frontmatter-status-duplicate` | Always auto-fixed in Mode A; only surfaces here if auto-fix failed |
| `status-coherence-breach` | Open the owning phase skill (`/business-analysis` for BA Draft, `/requirements-engineering` for RE-side BA promotion, `/architecture` for ADR Proposed), Defer (file as backlog item with Source=CONSISTENCY-CHECK), Skip with reason. No direct edit option: status promotion is a semantic claim and belongs in the phase skill. |
| `feature-activation-path-missing` | Open `/requirements-engineering` to add the Activation Path entry, Demote FEATURE backlog status from Done to Active, Defer (file as backlog item with Source=CONSISTENCY-CHECK), Skip with reason. No direct edit option: subtype-aware contract is owned by `/requirements-engineering`. |
| `stub-without-fix-row` | Open `/coding` to create the missing FIX-row, Remove the stale FIXME marker (only if the stub has been resolved in code), Skip with reason. |
| `fix-without-stub-evidence` | Open `/coding` to add the FIXME marker at the stubbed code location, Resolve the FIX (mark Done if the stub is gone), Defer, Skip with reason. |

**Output of the loop.** The loop writes a single audit row in
`_devprocess/context/METRICS.md` under "Consistency-Check Runs"
with: timestamp, mode (C), findings-total, fixed, skipped, deferred-
to-backlog, and the commit SHA when applicable.

## Invocation

- `/consistency-check` with no args: runs Mode A on the current
  project root, reports results, and writes
  `.git/consistency-check.last-run.json`.
- `/consistency-check --fix`: Mode A with auto-fix enabled (no user
  interaction). Used by the pre-commit hook before falling back to
  Mode C if findings remain.
- `/consistency-check --fix-interactive`: Mode C interactive
  fix-loop. Reads the last-run file and walks the user through.
- `/consistency-check --deep` or with user saying "semantic check":
  runs Mode A + Mode B.
- `/consistency-check --view` or user says "zeig mir den Graph",
  "show me the graph": runs Mode A and opens the interactive
  graph viewer (see Viewer-Tool below).
- Called from another skill: the calling skill passes a scope
  argument (e.g. `scope=feature:FEAT-NN-19` to check only a single
  feature's neighbourhood).
- Called from pre-commit hook: hook runs `--fix` first, then if
  findings remain prompts the user to launch `--fix-interactive`.

## Tooling

The syntactic checker (Mode A) and the pre-commit hook live in
`tools/` of this DIA repo:

- `tools/consistency-check.py` -- project-agnostic Mode A driver.
  Auto-detects the repo root via `git rev-parse --show-toplevel` and
  expects the standard DIA layout (`_devprocess/`, optional `src/`).
  Optional `dia.config.json` in the project root overrides defaults.
- `tools/git-hooks/pre-commit` -- pre-commit hook template that runs
  the Mode A driver, then on findings asks the user (y/N) whether to
  launch the interactive Mode C fix-loop in Claude Code.
- `tools/install-git-hooks.sh` -- installer. Run from the target
  project's repo root: `bash <DIA-checkout>/tools/install-git-hooks.sh`.
  Copies the script to the target's `.git/hooks-data/` and installs
  the pre-commit hook into `.git/hooks/pre-commit`.

Mode B (semantic) and Mode C (interactive fix-loop) are orchestrated
inside Claude Code by this skill, not by the script.

## Viewer tool (for team meetings and navigation)

The graph is NOT persisted in a separate file. It exists implicitly
in the backlog Refs columns and Markdown references; it is generated
on-demand from the source files.

Two entry points:

1. **Direct shell:**
   ```bash
   bash ~/.claude/skills/dia-guide/tools/open-graph.sh <project-root>
   ```
   The parser builds the JSON in memory, passes it as a URL parameter
   to the viewer, and opens the default browser. No file on disk.

2. **From this skill:** `/consistency-check --view` calls the same
   mechanism.

**Viewer features:**

- Cytoscape.js based, standalone HTML, no build pipeline.
- Filters / lenses: `Overview` (Epics, Features, ADRs),
  `Persona lens` (BA persona -> Epic -> Feature), `Phase lens`
  (colored by Released/Building/Planned/Candidates), `Health lens`
  (orphans highlighted), `Epic focus` (one Epic with direct
  neighbors).
- Click on a node: details panel with type, phase, status (read
  from the backlog row), and file path (clickable, opens in the
  default editor).
- No editor: all changes stay in Markdown. The viewer navigates;
  it does not persist.

**Use in meetings:**

- Screen share with the viewer URL.
- Phase lens gives the status panorama (mostly Building, a few
  Planned highlights).
- Health lens for backlog refinement sessions (what is loose, what
  is missing).

## Tool files

- `skills/dia-guide/tools/parse-graph.py` - Markdown to JSON.
  Stdlib only, no dependencies.
- `skills/dia-guide/tools/graph-viewer.html` - standalone
  viewer with Cytoscape.js (CDN).
- `skills/dia-guide/tools/open-graph.sh` - wrapper that
  parses and opens the viewer.

## Output

Every run produces two artifacts:

### 1. Console report (summary)

```
Consistency Check, Mode: {A | A+B}, Run: {date}

Graph state:
- Epics:     {n}
- Features:  {n} (Released {a}, Building {b}, Planned {c}, Candidates {d})
- ADRs:      {n}
- PLANs:     {n}
- BL-Items:  {n}

Findings:
- Dead links:               {n}
- Orphan features:          {n}
- Orphan Epics:             {n}
- Orphan ADRs:              {n}
- Features without SC:      {n}
- Source paths broken:      {n}
- Backlog format issues:    {n}
- arc42-ADR table drift:    {n}
- Status coherence breach:  {n} (warn, fail under --strict)
- Activation path missing:  {n} (warn, fail under --strict)
- Stub without FIX-row:     {n} (warn)
- FIX without stub evidence: {n} (warn)
{if Mode B:}
- Feature-ADR semantic:     {n}
- BA-Feature semantic:      {n}
- arc42-ADR semantic:       {n}
- Code-Feature semantic:    {n}
```

### 2. Backlog update in `{ROOT}/context/BACKLOG.md`

- **Graph-Health section** (create or replace):

  ```markdown
  ## Graph-Health (letzter Check: {YYYY-MM-DD}, Modus: {A | A+B})

  | Invariante                  | Status | Count |
  | --------------------------- | ------ | ----- |
  | Dead links                  | {ok/fail} | {n} |
  | Orphan features             | {ok/fail} | {n} |
  | Orphan Epics                | {ok/fail} | {n} |
  | Orphan ADRs                 | {ok/fail} | {n} |
  | Features without SC         | {ok/fail} | {n} |
  | Source paths broken         | {ok/fail} | {n} |
  | Backlog format issues       | {ok/fail} | {n} |
  | arc42-ADR table drift       | {ok/fail} | {n} |
  | Status coherence breach     | {ok/warn/fail} | {n} |
  | Activation path missing     | {ok/warn/fail} | {n} |
  | Stub-FIX binding (E-14)     | {ok/warn} | {n} |
  {...if Mode B, extra rows}
  ```

- **Automatic BL-items.** Every finding that represents a real gap
  (not a false positive) becomes a BL-row in the Standalone Items
  section with `Source = CONSISTENCY-CHECK`, `Prio = P3` (default,
  user reprioritises), `Phase = Candidates`, and a concrete
  `needs refinement: {specific issue}` note. Fixes that are purely
  mechanical (dead link, broken source path) get `Phase = Building`
  because no refinement is needed.

- **Deduplication.** If a finding from a previous run already has a
  BL-item, do not create a duplicate. Refresh the existing item's
  Notes with the latest run date.

## Workflow

1. **Detect project structure.** Same rules as `/reverse-engineering`:
   `docs/` or `_devprocess/` as root. Abort with a clear message if
   neither is found.
2. **Build the node set.** Grep for:
   - `_devprocess/requirements/epics/EPIC-*.md` -> Epics
   - `_devprocess/requirements/features/FEATURE-*.md` -> Features
   - `_devprocess/architecture/ADR-*.md` -> ADRs
   - `_devprocess/implementation/plans/PLAN-*.md` -> PLANs
   - `_devprocess/analysis/BA-*.md` -> BA sections (parsed by headers)
   - `_devprocess/architecture/arc42.md` -> arc42 sections
   - `src/ARCHITECTURE.map` -> wayfinder rows
   - JSDoc headers in entry-point files -> wayfinder cross-checks
   - `_devprocess/context/BACKLOG.md` -> BL-Items
3. **Build the edge set.** Parse references in each node:
   - Feature's `Epic:` field -> edge to Epic
   - Feature's `Related ADRs:` -> edges to ADRs
   - Feature's `Source (Implementation):` -> edges to Code files
   - ADR's `Related Decisions:` / `References:` -> edges to ADRs/Features
   - BL-Item's Feature-Spec / ADR columns -> edges
   - arc42 Par. 9 table -> edges to ADRs
   - Epic's / Feature's / IMP's / FIX's `ba-ref:` -> edge to BA
   - Item-BA's `project-ba-ref:` -> edge to Project-BA
   - architect-handoff `source-ba:` -> edge to BA
4. **Apply invariants.** For each check, list violations with file
   path and line number if possible. For N-17, walk the
   Status-Coherence-Pairs table from `graph-invariants.md`: per pair,
   read the parent's `status:` field and check the child evidence
   condition. Emit `status-coherence-breach` findings with parent
   path, parent status, child path, child evidence, and suggested
   promotion target. For N-18, walk Done-FEATUREs (per backlog),
   parse the FEATURE file for an `## Activation Path` section, emit
   `feature-activation-path-missing` if the section is absent or
   empty (and the FEATURE has `subtype:` set, otherwise skip per
   backwards-compat rule). For E-14, grep the source tree for
   `FIXME(stub):` markers, parse the embedded FIX-ID, cross-reference
   against backlog FIX-rows; bidirectional check both ways.
5. **Write report and backlog update.**
6. **Handoff.** Report completion with finding count. Hand back to
   the calling skill or return to user.

## Invariants reference

This is the binding set. The same list lives in
`skills/project-conventions/references/graph-invariants.md` (source
of truth for all V-Model skills).

### Node invariants

- `N-1` Every Feature has exactly one Epic parent.
- `N-2` Every Epic has either at least one Feature in its MVP table
  or is explicitly marked Phase Candidates with `needs refinement`.
- `N-3` Every ADR is referenced at least once from a Feature, arc42,
  or Backlog entry.
- `N-4` Every Feature has at least one Success Criterion entry
  (may be placeholder `[AWAITING BA]` or `[AWAITING RE]`).
- `N-6` Every backlog row has a Phase label
  (`Released | Building | Planned | Candidates`) and a Status label.
- `N-7` Every backlog row with Phase Candidates has a
  `needs refinement: {reason}` marker.
- `N-13` Every FIX has `feature:` and `epic:` in the frontmatter.
- `N-14` Every IMP has `feature:` and `epic:` in the frontmatter.
- `N-15` (NEW) No artifact frontmatter contains a `status:` or
  `phase:` field. The backlog row is the single source of truth.
- `N-17` (NEW) Status coherence between parent and child artifacts:
  a parent must not stay at a pre-validation status while a derived
  child has been exercised. Pair table below.

  Parent-child pair table (initial, append-only):

  | Parent | Parent draft status | Child evidence triggering breach |
  |--------|---------------------|----------------------------------|
  | BA | `Draft` or `Draft (...)` prefix (e.g. `Draft (reverse-engineered, ...)`) | `architect-handoff.md` exists and references this BA, OR an Epic / Feature / IMP / FIX with `ba-ref:` pointing here has phase `Building` or `Released` |
  | ADR | `Proposed` | A Feature with `adr-refs:` pointing here has phase `Building` or `Released` |

  Severity defaults to `warn` (Mode A reports, does not fail the run).
  Under `--strict` (typically before release), `warn` becomes `fail`.
  Auto-fix is NOT performed; the finding surfaces in Mode C with the
  fix option "Open the owning phase skill" so the promotion happens
  through the canonical path. Detail rule and match semantics live in
  `skills/project-conventions/references/graph-invariants.md` under
  "Status-Coherence-Pairs".
- `N-18` (NEW) Every FEATURE with backlog status `Done` carries an
  `## Activation Path` section in its Definition of Done with at
  least one filled entry (Type and Identifier non-empty). FEATUREs
  without `subtype:` in frontmatter are exempt for backwards
  compatibility; FEATUREs with `subtype: user-facing` (default when
  set) or `subtype: library` MUST satisfy this invariant. Severity
  defaults to `warn` (Mode A reports), `fail` under `--strict`. Auto-
  fix is NOT performed; Mode C surfaces "Open `/requirements-engineering`
  to add the Activation Path entry" or "Demote backlog status from
  Done to Active" as the resolution path.

### Edge invariants

- `E-1` Every Markdown link to a project-internal path resolves.
- `E-3` Every ADR listed in a FEATURE's `adr-refs` exists.
- `E-4` Every ADR listed in arc42 Par. 9 exists in
  `_devprocess/architecture/`.
- `E-5` Every ADR under `_devprocess/architecture/` appears in
  arc42 Par. 9 or is explicitly deprecated or superseded.
- `E-6` Every backlog row's Refs column resolves to existing rows
  or files.
- `E-10` Every `depends-on` entry resolves to an existing artifact
  ID.
- `E-11` The graph derived from `depends-on` AND backlog Refs
  columns is acyclic.
- `E-12` (NEW) Every artifact file under
  `_devprocess/requirements/`, `_devprocess/architecture/`,
  `_devprocess/implementation/plans/`, `_devprocess/requirements/fixes/`,
  `_devprocess/requirements/improvements/` has exactly one row in the
  backlog.
- `E-13` (NEW) Every entry-point file referenced in
  `src/ARCHITECTURE.map` exists.
- `E-14` (NEW) Bidirectional binding between `FIXME(stub):` markers in
  source code and FIX-rows in the backlog. For every
  `FIXME(stub): <reason> -- see FIX-{ee}-{ff}-{nn}` in the source tree:
  the referenced FIX-ID exists in the backlog and is in an unresolved
  state (status not `Done`). For every FIX-row whose notes contain
  `Wiring offen`, `stub`, or `deferred-stub`: at least one source
  location references this FIX-ID via a `FIXME(stub):` marker.
  Findings: `stub-without-fix-row` (marker references missing or
  resolved FIX-ID) and `fix-without-stub-evidence` (FIX-row claims a
  stub but no marker references it). Both surface as `warn` in Mode A.
  Auto-fix not performed (manual triage: either add the missing FIX-row,
  remove the stale marker, or resolve the FIX).

### ADR abstraction invariants

- `A-1` (NEW) No ADR contains `src/...` paths, file basenames, line
  numbers, or method signatures in the core sections (Context,
  Decision Drivers, Considered Options, Decision, Consequences).
  Code paths in the optional `## Implementation Notes` appendix are
  exempt and explicitly allowed to go stale.

### Semantic invariants (Mode B only)

- `S-1` FEATURE description does not contradict referenced ADRs.
- `S-2` FEATURE without a matching BA JTBD is flagged as
  `needs BA-anchor`.
- `S-3` arc42 sections describing an ADR's decision match the ADR's
  current Decision text (not an old revision).
- `S-4` FEATUREs with backlog status Done have their key Success
  Criteria verifiable in the code (plausibility, not exhaustive).
- `S-5` (NEW) Every module under `src/` that owns substance has an
  `ARCHITECTURE.map` row (heuristic: more than 3 source files in
  the directory, or any directory with a `README.md`).
- `S-6` (NEW) For every FEATURE with backlog status `Done`, every
  Success Criterion entry maps onto a concrete code path (file:line
  range or symbol). Subagent samples per FEATURE; reports
  `sc-without-evidence` findings for SCs that cannot be tied to code.
  Plausibility check, not exhaustive proof.
- `S-7` (NEW) The `## Activation Path` entry in a Done-FEATURE
  actually exists in the code. Subagent verifies the claim per
  activation type (route registered, command registered, public
  symbol exported, scheduled job hooked, etc.). Reports
  `activation-path-missing` findings when the claimed identifier is
  absent from the code.

## Quality gates for the skill itself

Before this skill reports completion:

1. Every reported finding includes file path and enough context to
   locate the issue.
2. No finding is silently dropped; unclear cases go into the report
   with an `unclear:` prefix so a human can triage.
3. BL-items created by this skill carry `Source = CONSISTENCY-CHECK`
   so they are distinguishable from other backlog entries.
4. Duplicates are avoided via the dedup rule.

## When NOT to use

- Trivial edits (typo fix, single comment). Running the full check
  is overkill.
- Active refactoring where artifacts are intentionally in flux.
  Wait for the refactor to settle, then run the check.
- Greenfield projects without V-Model artifacts. Bootstrap via
  `/dia-guide` or `/reverse-engineering` first.

## Keywords

consistency check, graph check, Konsistenzpruefung, graph-health,
dead links, orphan features, orphan epics, orphan ADRs, V-Model
integrity, artifact graph, reference check, semantic drift,
backlog health
