---
name: consistency-check
description: >
  Prueft die Konsistenz des V-Model-Artefakt-Graphen: BA-Sektionen,
  Epics, Features, Success Criteria, ADRs, arc42-Sektionen, PLANs,
  Backlog und Code-Referenzen. Liefert zwei Modi: syntaktisch (Links,
  IDs, Refs) und semantisch (inhaltliche Konsistenz via Agent).
  Default syntaktisch am Ende jeder Skill-Phase. Semantisch vor
  Release oder auf explizite Anfrage. Use this skill when the user
  mentions "consistency check", "graph check", "Konsistenzpruefung",
  "check references", "dead links", "orphan features", "graph-health",
  or when another V-Model skill completes a phase and wants to verify
  the artifact graph before handoff.
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

## Two modes

### Mode A: Syntactic check (default, fast, no LLM)

Runs on every Phase-End trigger. Uses Grep + filesystem probes
only. Costs near zero.

Checks:

1. **Dead links.** Every Markdown link to a project-internal path
   (`docs/...`, `_devprocess/...`, `src/...`) points to an existing
   file.
2. **Missing IDs.** Every Feature references a real Epic ID.
   Every Backlog row referencing a Feature/ADR/PLAN/BL-Item uses
   an ID that exists.
3. **Orphan features.** Every FEATURE has an Epic parent.
4. **Orphan Epics.** Every Epic has at least one Feature
   referenced in its MVP-Features table, or is explicitly marked
   `Planned` with a `needs refinement` note.
5. **Orphan ADRs.** Every ADR is referenced from at least one
   FEATURE, arc42, or Backlog entry.
6. **SC coverage.** Every FEATURE that is not marked `Planned`
   has at least one Success Criterion (may be `[AWAITING BA]` or
   `[AWAITING RE]` as placeholder).
7. **Source-path validity.** Every FEATURE's `Source (Implementation)`
   paths point to files that exist.
8. **Backlog integrity.** Every BL-item row has the required
   columns filled per BACKLOG-TEMPLATE.md. Phase is set to
   `Released | Building | Planned | Candidates`, with
   `needs refinement: {reason}` for Candidates items (and optionally
   Planned items). Legacy labels `Released/Building/Planned/Candidates` are
   auto-mapped to the new names during the syntactic check.
9. **arc42 ADR table completeness.** Every ADR under `docs/adr/`
   is listed in arc42 Par. 9 table, and vice versa.
10. **Phase/Status frontmatter required (N-10, N-11, N-12).** Every
    Feature has `phase:` and `status:` in YAML-frontmatter. Every
    Epic has `phase:`. Every ADR has `phase:` and `status:`. Missing
    fields are reported as drift.
11. **Backlog/frontmatter sync (E-7, E-8).** Feature-rows in the
    backlog must show the same phase as the feature file
    frontmatter. Epic header lines `Phase: X` in the backlog must
    match epic file frontmatter. Mismatches are reported per
    artifact.
12. **Dashboard consistency (E-9).** The phase counts in the backlog
    dashboard table match the computed totals from feature
    frontmatters + epic frontmatters + standalone-chores table.

## Auto-fix mode

When run with `--fix` (or when called by another skill with
`autofix=true`), the syntactic check repairs the following drift
types automatically, without asking:

- Missing `phase:` in Feature/Epic/ADR frontmatter: insert with the
  best available value (feature phase from backlog row; ADR phase
  from the drift table in backlog § ADR-Review-Status; epic phase
  via worst-wins over its features; fallback `Building`)
- Missing `status:` in Feature/ADR frontmatter: insert default
  (`Planned` for Feature, `Proposed` for ADR)
- Backlog feature-row phase differs from feature frontmatter phase:
  overwrite the backlog row with the frontmatter value (frontmatter
  is source of truth)
- Backlog epic header `Phase: X` differs from epic frontmatter:
  overwrite the header
- Dashboard phase counts differ from computed totals: rewrite the
  dashboard table

The auto-fix report lists what was changed. Items that cannot be
auto-fixed (e.g. orphan ADR, dead link) are reported as before and
left for the user.

### Mode B: Semantic check (on-demand, agent-based)

Runs on explicit user request or before a release. Uses subagents
to read paired artifacts and judge whether their content remains
consistent. Costs measurable agent-time.

Checks:

1. **Feature-ADR coherence.** The FEATURE description matches what
   the referenced ADR decided. If an ADR was superseded and the
   FEATURE still describes the old decision, flag it.
2. **BA-Feature coherence.** Each Feature traces to at least one
   JTBD in BA Par. 5 or is explicitly in Planned with no BA-anchor
   yet. If BA.JTBD exists but no Feature addresses it, flag it.
3. **arc42-ADR coherence.** arc42 sections that reference ADRs
   describe what the ADR actually decided; if ADR text changed but
   arc42 did not, flag it.
4. **Code-Feature coherence.** For each Feature with Status
   `Implemented`, stichprobenartige Agent-Pruefung ob die im
   FEATURE beschriebenen Success Criteria plausibel im Code
   belegt sind.

## Invocation

- `/consistency-check` with no args: runs Mode A on the current
  project root, reports results.
- `/consistency-check --deep` or with user saying "semantic check":
  runs Mode A + Mode B.
- `/consistency-check --view` or user says "zeig mir den Graph",
  "show me the graph": runs Mode A and opens the interactive
  graph viewer (see Viewer-Tool below).
- Called from another skill: the calling skill passes a scope
  argument (e.g. `scope=feature:FEATURE-019` to check only a single
  feature's neighbourhood).

## Viewer-Tool (fuer Team-Meetings und Navigation)

Der Graph wird **nicht** in einer eigenen Datei persistiert. Er
existiert implizit in den Markdown-Referenzen und wird on-demand
aus den Source-Dateien generiert.

Zwei Aufruf-Wege:

1. **Direkt per Shell:**
   ```bash
   bash ~/.claude/skills/v-model-workflow/tools/open-graph.sh <project-root>
   ```
   Startet den Parser, erzeugt das JSON in-memory, uebergibt es als
   URL-Parameter an den Viewer und oeffnet den Default-Browser.
   Keine Datei auf Disk.

2. **Aus diesem Skill heraus:** `/consistency-check --view` ruft
   den gleichen Mechanismus auf.

**Viewer-Features:**

- **Cytoscape.js**-basiert, standalone HTML (keine Build-Pipeline).
- Filter/Lenses: `Uebersicht` (Epics, Features, ADRs), `Persona-
  Lens` (BA-Persona -> Epic -> Feature), `Phase-Lens` (farbig nach
  Released/Building/Planned/Candidates), `Health-Lens` (Orphans hervorgehoben),
  `Epic-Fokus` (ein Epic mit direkten Nachbarn).
- Click auf Knoten: Details-Panel mit Typ, Phase, Status, Datei-
  pfad (klickbar, oeffnet im Default-Editor).
- Kein Editor (bewusst): alle Aenderungen bleiben im Markdown. Der
  Viewer navigiert, er persistiert nicht.

**Einsatz in Meetings:**

- Beamer oder Screen-Share mit Viewer-URL.
- Phase-Lens gibt den Status-Panorama-Effekt (Grossteil Building,
  einige Planned-Highlights).
- Health-Lens fuer Backlog-Refinement-Sessions (was ist lose, was
  fehlt).

## Tool-Dateien

- `skills/v-model-workflow/tools/parse-graph.py` - Markdown -> JSON.
  Stdlib-only, keine Dependencies.
- `skills/v-model-workflow/tools/graph-viewer.html` - Standalone-
  Viewer mit Cytoscape.js (CDN).
- `skills/v-model-workflow/tools/open-graph.sh` - Wrapper, parst
  und oeffnet den Viewer.

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
{if Mode B:}
- Feature-ADR semantic:     {n}
- BA-Feature semantic:      {n}
- arc42-ADR semantic:       {n}
- Code-Feature semantic:    {n}
```

### 2. Backlog update in `{ROOT}/context/10_backlog.md`

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
   - `docs/requirements/epics/EPIC-*.md` -> Epics
   - `docs/requirements/features/FEATURE-*.md` -> Features
   - `docs/adr/ADR-*.md` -> ADRs
   - `docs/implementation/plans/PLAN-*.md` -> PLANs
   - `docs/analysis/BA-*.md` -> BA sections (parsed by headers)
   - `docs/architecture/arc42.md` -> arc42 sections
   - `docs/context/10_backlog.md` -> BL-Items
3. **Build the edge set.** Parse references in each node:
   - Feature's `Epic:` field -> edge to Epic
   - Feature's `Related ADRs:` -> edges to ADRs
   - Feature's `Source (Implementation):` -> edges to Code files
   - ADR's `Related Decisions:` / `References:` -> edges to ADRs/Features
   - BL-Item's Feature-Spec / ADR columns -> edges
   - arc42 Par. 9 table -> edges to ADRs
4. **Apply invariants.** For each check, list violations with file
   path and line number if possible.
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
  or is explicitly marked `Phase: Candidates` with `needs refinement`.
- `N-3` Every ADR is referenced at least once from a Feature, arc42,
  or Backlog entry.
- `N-4` Every Feature has at least one Success Criterion entry
  (may be placeholder `[AWAITING BA]` or `[AWAITING RE]`).
- `N-5` Every FEATURE with `status: Implemented` has a
  `## Codebase-Verifikation` section.
- `N-6` Every BL-Item has a Phase label
  (`Released | Building | Planned | Candidates`).
- `N-7` Every BL-Item with `Phase: Candidates` has a
  `needs refinement: {reason}` marker.

### Edge invariants

- `E-1` Every Markdown link to a project-internal path resolves.
- `E-2` Every FEATURE `Source (Implementation)` path exists or is
  explicitly noted as planned (Phase = Planned).
- `E-3` Every ADR listed in a FEATURE's Related-ADRs section exists.
- `E-4` Every ADR listed in arc42 Par. 9 exists in `docs/adr/`.
- `E-5` Every ADR under `docs/adr/` appears in arc42 Par. 9 or is
  explicitly deprecated/superseded.
- `E-6` Every BL-Item's Feature-Spec / ADR column links to an
  existing file.

### Semantic invariants (Mode B only)

- `S-1` FEATURE description does not contradict referenced ADRs.
- `S-2` FEATURE without a matching BA JTBD is flagged as
  `needs BA-anchor`.
- `S-3` arc42 sections describing an ADR's decision match the ADR's
  current Decision text (not an old revision).
- `S-4` `Implemented` FEATUREs have their key Success Criteria
  verifiable in the code (plausibility, not exhaustive).

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
  `/v-model-workflow` or `/reverse-engineering` first.

## Keywords

consistency check, graph check, Konsistenzpruefung, graph-health,
dead links, orphan features, orphan epics, orphan ADRs, V-Model
integrity, artifact graph, reference check, semantic drift,
backlog health
