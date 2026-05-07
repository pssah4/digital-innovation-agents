---
title: Coding
description: The handoff skill that loads context, reviews critically, persists plans, briefs the Default agent, captures bugs, and writes artifacts back continuously.
---

# Coding

`/coding` is the most involved skill in the workflow. It does not
write code itself. The Default agent in your coding tool does that.
Instead, `/coding` acts as a briefing and review layer that
structures how the Default agent approaches the task.

## Two entry points (plus a fast lane)

`/coding` has two ways in:

1. **Implementation entry.** A handed-off feature with a
   `plan-context.md` and a clear backlog row. The four phases below
   apply.
2. **Bug-capture entry.** A reported bug outside an active
   implementation. `/coding` captures the FIX artefact (FIX backlog
   row, FIX detail file, branch) without forcing an immediate fix.
   The fix gets scheduled like any other backlog item.

Both entries share the same writeback discipline: backlog row first,
artifact body second.

A third path, the **[Hotfix lane](../concepts/hotfix-lane)**, is
allowed for trivial bug fixes that touch at most three files,
introduce no breaking change, and fit an existing FEAT. There the
fix runs first; the FIX-Row, detail file, commit, GitHub issue (in
`github-sync`), and `flow.py validate-fix` happen right after to
keep the work visible and the consistency graph intact.

## Four phases (implementation entry)

```
Phase 1: Triage gate + load context (plan-context.md, ADRs, FEAT, CLAUDE.md, wayfinder)
Phase 2: Critical review against the real codebase
Phase 3: Plan persistence (PLAN-NN) and implementation
Phase 4: Completion. Verification gate, regression cycle, final sync.
```

## Phase 1: Triage gate and load context

### Phase 1a: Triage gate

Before loading context, `/coding` confirms the artifact triage. Every
inbound item is one of: FEAT, IMP, FIX, ADR. The triage gate routes:

- A new capability that delivers user value -> FEAT
- An improvement of an existing FEAT -> IMP
- A bug in shipped code -> FIX
- A pure architectural decision with no implementation handoff -> ADR

If the inbound item is mistyped, `/coding` re-routes to the correct
phase before loading context.

### Phase 1b: Load context

`/coding` loads the full context stack:

- `plan-context.md` (architecture handoff)
- All ADRs referenced by the FEAT
- The FEAT spec itself
- `src/ARCHITECTURE.map` (wayfinder root)
- The relevant module READMEs under `src/{module}/README.md`
- The project `CLAUDE.md`
- `_devprocess/rules/{technical,design,domain}.md`
- The current backlog row for the FEAT

The wayfinder is loaded explicitly. It is the canonical answer to
"where does X live in the code?".

## Phase 2: Critical review

Before any code changes, `/coding` reconciles the design artifacts
with the real codebase:

- Do the ADR proposals match the actual architecture?
- Do existing patterns contradict the proposals?
- Are the tech-stack assumptions in `plan-context.md` correct?
- Are dependencies or constraints missing?
- Are modules affected but not mentioned in the designs?
- Does the wayfinder still match the code at the entry-points the
  ADR references?

Every divergence is written back into the source artifacts before
implementation begins:

- ADR drift -> amend the ADR (substance), update the backlog row
  (status, last-change), update the wayfinder if entry-points moved.
- FEAT Success Criteria drift -> adjust the FEAT, update the
  backlog row.
- Missing decisions -> create a new ADR, link from the backlog.

This is the moment where the V-Model turns from plan into reality.
The drift count goes into `METRICS.md`.

## Phase 3: Plan persistence and implementation

### Phase 3a: Plan persistence

Every non-trivial implementation is persisted as a
`PLAN-{nn}-{slug}.md` file in `_devprocess/implementation/plans/`.
The plan is added to the backlog as a row, and the plan id appears
in the FEAT's `Refs` column.

The plan file follows the standard structure:

1. **Context**: diagnostic, not descriptive. Root-cause analysis.
2. **Changes**: one subsection per file, BEFORE / AFTER code blocks.
3. **File summary**: table (File | Change | Risk).
4. **Not affected**: explicit list of unchanged files (blast radius).
5. **Verification**: acceptance criteria, build always step 1.
6. **Plan Coverage Gate**:
   - **SC coverage**: which Success Criterion each plan step closes
   - **ADR alignment**: which ADR each technical decision honours
   - **Codebase anchoring**: every file referenced in the plan exists
     in the repo or is named explicitly as new
   - **Verify commands**: ready to run, not pseudocode

Plans go through three states tracked in the backlog row: Draft (in
review), Active (executing), Done (closed with commit SHA).

For agents without a native planning mode, `/coding` writes the plan
to disk first and only then begins editing code. For agents with a
native planning mode (Claude Code's plan mode, Cursor's planner),
the native plan is exported to `PLAN-NN` after approval.

### Phase 3b: Task-breakdown guidelines

The Default agent is told:

- Split each task into bite-size steps (2 to 5 minutes each): write
  failing test, verify it fails, write minimal code, verify it
  passes, commit.
- Every task has a file list (Create / Modify / Test with exact
  paths) anchored in the wayfinder.
- No placeholders: "TBD", "TODO", "implement later", "Similar to
  Task N" are forbidden.
- Self-review after plan creation: spec coverage, placeholder scan,
  type consistency, wayfinder anchoring.

### Phase 3c: TDD mode (optional)

Opt-in. When the user enables TDD, `/coding` hands this rule to the
Default agent: "No production code without a failing test first."
RED, verify RED, GREEN, verify GREEN, REFACTOR.

Exceptions (with user confirmation): throwaway prototypes, generated
code, configuration files.

### Phase 3d: Debugging protocol

If a bug appears during implementation, the Default agent follows a
4-phase root-cause process:

- **Phase A: Root Cause.** Read error, reproduce, check recent
  changes, trace data flow backwards.
- **Phase B: Pattern Analysis.** Find working examples, read
  reference completely.
- **Phase C: Hypothesis.** One hypothesis, smallest possible change,
  one variable at a time.
- **Phase D: Implementation.** Failing test, single fix, verify.
- **Phase D.5: Architecture alarm.** After 3+ failed fix attempts,
  STOP. This is not a bug, it is a wrong architecture. Discuss
  with the user.

Every bug, even a trivial one, lands as a `FIX-{ee}-{ff}-{nn}` row
in `BACKLOG.md` BEFORE any fix is written. The detail file at
`_devprocess/requirements/fixes/FIX-{ee}-{ff}-{nn}-{slug}.md`
carries the causal chain (Problem, Root Cause, Chain of steps
leading to the error). Priority is P0 (immediate), P1 (short-term),
P2 (medium-term).

### Phase 3e: Mid-course discoveries

Three triggers can pause `/coding` and route work back to an earlier
phase:

- **Mid-course design discovery.** An ADR no longer matches reality.
  Pause, amend or supersede the ADR, update arc42, the wayfinder,
  and `plan-context.md`, then continue.
- **Mid-course requirements discovery.** A FEAT spec has a gap.
  Pause, route back to `/requirements-engineering` for a FEAT update.
- **Mid-course capability discovery.** The implementation needs
  something architecture never planned (a new library, a new
  infrastructure component, a new pattern). Pause, capture the
  capability gap as an ADR, route through `/architecture` to
  integrate the decision.

Each trigger follows the same 6-step pattern: STOP, triage, root
cause, backlog, change with commit Refs, Final sync.

## Phase 4: Completion

### Phase 4a: Verification gate

The rule: no completion claims without fresh verification evidence.

Before declaring anything "done", the Default agent runs the seven-step
gate function. Steps 1 to 5 verify the claim ("tests pass", "build
works", "bug fixed"). Steps 6 and 7 (added in v3.2.0) verify that the
new code is reachable and that a user or caller can actually trigger
the FEATURE.

1. **Identify** which command proves the claim
2. **Run** it fully (not cached)
3. **Read** the full output, check exit code, count failures
4. **Verify** the output matches the claim
5. **Claim** the status only now, with the evidence
6. **Reachability check** (subtype-aware). For every new top-level
   symbol introduced this session: verify a caller exists outside the
   definition file and outside test files. For `subtype: library`:
   accept a public API export as a valid alternative. On fail, the
   FEATURE Done-status is locked.
7. **Activation-path check.** Read the FEATURE's `## Activation Path`
   section and verify each entry exists in the code (route registered,
   command registered, public symbol exported, etc.). The activation
   path string is a grep target. On fail, the FEATURE Done-status is
   locked.

Forbidden language without fresh verification: "should work",
"probably okay", "tests should be green now". See
[Verification Gates](../concepts/verification-gates) for the
complete forbidden list. Reachability tooling per language lives in
the [reachability-by-stack reference](../reference/reachability-by-stack).

### Phase 4b: Regression test cycle (for every bug fix)

1. Write the regression test reproducing the bug.
2. **Run 1**: test MUST pass (fix is in).
3. Revert the fix temporarily.
4. **Run 2**: test MUST fail (proves it catches the bug).
5. Restore the fix.
6. **Run 3**: test MUST pass again.

The FIX detail file at
`_devprocess/requirements/fixes/FIX-{ee}-{ff}-{nn}-{slug}.md`
gets a `## Regression test` section: "Regression test verified via
red-green cycle on {date}". The commit SHA goes into the backlog row.

### Phase 4c: Deferred-stub marker convention (since v3.2.0)

Stubs are normal in iterative development. What is forbidden are
silent stubs. Every stub MUST carry a marker AND a paired FIX-row in
the backlog. The two are bidirectionally bound; `/consistency-check`
Mode A enforces the binding via invariant E-14.

Marker syntax (per-language comment style, identical content):

```
// FIXME(stub): <one-line reason> -- see FIX-{ee}-{ff}-{nn}
# FIXME(stub): <one-line reason> -- see FIX-{ee}-{ff}-{nn}
```

Use `//` for the C-family (TypeScript, JavaScript, Java, Go, Rust,
C#, Swift, Kotlin). Use `#` for Python, Ruby, R, shell scripts. The
FIX-row carries the context: why the stub is there, what unblocks it,
what to do when it is unblocked.

Mode A surfaces two finding types:
- `stub-without-fix-row` -- marker references a missing or resolved
  FIX-ID
- `fix-without-stub-evidence` -- FIX-row claims a stub but no marker
  references it

A marker without a FIX-row is invisible to the backlog, nobody plans
its removal. A FIX-row without a marker is stale paperwork, nobody can
find the actual code. The bidirectional binding turns silent deferrals
into auditable items.

### Final synchronization

After implementation is verified, `/coding` updates in this order
(state first, substance second):

1. **Backlog row** (Status -> Done, phase -> code, last-change,
   commit SHA, claim cleared).
2. **Wayfinder** (`src/ARCHITECTURE.map` row updated, JSDoc /
   docstring header in entry-point file refreshed, module README
   updated).
3. **FEAT spec** (substance only: Success Criteria verified,
   optional `## Code Pointer` appendix that references concept
   names, not file paths).
4. **ADRs** (`## Implementation Notes` appendix updated; status
   lives in the backlog row).
5. **PLAN-NN row** (Status -> Done, change log filled in).
6. **FIX detail files** (regression test reference, all FIX backlog
   rows updated with commit SHAs).
7. **`plan-context.md`, `arc42.md`, `memory/MEMORY.md`** (when
   applicable).
8. **`METRICS.md`** (cycle time per FEAT, drift count appended).

The result: documentation reflects the actual state, not the
original plan, with state in the backlog and substance in the
detail artifacts.

## Living Documents

This continuous writeback is the Living Documents pattern.
Artifacts are never frozen after Phase 3. They evolve with the
code. State changes always go through the backlog row first. See
[Living Documents](../concepts/living-documents) and the
[Three-layer documentation model](../concepts/three-layer-documentation)
for the full pattern.

## Handoff

`/coding` ends with the 4-part [Handoff Ritual](../concepts/handoff-rituals):
artifact report, handoff context in `HANDOFFS.md` with references
to the new FIX rows and PLAN ids, phase-end commit
(`feat(code): {ITEM-ID} implementation complete`) plus
`tag-phase --phase code` and `sync-status --item {ITEM-ID}` (no-op outside `mode = "github-sync"`), transition question for `/testing`.
The guide runs `/consistency-check` Mode A on the changed
artifacts at the boundary.

## Read the skill file

Want to see the exact instructions the agent follows? The skill
file is [`skills/coding/SKILL.md`](https://github.com/pssah4/digital-innovation-agents/blob/main/skills/coding/SKILL.md)
on GitHub.

## What's next

- [Testing guide](./testing), the next phase with the
  role-alongside-TDD section
- [Living Documents concept](../concepts/living-documents), the
  writeback pattern
- [Three-layer documentation model](../concepts/three-layer-documentation),
  why backlog row first
- [Verification Gates concept](../concepts/verification-gates), why
  evidence matters
