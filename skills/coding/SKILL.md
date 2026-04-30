---
name: coding
description: >
 Handoff skill: loads plan-context.md and all design artifacts, performs a
 critical review against the real codebase, and ensures continuous writeback
 to the artifacts during and after implementation. Use this skill when the
 user mentions "implement", "code", "realize plan-context", "build feature",
 or similar and a plan-context.md or FEATURE specs exist. This skill does
 NOT take over the coding workflow -- the Default Claude Code agent remains
 responsible for the actual implementation. This skill ensures the context
 is critically reviewed, cleanly handed off, and artifacts stay up to date.
disable-model-invocation: false
---

# Coding -- Review, Handoff & Living Documents

## MANDATORY Pre-Phase 0: Branch protection

Before any code or artefact edit, verify the user is not on a
protected branch (`main`, `master`, `dev`). If protected, ask via
`AskUserQuestion`:

- A) Create feature branch `feature/{feature-slug}` (recommended,
     mirrors the FEATURE ID)
- B) Stay on `{current_branch}` (only for emergency hot-fixes)
- C) Custom branch name

Recommendation: A. Coding produces commits that should land as a
single PR; those need a feature branch.

Full rules: `skills/project-conventions/references/branch-protection.md`.

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
- FIX: status Open, phase Building (or Released if shipped)
- IMP: status Planned, phase Building

**Sync chain on every status or phase change (binding order):**

1. Update the backlog row (status, phase, claim, last-change, refs)
   FIRST
2. Update the artifact body with the substance change
3. Record commit SHA in the backlog row after the commit lands
4. Recompute the dashboard counts at the bottom of the backlog
5. Run `/consistency-check` mode A at the end of the skill phase

The backlog-first order matters: it prevents the most common drift
class observed in the field (status fields stuck at "Planned" while
the code shipped). If the backlog write fails, the artifact write
does not run.

Full rules and enum values:
`skills/project-conventions/references/graph-invariants.md`,
section "Backlog row format".


## MANDATORY: Wayfinder maintenance

The wayfinder layer (`src/ARCHITECTURE.map` plus JSDoc headers in
entry-point files plus optional module READMEs) is the only place
where current code paths live. /coding owns the runtime upkeep:

- New entry-point file landed -> add a row to
  `src/ARCHITECTURE.map` AND write the JSDoc header at the top of
  the file. Templates:
  `skills/architecture/templates/ARCHITECTURE-MAP-TEMPLATE.md`,
  `skills/architecture/templates/JSDOC-HEADER-TEMPLATE.md`.
- Entry-point file renamed -> update the matching map row AND the
  JSDoc header.
- Entry-point file deleted -> remove the map row.
- New module created -> write `src/{module}/README.md`. Template:
  `skills/architecture/templates/MODULE-README-TEMPLATE.md`.

These updates are NOT a separate doc step. They land in the same
commit as the code change that triggered them. The verify gate
(Phase 4a) checks that `src/ARCHITECTURE.map` is consistent with
the codebase.

Concrete code paths NEVER appear in ADR core sections, FEATURE specs,
or PLAN bodies as the source of truth. Those artifacts can carry an
optional appendix (`## Implementation Notes`, `## Code Pointer`)
that is allowed to go stale; the wayfinder is the canonical source.


This skill has three main responsibilities:

1. **Load context** from the design phases
2. **Critically review** it before implementation begins
3. **Continuously write back** so artifacts always reflect the current state

The actual implementation is done by the Default Claude Code agent. This
skill briefs that agent with precise guidelines (see Phase 3 subsections
below) so the agent's work is structured, verified, and documented.

---


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

## MANDATORY: Writing style and humanizer rules

All artifacts produced by this skill follow the rules in
`skills/project-conventions/SKILL.md` under "Writing style for every
artifact". Zero em dashes (U+2014, U+2013, double-hyphen substitute).
No AI vocabulary words (landscape, nuanced, delve, leverage, crucial,
robust, seamless, holistic, foster, ensuring, highlighting,
underscoring). No negative parallelisms ("not X but Y"). Active
voice by default. Sentence case in headings. No rule-of-three
padding. Before saving, scan the artifact for the forbidden vocabulary
and fix any hit.

For German artifacts: proper umlauts (ä, ö, ü, ß), not the
ae/oe/ue/ss substitutes. Hypothesis and How-Might-We statements are
written as full prose paragraphs, not template placeholder lines.


## Phase 1: Load Context

### Phase 1a: Triage gate (before any edit)

Technical gate that enforces the **Phase 0** artifact triage. Phase 0
is the source of truth for the decision tree and exceptions; here we
only check that a concrete ID is in scope.

Before the first `Edit`/`Write`/`Bash` call, **exactly one** of these
IDs must be known:

- **FEATURE-ID** (e.g. `FEAT-01-03`, spec + optional PLAN)
- **IMP-ID** (e.g. `IMP-007`,
  `_devprocess/requirements/improvements/IMP-{ee}-{ff}-{nn}-slug.md`)
- **FIX-ID** (e.g. `FIX-012`,
  `_devprocess/requirements/fixes/FIX-{ee}-{ff}-{nn}-slug.md`)
- **ADR-ID** (e.g. `ADR-04`)

If the ID is missing, **the skill stops before the first edit** and
repeats the Phase 0 question (identical wording, not a new variant,
so the user is not asked the same thing twice in different words).

After the answer, the ID is anchored in the FEATURE/IMP/FIX
frontmatter (`feature:` and `epic:` mandatory for IMP and FIX). The
backlog row is created or updated FIRST, the frontmatter follows.
Exceptions and details: Phase 0 and
`skills/project-conventions/references/graph-invariants.md`
(section "Artifact triage at entry point").

### Phase 1b: Load Context

Read these documents in order:

```
REQUIRED:
1. _devprocess/requirements/handoff/plan-context.md (primary input)
2. _devprocess/architecture/ADR-*.md (architecture decisions)
3. _devprocess/requirements/features/FEATURE-*.md (feature details + Success Criteria)
4. CLAUDE.md (project-specific rules)

OPTIONAL (if present):
5. _devprocess/architecture/arc42.md (overall architecture)
6. _devprocess/requirements/epics/EPIC-*.md (strategic context)
7. _devprocess/implementation/plans/PLAN-*.md (prior and active plans; Status=Active carries in-flight work)
8. _devprocess/context/BACKLOG.md (open items)
9. _devprocess/context/20_bugs.md (known bugs, FIX-NN-NN-NN entries)
10. _devprocess/context/HANDOFFS.md (last handoff entry from /architecture)
11. memory/MEMORY.md (architecture key facts)
```

**Dialog check.** After loading `plan-context.md`, scan its `## Dialog`
section. If there are entries under "Answers from Architect" with
`Status: Resolved` that your previous session did not yet see, read
them now. They carry answers to questions you raised in an earlier
pass.

If there are "Questions from Coder" entries still at `Status: Pending`,
try to self-answer each one from the current artifacts (updated ADRs,
arc42, codebase). For every question you can answer from the
artifacts, append the resolution to "Answers from Architect" in the
plan-context Dialog section and mark the question Resolved. For every
question you still cannot answer, surface the remaining set to the
user in a single `AskUserQuestion` at the end of Phase 1: "N pending
Dialog questions could not be self-answered. Address now, defer to
end of session, or record as open issues?" Do not block. Proceed with
whatever the user chose.

If no `plan-context.md` exists:

```
No plan-context.md found. Options:

A) I have FEATURE-*.md files -- work directly with them
B) I want to run the V-Model workflow -> /dia-orchestrator
C) I have an informal description -- work with it
```

---

## Phase 2: Critical Review

BEFORE an implementation plan is created, critically check the design
artifacts against the real codebase. This is the most important step.

### 2a: Codebase reconciliation

Read the existing codebase and check:

- Do the ADR proposals match the real architecture?
- Are there existing patterns that contradict the proposals?
- Are the tech-stack assumptions in plan-context.md correct?
- Are dependencies or constraints missing?
- Are modules affected by the planned changes but not mentioned in the
 architecture?

### 2b: Review output

```
=== Critical Review: {project/feature} ===

Tech Stack: {from plan-context.md, with corrections if needed}
ADRs: {count} reviewed
Features: {count} reviewed
Success Criteria: {count} to verify

--- Codebase reconciliation ---

CONFIRMED (matches codebase):
- ADR-01: {title} -- proposal fits, {justification}
- FEAT-01-01 SC-01: {criterion} -- realistic

CHANGES NEEDED (divergence from codebase):
- ADR-02: {title} -- proposal: {original}
 Problem: {what doesn't fit}
 Recommendation: {what to do instead}
- FEAT-02-03 SC-02: {criterion}
 Problem: {why not as specified}
 Recommendation: {alternative}

MISSING (not addressed in designs):
- {module/pattern affected but not addressed}

RISKS:
- {risk 1}: {description and mitigation}

--- Decisions ---

Please confirm or correct the change proposals before I create the
implementation plan.
```

### 2c: Write changes back

Every change from the review is IMMEDIATELY written back into the source
artifacts BEFORE implementation begins:

- **ADR changed** -> update ADR file:
 - Adjust Decision section
 - Status -> `Accepted (modified by review)`
 - Document the justification for the change
- **ADR rejected** -> update ADR file:
 - Status -> `Deprecated`
 - Justification and reference to alternative
- **Feature SC changed** -> update FEATURE file:
 - Adjust Success Criteria
 - Reason for change as a comment
- **plan-context.md corrected** -> update file
- **New ADR needed** -> create new ADR file

After writing back: emit a summary of the changed files.

### 2d: Signal writeback (drift count)

Append a row to `_devprocess/context/METRICS.md` under the
"Drift count (plan-context.md vs. real code)" table:

- Date: today
- ADR count: how many ADRs were reviewed
- arc42 section count: how many arc42 sections were reviewed
- plan-context item count: how many plan-context entries were checked
- Drift flagged: count of CHANGES NEEDED + MISSING items from the review
- Drift resolved: count of items actually written back in step 2c
- Open: count that remained unresolved (for example because the user
 wanted to discuss first)

If `METRICS.md` does not yet exist, copy
`skills/dia-orchestrator/templates/METRICS-TEMPLATE.md` into the
file first, then append. A rising drift count over multiple
reconciliation runs signals that the ADRs or plan-context are losing
touch with reality.

---

## Phase 3: Implementation (delegated to Default Agent)

After the review, implementation is handed off to the Default Claude Code
agent. The `/coding` skill does two things before the agent writes code:
(a) persists the plan the agent produces (Phase 3a), and (b) carries
cross-cutting protocols the agent binds to for this session (TDD toggle,
debugging, verification gate, writeback). These are scoped per
sub-section below. Phase 3a itself does not impose a plan shape.

### Phase 3a: Plan persistence

**Persist the plan as a file (binding).**

Every non-trivial implementation run leaves a PLAN-{nn} file behind.
Without this file the plan lives only in the agent's session and
disappears after context reset.

Location: `_devprocess/implementation/plans/PLAN-{nn}-{slug}.md`.
Template: `skills/coding/templates/PLAN-TEMPLATE.md`.

**What this skill prescribes vs. what the coding agent owns.**

This skill prescribes only the traceability wrapper: frontmatter with
id / status / date / refs / pair-id, a Change Log section, and an
Implementation Notes section. Everything else -- how tasks are
decomposed, whether TDD is used, what structure the body has -- belongs
to the coding agent that produces the plan. Claude Code has a strong
native planning mode, and it keeps improving. This skill persists
whatever plan the agent produces; it does not reshape it into a fixed
schema that would freeze old patterns into every project.

Flow:

1. Determine the next free 2-digit number by scanning
 `_devprocess/implementation/plans/` (highest NNN + 1). If the
 directory does not exist, create it and start at `001`.
2. Copy the template to
 `_devprocess/implementation/plans/PLAN-{nn}-{slug}.md`.
3. Fill the frontmatter: id, title, date (today), feature-refs,
 adr-refs, bug-refs (if applicable), pair-id, status `Draft`.
4. Paste the coding agent's plan verbatim into the body section
 between the frontmatter and the `## Change Log` header. If the
 agent runs in Claude Code, this is the plan Claude Code wrote in
 plan-mode. Do not edit the structure. If the agent is less
 capable and produced nothing usable, fall back to the minimal
 structure described in the template.
5. Flip status to `Active` once implementation begins.
6. Every mid-course trigger (see "Mid-course bug discovery" and
 "Mid-course design discovery" below) appends a dated entry to the
 plan's `## Change Log` section BEFORE the code edit. Never
 rewrite earlier entries or earlier task descriptions.

Skip the plan file only for:
- Single-step typo / comment fixes
- Documentation-only edits
- Edits already covered by an existing Active plan (append a Change
 Log entry instead of creating a new file)

The plan file is part of the artifact report in the Handoff Ritual.

**Plan Coverage Gate (binding, runs before Status flips to Active).**

Regardless of which agent produced the plan, the skill checks four
things against the source artifacts. The check happens AFTER the
plan body is persisted and BEFORE implementation begins. If any item
fails, the flow loops: update the affected artifact, then re-run the
gate. No code is written while an item is open.

1. **SC coverage.** Every Success Criterion from every referenced
 FEATURE spec either maps to a concrete task in the plan or is
 explicitly marked "Deferred: {reason}" in the plan body.
 - Gap found -> two options:
 (a) add task(s) to the plan body (agent decides shape), or
 (b) amend the FEATURE: remove / split / reword the SC, with
 justification. Every FEATURE amendment bumps the FEATURE's
 `Last updated` and gets a one-line comment explaining the
 change.
2. **ADR alignment.** Every ADR listed in `adr-refs` has at least one
 task that operationalizes its Decision section.
 - Gap found -> either add a task, or route through the Mid-course
 design trigger (the ADR itself may be wrong).
3. **Codebase anchoring.** Every task names at least one concrete file
 path (Create / Modify / Test). Abstract tasks like "clean up state
 management" fail the gate until they name files.
4. **Verification gates.** The plan body contains at least one build
 command and one test command that prove the plan done. If the
 repo has no tests yet, a smoke script is acceptable; the plan
 names it.

On completion: add a short "## Coverage Gate" block at the bottom of
the plan body (before `## Change Log`) listing which SC mapped to
which task, which SC got deferred, and which ADRs got touched. This
block is what a later reviewer (human or agent) reads to verify the
gate actually ran.

**Re-run the gate whenever a source artifact changes.** If a FEATURE,
ADR, or plan-context.md is amended while a PLAN is at Status=Active
(from codebase reconciliation, mid-course triggers, or external
edits), the Coverage Gate runs again on that PLAN before the next
code edit. Log the re-run as a Change Log entry with trigger=coverage
and the amended artifact ID. This is the writeback loop that keeps
the plan honest when upstream artifacts move.

### Phase 3a-bis: Guidance for agents without a native planning mode

The rules below are a fallback. If the coding agent is Claude Code (or
any agent with its own mature planning conventions), its plan-mode
output supersedes this guidance. The skill persists that plan verbatim
(per Phase 3a above). Do not rewrite the agent's plan to match the
rules below. The point of the rules is to prevent an underpowered
agent from producing a plan that is too vague to execute; they are
not a ceiling on what a stronger agent can do.

Use the rules when:
- the coding agent has no native planning step, or
- its plan is visibly thin (no file paths, no test strategy, no
 verification gates) and needs to be repaired before implementation.

**Bite-size tasks (2-5 minutes per step):**

Every task decomposes into:
1. Write the failing test (one test, one behavior)
2. Run the test -- it MUST fail with the expected reason
3. Write the minimal implementation to make it pass
4. Run the test -- it MUST pass
5. Commit with a conventional prefix (feat/fix/chore/docs/refactor)

**Every task has a file list:**
- Create: `exact/path/to/file.py`
- Modify: `exact/path/to/existing.py:123-145`
- Test: `tests/exact/path/to/test.py`

**No placeholders in the plan:**
- Forbidden: "TBD", "TODO", "implement later", "fill in details"
- Forbidden: "Add appropriate error handling", "handle edge cases" (without concrete cases)
- Forbidden: "Write tests for the above" (without actual test code)
- Forbidden: "Similar to Task N" (repeat the code -- tasks may be read out of order)
- Forbidden: Steps that describe WHAT without showing HOW

**Self-review after plan creation:**

The agent re-reads the plan and checks:
1. **Spec Coverage:** Does every requirement from plan-context.md map to at least one task?
2. **Placeholder Scan:** Does the plan contain any red-flag patterns from the list above?
3. **Type Consistency:** Do function/type/property names match across tasks?

Fix gaps and placeholders inline before implementation starts.

### Phase 3b: TDD Mode (optional)

**Activation:** The user can enable TDD mode explicitly with "enable TDD
mode" or by starting `/coding` with a `--tdd` hint. Default is: TDD is NOT
enforced (because throwaway prototypes and exploration suffer under TDD
pressure).

When active, `/coding` hands this rule to the Default agent for this session:

**The rule:** No production code without a failing test written first.

**The cycle:**
1. **RED:** Write a failing test (one behavior, one assertion)
2. **Verify RED:** Run the test -- it MUST fail with the expected reason
 - If it passes immediately: the test isn't testing the new functionality, fix it
 - If it fails with a syntax error: fix the error and re-run
3. **GREEN:** Write the minimal code to pass the test (no more)
4. **Verify GREEN:** Run the test -- it MUST pass, no other tests broken
5. **REFACTOR:** Clean up while keeping tests green (no new behavior)

**Exceptions (only with user confirmation):**
- Throwaway prototypes
- Generated code
- Configuration files

### Phase 3c: Debugging protocol (if a bug appears)

When a test fails unexpectedly during implementation, or behavior is
incorrect, or a fix doesn't work, `/coding` hands the following 4-phase
protocol to the Default agent:

**The rule:** No fixes without root-cause investigation.

**Phase A: Root Cause (BEFORE any fix attempt)**
1. Read the error message completely -- stack trace, line numbers, codes
2. Check reproducibility -- does it happen every time?
3. Check recent changes -- `git diff`, last commits, new dependencies
4. In multi-component systems: add logging at every component boundary
5. Trace the data flow backwards -- where does the bad value originate?

**Phase B: Pattern Analysis**
1. Find working examples in the codebase
2. Read the reference implementation completely (don't skim)
3. List every difference -- even ones that seem irrelevant
4. Check dependencies and config assumptions

**Phase C: Hypothesis**
1. State one hypothesis: "Root cause is X because Y"
2. Make the smallest possible change to test it
3. One variable at a time
4. If the hypothesis is wrong: form a new one, don't pile fixes

**Phase D: Implementation**
1. Write a failing test that reproduces the bug
2. Apply exactly one fix that addresses the root cause
3. Verify: test passes, no regressions elsewhere
4. Document the bug in `_devprocess/context/20_bugs.md` with a FIX-NN-NN-NN ID,
 the causal chain (step 1 -> step 2 -> ... -> error), and priority (P0/P1/P2)

**Phase D.5: Architecture alarm (after 3+ failed fix attempts)**

If three or more fix attempts fail to resolve the situation, this is an
architecture problem, not a bug:
- Each fix reveals a new problem in a different place?
- Fixes require "massive refactoring"?
- Each fix creates new symptoms?

Then STOP. No fourth attempt. Instead:
- Question the pattern fundamentally -- is the approach sound?
- Discuss with the user before any more fixes
- This is not a failed hypothesis -- it's a wrong architecture

**Writeback:** Every bug found, even if the fix is trivial, gets an entry
in `_devprocess/context/20_bugs.md` with: symptom, root cause, causal chain,
fix commit SHA, FIX-NN-NN-NN ID, and priority.

### Continuous writeback during implementation

When changes to the planned architecture or features become necessary
during implementation, write back IMMEDIATELY:

**For every deviation from the plan:**

```
Change during implementation:

WHAT: {what changed}
WHY: {why it was necessary}
AFFECTED ARTIFACTS:
- {ADR-{nn}}: {what to adjust}
- {FEATURE-XXX}: {what to adjust}

Should I write these changes back now? [Y/N]
```

**Triggers for writeback:**
- A technical decision deviates from an ADR
- A Success Criterion isn't implementable as specified
- New pattern or new dependency introduced
- Scope change (feature larger/smaller than planned)
- Unexpected constraint discovered

**What gets written back:**
- PLAN-{nn}: append a Change Log entry (never rewrite past tasks in place)
- ADR: Decision, Status, Implementation Notes
- FEATURE: Success Criteria, Technical NFRs, Definition of Done
- plan-context.md: Tech Stack, Integrations (if fundamentally changed)
- arc42: affected sections (if architecture changes)

---

## Phase 4: Completion -- Final Synchronization

After implementation, final checks and writeback.

### Phase 4a: Verification gate before completion

Before `/coding` declares a task or the whole implementation as done, the
following gate function must run. This rule holds regardless of how
confident the agent is.

**The rule:** No completion claims without fresh verification evidence.

If the agent hasn't run the verification command in this message, it cannot
claim the task is successful.

**The gate function (5 steps, all mandatory):**

1. **Identify:** Which command proves the claim?
 - "Tests pass" -> concrete test command with path
 - "Build works" -> concrete build command
 - "Bug fixed" -> test that reproduces the original symptom
2. **Run:** Execute the command fully -- not cached, not partial
3. **Read:** Read the complete output, check exit code, count failures
4. **Verify:** Does the output confirm the claim?
 - No -> report actual status with evidence
 - Yes -> formulate the claim with evidence
5. **Claim:** Only now state the status

**Forbidden language without fresh verification:**
- "should work", "probably okay", "looks good"
- "tests should be green now"
- "the change should fix the bug"
- Any statement implying success without running the command

**Common failures -- what is not enough:**

| Claim | Sufficient proof |
|---|---|
| Tests pass | Test command output with 0 failures |
| Linter clean | Linter output with 0 errors |
| Build works | Build command with exit code 0 |
| Bug fixed | Test reproducing the original symptom passes |
| Subagent done | VCS diff shows the expected changes |
| Requirements met | Line-by-line checklist against the plan |

### Phase 4b: Regression test cycle (for bug fixes)

Every bug fix goes through this 6-step cycle to prove the regression test
actually catches the regression:

1. **Write the regression test** reproducing the bug behavior
2. **Run 1:** Run the test -- it MUST pass (because the fix is already in)
3. **Temporarily revert the fix** (`git stash` or code revert)
4. **Run 2:** Run the test -- it MUST FAIL
 - If it passes: the test isn't catching the bug, fix the test
5. **Restore the fix** (`git stash pop` or code restore)
6. **Run 3:** Run the test -- it MUST pass again

Only when all three runs return the expected result is the bug marked as
resolved and the regression test marked as valid.

**Documentation:** The entry in `_devprocess/context/20_bugs.md` gets a
note: "Regression test verified via red-green cycle on {date}".

### Mid-course bug discovery (binding trigger)

If a NEW bug surfaces while implementing the current plan (not in
the original feature specs, ADRs, or FIX-list), the coding flow
MUST pause and route through the artefact layer BEFORE writing the
fix. Skipping this step leaks code changes without backlog trace.

```
Mid-course handling, do NOT fix the bug silently:

1. STOP the current code edit. Do not write the fix yet.
2. Triage:
 - Is this a BUG in shipped code? -> create BUG-NNN
 - Is this a missing requirement in plan? -> create FEAT-NN-NN
 - Is this a design gap? -> amend ADR / arc42
3. Write a minimal root-cause analysis in _devprocess/analysis/
 (3-10 lines is fine: problem, cause, fix direction, risk)
4. Add the new item to _devprocess/context/BACKLOG.md under
 the active Epic so it appears in the backlog before any code
 touches disk
5. Append a Change Log entry to the active PLAN-{nn} file with
 trigger=bug, the new BUG-NNN reference, and a one-line summary
 of what the fix changes. Never rewrite past tasks in place.
6. NOW write the fix. Commit message cites BOTH the in-progress
 FEAT-NN-NN and the new BUG-NNN (e.g.
 `Refs: FEAT-05-07, BUG-018, PLAN-12`)
7. After the fix: run the standard Final synchronization block
 below, marking the new BUG-NNN as resolved
```

Why this matters: bugs surfaced during beta testing of a real
downstream project got fixed in code first and documented only
after release, so the backlog drifted from the code state for
days. This trigger closes that gap.

### Mid-course design discovery (binding trigger)

If the implementation reveals that an architectural decision does not
match reality (ADR says X, the codebase proves Y works better, or the
constraints the ADR relied on turned out to be wrong), pause the
coding flow and route through the architecture layer BEFORE continuing
the feature. Silent design drift is worse than a bug: the ADR keeps
claiming a state of the world that no longer exists.

```
Mid-course handling for a design finding, do NOT silently deviate:

1. STOP the current code edit. Do not keep coding around the
 mismatched ADR.
2. Triage:
 - Can the ADR be amended with a small correction?
 -> update ADR, keep status "Accepted (modified)"
 - Is the original decision wrong at the root?
 -> supersede ADR: old one becomes "Superseded by ADR-{nn}",
 new ADR captures the actual decision
 - Does the discovery only clarify wording, not decision?
 -> update ADR Context or Consequences in place
3. Write a root-cause entry in _devprocess/analysis/ADR-{nn}-review.md
 (3-10 lines: what the ADR claimed, what the code proves, what
 changes, what still holds)
4. Update arc42.md and plan-context.md if the discovery affects
 either. Keep them consistent with the ADR change.
5. Append a Change Log entry to the active PLAN-{nn} file with
 trigger=design, the affected ADR(s), and a one-line summary of
 how the plan pivots. If the pivot invalidates remaining tasks,
 mark the plan as Superseded and create PLAN-{NNN+1} with the
 revised task list; the old plan stays for traceability.
6. Only NOW resume or rewrite the code. Commit message cites the ADR
 change alongside the in-progress FEATURE and the plan
 (e.g. `Refs: FEAT-05-07, ADR-12 (amended), PLAN-12`)
7. After the fix: run the standard Final synchronization block
 below. The amended or superseded ADR is part of the writeback.
```

Why this matters: an ADR that silently diverges from the code stops
being a decision record and becomes a historical fiction. The next
reviewer who consults it makes worse decisions because they trust a
document that no longer reflects reality.

### Mid-course requirements discovery (binding trigger)

If the implementation reveals that a FEATURE spec is ambiguous,
incomplete, or contradicts what the codebase needs (a Success
Criterion cannot be met as written, an SC is missing, or an SC turns
out to mean something different than intended), pause the coding flow
and route through the requirements layer BEFORE continuing. Coding
around a broken FEATURE spec produces code that tests cannot verify
against the spec and a spec that stops describing the product.

```
Mid-course handling for a requirements finding, do NOT silently reinterpret:

1. STOP the current code edit. Do not paper over the spec gap with
 code that "should work".
2. Triage:
 - Is the SC only ambiguous (wording unclear)?
 -> update the FEATURE: rewrite the SC, keep its number, add a
 one-line comment with the clarification rationale
 - Is an SC missing (feature behavior exists in the codebase need
 but not in the spec)?
 -> add a new SC to the FEATURE with the next number
 - Is an SC wrong (impossible, contradicts another SC, or the user
 no longer wants it)?
 -> either amend the SC or mark it "Removed: {reason}". Do not
 delete the line; removal is an append-only event
 - Is the scope wrong at the root (FEATURE splits into two, or
 merges into another)?
 -> open the decision with the user via AskUserQuestion; do not
 re-shape the feature graph unilaterally
3. Update plan-context.md if the FEATURE change affects the tech
 stack or integration assumptions.
4. Re-run the Plan Coverage Gate on the active PLAN-{nn}. Every SC
 that was amended must re-map to a task or be marked Deferred.
 Append a Change Log entry to the plan with trigger=requirement,
 the amended SC IDs, and a one-line summary of how tasks changed.
5. Only NOW resume or rewrite the code. Commit message cites the
 FEATURE change alongside the plan
 (e.g. `Refs: FEAT-05-07 (SC-03 amended), PLAN-12`)
6. After the fix: run the standard Final synchronization block below.
 The amended FEATURE is part of the writeback.
```

Why this matters: a FEATURE that the code no longer matches is not a
spec anymore. Tests that pass against it prove nothing. The Coverage
Gate re-run is what closes the loop: the plan stays aligned with the
post-amendment spec, and a future reviewer can see, via the Change
Log trigger=requirement entry, that the gap was caught and closed in
the right order.

### Mid-course capability discovery (binding trigger, added 2026-04-20)

The prior trigger covers amendments to **existing** FEATUREs. This
one covers the other case: the implementation is about to introduce
a **new user-facing capability** that no FEATURE in the repository
describes yet. Agents that code without spec catch-up create exactly
the drift the consistency-check (see `/consistency-check`) flags as
orphan code. The fix is to pause and capture the capability with a
short user dialog, then resume.

**Detection.** A new capability is discovered when any of these
happen:

- A new route, handler, or command is added that was not in
 `plan-context.md` or in any existing FEATURE's
 `Source (Implementation):` list.
- A new Sidebar entry, Settings tab, or top-level UI surface is
 introduced.
- A new CLI flag or public API endpoint that changes the user-facing
 contract.

Tech-only changes (helpers, refactors, private utilities, bugfixes,
documentation, test additions) do NOT trigger this dialog.

```
Mid-course capability handling, do NOT silently add new features:

1. STOP the current code edit. A new FEATURE entry is needed
 before the code lands.
2. Triage with one `AskUserQuestion` at a time, per the User
 Interaction Protocol. The agent must not invent answers here;
 the WHY and WHO require user input.

 Question A - Is this a real new user-facing capability, or is
 it a technical byproduct? If technical byproduct: skip dialog,
 just add to code. If user-facing: continue.

 Question B - For which Persona? Pick from the BA's current
 persona list, or select "Other" and supply name + short
 description.

 Question C - Which Job-to-be-Done is solved? Free text. The
 agent does not infer from code paths; user articulates.

 Question D - Which measurable outcome do we expect? Free text.
 If the user cannot answer now, accept `[AWAITING BA Nachtrag]`
 and continue (the Feature will carry the placeholder).

3. Write the FEATURE-spec draft now, not after the code. Use
 `skills/requirements-engineering/templates/FEATURE-TEMPLATE.md`.
 Frontmatter: `status: Draft (User-Input {date})`,
 `source: capability-capture during /coding`. Fill Capability
 line (observable SC-01), Persona, JTBD, outcome-placeholder.

4. Write a BA-Nachtrag. Append to `docs/analysis/BA-{project}.md`
 under a `## User-Input-Capture ({date})` section. Mark the
 entry `unvalidated` with the same date. Never edit validated
 BA sections silently; appendix-only.

5. Update the Epic assignment. If the capability fits an existing
 Epic, add a row to that Epic's MVP-Features table. If not,
 create a new Epic with `status: Draft (User-Input {date})` and
 a placeholder Hypothesis Statement.

6. Add a FIX/IMP to the backlog under the relevant Epic section.
 Phase = Building if user provided all four answers;
 Phase = Candidates with `needs refinement: BA-Anchor fehlt` if
 Question D was deferred.

7. Run `/consistency-check` to verify the new Feature/Epic/BA
 links hold.

8. NOW continue the code edit. Commit message cites the new
 FEATURE-ID and FIX/IMP
 (e.g. `Refs: FEAT-08-17, PLAN-18`).

9. At the end of the session, the Final Synchronization block
 promotes the FEATURE status from Draft to Implemented if the
 capability is fully realised.
```

Why this matters: this is where the graph stays honest. Agents alone
cannot write a useful Persona or Business-Outcome for a capability
they did not conceive. The user is the only source for those; the
agent captures, does not invent. Without this trigger the code
outruns the graph and the consistency-check produces a growing list
of orphan-feature BL-items that nobody understands later.

**When this trigger is skipped.** If the user explicitly says "this
is a scratch change, no feature yet", the agent may bypass the
dialog for that one commit. The commit message then carries
`[no-capture: scratch]` and `/consistency-check` will later flag the
orphan for a retroactive capture. Deliberate bypass is a recorded
action, not a hidden one.

### Final synchronization (cross-artifact)

After implementation is verified, run the writeback in this order
(backlog FIRST, artifacts follow):

```
MANDATORY -- backlog row reflects the actual state BEFORE the artifact
bodies are touched:

1. Backlog (single source of truth for state and the relation graph):
 - Update _devprocess/context/BACKLOG.md per the binding format
 in skills/requirements-engineering/templates/BACKLOG-TEMPLATE.md
 - For every Feature, ADR, PLAN, FIX, IMP touched this session:
 set status (Done / Review / Active / Superseded), phase, commit
 SHA, claim cleared if work is done
 - Add new findings (improvements, tech debt, follow-ups) as new
 rows in the matching Epic section or Standalone Items
 - Refresh dashboard counts (status + phase + priority) and the
 "Last update" header
 - Update the Refs column for parent and child relations
 - **Per-commit gate (binding):** The backlog reflects the
 post-implementation state BEFORE every commit that references
 a FEATURE, FIX, IMP, ADR, or PLAN ID. Stricter than "before
 handoff ritual" because phase-end writeback drifts when phases
 stretch across multiple commits.
 - **Commit message cites the artifacts touched:**
 `Refs: FEAT-01-03, FIX-013, PLAN-07` (or similar). This
 creates a searchable trail from code back to backlog, so a
 future query `git log --grep="FEAT-01-03"` lists every
 commit that claimed to move that item forward.

2. Wayfinder layer:
 - src/ARCHITECTURE.map: update rows for new, renamed, or removed
 entry-points
 - JSDoc headers in new entry-point files: written
 - Module READMEs: written or updated for new modules
 - This step lands in the SAME commit as the code, never as a
 separate doc commit

3. Feature specs (substance, not status):
 - Substance unchanged unless a Mid-course requirements trigger
 fired (in which case the trigger already updated the spec)
 - NO status field changes here. Status lives in the backlog row.
 - Verify Success Criteria are still accurate; if reality differs,
 the Mid-course trigger should already have amended them.

4. ADRs (substance, not status):
 - Status field finalized in the BACKLOG ROW. The ADR file does not
 carry a status field in frontmatter.
 - Add Implementation Notes appendix with the actual outcome
 (allowed to go stale; the wayfinder is the source of truth).
 - Document deviations from the original proposal in the
 Consequences section if architecturally relevant.

5. Implementation plan (PLAN-{nn}):
 - Status (Done, Superseded) is set in the backlog row, not the
 PLAN frontmatter.
 - Fill "Implementation Notes" section: per-task commit SHA (short
 form), deviations summary, test count delta, cycle time
 (first-commit -> last-commit), wayfinder updates landed.
 - Every task either has a commit SHA or an explicit "Not executed
 because ..." note. No task silently dropped.
 - The Change Log keeps every mid-course entry appended during the
 run. Never rewrite past entries.

6. Bug log:
 - All FIX-NN-NN-NN entries in _devprocess/context/20_bugs.md updated
 (status resolved in the backlog row, commit SHA, regression test
 verified)

7. Metrics (signal layer):
 - Append a row to _devprocess/context/METRICS.md under the
 "Cycle time per FEATURE" table for each FEATURE that reached
 status Done this session
 - Columns: FEATURE ID, Started (first commit with Refs:FEATURE-NNN),
 Completed (latest commit with Refs:FEATURE-NNN), Cycle time,
 Scope, Notes
 - Append a row to "Phase transition counts" under "Coding -> Testing"
 (or the next phase) if this session ended a phase
 - Append a row to "Cross-phase trigger counts" for every
 mid-course trigger that fired during this session

IF APPLICABLE:
8. plan-context.md: update if tech stack has changed
9. arc42: update affected sections
10. _devprocess/rules/technical.md (or design.md, domain.md): update
 if a stable convention emerged or shifted during the session
11. memory/MEMORY.md: if architecture key facts have changed
12. CLAUDE.md: if new project conventions emerged
```

### Completion summary

```
Implementation complete!

Artifact status:
- {N} Plans closed (Status: Implemented, {N} superseded)
- {N} Features updated (Status: Implemented)
- {N} ADRs finalized ({N} accepted, {N} modified, {N} deprecated)
- {N} artifacts written back during implementation
- {N} bugs in 20_bugs.md (resolved: {N}, open: {N})
- Backlog updated

Deviations from the original design:
- {summary of most important changes, or "None"}
```

---

## Handoff Ritual (mandatory at end of phase)

`/coding` always runs this ritual at the end, regardless of how it was
started (directly or via `/dia-orchestrator`).

### Part 1: Artifact report

List all artifacts produced or updated with full paths:

```
Produced / updated:
- src/{files}: {summary}
- _devprocess/implementation/plans/PLAN-*.md: {status updates, SHAs}
- _devprocess/requirements/features/FEATURE-*.md: {status updates}
- _devprocess/architecture/ADR-*.md: {status and implementation notes}
- _devprocess/requirements/handoff/plan-context.md: {tech stack updates if any}
- _devprocess/context/20_bugs.md: {FIX-NN-NN-NN entries}
- _devprocess/context/BACKLOG.md: {new/resolved items}
```

### Part 2: Handoff context

Append a new entry to `_devprocess/context/HANDOFFS.md` with:

- Summary of what was implemented
- Deviations from plan (with references to the updated ADRs/Features)
- Bugs found and their FIX-NN-NN-NN IDs (resolved and open)
- Open concerns for testing or security phase
- Assumptions that were made and should be verified

### Part 3: Transition question

Ask the user:

> "Implementation is complete. The next step in the V-Model is `/testing`
> with input from the new code plus the updated FEATURE specs.
>
> Shall I start `/testing` now, or would you like to review first?"

**On agreement** ("yes" / "go" / "next") or when running inside
`/dia-orchestrator`:
-> Start `/testing` and pass the handoff context

**On rejection** ("no" / "stop" / "I want to check first"):
-> Pause and wait for user instruction

---

## Core principle: Living Documents

The artifacts (ADRs, Features, plan-context.md, arc42) are NOT one-off
specifications. They are continuously updated and always reflect the
actually-implemented state at the end.

```
Design -> Review (corrections) -> Implementation (running updates) -> Final Sync
 ^ | | |
 | v v v
 | Artifacts Artifacts Artifacts
 | adjusted adjusted finalized
 | |
 +------ Documentation == Code (always in sync) <------------------------+
```

## Keywords
Implement, code, build, plan-context, feature realization, review,
task breakdown, TDD, debugging, verification gate, regression test,
living documents, handoff, writeback, PLAN-{nn}, implementation plan,
persisted plan, plan change log
