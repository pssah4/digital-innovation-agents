---
title: Artifacts
description: The _devprocess/ directory structure, the wayfinder layer, the rule sets, and the files every phase produces.
---

# Artifacts

Every V-Model phase produces artifacts that feed the next phase. All
user-project artifacts split across **four locations** by purpose:

- `src/ARCHITECTURE.map` and module READMEs in `src/{module}/README.md`
  for the **wayfinder** layer (concept-to-file lookup)
- `_devprocess/rules/` for the **rule sets** (stable truths)
- `_devprocess/context/BACKLOG.md` for **state** (single source of
  truth)
- everything else under `_devprocess/` for **detail artifacts**
  (audit trail of decisions and process)

This split is the structural fix for the most common drift class:
status fields stuck at "Planned" while the code shipped. See the
[Three-layer documentation model](../concepts/three-layer-documentation).

## Directory tree

```
{project}/
  src/
    ARCHITECTURE.map               Wayfinder root: concept | entry-point | adr | how-to-extend
    {module}/README.md             Module wayfinder (one per substantive module)
  _devprocess/
    analysis/                      Flat. BA layers (Project-BA + Item-BA), EXPLORE, AUDIT, RESEARCH.
      BA-{PROJECT}.md                       Phase 1: Project-BA singleton (product layer)
      BA-EPIC-{nn}-{slug}.md                Phase 1: Item-BA per new epic (mandatory before EPIC)
      BA-FEAT-{ee}-{ff}-{slug}.md           Phase 1: Item-BA per new feature (mandatory before FEAT)
      BA-IMP-{ee}-{ff}-{nn}-{slug}.md       Phase 1: Item-BA per improvement (optional)
      BA-FIX-{ee}-{ff}-{nn}-{slug}.md       Phase 1: Item-BA per fix (optional)
      EXPLORE-{PROJECT}.md         Phase 1: Exploration Board (PoC/MVP)
      RESEARCH-{TOPIC}.md          Phase 1: Discovery research notes
      AUDIT-{PROJECT}-{YYYY-MM-DD}.md  Phase 6: Security audit report (flat, no subfolder)
      sources/                     User-supplied source files (only subfolder under analysis)
        SOURCE-{name}.{ext}
    requirements/
      epics/
        EPIC-{nn}-{slug}.md        Phase 2: Epic spec
      features/
        FEAT-{ee}-{ff}-{slug}.md   Phase 2: Feature spec (epic-local numbering)
      fixes/
        FIX-{ee}-{ff}-{nn}-{slug}.md   Phase 4 / bug-capture: Fix detail
      improvements/
        IMP-{ee}-{ff}-{nn}-{slug}.md   Phase 4: Improvement detail
      handoff/
        architect-handoff.md       Phase 2 -> 3: aggregated ASRs + NFRs
        plan-context.md            Phase 3 -> 4: tech stack + integrations
    architecture/
      ADR-{nn}-{slug}.md           Phase 3: Architecture Decision Record (MADR)
      arc42.md                     Phase 3: arc42 documentation
    rules/                         Stable rule sets, hard cap 500 lines TOTAL
      technical.md                 Stack, conventions, library choices
      design.md                    UI rules (only if project has UI)
      domain.md                    Domain glossary, business invariants
    implementation/
      plans/
        PLAN-{nn}-{slug}.md        Phase 4: persisted implementation plan
    context/
      BACKLOG.md                   Single source of truth for project state
                                   (per BACKLOG-TEMPLATE.md). Status, phase,
                                   last-change, and claim live HERE.
      HANDOFFS.md                  Append-only phase handoffs log (all phases)
      METRICS.md                   Signal layer (per METRICS-TEMPLATE.md):
                                   cycle time, drift count, hypothesis status,
                                   phase transitions, cross-phase triggers
```

There is no `analysis/security/` subfolder. Audit reports are flat
under `analysis/`.

There is no `20_bugs.md` file. Bugs live as `FIX-{ee}-{ff}-{nn}` rows
in `BACKLOG.md` plus a detail file at
`_devprocess/requirements/fixes/FIX-{ee}-{ff}-{nn}-{slug}.md`.

## Wayfinder layer

The wayfinder is the canonical answer to "where does X live in the
code?". A model can grep one file and get a single, current,
machine-readable answer. The wayfinder updates with every code edit
that creates or renames an entry-point. Detail artifacts (ADRs,
features) reference concepts by name, not by file path.

### `src/ARCHITECTURE.map`

A pipe-delimited table:

```
concept              | entry-point                          | adr      | how-to-extend
---------------------|--------------------------------------|----------|----------------
semantic-search      | src/search/semantic.ts:export class  | ADR-03   | Add a new SearchProvider in src/search/providers/
embedding-provider   | src/embed/provider.ts:export factory | ADR-07   | Implement EmbeddingProvider interface
backlog-parser       | src/backlog/parser.ts:export class   | ADR-12   | Extend ParserRule registry
```

### Module READMEs

Each substantive module under `src/{module}/` carries a 5- to 30-line
`README.md` describing what the module owns, the entry points, the
ADRs it implements, and how to extend it. Module READMEs do not
duplicate detail artifacts; they point to them.

### JSDoc / docstring headers

Every exported entry-point that ARCHITECTURE.map references carries a
header comment with: one-line purpose, the ADRs it implements, and a
link to the feature id it serves.

## Rule sets

Stable truths that change rarely. Hard cap **500 lines total** across
the three files. If you cross the cap, condense or move detail to an
ADR.

### `_devprocess/rules/technical.md`

Stack, libraries, conventions, language version, build tool,
deployment target. The technical bedrock that every coding decision
stands on.

### `_devprocess/rules/design.md` (only if UI)

UI design system, component library, accessibility rules, typography,
spacing, colour tokens.

### `_devprocess/rules/domain.md`

Glossary of domain terms, business invariants, regulated language.
What an `Order` is, what a `Member` is, what counts as `revenue`.

## Detail artifacts

Detail artifacts hold the substance that does not age fast: problem,
decision, rejected alternatives, success criteria, reasoning. They
do **not** list current code paths in core sections.

- ADRs are allowed an optional `## Implementation Notes` appendix
  that may go stale.
- FEATUREs are allowed an optional `## Code Pointer` appendix that
  references an ARCHITECTURE.map concept name, not a file path.
- FEATUREs (since v3.2.0) carry `subtype: user-facing | library` in
  frontmatter and a mandatory `## Activation Path` section in the
  Definition of Done. The Activation Path is a Type/Identifier pair
  that names how a user or caller reaches the FEATURE. See
  [Conventions: required frontmatter](./conventions#required-frontmatter)
  and the [requirements engineering guide](../guides/requirements-engineering)
  for the full contract.

## Living documents

Artifacts are not one-off specifications. They are continuously
updated during and after implementation. At the end of a V-Model
cycle, every detail artifact reflects the actually-implemented state,
not the originally-planned state. State lives in the backlog row, not
in the artifact frontmatter, so a status change touches one place.

See [Living Documents](../concepts/living-documents).

## The three context files

`BACKLOG.md`, `HANDOFFS.md`, and `METRICS.md` serve different
purposes:

- **`BACKLOG.md`** is the **single source of truth for project
  state**. Follows the binding format in
  [`skills/requirements-engineering/templates/BACKLOG-TEMPLATE.md`](https://github.com/pssah4/digital-innovation-agents/blob/main/skills/requirements-engineering/templates/BACKLOG-TEMPLATE.md):
  dashboard on top, entries grouped by Epic (`FEAT-EE-FF`,
  `FIX-EE-FF-NN`, `IMP-EE-FF-NN`, `PLAN-NN`, `ADR-NN` rows with
  status, phase, priority, **Claim** (`{pair-id} @ YYYY-MM-DD`), Refs,
  source, commit), standalone items for epic-free findings, deferred
  items. Every phase skill that changes project state updates this
  file BEFORE touching the artifact body. The Claim column lets
  multiple human-agent pairs work the backlog concurrently without a
  central lock service. The pair-id convention is
  `{human-handle}-{model}`, for example `seb-opus-4-7`.
- **`HANDOFFS.md`** is an append-only phase handoffs log. Each phase
  skill appends one entry at the end of its run with artifacts
  produced, handoff context (open questions, assumptions, risks), and
  the next phase. the Closing Handoff also appends a
  `release-to-ba` entry that queues the BA Post-Release Review.
- **`METRICS.md`** is the signal layer. Five append-additive tables
  seeded from
  [`skills/dia-guide/templates/METRICS-TEMPLATE.md`](https://github.com/pssah4/digital-innovation-agents/blob/main/skills/dia-guide/templates/METRICS-TEMPLATE.md):
  cycle time per FEAT, drift count (wayfinder vs. real code), BA
  hypothesis validation status, phase transition counts, cross-phase
  trigger counts. Writes happen inside existing phase actions, no
  separate metrics-collection ceremony. Rows are never deleted.

## Traceability chain

```
Project-BA + Item-BA in analysis/ (Why?)
  -> Epic / Feature spec with `ba-ref:` (What?)
    -> Feature spec (What, concrete?)
      -> ASR (What is architecture-relevant?)
        -> ADR (How do we solve it?)
          -> Wayfinder + plan-context.md (Where does it live?)
            -> PLAN-NN (Concrete tasks)
              -> Code (Implementation)
                -> Tests (Does it work?)
                  -> Security Audit (Is it safe?)
                    -> Closing Handoff (consistency-check mode B + optional release)
                      -> BA Post-Release Review (Did the hypothesis hold?)
```

Every step writes back into the source artifacts (substance) and into
the backlog (state). Status changes always go through the backlog row
first, so the chain is never silently broken.

## Project initialization

When starting a new project, initialize the structure:

```bash
mkdir -p _devprocess/{analysis/sources,requirements/{epics,features,fixes,improvements,handoff},architecture,rules,implementation/plans,context}
touch _devprocess/context/HANDOFFS.md
cp skills/requirements-engineering/templates/BACKLOG-TEMPLATE.md \
   _devprocess/context/BACKLOG.md
cp skills/dia-guide/templates/METRICS-TEMPLATE.md \
   _devprocess/context/METRICS.md
cp skills/project-conventions/templates/technical.md \
   _devprocess/rules/technical.md
cp skills/project-conventions/templates/domain.md \
   _devprocess/rules/domain.md
# only if the project has UI surface:
cp skills/project-conventions/templates/design.md \
   _devprocess/rules/design.md
touch src/ARCHITECTURE.map
```

`BACKLOG.md`, `METRICS.md`, and the rule files are seeded from the
templates (not created empty) so the first write already follows the
binding format. Replace `{PROJECT}` in the header with the actual
project name.

The `/project-conventions` skill runs this for you if you invoke it.

## See also

- [Conventions](./conventions): naming rules, frontmatter, language
  conventions
- [V-Model concept](../concepts/v-model): why this structure
- [Living Documents concept](../concepts/living-documents)
- [Three-layer documentation model](../concepts/three-layer-documentation):
  the rationale behind the wayfinder / rules / backlog / detail split
