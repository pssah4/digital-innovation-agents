---
name: coding
description: >
 Handoff and bug-capture skill: loads plan-context and design artifacts,
 reviews them critically against the real codebase, and keeps artifacts in
 sync during and after implementation. TDD is the default. Use for
 "implement", "code", "build feature", "realize plan-context", "Bug
 gefunden", "es gibt einen Fehler", "Fix erfassen".
disable-model-invocation: false
---

# Coding -- review, handoff and living documents

Two entry conditions:

1. **Implementation entry** (typical): a FEAT / IMP / ADR / FIX is
   ready to be built. The full review-implement-writeback flow applies.
2. **Bug-capture entry**: the user reports a bug outside an active
   implementation run. Capture the FIX artefact without forcing an
   immediate fix: `references/bug-capture.md`. Trivial bugs may take
   the hotfix lane (fix-now, document-after, five conditions):
   `references/hotfix-lane.md`.

The actual implementation is done by the default Claude Code agent.
This skill loads and reviews context, persists the plan, hands the
binding protocols to the agent, and keeps the artifacts in sync.

## MANDATORY Pre-Phase 0: Branch and item check

Standard ritual, full rules in
`skills/project-conventions/references/team-workflow.md`: identify the
active item (BACKLOG row first for anything new), verify the branch
matches `<type>/<item-id-lower>-<slug>` (AskUserQuestion on mismatch),
run `flow.py create-issue` + `open-draft-pr` when GitHub sync is on,
tag the phase at ritual end (`--phase code`), and write
`.git/dia-active-skill` so subsequent invocations stay silent.

## MANDATORY Phase 0: Artifact triage

Before any code, doc, or spec change, determine the artifact category:
**new FEATURE**, **IMP** on an existing feature, **FIX** for a bug, or
**ADR** for an architecture decision. A `DIA-Triage` trailer on a
prior commit for this item answers the question; otherwise, if the
assignment cannot be derived unambiguously from the prompt, ask ONE
short question before anything else:

> "Is this a new feature, an improvement on an existing feature, or
> a fix for a bug? If feature or IMP/FIX: which feature and which
> epic?"

No code or spec change without this assignment. FIX and IMP require
`feature:` and `epic:` in the frontmatter. Decision tree and
exceptions:
`skills/project-conventions/references/graph-invariants.md`.

## MANDATORY: Backlog as single source of truth

Whenever this skill creates or modifies a Feature, Epic, ADR, FIX,
IMP, or PLAN, it writes the backlog row BEFORE touching the artifact
body. Sync chain and lifecycle:
`skills/project-conventions/references/backlog-sot.md`. If the
backlog write fails, the artifact write does not run. The pre-commit
hook enforces the drift-critical invariants automatically; the full
`/consistency-check` runs before release, not per phase.

## MANDATORY: Wayfinder maintenance

The wayfinder layer (`src/ARCHITECTURE.map` + JSDoc headers +
optional module READMEs) is the only place where current code paths
live. `/coding` owns the runtime upkeep, in the SAME commit as the
code change:

- New entry-point file -> add an ARCHITECTURE.map row AND write the
  JSDoc header (templates under `skills/architecture/templates/`).
- Renamed -> update row and header. Deleted -> remove the row.
- New module -> write `src/{module}/README.md`.

Concrete code paths NEVER appear in ADR core sections, FEATURE specs,
or PLAN bodies as the source of truth (optional stale-allowed
appendices excepted; see
`skills/project-conventions/references/three-layer-model.md`).

## MANDATORY: FIX/IMP and depends-on

Every piece of work outside a Feature is either a `FIX-{ee}-{ff}-{nn}`
(`_devprocess/requirements/fixes/`, template `FIX-TEMPLATE.md`) or an
`IMP-{ee}-{ff}-{nn}` (`.../improvements/`, template
`IMP-TEMPLATE.md`). Frontmatter spec and `depends-on` semantics:
`skills/project-conventions/SKILL.md#canonical-specs`.

## MANDATORY: Writing style

`skills/project-conventions/references/writing-style.md` applies to
every artifact this skill produces.

## Phase 1: Load context

### 1a: Triage gate (before any edit)

Before the first `Edit`/`Write`/`Bash` call, exactly ONE of these IDs
must be known: FEATURE-ID, IMP-ID, FIX-ID, or ADR-ID. If missing, the
skill stops and repeats the Phase 0 question (identical wording).
After the answer: backlog row first, then frontmatter anchoring.

### 1b: Load context

Read in order:

```
REQUIRED:
1. _devprocess/requirements/handoff/plan-context.md (ref index)
2. _devprocess/architecture/ADR-*.md (the decisions the index points to)
3. _devprocess/requirements/features/FEAT-*.md (feature + Success Criteria)
4. CLAUDE.md (project rules)

OPTIONAL (if present):
5. _devprocess/architecture/arc42.md
6. _devprocess/requirements/epics/EPIC-*.md
7. _devprocess/implementation/plans/PLAN-*.md (In Progress = in-flight work)
8. _devprocess/context/BACKLOG.md (open items incl. FIX rows)
9. _devprocess/requirements/fixes/FIX-*.md
10. git log --format='%(trailers:key=DIA-Handoff,valueonly)' -5 (last handoffs)
11. memory/MEMORY.md
```

Open questions to the architect are NOT a blocker: try to self-answer
from the current artifacts and codebase first; what remains goes into
ONE AskUserQuestion at the end of Phase 1, and unresolved items land
as a note in the BACKLOG row or a PR comment.

If no `plan-context.md` exists:

```
No plan-context.md found. Options:

A) I have FEAT-*.md files -- work directly with them
B) I want to run the V-Model workflow -> /dia-guide
C) I have an informal description -- work with it
```

## Phase 2: Critical review

BEFORE an implementation plan is created, check the design artifacts
against the real codebase. This is the most important step.

**2a: Codebase reconciliation.** Do the ADR decisions match the real
architecture? Existing patterns that contradict them? Missing
dependencies or constraints? Modules affected but not mentioned?

**2b: Review output** (only divergence, gaps, and risks; absence
means "matches the codebase"):

```
=== Critical Review: {project/feature} ===

ADRs: {count} reviewed | Features: {count} | Success Criteria: {count}

| Category        | Item                       | Action                        |
|-----------------|----------------------------|-------------------------------|
| CHANGES NEEDED  | ADR-02: {title}            | {recommendation}              |
| MISSING         | {module/pattern}           | {what to add}                 |
| RISKS           | {risk}                     | {mitigation}                  |

Please confirm or correct before I create the implementation plan.
```

**2c: Write changes back IMMEDIATELY**, before implementation:
changed ADR -> update Decision + status `Accepted (modified by
review)`; rejected ADR -> `Deprecated` with justification; changed SC
-> update FEATURE with reason; corrected refs -> plan-context.md; new
decision -> new ADR. Then emit a summary of changed files.

**2d: Drift count.** Append a row to `_devprocess/context/METRICS.md`
under "Drift count": Date | Drift flagged (CHANGES NEEDED + MISSING)
| Drift resolved (written back in 2c). Seed from
`skills/dia-guide/templates/METRICS-TEMPLATE.md` if absent.

## Phase 3: Implementation (delegated to the default agent)

### 3a: Plan persistence (binding)

Every non-trivial run leaves a PLAN file behind at
`_devprocess/implementation/plans/PLAN-{ee}-{ff}-{nn}-{slug}.md`
(template: `templates/PLAN-TEMPLATE.md`). This skill prescribes only
the traceability wrapper (frontmatter, `## Change Log`,
`## Implementation Notes`); the plan BODY belongs to the coding agent
and is pasted verbatim. Flow: next free number -> copy template ->
fill frontmatter (status `Draft`) -> paste body -> flip to
`In Progress` when implementation begins. Mid-course triggers append
dated Change Log entries BEFORE the code edit; never rewrite earlier
entries.

Skip the plan file only for single-step typo/comment fixes,
documentation-only edits, or edits covered by an existing In Progress
plan (append a Change Log entry instead).

**Plan Coverage Gate (binding, before Status flips to In Progress):**
four checks (SC coverage, ADR alignment, codebase anchoring,
verification gates) against the source artifacts, plus the
`## Coverage Gate` evidence block and the re-run rule:
`references/plan-coverage-gate.md`. No code while a check is open.

### 3b: TDD (default: active)

TDD is the default for every implementation task. Opt-out only for
the three exceptions (throwaway prototypes, generated code, config
files), each with explicit user confirmation logged in the PLAN
Change Log; `--no-tdd` opts out for a session. The cycle including
the binding Verify-RED evidence format (state expected failure
signature BEFORE the run, quote the observed output verbatim, give a
verdict): `references/tdd-protocol.md`. Read it before the first test.

### 3c: Debugging protocol

On unexpected failures: no fixes without root-cause investigation.
The 4-phase protocol (root cause, pattern analysis, hypothesis,
implementation) plus the architecture alarm after 3 failed attempts:
`references/debugging-protocol.md`.

### Continuous writeback

Every deviation from the plan is written back IMMEDIATELY, with a
short WHAT / WHY / AFFECTED ARTIFACTS confirmation to the user.
Triggers: decision deviates from an ADR; SC not implementable as
specified; new pattern or dependency; scope change; unexpected
constraint. Targets: PLAN Change Log (append-only), ADR, FEATURE,
plan-context.md refs, arc42 sections.

## Phase 4: Completion

### 4a: Verification gate (binding)

No completion claims without fresh verification evidence run in THIS
message.

| Claim                      | Required proof                                                    | Pass / Fail                          |
|----------------------------|-------------------------------------------------------------------|--------------------------------------|
| Tests / build / bug-fix    | Run the concrete command in this message; read full output        | Exit code 0 and 0 failures           |
| New symbol is reachable    | Caller exists outside definition file and outside tests           | Subtype-aware (see references)       |
| FEATURE Activation Path    | Every entry in `## Activation Path` matches an identifier in code | Grep or AST query returns a hit      |
| Wayfinder consistent       | `src/ARCHITECTURE.map` reflects new/renamed/removed entry-points  | Row matches the codebase             |

Subtype rules, forbidden language, and "what is not enough":
`references/verification-gate-subtypes.md`.

### 4b: Regression test cycle (for bug fixes)

Prove the regression test catches the regression: write the test ->
run 1 MUST pass (fix is in) -> temporarily revert the fix -> run 2
MUST FAIL (else fix the test) -> restore the fix -> run 3 MUST pass.
Note "Regression test verified via red-green cycle on {date}" in the
FIX file's `## Regression test` section.

### 4c: Deferred stubs

Every intentional stub carries a `FIXME(stub): ... -- see
FIX-{ee}-{ff}-{nn}` marker bidirectionally bound to an open FIX row
(enforced as E-13). Syntax and rationale:
`references/deferred-stub-convention.md`.

### Mid-course triggers (binding)

Four conditions interrupt coding and route through the artefact layer
BEFORE the next code edit: `bug` (new FIX), `design` (amend or
supersede ADR), `requirement` (amend FEATURE, re-run Coverage Gate),
`capability` (capture FEATURE + BA-Nachtrag). Pattern: STOP, route,
append a Change Log entry with the `trigger=` tag, THEN resume. Full
step lists and the `[no-capture: scratch]` bypass:
`references/mid-course-triggers.md`.

### Final synchronization

Backlog FIRST, artifacts follow. Every commit that references an
artifact id cites it (`Refs:` trailer).

| # | Layer         | Action                                                                     |
|---|---------------|-----------------------------------------------------------------------------|
| 1 | Backlog       | Status/phase/SHA/claim/refs for every touched item; refresh dashboard      |
| 2 | Wayfinder     | Map rows, JSDoc headers, module READMEs, in the SAME commit as the code    |
| 3 | FEATURE specs | Substance only; SC accuracy. Status lives in the backlog row               |
| 4 | ADRs          | `## Implementation Notes` appendix; deviations into Consequences           |
| 5 | PLAN          | `## Implementation Notes`: per-task SHA, deviations, test delta, cycle time |
| 6 | FIX artefacts | Row resolved; `## Fix` and `## Regression test` sections filled            |
| 7 | METRICS       | Cycle time, phase transitions, trigger counts                              |

**Post-hoc ADR sweep:** after the item merges, check whether a
decision taken in the PLAN deserves an ADR. If yes, write it with
`kind: post-hoc` (Context, Decision, Consequences, Sources with code
paths) and link it from the backlog row.

If applicable: plan-context.md refs, arc42 sections, rules files,
memory/MEMORY.md, CLAUDE.md.

**Completion summary:** `Done: {what landed}. Deviations: {one-liner
or None}.`

## Handoff ritual (mandatory at end of phase)

1. **Artifact report** with full paths (format:
   `references/handoff-ritual-formats.md`).
2. **Handoff context**: open concerns, assumptions, and bugs found go
   into the phase-end commit BODY; the machine-readable transition
   lives in the `DIA-Phase` / `DIA-Handoff` / `DIA-Triage` trailers.
3. **Phase-end commit** per
   `skills/project-conventions/references/team-workflow.md` (branch
   check, staging, canonical message with DIA trailers, phase tag,
   draft PR). Exact CODING format:
   `references/handoff-ritual-formats.md`.
4. **Transition question**: recommend `/testing`; on agreement start
   it, on rejection pause (wording in the reference).

## Core principle: living documents

The artifacts (ADRs, Features, plan-context.md, arc42) are NOT
one-off specifications. They are continuously updated and always
reflect the actually-implemented state at the end. Review corrections,
mid-course writebacks, and the final sync are the three loops that
keep documentation equal to code.

## Keywords

Implement, code, build, plan-context, feature realization, review,
TDD, debugging, verification gate, regression test, living documents,
handoff, writeback, implementation plan, hotfix, bug capture
