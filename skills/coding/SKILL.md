---
name: coding
description: >
 Handoff skill and bug-capture entry point: loads plan-context.md and all
 design artifacts, performs a critical review against the real codebase, and
 ensures continuous writeback to the artifacts during and after
 implementation. Also the entry point when a bug is reported outside of an
 active implementation run -- captures the FIX artefact (BACKLOG row + FIX
 detail file + branch) without forcing an immediate fix. Use this skill when
 the user mentions "implement", "code", "realize plan-context", "build
 feature", "Bug gefunden", "es gibt einen Fehler", "Fix erfassen", or similar,
 and either a plan-context.md / FEATURE spec exists OR a bug surfaced.
 This skill does NOT take over the coding workflow -- the Default Claude
 Code agent remains responsible for the actual implementation. This skill
 ensures the context is critically reviewed, cleanly handed off, and
 artifacts stay up to date.
disable-model-invocation: false
---

# Coding -- Review, Handoff & Living Documents

This skill has two entry conditions:

1. **Implementation entry** (the typical case): a FEATURE / IMP / ADR /
   FIX is ready to be built. The full review-implement-writeback flow
   below applies.
2. **Bug-capture entry** (no implementation required): the user
   reports a bug outside of an active implementation run. The skill
   captures the FIX artefact (BACKLOG row + FIX detail file + branch)
   and lets the user decide whether to implement now or later. See
   "Bug-capture entry point" in MANDATORY Phase 0 below.

The triggers in the description ("implement", "code", "build feature")
cover case 1. Phrases like "Bug X", "Fix gefunden", "es gibt einen
Fehler in FEAT-..." cover case 2.

## MANDATORY Pre-Phase 0: Branch and item check

Coding implements a specific FEAT / FIX / IMP from the backlog.
Run the team-workflow check (full rules:
`skills/project-conventions/references/team-workflow.md`):

1. Identify the active item. For mid-cycle FIX or IMP discovered
   during coding, write the BACKLOG row first.
2. Verify the branch matches `feature/<item-id-lower>-<slug>` (or
   `fix/...` / `chore/...`). On a wrong branch, AskUserQuestion to
   switch.
3. Skill-triggered GitHub integration:

   ```
   python3 tools/github-integration/flow.py create-issue --item <ID>
   python3 tools/github-integration/flow.py open-draft-pr --item <ID>
   ```

4. At Handoff Ritual end, tag the phase:

   ```
   python3 tools/github-integration/flow.py tag-phase --item <ID> --phase code
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

### Bug-capture entry point (no implementation required)

`/coding` is also the entry point when the user reports a bug
**outside** of an active implementation run ("ich habe einen Bug in
Feature X gefunden", "Login bricht ab"). The skill MUST be able to
capture the bug without forcing the user into an immediate fix. Flow:

1. Run the same Phase 0 triage. The user's prompt usually maps to FIX.
2. Identify the affected `FEAT-{ee}-{ff}` (ask if unclear).
3. Write the BACKLOG row first (status `Ready`, phase `Building`,
   priority from the user, Source `BUG`).
4. Create the detail file at
   `_devprocess/requirements/fixes/FIX-{ee}-{ff}-{nn}-{slug}.md` from
   `templates/FIX-TEMPLATE.md`. Fill Symptom and what is currently
   known about the cause; leave Fix and Regression test empty.
5. Run the phase-end commit (per `team-workflow.md`) with message
   `chore(fix): FIX-{ee}-{ff}-{nn} bug captured`. The commit creates
   the `fix/<id-lower>-<slug>` branch via the commit-boundary check.
6. Ask the user: "Bug erfasst. Soll ich jetzt den Fix implementieren
   (`/coding` Phase 1+ auf diesem Branch), oder reicht die Erfassung
   fuer jetzt?"

If the user picks "nur erfassen", the skill ends after the commit
and the bug waits in the backlog as a regular FIX item. The next
`/coding` invocation on that FIX-ID resumes from Phase 1.

The capture path is identical to the in-flight Mid-course bug
discovery trigger (Phase 4b later in this file), only the entry
condition differs. Both converge on the same artefact shape: BACKLOG
row + FIX detail file + branch.

### Hotfix lane (fix-now, document-after)

Trivial bugs may fix first, document after, when **all five** hold:
at most 3 files; no new feature or dependency; no breaking change to
a public API; under 15 minutes; existing FEAT as parent. Any miss ->
standard bug-capture flow.

Flow when allowed:

1. Fix immediately; run relevant tests.
2. Write the FIX BACKLOG row and detail file. Commit
   `fix: FIX-{ee}-{ff}-{nn} <desc>` with `Refs:` trailer.
3. In `github-sync` mode: `gh issue create --title "FIX-{ee}-{ff}-{nn}: {slug}" --label "fix,hotfix"`,
   then `python3 tools/github-integration/flow.py sync-status --item FIX-{ee}-{ff}-{nn}`.
4. Always close with `python3 tools/github-integration/flow.py validate-fix --item FIX-{ee}-{ff}-{nn}`.
5. Acknowledge in chat: modified files, FIX-ID, issue URL, validate-fix verdict.

The regression-test cycle (Phase 4b) still runs; the 15-minute budget
includes the test.

Four safety nets keep the lane honest:

- **FIX-Row** in BACKLOG.md (mandatory, even retroactively).
- **Commit cites FIX-ID** in subject and `Refs:` trailer.
- **Deferred-stub markers** bind `// FIXME(stub): ... -- see FIX-{id}` to
  the FIX row's Notes column.
- **Regression-test cycle** writes a `## Regression test` entry.

`validate-fix` runs the hotfix-scoped consistency check: FIX row
exists with correct id and refs; at least one commit cites the id;
no orphan `FIXME(stub):` references.

Anti-misuse: if hotfixes exceed 30% of an iteration, the lane is being
abused as a process bypass; file a quality-debt item.


## MANDATORY: Backlog as single source of truth (no asking)

Whenever this skill creates or modifies a Feature, Epic, ADR, FIX,
IMP, or PLAN, it writes the backlog row in
`_devprocess/context/BACKLOG.md` BEFORE touching the artifact body.

Status vocabulary, defaults per artifact type, and frontmatter status
fields for ADR/PLAN: see
`skills/project-conventions/SKILL.md#canonical-specs` (Backlog
vocabulary, Frontmatter spec).

**Sync chain on every status or phase change (binding order):**

1. Update the backlog row (status, phase, claim, last-change, refs) FIRST
2. Update the artifact body
3. Record commit SHA after the commit lands
4. Recompute dashboard counts
5. Run `/consistency-check` mode A at the end of the skill phase

Backlog-first order prevents the dominant drift class (status stuck at
"Ready" while code shipped). If the backlog write fails, the artifact
write does not run. Full rules:
`skills/project-conventions/references/graph-invariants.md` (section
"Backlog row format").


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

Chores are not a separate node type. Every piece of work outside of a
Feature is either a **FIX-{ee}-{ff}-{nn}** at
`_devprocess/requirements/fixes/` (seeded from `templates/FIX-TEMPLATE.md`)
or an **IMP-{ee}-{ff}-{nn}** at
`_devprocess/requirements/improvements/` (seeded from
`templates/IMP-TEMPLATE.md`).

Frontmatter spec (required keys, forbidden keys, `feature:` / `epic:`
mandatory for FIX and IMP, `depends-on` semantics): see
`skills/project-conventions/SKILL.md#canonical-specs` (Frontmatter
spec). Details on dependency graph acyclicity:
`graph-invariants.md` (section "Dependencies and implementation order").

## MANDATORY: Writing style

See `skills/project-conventions/SKILL.md#canonical-specs` (Writing
style). Same rules apply to every artifact this skill produces.


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
8. _devprocess/context/BACKLOG.md (open items, including FIX-{ee}-{ff}-{nn} rows)
9. _devprocess/requirements/fixes/FIX-*.md (open and resolved bug specs)
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
B) I want to run the V-Model workflow -> /dia-guide
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
ADRs: {count} reviewed | Features: {count} | Success Criteria: {count}

| Category        | Item                       | Action                        |
|-----------------|----------------------------|-------------------------------|
| CHANGES NEEDED  | ADR-02: {title}            | {recommendation}              |
| MISSING         | {module/pattern}           | {what to add}                 |
| RISKS           | {risk}                     | {mitigation}                  |

Please confirm or correct before I create the implementation plan.
```

CONFIRMED items are omitted; absence from the table means "matches the
codebase". Only divergence, gaps, and risks are listed.

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
"Drift count (plan-context.md vs. real code)" table with three columns:

| Date | Drift flagged | Drift resolved |
|------|---------------|----------------|

Drift flagged = count of CHANGES NEEDED + MISSING items. Drift
resolved = items actually written back in step 2c. If `METRICS.md`
does not yet exist, copy `skills/dia-guide/templates/METRICS-TEMPLATE.md`
first, then append. Rising drift means the ADRs or plan-context are
losing touch with reality.

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
5. Flip status to `In Progress` once implementation begins.
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

**Plan Coverage Gate (binding, runs before Status flips to In Progress).**

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
4. Document the bug as a FIX artefact:
   - Add a row to `_devprocess/context/BACKLOG.md` under the affected
     Epic with ID `FIX-{ee}-{ff}-{nn}`, status, phase, priority
     (P0/P1/P2), and the commit SHA once the fix lands.
   - Create the detail file at
     `_devprocess/requirements/fixes/FIX-{ee}-{ff}-{nn}-{slug}.md`
     using `templates/FIX-TEMPLATE.md`. The file carries Symptom,
     Root cause (causal chain), Fix, Regression test.

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

**Writeback:** Every bug found, even if the fix is trivial, gets a
BACKLOG row (`FIX-{ee}-{ff}-{nn}`) plus a detail file at
`_devprocess/requirements/fixes/FIX-{ee}-{ff}-{nn}-{slug}.md`
carrying symptom, root cause, causal chain, fix description,
priority. The BACKLOG row carries status, phase, claim, last-change,
and commit SHA; the FIX file carries the substance.

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

**The gate (4 rows, all mandatory):**

| Claim                      | Required proof                                                    | Pass / Fail                          |
|----------------------------|-------------------------------------------------------------------|--------------------------------------|
| Tests / build / bug-fix    | Run the concrete command in this message; read full output        | Exit code 0 and 0 failures           |
| New symbol is reachable    | Caller exists outside definition file and outside tests           | Subtype-aware (see references)       |
| FEATURE Activation Path    | Every entry in `## Activation Path` matches an identifier in code | Grep or AST query returns a hit      |
| Wayfinder consistent       | `src/ARCHITECTURE.map` reflects new/renamed/removed entry-points  | Row matches the codebase             |

Subtype rules for reachability and activation-path entry types
(command / route / UI-element / endpoint / scheduled-job / tool /
hotkey / public-API), forbidden language list, and "what is not enough"
table: `references/verification-gate-subtypes.md`.

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

**Documentation:** The FIX detail file at
`_devprocess/requirements/fixes/FIX-{ee}-{ff}-{nn}-{slug}.md` gets a
note in its `## Regression test` section: "Regression test verified
via red-green cycle on {date}".

### Phase 4c: Deferred-stub marker convention (binding)

A stub implementation is any code that intentionally returns a no-op,
empty result, or hard-coded placeholder while waiting on later wiring,
external data, an upstream feature, or a real implementation in a
later phase. Stubs are normal in iterative development; what is
forbidden is silent stubs.

**Every stub MUST carry a `FIXME(stub):` marker AND a paired
`FIX-{ee}-{ff}-{nn}` row in the backlog.** The two are bidirectionally
bound: each marker references its FIX-ID, each FIX-row that documents
a stub references at least one source location.

Marker syntax (per-language comment style, identical content):

```
// FIXME(stub): <one-line reason> -- see FIX-{ee}-{ff}-{nn}
# FIXME(stub): <one-line reason> -- see FIX-{ee}-{ff}-{nn}
```

Use `//` for C-family languages (TypeScript, JavaScript, Java, Go,
Rust, C#, Swift, Kotlin). Use `#` for Python, Ruby, R, shell scripts.

The FIX-row in `_devprocess/context/BACKLOG.md` and its detail file at
`_devprocess/requirements/fixes/FIX-{ee}-{ff}-{nn}-{slug}.md` carry the
context: why the stub is there, what unblocks it, what to do when it
is unblocked.

**`/consistency-check` Mode A enforces the binding (E-13):**

- Every `FIXME(stub):` in the source tree must reference an open
 FIX-row by ID; missing or unresolved IDs surface as
 `stub-without-fix-row` findings.
- Every FIX-row whose notes contain `Wiring offen`, `stub`, or similar
 deferral language must reference at least one source location;
 missing references surface as `fix-without-stub-evidence` findings.

**Why bidirectional.** A marker without a FIX-row is invisible at the
backlog level; nobody plans to remove it. A FIX-row without a marker
is stale paperwork; nobody can find the actual code to remove. The
bidirectional binding turns silent deferrals into auditable items.

### Mid-course triggers (binding)

Four conditions interrupt coding and route through the artefact layer
BEFORE the next code edit. The common pattern: STOP, route, append a
Change Log entry to the active PLAN with the right `trigger=` tag,
THEN resume. Commit cites every artefact touched.

| Trigger        | Fires when                                       | Routes through               |
|----------------|--------------------------------------------------|------------------------------|
| `bug`          | New bug surfaces, not in any spec or FIX list    | New FIX or amended ADR       |
| `design`       | ADR no longer matches the codebase               | Amend or supersede ADR       |
| `requirement`  | FEATURE SC is ambiguous, missing, wrong, or scoped wrong | Amend FEATURE, re-run Coverage Gate |
| `capability`   | New user-facing capability has no FEATURE yet    | Capture FEATURE + BA-Nachtrag via user dialog |

Full step lists, detection signals for `capability`, BA-Nachtrag
options (Project-wide vs. Item-scoped), and the `[no-capture: scratch]`
bypass: `references/mid-course-triggers.md`.

Why this matters: bugs and design pivots that ship in code without an
artefact trail produce backlog drift within days. The Change Log entry
is the audit hook that lets a future reviewer (human or
`/consistency-check`) reconstruct what changed and why.

### Final synchronization (cross-artifact)

After verification, run writeback in this order. Backlog FIRST,
artifacts follow. **Per-commit gate (binding):** the backlog reflects
post-implementation state BEFORE every commit that references a
FEATURE, FIX, IMP, ADR, or PLAN id. Every such commit message cites
the artifacts touched (`Refs: FEAT-01-03, FIX-013, PLAN-07`).

| # | Layer            | Action                                                                                                  |
|---|------------------|---------------------------------------------------------------------------------------------------------|
| 1 | Backlog          | Update status/phase/SHA/claim/refs for every Feature, ADR, PLAN, FIX, IMP touched. Refresh dashboard.   |
| 2 | Wayfinder        | `src/ARCHITECTURE.map` rows, JSDoc headers in new entry-points, module READMEs; in the SAME commit as the code. |
| 3 | FEATURE specs    | Substance only; SC accuracy. Status lives in the backlog row.                                           |
| 4 | ADRs             | Add `## Implementation Notes` appendix with actual outcome. Document architecturally relevant deviations in Consequences. |
| 5 | PLAN-{nn}        | Fill `## Implementation Notes`: per-task SHA, deviations, test-count delta, cycle time. Change Log appended, never rewritten. |
| 6 | FIX artefacts    | BACKLOG row resolved; FIX detail file's `## Fix` and `## Regression test` sections filled.              |
| 7 | METRICS          | Append rows: "Cycle time per FEATURE", "Phase transition counts", "Cross-phase trigger counts".         |

If applicable: plan-context.md (tech stack changed), arc42 sections,
`_devprocess/rules/{technical,design,domain}.md` (new convention),
memory/MEMORY.md, CLAUDE.md.

### Completion summary

```
Done: {what landed}.
Deviations: {one-liner or None}.
```

---

## Handoff Ritual (mandatory at end of phase)

`/coding` always runs this ritual at the end, regardless of how it was
started (directly or via `/dia-guide`).

### Part 1: Artifact report

List all artifacts produced or updated with full paths:

```
Produced / updated:
- src/{files}: {summary}
- _devprocess/implementation/plans/PLAN-*.md: {status updates, SHAs}
- _devprocess/requirements/features/FEATURE-*.md: {status updates}
- _devprocess/architecture/ADR-*.md: {status and implementation notes}
- _devprocess/requirements/handoff/plan-context.md: {tech stack updates if any}
- _devprocess/requirements/fixes/FIX-*.md: {new or updated FIX specs, FIX-{ee}-{ff}-{nn}}
- _devprocess/context/BACKLOG.md: {new/resolved items, including FIX rows}
```

### Part 2: Handoff context

Append a new entry to `_devprocess/context/HANDOFFS.md` with:

- Summary of what was implemented
- Deviations from plan (with references to the updated ADRs/Features)
- Bugs found and their FIX-{ee}-{ff}-{nn} IDs (resolved and open)
- Open concerns for testing or security phase
- Assumptions that were made and should be verified

### Part 3: Phase-end commit

Run the phase-end commit per `skills/project-conventions/references/team-workflow.md`
section "Phase-end commit (binding)". The block fires the binding
branch-and-item check, stages every artefact this phase produced
(source code, ARCHITECTURE.map updates, JSDoc headers, module
READMEs, PLAN, FIX specs, FEATURE/ADR writeback, BACKLOG row
updates), commits with the canonical message, sets the phase tag,
and opens a draft PR if one does not exist yet.

Canonical commit message for CODING:

```
<feat|fix>(code): <ITEM-ID> coding complete

<one-line summary of what shipped>

Refs: <ITEM-ID>[, ADR-NN, PLAN-NN, FIX-...]
```

Use `feat` for new FEATURE work, `fix` for FIX work, `chore` for IMP
work. Long coding phases produce multiple intermediate commits per
task; only the final phase-end commit gets the `<id>/code-done` tag.

After the commit lands, run:

```
python3 tools/github-integration/flow.py tag-phase --item <ID> --phase code
python3 tools/github-integration/flow.py sync-status --item <ID>
```

`sync-status` mirrors the BACKLOG Status column to the GitHub
issue and project (and the GitHub Assignee back into the BACKLOG
Claim column). It is a no-op outside `mode = "github-sync"`.

Skip the commit silently if the working tree has no changes.

### Part 4: Transition question

Ask the user:

> "Implementation is complete. Recommended next: `/testing` -- input
> from the new code plus the updated FEATURE specs.
>
> Shall I start `/testing` now, or would you like to review first?"

**On agreement** ("yes" / "go" / "next") or when running inside
`/dia-guide`:
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
