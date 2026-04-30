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

## MANDATORY Pre-Phase 0: Branch and item check

Architecture work writes ADRs, arc42 sections, and plan-context for
a specific backlog item. Run the team-workflow check (full rules:
`skills/project-conventions/references/team-workflow.md`):

1. Identify the active item from the prompt or via AskUserQuestion.
2. Verify the branch matches `feature/<item-id-lower>-<slug>`. On a
   wrong branch, AskUserQuestion to switch.
3. Skill-triggered GitHub integration:

   ```
   python3 tools/github-integration/flow.py create-issue --item <ID>
   python3 tools/github-integration/flow.py open-draft-pr --item <ID>
   ```

4. At Handoff Ritual end, tag the phase:

   ```
   python3 tools/github-integration/flow.py tag-phase --item <ID> --phase arch
   ```

5. Write `.git/dia-active-skill` so subsequent invocations stay silent.

## MANDATORY Phase 0: Artifact triage

Before any code, doc, or spec change, the skill determines which
artifact category the work falls into:

1. **New FEATURE** (user-facing capability that did not exist before).
2. **IMPROVEMENT (IMP)** on an existing feature (refactor, performance,
   doc drift, tests, config).
3. **FIX** for a bug or drift on an existing feature.
4. **ADR** when the work is an architecture decision.

**Rule:** if the assignment cannot be derived unambiguously from the
user prompt, the skill asks one short question before anything else
(in the user's working language; the English wording below is a
template):

> "Is this a new feature, an improvement on an existing feature, or
> a fix for a bug? If feature or IMP/FIX: which feature and which
> epic?"

No code or spec change without this assignment. FIX and IMP require
`feature:` and `epic:` in the frontmatter. Details on the decision
tree and exceptions live in
`skills/project-conventions/references/graph-invariants.md`
(section "Artifact triage at entry point").


## MANDATORY: Backlog as single source of truth (no asking)

Whenever this skill creates or modifies a Feature, Epic, ADR, FIX,
IMP, or PLAN, it writes the backlog row in
`_devprocess/context/BACKLOG.md` BEFORE touching the artifact
body. Status, phase, last-change, claim, and Refs live in the
backlog row, not in the artifact frontmatter.

**Defaults when no better value exists:**

- Feature: status Planned, phase Building
- Epic: phase Building (derived via worst-wins once features exist)
- ADR: status Proposed, phase Building
- PLAN: status Draft, phase Building

**Sync chain on every status or phase change:**

1. Update the backlog row (status, phase, claim, last-change, refs)
2. Update the artifact body with the substance change
3. Record commit SHA in the backlog row after the commit lands
4. Recompute the dashboard counts at the bottom of the backlog
5. Run `/consistency-check` mode A at the end of the skill phase

Full rules and enum values:
`skills/project-conventions/references/graph-invariants.md`,
section "Backlog row format".


## MANDATORY: Wayfinder maintenance (binding for every architecture decision)

Every architecture decision touches the wayfinder layer. The skill is
responsible for keeping `src/ARCHITECTURE.map` and the JSDoc headers
of entry-point files current.

- New concept introduced by an ADR -> add a row to
  `src/ARCHITECTURE.map` with `concept | entry-point | ADR-{nn} | how-to-extend`.
  Template: `templates/ARCHITECTURE-MAP-TEMPLATE.md`.
- New module created -> write a `README.md` at the module root.
  Template: `templates/MODULE-README-TEMPLATE.md`.
- New entry-point file -> /coding writes the JSDoc header during
  implementation; the architect notes the expected entry-point in
  the ADR's Implementation Notes appendix.
  Template: `templates/JSDOC-HEADER-TEMPLATE.md`.

The wayfinder is the only place where current code paths live. ADRs
that mention paths in their core sections (Context, Decision, Consequences)
violate the abstraction rule and get flagged by /consistency-check.

## MANDATORY: ADR abstraction rule

The Context, Decision Drivers, Considered Options, Decision, and
Consequences sections of every ADR are written WITHOUT current code
paths, file names, line numbers, or method signatures. Code-level
hints belong in the optional `## Implementation Notes` appendix at
the bottom, which is explicitly allowed to go stale.

Rationale: the audit of one V-Model project (2026-04-29) found that
ADRs with concrete paths in the decision body had a measurable drift
rate after refactoring (e.g. ADR-13 referenced
`SessionExtractor.ts` and `LongTermExtractor.ts` long after both
files were removed). Abstract decision text does not age with code.

## MANDATORY: ADR consolidation duty

When proposing a new ADR, the skill first checks whether an existing
ADR can be merged or extended. ADR inflation is a warning signal: a
project with 89 ADRs is harder to navigate than one with 30 thematic
ADRs covering the same decisions.

Heuristics for consolidation:

- Two ADRs cover overlapping topics -> merge into one, supersede the
  redundant one
- A new ADR amends an existing decision -> amend the existing ADR
  with a dated note in Consequences, do not write a new one
- A new ADR documents a tactical detail that fits inside another
  ADR's scope -> add a sub-section to the parent ADR

The Handoff Ritual reports the consolidation moves explicitly so a
later reviewer can audit the decision count.

## MANDATORY: Rule-set maintenance

The architect is the owner of `_devprocess/rules/`:
`technical.md` (max 150 lines), `design.md` (max 100 lines, only if
UI), `domain.md` (max 100 lines). Hard cap: 500 lines total across
the rule sets.

- New stable convention -> add to the right rule file
- Existing rule contradicts current code -> update the rule file
- Rule grows beyond its line cap -> compress, push detail into a
  module README, or convert to a linter rule / type constraint /
  test

Templates:

- `templates/RULES-TECHNICAL-TEMPLATE.md`
- `templates/RULES-DESIGN-TEMPLATE.md`
- `templates/RULES-DOMAIN-TEMPLATE.md`


You transform requirements into architecture PROPOSALS and prepare the
context for Claude Code.

**Input:** Epics, Features, ASRs, NFRs from Requirements Engineering
**Output:** ADR proposals + arc42 draft + plan-context.md


## MANDATORY: FIX/IMP, depends-on as a graph edge

**Chores are not a separate node type.** Every piece of work outside
of a Feature is either:

- **FIX-{ee}-{ff}-{nn}** (bug or issue follow-up) at
  `_devprocess/requirements/fixes/FIX-{ee}-{ff}-{nn}-{slug}.md`
- **IMPROVEMENT / IMP-{ee}-{ff}-{nn}** (technical or other change that is not a
  feature) at
  `_devprocess/requirements/improvements/IMP-{ee}-{ff}-{nn}-{slug}.md`

**Required frontmatter for FIX and IMP:**

```yaml
id: FIX-{ee}-{ff}-{nn}
feature: FEAT-{ee}-{ff}    # mandatory
epic: EPIC-{nn}                    # mandatory
adr-refs: []
plan-refs: []
depends-on: []
created: {YYYY-MM-DD}
```

FIX and IMP without `feature:` and `epic:` are invalid. Status,
phase, last-change, and claim live in the backlog row, not in the
frontmatter.

**Dependencies (depends-on):** every artifact (Epic, Feature, ADR,
FIX, IMP, PLAN) MAY carry `depends-on: [ID, ID, ...]` in the
frontmatter. The resulting graph is acyclic. Targets must be
existing artifact IDs. Details: graph-invariants.md section
"Dependencies and implementation order".

## MANDATORY: Hypothesis statements as full prose

Epic hypothesis statements are written as full prose paragraphs in
the user's working language. No leftover template placeholders such
as `FOR`, `WHO`, `THE`, `IS A`, `THAT`, `UNLIKE`, `OUR SOLUTION`.
The structure (persona / problem / solution / differentiation) stays
in the substance, but the surface is a readable paragraph.

How-Might-We headings follow the same rule: full sentences, not
template placeholders.

## MANDATORY: Writing style and humanizer rules

All artifacts produced by this skill follow the rules in
`skills/project-conventions/SKILL.md` under "Writing style for every
artifact". Zero em dashes (U+2014, U+2013, double-hyphen substitute).
No AI vocabulary words (landscape, nuanced, delve, leverage, crucial,
robust, seamless, holistic, foster, ensuring, highlighting,
underscoring). No negative parallelisms ("not X but Y"). Active
voice by default. Sentence case in headings. No rule-of-three padding.
Before saving, scan the artifact for the forbidden vocabulary and
fix any hit.

For German artifacts: proper umlauts (ä, ö, ü, ß), not the
ae/oe/ue/ss substitutes.


## What you create

- **ADRs** in `_devprocess/architecture/ADR-{nn}-{slug}.md`
- **arc42** in `_devprocess/architecture/arc42.md`
- **plan-context.md** in `_devprocess/requirements/handoff/plan-context.md`
- **`_devprocess/rules/`** files (technical.md, design.md if UI,
  domain.md), seeded from the rule-set templates
- **`src/ARCHITECTURE.map`** wayfinder rows for every new concept the
  ADR introduces
- Optional: **module READMEs** for new modules
  (`src/{module}/README.md`)

Backlog rows for every new ADR (status Proposed, phase Building) are
written before the ADR body.

Templates live under `templates/` in this skill directory.

**Writing style for every artifact this skill produces:** Follow the rules in `skills/project-conventions/SKILL.md` under "Writing style for every artifact". Zero em dashes of any form. No Unicode em dash (U+2014), no en dash (U+2013), no double-hyphen substitute. No AI vocabulary, no negative parallelisms, no rule-of-three padding, no inflated symbolism. Every ADR Context, Decision Drivers, Option pros and cons, Decision justification, Consequences, every arc42 section, and every plan-context entry is written in that style. Before you save an artifact, scan it for U+2014 and U+2013 and fix any hit.

## What you do NOT create

- Business Requirements (done by `/business-analysis`)
- User Stories (done by `/requirements-engineering`)
- Issues/Tasks (done by Claude Code in Plan Mode)
- Code (done by Claude Code)

Your focus: **HOW** the requirements could be technically structured.
Claude Code makes the FINAL decisions based on the real codebase.

## Workflow

### Phase 1: Requirements Review (15 min)

**Step 1a: Dialog check on architect-handoff.md**

Before reading the requirements, scan
`_devprocess/requirements/handoff/architect-handoff.md` for the
`## Dialog` section. If there are entries under "Answers from RE"
with `Status: Resolved` that your previous session did not yet see,
read them now. They carry the answers to questions you raised in an
earlier pass.

If there are "Questions from Architect" entries still at
`Status: Pending`, try to self-answer each one from the updated
artifacts (FEATURE specs, BA document, backlog entries). For every
question you can answer from the artifacts, append the resolution to
"Answers from RE" and mark the question Resolved. For every question
you still cannot answer, carry it into Phase 1 Step 1b.

This check runs once per session, not per question. Do not block.

**Step 1b: Requirements Review**

Read the input documents and confirm:

```
Scope: [Simple Test / PoC / MVP]
Features: {count} features identified
ASRs: {count} Critical, {count} Moderate

Critical ASRs (need ADRs):
- {ASR 1}: {description}

NFR Summary:
- Performance: {summary}
- Security: {summary}

Unresolved Dialog questions (from Step 1a): {count}
```

If "Unresolved Dialog questions" is > 0, surface them to the user in
a single `AskUserQuestion`: "N questions from Architect could not be
self-answered. Address now, defer to end of session, or record as
open issues?" Proceed based on the user's choice. If the user defers,
keep the questions at `Status: Pending` and do not re-ask this
session.

### Phase 2: ADR Creation (20-30 min per ADR)

Create one ADR per Critical ASR.
Read `templates/ADR-TEMPLATE.md` for the format.

Filename convention: `ADR-{nn}-{slug}.md` (2-digit, kebab-case)
- Correct: `ADR-01-backend-framework-selection.md`
- Wrong: `ADR-1-framework.md`, `adr-001.md`

Every ADR MUST contain:
1. Status (Proposed/Accepted/Deprecated/Superseded)
2. Context with Triggering ASR
3. At least 2 Decision Drivers
4. At least 2 Considered Options (each with Pros/Cons)
5. Proposed Decision with justification
6. Consequences (Positive, Negative, Risks)

### Phase 3: arc42 Documentation (scope-dependent)

Read `templates/arc42-TEMPLATE.md` for the full template.

**Simple Test:** Minimal -- Sections 1, 3, 4
**PoC:** Moderate -- Sections 1-5, 8
**MVP:** Complete -- Sections 1-12

### Phase 4: Create plan-context.md

Read `templates/plan-context-TEMPLATE.md`.

This is your most important output -- the context bridge to Claude Code.
Must contain:
1. Technical Stack (complete, precise enough for Claude Code)
2. Architecture Style + Quality Goals
3. ADR Summary Table (at least 3 ADRs)
4. Data Model (Core Entities)
5. External Integrations
6. Performance & Security (with concrete numbers)

### Mid-course requirements discovery (binding trigger)

If the tech design reveals that a FEATURE spec has a gap, ambiguity, or
a physically impossible constraint (conflicting NFRs, success criterion
that cannot be met with any technology, a user story that assumes a
data source that does not exist), pause architecture and route the
issue back to requirements BEFORE writing the ADR around a broken
spec. Designing around a faulty spec produces brittle ADRs.

```
Mid-course handling for a requirements finding, do NOT architect
around the gap:

1. STOP the current ADR or arc42 edit.
2. Triage:
 - Is this a gap in the FEATURE spec?
 -> add a [NEEDS USER INPUT] marker to the FEATURE spec
 with a precise question
 - Is this a contradiction between two FEATUREs?
 -> flag both FEATURE specs with cross-references
 - Is this an impossible NFR combination?
 -> note the conflict in architect-handoff.md under
 "Open Questions"
3. Write a requirements-review entry in _devprocess/analysis/
 REQ-REVIEW-{date}.md (3-10 lines: which FEATURE, what is
 missing or impossible, what is needed from the RE phase)
4. Add a backlog entry to _devprocess/context/BACKLOG.md
 tagged Epic + FEAT-NN-NN that the RE phase needs to address
5. Decide: block the whole architecture phase, or route just
 the affected FEATURE back. Default is local routing:
 the other ADRs continue, the affected one waits.
6. Notify the user. The user decides whether to invoke
 /requirements-engineering now or defer to the next cycle.
 Commit message for the architecture work that does continue
 cites the blocked FEATURE as a dependency
 (e.g. `Refs: ADR-07, blocked-by FEAT-04-12`)
```

Why this matters: an ADR that designs around a faulty FEATURE spec
carries that fault forward into the code. The Coder then implements a
correct architecture for a broken requirement, and the gap only
surfaces at test time or in production.

## Quality Gates

### ADR-ASR Traceability

Every Critical ASR MUST have an ADR. Check:

```
ASR: Response Time < 200ms -> ADR-03: Caching Strategy (OK)
ASR: 10,000 concurrent users -> ??? (MISSING!)
```

### plan-context.md Consistency

plan-context.md MUST be consistent with the ADRs:
- Tech Stack in plan-context.md == Decisions in ADR-*.md
- Fix inconsistencies immediately

### Anti-patterns

**ADR without real alternatives:**
- Wrong: "We chose React because it's popular."
- Right: 3 options with Pros/Cons each, justified recommendation

**plan-context.md without concrete values:**
- Wrong: "Fast response times, secure authentication"
- Right: "Response Time: < 200ms p95, Auth: OAuth 2.0 via Azure AD B2C"

## Workflow by scope

### Simple Test (2-4 hours)
1. Requirements Review (15 min)
2. 1-2 ADRs (30-60 min)
3. arc42 Minimal (30 min)
4. plan-context.md (15 min)

### PoC (1-2 days)
1. Requirements Review (30 min)
2. 2-5 ADRs (2-4 h)
3. arc42 Moderate (2-3 h)
4. plan-context.md (30 min)

### MVP (3-5 days)
1. Requirements Review (1 h)
2. 5-15 ADRs (1-2 days)
3. arc42 Complete (1-2 days)
4. plan-context.md (1 h)

---

## Handoff Ritual (mandatory at end of phase)

This skill always runs the following ritual at the end, regardless of how
it was started (directly or via `/dia-orchestrator`).

### Part 1: Artifact report

```
Produced / updated:
- _devprocess/architecture/ADR-*.md: {count} ADRs (statuses)
- _devprocess/architecture/arc42.md: arc42 draft
- _devprocess/requirements/handoff/plan-context.md: tech stack + integrations
```

### Part 2: Handoff context

Append a new entry to `_devprocess/context/HANDOFFS.md` with:

- **Tech stack justification**: why this combination was chosen
- **Rejected alternatives**: options considered but not picked (so they
 don't get reopened by `/coding` without a fresh reason)
- **Known risks**: architectural risks that need monitoring during coding
 (e.g. "library X has an open issue with feature Y")
- **Open items**: decisions explicitly deferred to `/coding` because they
 depend on the real codebase state
- **Consistency check**: confirmation that plan-context.md matches all ADRs

### Part 3: Transition question

Ask the user:

> "Architecture proposals are ready. Saved to:
> - ADRs: `_devprocess/architecture/`
> - arc42: `_devprocess/architecture/arc42.md`
> - plan-context.md: `_devprocess/requirements/handoff/plan-context.md`
>
> The next step in the V-Model is `/coding`, which will:
> 1. Load plan-context.md + all ADRs + Features
> 2. Critically review against the real codebase
> 3. Write changes back to artifacts
> 4. Hand off to the Default Claude Code agent for implementation
> 5. After completion: suggest `/testing` -> `/security-audit`
>
> ADRs are **proposals**. `/coding` makes the final call based on the
> actual codebase state.
>
> Shall I start `/coding` now, or would you like to review the proposals
> first?"

**On agreement** ("yes" / "go" / "next") or when running inside
`/dia-orchestrator`:
-> Start `/coding` and pass the handoff context

**On rejection** ("no" / "stop" / "I want to check first"):
-> Pause and wait for user instruction

## Project Structure

This skill follows the conventions from `/project-conventions`.
Ensure `_devprocess/architecture/` exists.
Filenames: `ADR-{nn}-{slug}.md` (2-digit, kebab-case).

## Keywords
Architecture, ADR, arc42, Architecture Decision, Tech Stack, Solution Design,
System Design, plan-context, Architecture Review, Building Blocks, Deployment
