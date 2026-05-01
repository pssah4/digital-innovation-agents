---
name: dia-guide
description: >
 Guides users through the V-Model workflow: takes stock of the current
 project state, recommends the next phase skill, audits handoff entries
 for completeness, and runs the Closing Handoff after a successful
 security audit. The guide does not perform CRUD work on artifacts;
 every concrete change lives in the phase skill it dispatches to.
 TRIGGER when the user asks "where do I start", "what comes next", "I
 am lost in the workflow", "which phase fits", "wo bin ich gerade",
 "wo soll ich anfangen", "was kommt jetzt", or explicitly requests the
 V-Model overview or end-to-end orientation. DO NOT trigger for
 individual phase work (use the specific phase skill instead:
 business-analysis, requirements-engineering, architecture, coding,
 testing, security-audit), generic mentions of "workflow", "process",
 or "next step" inside an already-running phase skill, or when a
 phase skill is already active.
disable-model-invocation: false
---

# V-Model Workflow Guide

## What this skill does (and does not do)

`/dia-guide` is the read-only orientation layer of DIA. It:

- Reads `BACKLOG.md`, the latest `HANDOFFS.md` entry, and git
  state when the user invokes it
- Recommends the next phase skill in plain text
- Audits whether the last handoff carries the binding fields
  (`triage:`, `triage_kind:`, `epic:`, `feature:`)
- Runs the Closing Handoff after a green `/security-audit`
- Does the post-`/reverse-engineering` item promotion (the only
  CRUD moment the guide owns, because it is a multi-item user
  interaction at a workflow boundary that no single phase skill
  covers)

What the guide does NOT do:

- It does not perform artifact triage. Triage lives in every phase
  skill's MANDATORY Phase 0 block. See
  `skills/project-conventions/references/graph-invariants.md`,
  section "Artifact triage at entry point".
- It does not enforce the plan gate. The plan gate lives in
  `/coding` Phase 3a as the "Plan Coverage Gate (binding, runs
  before Status flips to Active)". `/coding` runs the gate;
  the guide only reads the result.
- It does not run `/consistency-check` mode A at phase boundaries.
  Each phase skill runs mode A in its own handoff ritual. Mode B
  fires from the Closing Handoff, see below.
- It does not call other skills. It recommends; the user invokes.

## Post-reverse-engineering item promotion (the only CRUD moment)

`/reverse-engineering` finishes with a backlog seed: 20+ items at
`Status: Anticipated, Source: REV` on a single
`feature/reverse-engineer-<repo-name>` branch. Per-item branches
and per-item GitHub issues kick in only after a user-driven triage:
which seed items become real backlog candidates? `/reverse-engineering`
explicitly defers this step to the guide (see RE's Pre-Phase 0).

This is the only place where the guide writes. It is a multi-item
user interaction at a workflow boundary that no single phase skill
covers. The user drives the triage; the guide executes the per-item
operations.

Steps:

1. Read `BACKLOG.md`, list items with `Status: Anticipated, Source: REV`.
2. AskUserQuestion: which items should be promoted now (vs. left as
   anticipated for later)?
3. For each promoted item:
   ```
   python3 tools/github-integration/flow.py create-issue --item <ID>
   git tag -a <id-lower>/reverse-engineered -m "Item promoted from /reverse-engineering"
   ```
4. Update BACKLOG row: `Status` -> `Planned` (or as appropriate).
5. Recommend the next skill: typically `/business-analysis` to
   validate the BA draft, or `/coding` for items that already
   ship and just need the inventory recorded.

## Handoff state audit (read-only, on user invocation)

When the user invokes `/dia-guide` after a phase skill has finished,
the guide reads the team-workflow surface and reports any drift
between artifact state and collaboration state. It does NOT write,
fix, or tag. It surfaces, the user decides.

Audited surfaces (full reference:
`skills/project-conventions/references/team-workflow.md`):

1. **Branch.** Is the current branch on an item-branch (per
   `team-workflow.md` schema)? If not, surface a warning.
2. **Phase tag.** Did the just-finished phase set its
   `<item-id>/<phase>-done` tag via
   `tools/github-integration/flow.py tag-phase`? Each phase skill is
   responsible for setting its own tag during its handoff ritual.
   If missing, the guide names the phase skill that should re-run
   its handoff ritual.
3. **Backlog row.** Does the BACKLOG row's status reflect the phase
   progress (Building during BA -> RE -> Coding, Released only
   after merge)? Discrepancies indicate the phase skill's handoff
   ritual did not write the row before the phase-end commit.
4. **GitHub issue.** Does the issue exist and carry the right phase
   label and ticked checklist? Each phase skill calls
   `flow.py update-issue` in its handoff ritual; the guide reads
   `flow.py status --item <ID>` and reports the snapshot.
5. **HANDOFFS entry.** Does the latest entry have `triage:`,
   `triage_kind:`, and (for IMP/FIX) `epic:` + `feature:`? Missing
   fields are flagged with the responsible phase skill named.

The guide reports findings in plain text and recommends the next
step. It does not auto-fix, does not append to METRICS, does not
tag, and does not call other skills. METRICS is written by phase
skills directly; the guide only reads it.

## Feature-complete read (before release)

When the user asks "is this item ready for release?", the guide
reads the phase tags and reports. No tagging, no PR transition,
no skill invocation.

Audit:

1. Verify all required phase tags exist for the active item:
   - `<id>/code-done` (always)
   - `<id>/test-done` (always)
   - `<id>/audit-done` (when item touches security-relevant surface)

2. Run `flow.py status --item <ID>` and show the user the result.

3. Report in plain text:
   ```
   Item '<ID>' phase status:
   - code-done: yes/no
   - test-done: yes/no
   - audit-done: yes/no/n-a

   Verdict: feature-complete | missing tags: <list>
   ```

If a tag is missing, the guide names the responsible phase skill so
the user can re-run it. If feature-complete, the user can mark the
PR ready (`flow.py ready-for-review --item <ID>`) and invoke their
private release skill themselves. The guide does neither.

---

This skill is the navigation layer. Each phase builds on the previous
one and produces artifacts as input for the next phase. All phases
follow the conventions from `/project-conventions`.

## Workflow Overview

```
Phase 0 (brownfield only): /reverse-engineering REVERSE WALK
 Input: existing codebase + documentation (backwards
 Output: plan-context.md, ADRs (Inferred), up the V)
 arc42 (Snapshot), FEATURE-*.md (Observed),
 BA-{PROJECT}.md (Draft), backlog seed
 |
 v (forward walk starts here)
Phase 1: /business-analysis DESIGN
 Output: _devprocess/analysis/BA-{PROJECT}.md (left side
 | of the V)
 v
Phase 2: /requirements-engineering
 Input: BA document
 Output: Epics, Features, architect-handoff.md
 |
 v
Phase 3: /architecture
 Input: Features, ASRs, NFRs
 Output: ADRs, arc42, plan-context.md
 |
 v
Phase 4: /coding IMPLEMENTATION
 Input: plan-context.md + ADRs + Features (bottom of the V)
 Action: Load context, critical review,
 brief the Default agent (task breakdown,
 optional TDD, debugging protocol,
 verification gate), write artifacts back
 |
 v
Phase 5: /testing VERIFICATION
 Input: Implemented codebase + Features (right side
 Output: Unit + integration tests, fix-loop of the V)
 |
 v
Phase 6: /security-audit
 Input: Implemented codebase
 Output: Security report + remediation, fix-loop
 |
 v
Closing Handoff (not a phase)
 Input: Green security audit
 Output: /consistency-check mode B verdict + release-to-ba
 HANDOFFS template; user can run their private release skill
```

## Phase Transitions (read-only audit)

When the user invokes `/dia-guide` between phases, the guide reads
project state and surfaces the next step. The guide does not drive
or launch phase skills; phase skills are autonomous and own their
own handoff ritual. The guide observes:

1. Reads the latest entry in `_devprocess/context/HANDOFFS.md`
   (artifact report, triage IDs, release-readiness markers)
2. Reports the recommended next step in plain text and names the
   skill to invoke (e.g. "Recommended next: `/coding`")
3. The user invokes the next phase skill themselves; the guide does
   not call other skills

The guide does not loop, does not auto-advance, and does not block.
Every phase transition is a separate user action. The guide is
re-invoked whenever the user wants the next-step audit again.

**When a phase-skill is invoked directly (without `/dia-guide`):**
The Handoff Ritual still runs, and the handoff context is still written
to `_devprocess/context/HANDOFFS.md`. The user can then manually start
the next skill, which will pick up the handoff entry.

### Handoff entry format (binding)

Every new handoff entry in `_devprocess/context/HANDOFFS.md` starts
with a short header block that carries the **artifact triage** from
Phase 0. The next skill does not need to re-ask the triage question.

```
## {skill-from}-to-{skill-to} {YYYY-MM-DD}

triage: FEAT-01-03         # or IMP-007 / FIX-012 / ADR-04
triage_kind: feature             # one of: feature | improvement | fix | adr
epic: EPIC-01                   # mandatory for IMP/FIX; recommended otherwise
feature: FEAT-01-03         # mandatory for IMP/FIX

... (phase-specific fields, e.g. NFR summary, open questions, ...)
```

**Rule:** a skill that reads a handoff entry and finds a `triage`
ID uses it as the Phase-0 assignment and skips the triage question.
If the field is missing, the skill falls back to normal Phase-0 logic
(derive from prompt, ask if needed).

Exception: the very first handoff entry in a greenfield project
(e.g. `/business-analysis` to `/requirements-engineering` without an
existing feature) MAY carry `triage: new-feature-pending`. The
concrete FEATURE ID is then assigned by `/requirements-engineering`
and written into the next handoff entry.

## Ensure project structure exists

Before a phase starts, check whether the directory structure exists.
If not, initialize it per `/project-conventions`:

```bash
mkdir -p _devprocess/{analysis/sources,requirements/{epics,features,fixes,improvements,handoff},architecture,rules,implementation/plans,context}
mkdir -p src docs scripts memory
touch _devprocess/context/HANDOFFS.md
```

For `_devprocess/context/BACKLOG.md`, do not `touch` an empty file.
Seed it from
`skills/requirements-engineering/templates/BACKLOG-TEMPLATE.md` with
the project name, an empty dashboard, and the placeholder sections.
Every phase skill updates this file per the binding format.

For `_devprocess/rules/`, seed `technical.md` from
`skills/architecture/templates/RULES-TECHNICAL-TEMPLATE.md`. Add
`design.md` only if the project has UI surface, seeded from
`RULES-DESIGN-TEMPLATE.md`. Add `domain.md` if the project has
business-domain rules, seeded from `RULES-DOMAIN-TEMPLATE.md`.

For `src/ARCHITECTURE.map`, seed from
`skills/architecture/templates/ARCHITECTURE-MAP-TEMPLATE.md` with
empty rows. `/architecture` and `/coding` populate it as
entry-points appear.

## Start: Determine Phase

Before asking the user, the guide runs a **hybrid entry-point
detection** (added 2026-04-20): it scans the project, diagnoses the
graph state, and formulates a recommendation. The user keeps the
override.

### Step 1: Scan + recommend

1. Detect the project root convention (`_devprocess/` or `docs/`).
2. Run `/consistency-check` in Mode A (syntactic). The result is the
 current Graph-Health snapshot.
3. Infer the likely entry point from the snapshot:

| Observation | Recommended entry |
| ------------------------------------------------------------- | ------------------------------------------ |
| No V-Model artifacts at all, empty repo or pure greenfield | `/business-analysis` |
| Code exists, no `docs/analysis/BA-*.md`, no FEATUREs | `/reverse-engineering` |
| BA exists as Draft, not yet validated | `/business-analysis` Validation Mode |
| BA validated, no Epics or Features | `/requirements-engineering` |
| Features exist, no ADRs or plan-context.md | `/architecture` |
| plan-context.md exists, no recent code changes | `/coding` |
| Coding done, no test coverage / failing tests | `/testing` |
| Tests green, no security audit | `/security-audit` |
| Everything closed, release pending | Closing Handoff (`/consistency-check` mode B + `/release` if configured) |
| Graph-Health shows many orphans or dead links | `/consistency-check` + Cleanup first |

### Step 2: Present recommendation + alternatives

Show the user one `AskUserQuestion` with the recommendation as the
first option and the manual list as alternatives:

```
Graph-State (letzter Check {date}):
- Epics {n}, Features {n} (Released {a}, Building {b}, Planned {c}, Candidates {d}),
 ADRs {n}, FIX/IMPs {n}, offene Luecken {n}.

Empfehlung basierend auf dem Graph-State: {recommended entry}

Oder du waehlst manuell aus:
A0 /reverse-engineering (brownfield)
A /business-analysis (BA von Beginn)
B /requirements-engineering
C /architecture
D /coding
E /testing
F /security-audit
G Closing Handoff (Audit ist gruen, Cycle abschliessen)
H /consistency-check (nur Graph-Pflege)
I Orientierungs-Interview (helfe beim Entscheiden)
```

If the user picks the recommended option or says "ok/go/next", start
that phase. If the user picks a different option, start that one. If
the user wants an interview, ask short follow-up questions to refine
the recommendation.

### Step 3: Phase-Entry mit Konsistenz-Hinweis

Beim Start der gewaehlten Phase zeigt der Guide eventuelle
Konsistenz-Luecken aus `/consistency-check`, die fuer die Phase
relevant sind. Beispiel: vor `/architecture`-Start "Du hast 3
Features ohne Epic-Parent, das sollten wir vorher klaeren, willst
du `/consistency-check` auto-fixes laufen lassen?"

## Recommended next step per phase

These are the standard recommendations the guide surfaces when a
phase is complete. The guide does not invoke the next skill; it
prints the recommendation and the user types the slash command.

### After Reverse Engineering -> Business Analysis (brownfield only)

`/reverse-engineering` walks the V backwards and produces technical
artifacts (plan-context.md, ADRs, arc42 snapshot, FEATURE inventory,
backlog seed) plus an **evidence-based BA draft**. The draft is not
validated: it contains only what could be cited from existing
documentation, with `[NEEDS USER INPUT]` placeholders everywhere
else.

The guide **always** recommends `/business-analysis` next, even if
the draft looks complete. Code is a good technical foundation but
does not prove the product solves the right problem. The user must
validate each section.

```
Reverse engineering complete! Next step:
/business-analysis
Input: _devprocess/analysis/BA-{PROJECT}.md (Draft, reverse-engineered)

/business-analysis will:
1. Detect the draft via its status frontmatter
2. Enter Validation Mode automatically
3. Walk through each section with the user
4. Promote the status from Draft to Validated
```

### After Business Analysis -> Requirements Engineering

Check the Quality Gates from `/business-analysis`, then hand off:

```
BA complete! Next step:
/requirements-engineering
Input: _devprocess/analysis/BA-{PROJECT}.md + last entry in HANDOFFS.md
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
3. Persist an implementation plan as
 _devprocess/implementation/plans/PLAN-{nn}-{slug}.md
 (template: skills/coding/templates/PLAN-TEMPLATE.md)
4. Hand off to the Default agent with the persisted plan as
 source of truth; mid-course deviations append to the plan's
 Change Log, never rewrite past entries
5. Apply the verification gate before every completion claim
6. Close the plan (Status: Implemented, task commit SHAs) and
 write Feature specs, ADRs, and backlog back to artifacts
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

### After Security Audit -> Closing Handoff

When `/security-audit` returns a green or yellow verdict, the
guide does NOT run a release-closure phase. Cycle closure
splits into two responsibilities:

- **Artifact-graph closure** -> delegated to `/consistency-check`
  mode B (semantic). It runs the cross-phase artifact sync (BA
  Validation, Feature/ADR finalisation, arc42, plan-context
  coherence).
- **Release act** (version bump, merge chain, tag, GitHub release)
  -> delegated to the user's private `/release` skill if configured.
  DIA does not own this step; the public plugin contains no release
  mechanics because release pipelines are project-specific.

---

## Closing Handoff

The Closing Handoff is a short guide output, not a phase. It
fires after `/security-audit` has produced a non-red verdict and the
fix-loop is closed.

### Step 1: Suggest `/consistency-check` mode B

```
Security audit verdict: {green|yellow}.
Recommended next: /consistency-check mode B (semantic).
-> Confirms BA Validation is filled, all Feature/ADR statuses are
   final, arc42 reflects the actual decisions, plan-context matches
   the real tech stack.
-> Returns Release-Ready: yes/no.
```

### Step 2: On Release-Ready: yes -> closing report

```
V-Model cycle complete for {PROJECT}.

Features: {N} implemented, {N} deferred, {N} removed
Bugs: {N} resolved, {N} in backlog
Security: {N} P0/P1 resolved, {N} deferred
Tests: {N} passing, Coverage {line}/{branch}/{function}

Artifacts finalized:
- BA, {N} Epics, {N} Features
- {N} ADRs
- arc42 updated
- BACKLOG clean

Optional next step (not enforced):
- If you have a private release skill configured for this project,
  you can run it now to bump version, merge, tag, and publish. The
  cycle is otherwise complete and you can iterate from
  /business-analysis or /requirements-engineering.

After release ships, append a `release-to-ba` entry to
_devprocess/context/HANDOFFS.md so the BA Post-Release Review is
queued. Template below.
```

### Step 3: Post-release BA review queue (template)

The `release-to-ba` HANDOFFS entry queues `/business-analysis` Phase 8
against real usage data. Without it, the BA freezes at `Status:
Validated` forever and the post-release review depends on human
memory.

```
## release-to-ba {YYYY-MM-DD}

Project: {PROJECT}
Version: v{version}
Release date: {YYYY-MM-DD}
Signals source: _devprocess/context/METRICS.md (or user-provided)

Ready for BA Post-Release Review: yes
Recommended timing: {after N days of real usage, per scope:
 Simple Test: 1-3 days; PoC: 7-14 days; MVP: 14-30 days}

Hypotheses to re-validate:
- H-01: {text}
- H-02: {text}
...
```

Either the user or the guide on a later invocation reads
this entry and triggers `/business-analysis` Phase 8 once enough
signal has accumulated.

### Step 4: On Release-Ready: no -> back to the responsible skill

If `/consistency-check` mode B reports gaps (e.g. open Feature
status drift, unfinalised ADR, missing Validation numbers), the
guide names the responsible skill and the items to fix.
Cycle closure resumes after the fix.

---

## Artifact Directory Structure

```
_devprocess/
  analysis/
    BA-{PROJECT}.md                 <- Phase 1: Business Analysis
    EXPLORE-{PROJECT}.md            <- Phase 1 (PoC/MVP)
    security/
      AUDIT-{PROJECT}-{DATE}.md     <- Phase 6: Security Audit
  requirements/
    epics/
      EPIC-{nn}-{slug}.md          <- Phase 2: Requirements
    features/
      FEAT-{ee}-{ff}-{slug}.md <- Phase 2: Requirements
    handoff/
      architect-handoff.md          <- Phase 2 -> 3 handoff
      plan-context.md               <- Phase 3 -> 4 handoff
  architecture/
    ADR-{nn}-{slug}.md             <- Phase 3: Architecture
    arc42.md                        <- Phase 3: Architecture
  rules/
    technical.md                    <- Stable technical rules (max 150 lines)
    design.md                       <- UI rules (max 100 lines, optional)
    domain.md                       <- Domain rules (max 100 lines)
  implementation/
    plans/
      PLAN-{nn}-{slug}.md          <- Phase 4: persisted implementation plan
  context/
    BACKLOG.md                   <- Single source of truth for state and graph (incl. FIX rows)
    HANDOFFS.md                  <- append-only handoffs log
    METRICS.md                   <- signal layer
  requirements/
    fixes/
      FIX-{ee}-{ff}-{nn}-{slug}.md           <- Substance of bug fixes
    improvements/
      IMP-{ee}-{ff}-{nn}-{slug}.md           <- Substance of improvements

src/
  ARCHITECTURE.map                  <- Wayfinder: concept -> entry-point -> ADR
  {module}/
    README.md                       <- Optional module wayfinder
    {file}.ts                       <- Entry-points carry JSDoc headers
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
 -> PLAN-{nn} (Which tasks, in what order, with TDD gates?)
 -> Code (Implementation, commits cite PLAN-{nn})
 -> Tests (Does it work?)
 -> Fix-loop until green
 -> Security Audit (Is it safe?)
 -> Fix-loop until resolved
 -> Backlog (What's still open?)
 -> Closing Handoff (consistency-check mode B + optional /release)
```

Backchannel: changes in every phase flow back into the source artifacts
(Features, ADRs, plan-context.md). At the end, the documentation always
reflects the actual state.

## Conventions

This workflow follows the standards from `/project-conventions`:
- File names: 2-digit numbers (counters), kebab-case, English
- Language: skill instructions in English, user dialog in the user's language
- Directories: `_devprocess/` for internal documents
- Feature lifecycle: BACKLOG -> SPEC -> PLAN -> IMPL -> UPDATE

## V-Model as a decision graph, not a straight path

The Workflow Overview above shows phases in a linear sequence for
readability. In practice, the V is a decision graph. You do not always
walk it once from Phase 0 to the Closing Handoff. Several triggers
allow a running
phase to pause and route work back to a previous phase before
continuing.

The three cross-phase feedback triggers:

1. **Mid-course bug discovery** (in `/coding`). A new bug surfaces
 during implementation that is not in the feature specs, ADRs, or
 FIX-list. The coding flow pauses, routes through BUG-NNN triage,
 writes a root-cause analysis, adds the backlog entry, and only
 then writes the fix. Commit references both items.
2. **Mid-course design discovery** (in `/coding`). The implementation
 reveals that an architectural choice does not match reality. The
 coding flow pauses, amends or supersedes the affected ADR, updates
 arc42 and plan-context.md, and only then continues the feature.
3. **Mid-course requirements discovery** (in `/architecture` or
 `/coding`). The tech design or the implementation reveals that a
 FEATURE spec has a gap, ambiguity, or impossible constraint.
 Architecture pauses, routes the issue back to
 `/requirements-engineering` as a FEATURE-spec update, waits for
 the updated handoff, and only then proceeds with ADRs. Coding
 amends the FEATURE in place (per the Mid-course requirements
 trigger in `/coding`), re-runs the Plan Coverage Gate against the
 amended spec, and only then continues implementation.

Each trigger follows the same 6-step pattern: STOP, triage, write a
minimal root-cause analysis, add a backlog entry BEFORE any code or
artifact change, make the change with a commit that cites the
artefacts, then run the Final synchronization block.

**When a phase returns to an earlier phase, the lower phases downstream
do NOT re-run automatically.** The user decides whether the trigger
fix is local or whether the full walk continues from the updated
phase. The backlog entry carries the decision.

The linear look is a simplification for the guided flow, not a
law. Real projects iterate. The workflow acknowledges iteration
explicitly and keeps the forward walk as the default, not the only
path.

## Dialog handoffs

Both handoff documents (`architect-handoff.md` and `plan-context.md`)
carry a `## Dialog` section that creates a bidirectional channel
between phases. The sender writes answers to questions the receiver
raised earlier. The receiver writes new questions that came up on
this pass. This turns the handoff from a one-way throw-over-the-fence
into a conversation that works across agent sessions (which have no
memory) and human pauses.

**Binding rules:**

- **Not a blocker.** Pending dialog entries never stop unrelated work.
 Only the specific ADR, FEATURE, or code change that depends on a
 pending question waits. Everything else continues.
- **Try to self-answer first.** When a phase-skill starts a new
 session and sees pending dialog entries addressed to its side, it
 attempts to answer each from existing artifacts (codebase, ADRs,
 FEATURE specs, BA doc) BEFORE asking the user.
- **One question per session to the user.** If self-answering fails,
 the skill surfaces ALL unresolved entries in a single
 `AskUserQuestion` at session start: "N questions from {sender}
 could not be self-answered. Address now, defer to end of session,
 or record as open issues?" Per the User Interaction Protocol, one
 question per turn.
- **Append-only.** Entries and answers are never deleted. Answered
 questions have `Status: Resolved`. Questions that outlive multiple
 sessions without resolution become candidates for a backlog entry.

**Agent-agent and agent-human paths.** The self-answer step is the
agent-agent path. Two agent sessions (across time) negotiate via the
shared handoff document without a human in the loop, as long as the
artifacts contain the answer. The user only enters the loop when an
answer cannot be derived. This preserves fast forward progress
without losing the conversation trail.

See:
- `skills/requirements-engineering/templates/ARCHITECT-HANDOFF-TEMPLATE.md`
- `skills/architecture/templates/plan-context-TEMPLATE.md`

## Concurrent-agent coordination

When multiple human-agent pairs work on the same repo in parallel, the
backlog is the single synchronization point. Without explicit
ownership, two pairs can start the same backlog row at the same time,
write conflicting commits, and discover the collision only at merge.

The backlog template adds a `Claim` column to every active row. The
value encodes the human-agent pair and the claim timestamp:

```
{pair-id} @ {YYYY-MM-DD}
```

Example: `sebastian-opus-4.7 @ 2026-04-19`. An empty Claim cell means
the row is free to be picked up.

**Claim protocol:**

1. **Claim on phase start.** When a phase-skill starts work on a
 backlog row (reading FEATURE spec, writing ADR, implementing),
 it sets the Claim column to its own `pair-id` and today's date
 BEFORE any other write. The write is atomic: set Claim, then
 work.
2. **Release on phase end or `Status: Done`.** When the phase
 finishes (Handoff Ritual runs) or the item reaches Status=Done,
 the Claim column gets cleared. Rows at Status=Done do not need
 a Claim.
3. **Claim conflict.** If a pair wants to claim a row that already
 has a non-empty Claim, it does NOT overwrite. It surfaces the
 conflict to the user via `AskUserQuestion`:
 "BL-{NNN} is already claimed by {other-pair} since {date}.
 Options: (a) Ask the other pair to release; (b) Take over with
 acknowledgement; (c) Work on a different item; (d) Split the row
 into two related entries." The user decides. If "Take over" is
 chosen, the new pair appends a note to the Claim history (see
 rule 5).
4. **Stale claims.** Claims older than the phase-expected duration
 (e.g. a Feature stuck at Active for >14 days with an active
 Claim) get flagged in the next Handoff Ritual as stale. The
 guide proposes to ask the claiming pair for status or to
 release.
5. **Claim history is append-additive.** The Claim cell always holds
 the CURRENT claim. Previous claims live in the `Notizen` column
 as a dated note: `Notizen: Claim handover 2026-04-19:
 sebastian-opus-4.7 -> anna-sonnet-4.6 (context: ADR-12
 rework)`.

**Pair-id convention:** `{human-handle}-{model}`. Use a model slug that
distinguishes sessions (e.g. `opus-4.7`, `sonnet-4.6`). No spaces. If
your organisation already has a naming convention, use that instead
and document it in the project CLAUDE.md.

**No central lock service.** The backlog is the lock. Every write
happens through the normal Markdown edit cycle, so merge conflicts on
the Claim column surface the collision at the exact moment two pairs
try to own the same row. That is the correct behaviour.

## Signal layer

The workflow writes a set of lightweight signals to
`_devprocess/context/METRICS.md`, seeded from
`skills/dia-guide/templates/METRICS-TEMPLATE.md`. The file
answers one question: **is this project pulsing in the right direction
or just moving fast somewhere else?**

Signals and who writes them:

| Signal | Writer | When |
|---|---|---|
| Cycle time per FEATURE | `/coding` | Final synchronization, after commits with `Refs: FEAT-NN-NN` |
| Drift count (plan-context vs. code) | `/coding` | After Phase 2a codebase reconciliation |
| BA hypothesis validation status | `/business-analysis` | Phase 8 Post-Release Review, or any re-validation |
| Phase transition counts | this guide (or phase-skill if invoked standalone) | Every Handoff Ritual |
| Cross-phase trigger counts | the firing skill | On every mid-course trigger |

**Rules:**
- The metrics file is **append-additive**. Rows are never deleted.
 Stale cells get superseded by a new row with the same key
 (FEATURE ID, date, or trigger type).
- Writes happen **inside existing phase actions** (Handoff Ritual,
 codebase reconciliation, mid-course triggers). No separate
 metrics-collection step, no new ceremony.
- If the file does not yet exist when a skill wants to write, the
 skill copies `METRICS-TEMPLATE.md` first, then adds its row.
- Consumers read the file to decide whether to trigger a
 reconciliation run, a post-release review, or a conversation
 about workflow adherence.

## User Interaction Protocol (binding for all phase-skills)

When a phase-skill (`/business-analysis`, `/requirements-engineering`,
`/architecture`, `/coding`, `/testing`, `/security-audit`) or this
guide needs a decision from the user, the following rules apply.
They bind whether the skill is invoked via `/dia-guide` or
standalone.

1. **One question per turn.** Never batch multiple open decisions into one
 message. Finish Q1 (ask, wait, receive answer) before asking Q2.
2. **Use `AskUserQuestion`.** Plain markdown lists force the user to type
 back; the tool gives them clickable options plus a free-text "Other"
 slot.
3. **Every option must state BOTH a Pro and a Con, explicitly labelled.**
 Format the `description` field so the trade-off is scannable:
 ```
 + Pro: one short sentence stating the main upside.
 - Con: one short sentence stating the main downside or cost.
 ```
 Descriptions that list only advantages (or only risks) are a bug.
 The user decides by comparing, so both sides must be visible.
4. **Mark the recommended option as the first entry** with
 "(Recommended)" in its label. If the rationale is not obvious from the
 Pros/Cons alone, add a one-line "Empfehlung: ... weil ..." sentence in
 the turn text BEFORE the `AskUserQuestion` call.
5. **No bundled questions under time pressure.** If three decisions block
 progress, ask the first, wait for the answer, then ask the next.
 Sequencing beats efficiency here. Users get to reason about one thing
 at a time.
6. **Exceptions:** quick factual confirmations ("Proceed with the
 well-known Y/N step?") may stay as plain prompts. The rule targets
 *decisions between alternatives*, not acknowledgements.

## Keywords
V-Model, workflow, full cycle, new project, development cycle,
from analysis to implementation, full run, guide, phase transitions,
closing handoff, AskUserQuestion, one question at a time, pro/con,
recommendation
