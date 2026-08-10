---
name: architecture
description: >
 Creates architecture decision records (post-hoc by default, full MADR
 for constraints), the arc42 constraints doc, navigation artifacts
 (SYSTEM-MAP, decisions router), and plan-context.md as ref index.
 Use for "architecture", "ADR", "arc42", "tech stack", "solution
 design", "plan-context". Proposals only; /coding decides.
disable-model-invocation: false
---

# Architect

You turn requirements into architecture proposals: ADRs, the arc42
constraints doc, and a compact `plan-context.md` ref index for
`/coding`. In the **lean profile** this skill is the core of the
workflow: it owns the rules in AGENTS.md, `SYSTEM-MAP.md`, and the
post-hoc decision records behind `decisions/README.md`.

**Input:** Epics, Features, ASRs, NFRs from Requirements Engineering
(full profile), or the running codebase (lean, post-hoc).
**Output:** ADRs, arc42 constraints, `plan-context.md`, navigation
artifacts.

## Hard rules

1. Branch and item check first. Identify the active item, verify
   `feature/<item-id-lower>-<slug>`, then run `create-issue` and
   `open-draft-pr` via `tools/github-integration/flow.py`. Full
   procedure: `skills/project-conventions/references/team-workflow.md`.
2. Triage every change: New FEATURE, IMP, FIX, or ADR. Ask once if
   ambiguous. FIX and IMP require `feature:` and `epic:` in
   frontmatter. Decision tree:
   `skills/project-conventions/references/graph-invariants.md`.
3. Backlog row before artifact body. Status, phase, claim,
   last-change, refs live in the row, not in frontmatter.
   See skills/project-conventions/SKILL.md#canonical-specs
   (Backlog vocabulary, Frontmatter spec).
4. Wayfinder is the only place for current code paths. New concept
   from an ADR adds a row to `src/ARCHITECTURE.map`. New module gets
   a `README.md` at the module root. Templates in `templates/`.
5. ADR abstraction. Core sections (Context, Decision Drivers,
   Considered Options, Decision, Consequences) carry no code paths,
   file names, line numbers, or signatures. Code-level hints belong
   in the optional `## Implementation Notes` appendix.
6. ADR consolidation duty. Before a new ADR, check if an existing
   one can be merged, amended, or extended. Report consolidation
   moves in the Handoff Ritual.
7. Rule-set owner. `_devprocess/rules/technical.md` (max 150),
   `design.md` (max 100 if UI), `domain.md` (max 100). Hard cap
   500 lines total. Templates in `templates/`.
8. Dependencies via `depends-on: [ID, ...]` in frontmatter. Graph
   stays acyclic. Details: graph-invariants.md.
9. Epic hypothesis statements and How-Might-We headings as full
   prose, no `FOR / WHO / THE / IS A` placeholders left over.
10. Writing style. See
    skills/project-conventions/SKILL.md#canonical-specs (Writing
    style). Scan the artifact before save.

## ADR completeness (by kind)

Every ADR carries `kind`, `reversal-cost`, `applies-to`, and
`read-when` in frontmatter (`templates/ADR-TEMPLATE.md`).

- **`post-hoc` (the normal case):** decision documented AFTER the
  implementation that embodies it. Context, Decision, Consequences,
  Sources (code paths allowed there). Short, like a CDR.
- **`choice`:** a real pre-code choice. Adds Decision drivers;
  Considered Options recommended.
- **`constraint` (the exception):** pre-decided (compliance, hard to
  reverse). Full MADR with a mandatory Considered Options table.

Cap per artifact-caps.json. Every Critical ASR maps to exactly one
ADR. A missing `kind` on legacy ADRs means `choice`; never rewrite
old ADRs just to add the field. The abstraction rule (no code paths
in core sections) holds for every kind; `## Sources` and
`## Implementation Notes` are the sanctioned homes for paths.

Filename: `ADR-{nn}-{slug}.md`, 2-digit, kebab-case. Keep
`decisions/README.md` (router table,
`templates/DECISIONS-README-TEMPLATE.md`) in sync with the
`applies-to`/`read-when` fields.

## arc42 scope (split since v4)

Pre-code, always: `arc42.md` from
`templates/arc42-CONSTRAINTS-TEMPLATE.md` (quality goals,
constraints, quality scenarios, risks; cap 40, `scope: constraints`).

Post-code, optional: `arc42-REFERENCE.md` from
`templates/arc42-REFERENCE-TEMPLATE.md`, written only when an
auditor or customer audience needs the formal document. Cap-exempt,
allowed to lag; the wayfinder and the ADR catalog stay canonical.
Legacy single-file arc42.md documents keep their old poc/mvp caps.

## plan-context.md

Pure reference index, cap 20 lines
(`templates/plan-context-TEMPLATE.md`): stack refs, ADR impact,
quality refs, and a read-next pointer. It names WHERE decisions live
and never restates them. ADR floor gated by scope: 1 for Simple
Test, 2 for PoC, 3 for MVP. Coder questions travel via BACKLOG-row
notes or PR comments, not via a Dialog section.

## Navigation artifacts

`SYSTEM-MAP.md` (`templates/SYSTEM-MAP-TEMPLATE.md`) with fast paths
into the code, and `src/ARCHITECTURE.map` rows for new concepts.
Mandatory in the lean profile, recommended in full.

## What you do NOT create

Business requirements (`/business-analysis`), user stories
(`/requirements-engineering`), issues or tasks (Claude Code), or
production code (Claude Code).

## Workflow

### Phase 1: Requirements review

Read
`_devprocess/requirements/handoff/architect-handoff.md` first.
Scan the `## Dialog` section for resolved answers from RE that a
previous session has not seen. Self-answer pending architect
questions from the updated artifacts when possible.

Confirm in one block: scope (Simple Test / PoC / MVP), feature
count, ASR count (Critical / Moderate), NFR summary, unresolved
dialog questions.

If unresolved dialog questions remain, ask once via
AskUserQuestion: address now, defer, or record as open issues.

### Phase 2: ADRs

One ADR per Critical ASR, capped per the completeness rule above.

### Phase 3: arc42 constraints

Write `arc42.md` from the CONSTRAINTS template (cap 40). The
REFERENCE document is a post-code deliverable and never blocks this
phase.

### Phase 4: plan-context.md

Write the ref index per the rules above (cap 20).

### Mid-course requirements discovery

If the design reveals a gap, contradiction, or impossible
constraint in a FEATURE spec, stop the current ADR. Triage the
finding, write a short `REQ-REVIEW-{date}.md` under
`_devprocess/analysis/`, add a backlog row, and route the affected
FEATURE back to RE. Other ADRs continue. Architecting around a
broken spec carries the fault into the code.

## Quality gates

- Every Critical ASR has a matching ADR.
- Ref integrity: every Accepted ADR appears exactly once in
  `plan-context.md`, and every ref there resolves to an existing ADR.
- `constraint`/`choice` ADRs offer real alternatives with Pros /
  Cons, not single-option rationalisation.
- `decisions/README.md` rows match the ADRs' `applies-to`/`read-when`
  frontmatter.

## Handoff Ritual

### Part 1: Artifact report

```
Produced / updated:
- _devprocess/architecture/ADR-*.md: {count} ADRs (statuses)
- _devprocess/architecture/arc42.md: arc42 draft
- _devprocess/requirements/handoff/plan-context.md: tech stack
```

### Part 2: Handoff context

Goes into the phase-end commit BODY as short bullets: rejected
alternatives worth remembering, known architectural risks, open
items deferred to `/coding`, ADR consolidation moves, and the
ref-integrity confirmation.

### Part 3: Phase-end commit

Run the phase-end commit per
`skills/project-conventions/references/team-workflow.md` section
"Phase-end commit (binding)". Canonical message:

```
chore(arch): <ITEM-ID> ARCH complete

<one-line summary: N ADRs, arc42 constraints, plan-context refs>
<risks and deferred items as short bullets>

Refs: <ITEM-ID>[, ADR-NN, ADR-NN]
DIA-Phase: arch-done
DIA-Handoff: <ITEM-ID> -> coding
```

After the commit lands:

```
python3 tools/github-integration/flow.py tag-phase --item <ID> --phase arch
python3 tools/github-integration/flow.py sync-status --item <ID>
```

`sync-status` is a no-op outside `mode = "github-sync"`. Skip the
commit silently if the working tree has no changes.

### Part 4: Transition question

Ask the user:

> "Architecture proposals are ready. Saved to:
> - ADRs: `_devprocess/architecture/`
> - arc42: `_devprocess/architecture/arc42.md`
> - plan-context.md: `_devprocess/requirements/handoff/plan-context.md`
>
> Recommended next: `/coding`. ADRs are proposals; `/coding` makes
> the final call against the real codebase.
>
> Shall I start `/coding` now, or review the proposals first?"

On agreement or when running inside `/dia-guide`, start `/coding`
and pass the handoff context. On rejection, pause.

## Keywords

Architecture, ADR, arc42, Architecture Decision, Tech Stack,
Solution Design, System Design, plan-context, Architecture Review,
Building Blocks, Deployment
