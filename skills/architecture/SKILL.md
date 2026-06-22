---
name: architecture
description: >
 Creates Architecture Decision Records (ADRs) in MADR format and arc42
 documentation. Generates plan-context.md as the context bridge to
 Claude Code. Use this skill when the user mentions "architecture",
 "ADR", "arc42", "Architecture Decision", "tech stack", "solution
 design", "system design", "architecture review", "plan-context", or
 similar. Also when requirements exist and the next step is technical
 structuring. This skill creates PROPOSALS. Claude Code makes the
 final decisions based on the real state of the codebase.
disable-model-invocation: false
---

# Architect

You turn requirements into architecture proposals: ADRs, an arc42
sketch, and a compact `plan-context.md` for Claude Code.

**Input:** Epics, Features, ASRs, NFRs from Requirements Engineering.
**Output:** ADR proposals, arc42 draft, `plan-context.md`.

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

## ADR completeness

Decision plus one-paragraph context, a two-option Pros/Cons table,
and labeled consequences bullets (Positive, Negative, Risks).
50-line cap. Every Critical ASR maps to exactly one ADR.

Filename: `ADR-{nn}-{slug}.md`, 2-digit, kebab-case. Template:
`templates/ADR-TEMPLATE.md`.

## arc42 scope

Always-required: section 1.2 (Quality Goals), 4 (Solution
Strategy), 9 (Architecture Decisions). Other sections only when
they carry a decision worth recording. Caps: 100 lines (MVP),
60 lines (PoC), 30 lines (Simple Test). Template:
`templates/arc42-TEMPLATE.md`.

## plan-context.md

Compact handoff to Claude Code. Cap 55 lines. Contains tech stack,
architecture style and quality goals, ADR summary table, external
integrations, and concrete performance / security values. Data
Model only when entities were actually designed. ADR summary floor
gated by scope: 1 for Simple Test, 2 for PoC, 3 for MVP.
Template: `templates/plan-context-TEMPLATE.md`.

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

### Phase 3: arc42

Write the always-required sections. Add any further section only
when a real decision needs a home. Respect the scope caps.

### Phase 4: plan-context.md

Write the compact handoff per the rules above.

### Mid-course requirements discovery

If the design reveals a gap, contradiction, or impossible
constraint in a FEATURE spec, stop the current ADR. Triage the
finding, write a short `REQ-REVIEW-{date}.md` under
`_devprocess/analysis/`, add a backlog row, and route the affected
FEATURE back to RE. Other ADRs continue. Architecting around a
broken spec carries the fault into the code.

## Quality gates

- Every Critical ASR has a matching ADR.
- `plan-context.md` tech stack matches every ADR Decision.
- ADRs offer real alternatives with Pros / Cons, not single-option
  rationalisation.
- `plan-context.md` carries concrete numbers, not vague qualifiers.

## Handoff Ritual

### Part 1: Artifact report

```
Produced / updated:
- _devprocess/architecture/ADR-*.md: {count} ADRs (statuses)
- _devprocess/architecture/arc42.md: arc42 draft
- _devprocess/requirements/handoff/plan-context.md: tech stack
```

### Part 2: Handoff context

Append an entry to `_devprocess/context/HANDOFFS.md` with tech
stack justification, rejected alternatives, known architectural
risks, open items deferred to `/coding`, and the
plan-context-vs-ADR consistency confirmation. Report ADR
consolidation moves explicitly.

### Part 3: Phase-end commit

Run the phase-end commit per
`skills/project-conventions/references/team-workflow.md` section
"Phase-end commit (binding)". Canonical message:

```
chore(arch): <ITEM-ID> ARCH complete

<one-line summary: N ADRs, arc42 sections X.Y, plan-context tech-stack>

Refs: <ITEM-ID>[, ADR-NN, ADR-NN]
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
