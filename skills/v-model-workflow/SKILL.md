---
name: v-model-workflow
description: >
  Orchestrates the V-Model development cycle: Business Analysis ->
  Requirements Engineering -> Architecture -> Coding (Implementation) ->
  Testing -> Security Audit -> Release Closure. Use this skill when the
  user mentions "V-Model", "full workflow", "set up new project", "from
  analysis to implementation", "full cycle" or similar. Also when it is
  unclear which phase to start in. All phases follow the conventions from
  /project-conventions.
disable-model-invocation: true
---

# V-Model Workflow Orchestrator

This skill guides you through the V-Model development cycle. Each phase
builds on the previous one and produces artifacts as input for the next
phase. All phases follow the conventions from `/project-conventions`.

## Workflow Overview

```
Phase 0 (brownfield only): /reverse-engineering    REVERSE WALK
  Input:  existing codebase + documentation          (backwards
  Output: plan-context.md, ADRs (Inferred),           up the V)
          arc42 (Snapshot), FEATURE-*.md (Observed),
          BA-{PROJECT}.md (Draft), backlog seed
    |
    v (forward walk starts here)
Phase 1: /business-analyse                         DESIGN
  Output: _devprocess/analysis/BA-{PROJECT}.md       (left side
    |                                                 of the V)
    v
Phase 2: /requirements-engineering
  Input:  BA document
  Output: Epics, Features, architect-handoff.md
    |
    v
Phase 3: /architecture
  Input:  Features, ASRs, NFRs
  Output: ADRs, arc42, plan-context.md
    |
    v
Phase 4: /coding                                   IMPLEMENTATION
  Input:  plan-context.md + ADRs + Features          (bottom of the V)
  Action: Load context, critical review,
          brief the Default agent (task breakdown,
          optional TDD, debugging protocol,
          verification gate), write artifacts back
    |
    v
Phase 5: /testing                                  VERIFICATION
  Input:  Implemented codebase + Features            (right side
  Output: Unit + integration tests, fix-loop          of the V)
    |
    v
Phase 6: /security-audit
  Input:  Implemented codebase
  Output: Security report + remediation, fix-loop
    |
    v
Phase 7: Release Closure                           CLOSING
  Input:  All artifacts + test + security results
  Output: Finalized artifacts, release notes,
          CHANGELOG update, clean backlog
```

## Orchestrated Phase Transitions

When the workflow runs via `/v-model-workflow`, the orchestrator actively
drives phase transitions. Every phase ends with the **Handoff Ritual** of
the respective skill (see each skill for details). The orchestrator then:

1. Reads the phase-skill's artifact report and handoff context
2. Asks the user the transition question from the phase-skill
3. On agreement: launches the next phase-skill, passing the handoff context
   from `_devprocess/context/30_handoffs.md` as input
4. On rejection: pauses, reports the current state, waits for user instruction
5. Repeats until all phases complete, ending at Phase 7

**The orchestrator never runs in a loop without user consent.** Every
transition needs either an implicit "yes" (user says "go"/"next"/"continue")
or an explicit approval. The user can exit at any point and manually
resume later by re-invoking `/v-model-workflow`.

**When a phase-skill is invoked directly (without `/v-model-workflow`):**
The Handoff Ritual still runs, and the handoff context is still written
to `_devprocess/context/30_handoffs.md`. The user can then manually start
the next skill, which will pick up the handoff entry.

## Ensure project structure exists

Before a phase starts, check whether the directory structure exists.
If not, initialize it per `/project-conventions`:

```bash
mkdir -p _devprocess/{analysis/security,requirements/{epics,features,handoff},architecture,context}
mkdir -p src docs scripts memory
touch _devprocess/context/20_bugs.md _devprocess/context/30_handoffs.md
```

For `_devprocess/context/10_backlog.md`, do not `touch` an empty file.
Seed it from
`skills/requirements-engineering/templates/BACKLOG-TEMPLATE.md` with
the project name, an empty dashboard, and the placeholder sections.
Every phase skill updates this file per the binding format.

## Start: Determine Phase

Ask the user:

```
V-Model Workflow -- where are you?

A0) I have an existing codebase but no V-Model artifacts (brownfield)
    -> Start with /reverse-engineering (walks the V backwards to
       capture technical context + evidence-based BA draft)
    -> Then /business-analyse to validate the WHY
    -> Then continue forward through the normal phases

A)  Starting from scratch -- project/feature not yet analyzed
    -> Start with /business-analyse

B)  Problem is clear, need structured requirements
    -> Start with /requirements-engineering

C)  Requirements exist, need architecture proposals
    -> Start with /architecture

D)  Architecture exists, plan-context.md is ready
    -> Start with /coding

E)  Implementation done, need tests
    -> Start with /testing

F)  Tests passed, need security review
    -> Start with /security-audit

G)  Security audit done, need release closure
    -> Start Phase 7 (Release Closure, see below)

H)  Unsure -- help me figure out where to start
    -> Short orientation interview
```

## Phase Transitions

### After Reverse Engineering -> Business Analysis (brownfield only)

`/reverse-engineering` walks the V backwards and produces technical
artifacts (plan-context.md, ADRs, arc42 snapshot, FEATURE inventory,
backlog seed) plus an **evidence-based BA draft**. The draft is not
validated: it contains only what could be cited from existing
documentation, with `[NEEDS USER INPUT]` placeholders everywhere
else.

The orchestrator **always** hands off to `/business-analyse` next,
even if the draft looks complete. Code is a good technical foundation
but does not prove the product solves the right problem. The user
must validate each section.

```
Reverse engineering complete! Next step:
/business-analyse
Input: _devprocess/analysis/BA-{PROJECT}.md (Draft, reverse-engineered)

/business-analyse will:
1. Detect the draft via its status frontmatter
2. Enter Validation Mode automatically
3. Walk through each section with the user
4. Promote the status from Draft to Validated
```

### After Business Analysis -> Requirements Engineering

Check the Quality Gates from `/business-analyse`, then hand off:

```
BA complete! Next step:
/requirements-engineering
Input: _devprocess/analysis/BA-{PROJECT}.md + last entry in 30_handoffs.md
```

### After Requirements Engineering -> Architecture

Check: Features have tech-agnostic SC, architect-handoff.md exists.

```
Requirements complete! Next step:
/architecture
Input: _devprocess/requirements/handoff/architect-handoff.md
```

### After Architecture -> Coding

Check: plan-context.md exists and is consistent with ADRs.

```
Architecture proposals ready! Next step:
/coding
Input: _devprocess/requirements/handoff/plan-context.md

/coding will:
1. Load plan-context.md + all ADRs + Features
2. Accept/modify ADR proposals (critical codebase review)
3. Create an implementation plan (plan-mode) with task-breakdown guidelines
4. Apply the verification gate before every completion claim
5. Write Feature specs and backlog back to artifacts
```

### After Coding -> Testing

`/coding` automatically recommends testing after completion:

```
Implementation complete!

Next step:
/testing
-> Creates unit + integration tests
-> On failing tests: fix-loop with user approval
```

### After Testing -> Security Audit

```
All tests passing!

Next step:
/security-audit
-> Scans the codebase for OWASP, CWE, dependency vulnerabilities
-> Creates a prioritized remediation plan
```

### After Security Audit -> Phase 7 Release Closure

After the security fix-loop is closed, the orchestrator invokes Phase 7
(see below). This is the final phase that closes the V-Model cycle.

---

## Phase 7: Release Closure

After a successful security audit, the orchestrator explicitly runs the
Release Closure phase. This is the endpoint that closes the cycle cleanly.

**Goal:** Bring all artifacts into a consistent, release-ready state and
prepare the next iteration.

### Step 1: Final artifact synchronization (cross-phase)

Check and update every artifact so it reflects the actual state:

- **BA**: update the Validation section with real numbers if measurable
- **Features**: all statuses correct (Implemented / Deferred / Removed)
- **ADRs**: all statuses finalized (Accepted / Accepted (modified) / Deprecated)
- **arc42**: affected sections up to date
- **plan-context.md**: tech stack matches the actual state

### Step 2: Generate release notes

- List implemented features
- Fixed bugs from `_devprocess/context/20_bugs.md` (Status=resolved)
- Open bugs moved to backlog
- Security findings (resolved + deferred)
- Breaking changes if any

### Step 3: Update CHANGELOG

- New section: `[Unreleased]` -> `[{version}] - {date}`
- Features, Fixes, Breaking Changes sorted in
- Decide semver bump (patch/minor/major)

### Step 4: Backlog cleanup

- All open bugs from `20_bugs.md` referenced in `10_backlog.md`
- Deferred security findings in backlog
- New ideas from implementation (out of scope) documented as
  future-considerations
- Completed items archived

### Step 5: Closing report to the user

```
V-Model cycle complete for {PROJECT} v{version}

Features: {N} implemented, {N} deferred, {N} removed
Bugs: {N} resolved, {N} in backlog
Security: {N} P0/P1 resolved, {N} deferred
Tests: {N} passing, Coverage {line}/{branch}/{function}

Artifacts finalized:
- BA-{PROJECT}.md
- {N} Epics, {N} Features
- {N} ADRs
- arc42 updated
- CHANGELOG v{version}
- Release notes generated

Next iteration:
- {recommendation based on backlog}

Tip: For a new cycle, start again with /business-analyse or
     /requirements-engineering (depending on how deep the change is).
```

---

## Artifact Directory Structure

```
_devprocess/
  analysis/
    BA-{PROJECT}.md                    <- Phase 1: Business Analysis
    EXPLORE-{PROJECT}.md               <- Phase 1 (PoC/MVP)
    security/
      AUDIT-{PROJECT}-{DATE}.md        <- Phase 6: Security Audit
  requirements/
    epics/
      EPIC-{NNN}-{slug}.md             <- Phase 2: Requirements
    features/
      FEATURE-{EPIC}-{NNN}-{slug}.md   <- Phase 2: Requirements (epic-local)
    handoff/
      architect-handoff.md             <- Phase 2 -> 3 handoff
      plan-context.md                  <- Phase 3 -> 4 handoff
  architecture/
    ADR-{NNN}-{slug}.md                <- Phase 3: Architecture
    arc42.md                           <- Phase 3: Architecture
  context/
    10_backlog.md                      <- living backlog (per BACKLOG-TEMPLATE.md)
    20_bugs.md                         <- FIX-NN bug log (Phase 4)
    30_handoffs.md                     <- append-only handoffs log
```

## Traceability Chain

```
BA document (Why?)
  -> Epic (What, strategic?)
    -> Feature (What, concrete?)
      -> ASR (What is architecture-relevant?)
        -> ADR (How do we solve it?)
          -> plan-context.md (Context bridge)
            -> Critical Review (Does it fit the codebase?)
              -> Code (Implementation)
                -> Tests (Does it work?)
                  -> Fix-loop until green
                    -> Security Audit (Is it safe?)
                      -> Fix-loop until resolved
                        -> Backlog (What's still open?)
                          -> Phase 7 Release Closure (Close the cycle)
```

Backchannel: changes in every phase flow back into the source artifacts
(Features, ADRs, plan-context.md). At the end, the documentation always
reflects the actual state.

## Conventions

This workflow follows the standards from `/project-conventions`:
- File names: 3-digit numbers, kebab-case, English
- Language: skill instructions in English, user dialog in the user's language
- Directories: `_devprocess/` for internal documents
- Feature lifecycle: BACKLOG -> SPEC -> PLAN -> IMPL -> UPDATE

## Keywords
V-Model, workflow, full cycle, new project, development cycle,
from analysis to implementation, full run, orchestrator, phase transitions,
release closure
