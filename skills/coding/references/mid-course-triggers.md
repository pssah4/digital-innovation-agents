# Mid-course triggers (binding, full detail)

The SKILL.md keeps a one-table summary of the four mid-course triggers.
This file holds the full step lists. Every trigger pauses the code edit,
routes through the right artefact layer, appends a Change Log entry to
the active PLAN, and only then resumes coding. The commit message cites
every artefact touched. After the fix, the Final Synchronization block
runs.

## 1. Bug discovery (trigger=bug)

If a NEW bug surfaces while implementing the current plan, do not fix
silently:

1. STOP the code edit.
2. Triage: shipped-code bug -> `FIX-{ee}-{ff}-{nn}`; missing requirement
   -> new FEAT; design gap -> amend ADR/arc42.
3. Write a minimal root-cause analysis in `_devprocess/analysis/`
   (3-10 lines: problem, cause, fix direction, risk).
4. Add the BACKLOG row under the active Epic BEFORE any code change.
5. Append a Change Log entry to the active PLAN with `trigger=bug`,
   the new FIX/FEAT id, and a one-liner.
6. NOW write the fix. Commit cites in-progress FEAT and new FIX
   (`Refs: FEAT-05-07, FIX-05-07-01, PLAN-12`).
7. Run the Final Synchronization block, marking the new item resolved.

## 2. Design discovery (trigger=design)

If an ADR no longer matches reality, do not deviate silently:

1. STOP the code edit.
2. Triage: small correction -> amend ADR, status "Accepted (modified)";
   root-wrong -> supersede (old ADR "Superseded by ADR-{nn}", new ADR
   captures the actual decision); wording-only -> update Context or
   Consequences in place.
3. Write a root-cause entry in
   `_devprocess/analysis/ADR-{nn}-review.md` (3-10 lines: what the ADR
   claimed, what the code proves, what changes, what still holds).
4. Update arc42.md and plan-context.md if affected.
5. Append a Change Log entry to the PLAN with `trigger=design`. If the
   pivot invalidates remaining tasks, mark the plan Superseded and
   create PLAN-{NNN+1}; the old plan stays for traceability.
6. Resume coding. Commit cites the ADR change
   (`Refs: FEAT-05-07, ADR-12 (amended), PLAN-12`).
7. Run Final Synchronization.

## 3. Requirements discovery (trigger=requirement)

If a FEATURE spec is ambiguous, incomplete, or contradicts the codebase,
do not reinterpret silently:

1. STOP the code edit.
2. Triage:
   - Ambiguous SC -> rewrite, keep number, add rationale comment.
   - Missing SC -> add a new SC with the next number.
   - Wrong SC -> amend OR mark "Removed: {reason}" (append-only, never
     delete the line).
   - Scope wrong at the root -> open the decision with the user via
     AskUserQuestion; do not re-shape the feature graph unilaterally.
3. Update plan-context.md if tech stack or integrations shift.
4. Re-run the Plan Coverage Gate on the active PLAN. Every amended SC
   re-maps to a task or is marked Deferred. Append Change Log entry
   with `trigger=requirement`.
5. Resume coding. Commit cites the FEATURE change
   (`Refs: FEAT-05-07 (SC-03 amended), PLAN-12`).
6. Run Final Synchronization.

## 4. Capability discovery (trigger=capability)

The code is about to add a NEW user-facing capability that no FEATURE
describes yet.

**Detection signals (any one):** new route/handler/command not in
plan-context.md or any FEATURE's `Source (Implementation):`; new Sidebar
entry, Settings tab, or top-level UI surface; new CLI flag or public
API endpoint changing the user contract.

**Tech-only changes do NOT trigger this dialog** (helpers, refactors,
private utilities, bugfixes, docs, tests).

1. STOP the code edit.
2. Triage with one `AskUserQuestion` at a time. The agent does not
   invent persona, JTBD, or outcome:
   - A: Real new user-facing capability, or technical byproduct?
     (byproduct -> skip dialog and code on.)
   - B: For which Persona? (pick from BA's list, or "Other" + short
     description.)
   - C: Which Job-to-be-Done is solved? (free text.)
   - D: Which measurable outcome do we expect? (free text; if user
     defers, accept `[AWAITING BA Nachtrag]`.)
3. Write the FEATURE-spec draft now, not after the code, from
   `skills/requirements-engineering/templates/FEATURE-TEMPLATE.md`.
   Frontmatter: `source: capability-capture during /coding`. Fill
   Capability (observable SC-01), Persona, JTBD, outcome.
4. Write the BA-Nachtrag. Two options:
   - **Project-wide:** append to
     `_devprocess/analysis/BA-{PROJECT}.md` under
     `## User-Input-Capture ({date})`. Mark `unvalidated`.
   - **Item-scoped:** create a stub Item-BA at
     `_devprocess/analysis/BA-FEAT-{ee}-{ff}-{slug}.md` from
     `BA-MINI-TEMPLATE.md`. The FEATURE gets `ba-ref:` pointing at it.
   Never edit validated BA sections silently.
5. Epic assignment: fit existing Epic (add to its MVP-Features table)
   or create new Epic with a placeholder Hypothesis Statement.
6. Add the FIX/IMP backlog row. Phase = Building if all four answers
   provided; Phase = Candidates with `needs refinement: BA-Anchor
   fehlt` if Question D was deferred.
7. Run `/consistency-check` to verify the new Feature/Epic/BA links.
8. Resume coding. Commit cites the new FEATURE-ID
   (`Refs: FEAT-08-17, PLAN-18`).
9. Final Synchronization promotes the FEATURE to Done if fully
   realised.

**Bypass.** If the user says "scratch change, no feature yet", the
commit carries `[no-capture: scratch]` and `/consistency-check` flags
the orphan later for retroactive capture. Deliberate bypass is a
recorded action, not a hidden one.
