---
title: Consistency Check
description: "Verify the V-Model artifact graph is intact: dead links, orphan features, status drift, ADR abstraction violations. Three modes (syntactic, semantic, interactive fix-loop)."
---

# Consistency Check

`/consistency-check` treats the V-Model artifacts as a graph: nodes
are artifacts (BA sections, Epics, Features, Success Criteria,
ADRs, arc42 sections, PLANs, Backlog rows, Wayfinder rows, code
files), edges are references between them. The skill answers one
question: **is the graph complete and consistent, or do we have
orphans, dead links, and semantic drift?**

It runs at every phase boundary in the V-Model, on demand from the
user, and from the pre-commit hook. It is the structural counter-
weight to the [three-layer documentation model](../concepts/three-layer-documentation):
the model defines where state lives, this skill verifies that
nobody let state escape.

## When to use

- The guide runs Mode A automatically at every phase
  boundary. You see a green "graph healthy" or a list of findings.
- Run `/consistency-check` before a release. Mode A is fast; Mode B
  catches semantic drift that the syntactic check cannot see.
- Run `/consistency-check --fix-interactive` after a Mode A run
  produced findings you want to walk through one by one.
- Run `/consistency-check --view` in a backlog grooming meeting.
  The interactive graph viewer surfaces orphans visually.

Trigger phrases that route to the skill: "consistency check",
"graph check", "check references", "dead links", "orphan features",
"graph-health", "Konsistenzpruefung".

## Three modes

### Mode A: syntactic (default, fast, no LLM)

Runs on every phase-end trigger and pre-commit hook. Pure
filesystem and grep, costs near zero. Eight quick-check items:

1. **Dead links.** Every Markdown link to a project-internal path
   resolves to an existing file.
2. **Backlog completeness.** Every artifact file under
   `_devprocess/requirements/`, `_devprocess/architecture/`,
   `_devprocess/implementation/plans/`,
   `_devprocess/requirements/fixes/`, and
   `_devprocess/requirements/improvements/` has exactly one row in
   `BACKLOG.md`. No artifact without a row, no row without an
   artifact.
3. **Backlog as single source.** Artifact frontmatter does NOT
   carry `status:` or `phase:` fields. The backlog row is
   authoritative. Frontmatter that duplicates these fields is
   flagged.
4. **Spec references valid.** Every Feature references a real
   Epic id; every backlog Refs entry resolves; every PLAN's
   `feature-refs`, `adr-refs`, `fix-refs`, `imp-refs` resolve.
5. **ADR references valid.** Every ADR id listed in a FEATURE's
   `adr-refs`, in arc42 Par. 9, in JSDoc headers, or in
   `src/ARCHITECTURE.map` resolves to an existing ADR file.
6. **ADR contradictions.** No two ADRs cover overlapping topics
   with opposing decisions (heuristic: similar titles or matching
   triggering ASRs).
7. **ADR abstraction rule.** No ADR contains code paths
   (`src/...`, file basenames, line numbers, method signatures)
   in the core sections (Context, Decision Drivers, Considered
   Options, Decision, Consequences). Code paths in the
   `## Implementation Notes` appendix are exempt.
8. **Backlog graph health.** Every Refs entry in the backlog
   points at an existing row. The graph derived from the Refs
   columns is acyclic (Epic -> Feature -> Plan -> Fix forms a DAG).

#### Auto-fix

`/consistency-check --fix` repairs the following drift types
automatically:

- Frontmatter `status:` or `phase:` field present: removed.
- Backlog row missing for an existing artifact: created with
  `Status: Planned` defaults.
- Dashboard counts out of sync with computed totals: rewritten.

Items that cannot be auto-fixed (orphan ADR, dead link, ADR
abstraction violation) are reported and left for the user.

### Mode B: semantic (on-demand, agent-based)

Runs on explicit user request or before a release. Subagents read
paired artifacts and judge whether their content is still
consistent. Six deep-check items:

1. **Spec-code coherence.** For every FEAT with status Done, are
   the Success Criteria plausibly verifiable in the code?
2. **Rule-set drift.** Compare `_devprocess/rules/technical.md`
   against the actual project state.
3. **Orphan artifacts.** FEAT Done in backlog but no entry-point
   in the wayfinder; entry-point in the wayfinder with no matching
   FEAT row.
4. **ADR duplication.** Two ADRs covering the same topic at
   different abstraction levels are flagged for consolidation.
5. **Wayfinder completeness.** Every substantive module has an
   ARCHITECTURE.map entry.
6. **Backlog graph render.** Mermaid or JSON graph from the
   backlog Refs columns, surfacing orphan nodes and status
   mismatches.

Mode B costs measurable agent-time. Run it before a release or
when Mode A has been clean for a while but you suspect deeper
drift.

### Mode C: interactive fix-loop

`/consistency-check --fix-interactive` walks every finding from
the latest Mode A run with the user, one by one. Each step ends
with an `AskUserQuestion`:

- One short recommendation sentence
- Two to four concrete fix options, each with `Pro:` and `Con:`
- A `Skip` option that defers without losing the finding
- A `Custom` option for free-form intervention

The loop persists across Claude Code sessions in
`.git/consistency-check.last-run.json`. If you exit mid-loop, the
next `--fix-interactive` invocation continues at the first
unresolved finding.

**Trust mode.** Saying "mach wie du denkst" or selecting trust
mode in the triage step delegates all fix decisions to the agent.
The loop applies the recommended option for every finding without
asking, except when:

- A finding has no clear recommendation
- A fix touches shared infrastructure (CI, hooks, governance)
- A fix would delete substance, not just a duplicate

In trust mode, the loop posts a one-line progress update every
ten fixes and produces a complete audit log at the end.

## Invocation

| Command | Effect |
|---|---|
| `/consistency-check` | Mode A, report only |
| `/consistency-check --fix` | Mode A with auto-fix |
| `/consistency-check --fix-interactive` | Mode C, walk findings with user |
| `/consistency-check --deep` | Mode A + Mode B |
| `/consistency-check --view` | Mode A and open the graph viewer in a browser |
| Called from another skill | Scoped check (e.g. one feature's neighbourhood) |
| Called from pre-commit hook | `--fix` first, then `--fix-interactive` if findings remain |

## Tooling

The Mode A driver lives in `tools/consistency-check.py` and runs
on any DIA project. Optional `dia.config.json` in the project
root overrides defaults. The pre-commit hook template is at
`tools/git-hooks/pre-commit`; install with
`bash tools/install-git-hooks.sh` from the target project.

The interactive graph viewer is a standalone HTML file
(Cytoscape.js, no build pipeline). `/consistency-check --view`
parses the graph in memory, passes it as a URL parameter, and
opens the default browser. The viewer offers Overview, Persona,
Phase, Health, and Epic-focus lenses; clicking a node opens the
file in the default editor. The viewer never edits, only
navigates.

## Output

Every run produces a console report (summary of node counts and
findings) plus a Graph-Health section in `BACKLOG.md`:

```markdown
## Graph-Health (last check: 2026-04-30, mode: A)

| Invariant | Status | Count |
|---|---|---|
| Dead links | ok | 0 |
| Orphan features | ok | 0 |
| Orphan ADRs | fail | 2 |
| Frontmatter status duplicate | ok | 0 |
| ADR abstraction violation | fail | 1 |
| Source paths broken | ok | 0 |
| Backlog format | ok | 0 |
| arc42-ADR table drift | ok | 0 |
```

Findings that represent real gaps become backlog rows in the
Standalone Items section with `Source = CONSISTENCY-CHECK`. The
skill deduplicates: a finding from a previous run that already
has a backlog row gets its Notes refreshed instead of a duplicate
row.

## When NOT to use

- Trivial edits (typo fix, single comment). The full check is
  overkill.
- Active refactoring where artifacts are intentionally in flux.
  Wait for the refactor to settle.
- Greenfield projects without V-Model artifacts. Bootstrap via
  `/dia-guide` or `/reverse-engineering` first.

## Read the skill file

[`skills/consistency-check/SKILL.md`](https://github.com/pssah4/digital-innovation-agents/blob/main/skills/consistency-check/SKILL.md)
on GitHub.

## See also

- [Three-layer documentation model](../concepts/three-layer-documentation):
  the structural rules this skill verifies
- [Project Conventions guide](./project-conventions): graph
  invariants reference
- [V-Model workflow guide](./dia-guide): the guide
  that runs Mode A at every phase boundary
