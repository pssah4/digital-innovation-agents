---
name: dia-guide
description: >
 Guides users through the V-Model workflow: takes stock of the project
 state, recommends the next phase skill, audits handoff state, and runs
 the Closing Handoff after a green security audit. Explicit user command:
 invoke for "where do I start", "what comes next", "wo bin ich gerade",
 "was kommt jetzt", or the V-Model overview. Never for individual phase
 work.
disable-model-invocation: true
---

# V-Model Workflow Guide

## What this skill does (and does not do)

`/dia-guide` is the read-only orientation layer of DIA, invoked
explicitly by the user. It:

- Reads `BACKLOG.md`, the latest DIA commit trailers
  (`git log --format='%(trailers:key=DIA-Handoff,valueonly)'`), and
  git state
- Recommends the next phase skill in plain text
- Audits whether the last phase-end commit carries the binding
  trailers (`DIA-Phase`, `DIA-Handoff`, and `DIA-Triage` where triage
  happened)
- Runs the Closing Handoff after a green `/security-audit`
- Owns two narrow CRUD moments at workflow boundaries: (a) the
  **post-`/dia-realign` item promotion** (below), and (b) the
  **item-start branch creation** when the user enters at A/B/C from a
  fresh repo

What the guide does NOT do:

- It does not perform artifact triage. Triage lives in every phase
  skill's MANDATORY Phase 0 block (see
  `skills/project-conventions/references/graph-invariants.md`).
- It does not enforce the plan gate; `/coding` runs it, the guide
  only reads the result.
- It does not run consistency checks per phase. The pre-commit hook
  enforces the drift-critical invariants; the full check runs before
  release (security-audit Step 7 / Closing Handoff).
- It does not call other skills. It recommends; the user invokes.

## Item-start branch creation

When the user picks entry-point A, B, or C in the hybrid entry-point
detection (see "Start: Determine Phase" below), the guide creates a
fresh feature branch from the configured source branch before the
phase skill takes over. The phase skill itself does not own this
because the branch must exist before the first artifact is written.

Steps:

1. **Read `.dia/config.toml`.** Extract `source_branch` (default
   `develop`), `mode`, and `profile`. If the file is missing, fall
   back to `develop`, `git-only`, `full`.
2. **Slug input.** Ask the user (single `AskUserQuestion`, short
   plain-text "Other" slot) for a short kebab-case slug describing
   the item. The slug becomes the suffix of the feature branch name.
3. **Branch creation.**
   ```bash
   git fetch origin <source_branch> --quiet || true
   git checkout <source_branch>
   git pull --ff-only origin <source_branch> 2>/dev/null || true
   git checkout -b feature/<slug>
   ```
   If the branch already exists, switch to it and warn the user. Do
   not overwrite work.
4. **Mode-aware GitHub side-effect.** If `mode = "github-sync"` and an
   issue already tracks this item, remind the user to assign
   themselves so `flow.py sync-status` can mirror the assignee into
   the BACKLOG `Claim` column once the item has a real ID. The phase
   skill that first writes a backlog row calls `flow.py create-issue`.
5. **Hand-off.** Print the branch name, then recommend the phase
   skill: A -> `/business-analysis`, B ->
   `/requirements-engineering`, C -> `/architecture`.

Branch rename after RE: once the EPIC ID is known, the user can run
`python3 tools/github-integration/flow.py promote-to-epic --item
EPIC-NN --rename-branch` to retitle the parent issue, create
sub-issues, and rename the branch to `feature/epic-NN-<slug>`.

## Post-realign item promotion (the only CRUD moment)

`/dia-realign` finishes with a backlog seed: many items at
`Status: Backlog, Source: REV, Notes: anticipated` on a single
realign branch. Per-item branches and issues kick in only after a
user-driven triage, which the realign skill defers to the guide.

Steps:

1. Read `BACKLOG.md`, list items with `Status: Backlog, Source: REV`
   whose Notes column contains `anticipated`.
2. AskUserQuestion: which items should be promoted now?
3. For each promoted item:
   ```
   python3 ${DIA_PLUGIN_ROOT:-.}/tools/github-integration/flow.py create-issue --item <ID>
   git tag -a <id-lower>/realigned -m "Item promoted from /dia-realign"
   ```
   (Legacy `<id-lower>/reverse-engineered` tags from earlier runs
   stay valid.)
4. Update the BACKLOG row: `Status` -> `Ready` (or `In Progress` if
   the item already ships). Remove the `anticipated` note.
5. Recommend the next skill: typically `/business-analysis` to
   validate the BA draft, or `/coding` for items that already ship.

## Handoff state audit (read-only, on user invocation)

When the user invokes `/dia-guide` after a phase skill has finished,
the guide reads the team-workflow surface and reports drift between
artifact state and collaboration state. It does NOT write, fix, or
tag. Audited surfaces (full reference:
`skills/project-conventions/references/team-workflow.md`):

1. **Branch.** Current branch on an item-branch per schema? If not,
   warn.
2. **Phase tag.** Did the finished phase set `<item-id>/<phase>-done`?
   If missing, name the phase skill that should re-run its ritual.
3. **Backlog row.** Does the row's status reflect the phase progress?
   Discrepancies mean the ritual did not write the row before the
   commit.
4. **GitHub issue.** Read `flow.py status --item <ID>` and report the
   snapshot (labels, checklist).
5. **Commit trailers.** Does the last phase-end commit carry
   `DIA-Phase` and `DIA-Handoff` (plus `DIA-Triage` where triage
   happened)? Read via
   `git log -n 5 --format='%h %(trailers:key=DIA-Phase,valueonly) %(trailers:key=DIA-Handoff,valueonly)'`.
   Missing trailers are flagged with the responsible phase skill
   named.

## Feature-complete read (before release)

When the user asks "is this item ready for release?", the guide reads
the phase tags and reports. No tagging, no PR transition, no skill
invocation.

1. Verify required phase tags: `<id>/code-done` (always),
   `<id>/test-done` (always), `<id>/sec-done` (when the item touches
   security-relevant surface; legacy `<id>/audit-done` accepted).
2. Run `flow.py status --item <ID>` and show the result.
3. Report:
   ```
   Item '<ID>' phase status:
   - code-done: yes/no
   - test-done: yes/no
   - sec-done: yes/no/n-a

   Verdict: feature-complete | missing tags: <list>
   ```

If a tag is missing, name the responsible phase skill. If
feature-complete, the user can mark the PR ready
(`flow.py ready-for-review --item <ID>`) and run their private
release skill. The guide does neither.

---

## Workflow Overview

```
Phase 0 (brownfield only): /dia-realign        REVERSE WALK
 Input: existing codebase + documentation      (backwards up the V)
 Output: plan-context.md, ADRs (post-hoc), arc42 snapshot,
 FEATURE inventory, BA draft, backlog seed
 |
 v (forward walk starts here)
Phase 1: /business-analysis                    DESIGN
 Output: _devprocess/analysis/BA-{PROJECT}.md  (left side of the V)
 |
 v
Phase 2: /requirements-engineering
 Output: Epics, Features, architect-handoff.md
 |
 v
Phase 3: /architecture
 Output: ADRs, rules, navigation, plan-context.md
 |
 v
Phase 4: /coding                               IMPLEMENTATION
 Load context, critical review, TDD by default,
 verification gate, writeback
 |
 v
Phase 5: /testing                              VERIFICATION
 Unit + integration tests, fix-loop            (right side of the V)
 |
 v
Phase 6: /security-audit
 SAST, SCA, supply chain, fix-loop, pre-release check
 |
 v
Closing Handoff (not a phase)
 /consistency-check mode B verdict; user runs their private
 release skill; post-release review queued as a BACKLOG row
```

In the **lean profile** (`profile = "lean"` in `.dia/config.toml`)
only `/architecture` artifacts and backlog state are binding; the
guide recommends `/architecture` or `/coding` directly and skips
BA/RE recommendations unless the user asks for them.

## Phase Transitions (read-only audit)

Between phases, the guide reads project state and surfaces the next
step. Phase skills are autonomous and own their handoff ritual; the
guide observes:

1. Reads the latest DIA trailers
   (`git log --format='%(trailers:key=DIA-Handoff,valueonly)' -5`)
   and the BACKLOG rows they reference
2. Reports the recommended next step in plain text ("Recommended
   next: `/coding`")
3. The user invokes the next skill themselves

The guide does not loop, does not auto-advance, and does not block.
The trailer format is binding and lives in
`skills/project-conventions/references/canonical-specs.md` (Backlog
vocabulary, "Phase-end commit trailers"). A skill that finds a
`DIA-Triage` trailer for its item skips its Phase-0 triage question.

## Ensure project structure exists

Before a phase starts, check whether the directory structure exists.
If not, initialize per `/project-conventions`:

```bash
mkdir -p _devprocess/{analysis/sources,requirements/{epics,features,fixes,improvements,handoff},architecture,rules,implementation/plans,context}
mkdir -p src docs scripts memory
```

Seed `BACKLOG.md` from
`skills/requirements-engineering/templates/BACKLOG-TEMPLATE.md` (never
`touch` an empty file). Full profile: seed `_devprocess/rules/` from
the RULES templates. Lean profile: rules go into AGENTS.md instead
(see `/dia-setup`). Seed `src/ARCHITECTURE.map` from
`ARCHITECTURE-MAP-TEMPLATE.md` with empty rows.

## Start: Determine Phase

Before asking the user, the guide runs a hybrid entry-point
detection: scan the project, diagnose the graph state, formulate a
recommendation. The user keeps the override.

### Step 1: Scan + recommend

1. Detect the project root convention (`_devprocess/` or `docs/`).
2. Optionally run `python3 tools/consistency-check.py --check`
   (resolve against `$DIA_PLUGIN_ROOT`) for a Graph-Health snapshot.
3. Infer the likely entry point:

| Observation | Recommended entry |
| ------------------------------------------------------------- | ------------------------------------------ |
| No V-Model artifacts at all, empty repo or pure greenfield | `/business-analysis` (Project-BA) |
| Code exists, no `_devprocess/analysis/BA-*.md`, no FEATUREs | `/dia-realign` |
| Legacy DIA artifacts (old IDs, HANDOFFS.md, v1/v2 layout) | `/dia-realign` |
| `profile = "lean"` in `.dia/config.toml` | `/architecture` or `/coding` directly |
| Project-BA exists as Draft, not yet validated | `/business-analysis` Validation Mode |
| Project-BA validated, user wants a new epic / feature | `/business-analysis` (Item-BA) |
| Project-BA validated and Item-BA exists, no EPIC/FEAT yet | `/requirements-engineering` |
| Features exist, no ADRs or plan-context.md | `/architecture` |
| plan-context.md exists, no recent code changes | `/coding` |
| Coding done, no test coverage / failing tests | `/testing` |
| Tests green, no security audit | `/security-audit` |
| Everything closed, release pending | Closing Handoff (`/consistency-check` mode B + `/release` if configured) |
| Graph-Health shows many orphans or dead links | `/consistency-check` + cleanup first |

### Step 2: Present recommendation + alternatives

Show the user one `AskUserQuestion` with the recommendation as the
first option and the manual list as alternatives:

```
Graph-State (letzter Check {date}):
- Epics {n}, Features {n} (Released {a}, Building {b}, Planned {c}, Candidates {d}),
 ADRs {n}, FIX/IMPs {n}, offene Luecken {n}.

Empfehlung basierend auf dem Graph-State: {recommended entry}

Oder du waehlst manuell aus:
A0 /dia-realign (brownfield oder Legacy-Upgrade)
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
the user wants an interview, ask short follow-up questions.

### Step 3: Phase entry with consistency hint

Beim Start der gewaehlten Phase zeigt der Guide eventuelle
Konsistenz-Luecken aus dem Snapshot, die fuer die Phase relevant sind.
Beispiel: vor `/architecture` "Du hast 3 Features ohne Epic-Parent,
das sollten wir vorher klaeren."

## Recommended next step per phase

The guide prints the recommendation; the user types the slash
command. One line each; input paths are what the next skill loads.

| Phase complete | Recommend | Input for the next skill |
|---|---|---|
| /dia-realign | `/business-analysis` (always; the BA draft needs validation) | `_devprocess/analysis/BA-{PROJECT}.md` (Draft) |
| /business-analysis | `/requirements-engineering` | `BA-{PROJECT}.md` + Item-BA + last DIA trailers |
| /requirements-engineering | `/architecture` | `_devprocess/requirements/handoff/architect-handoff.md` |
| /architecture | `/coding` | `_devprocess/requirements/handoff/plan-context.md` |
| /coding | `/testing` | new code + updated FEATURE specs |
| /testing | `/security-audit` | codebase + coverage report |
| /security-audit | Closing Handoff | audit report verdict |

## Closing Handoff

A short guide output, not a phase. Fires after `/security-audit`
returns a non-red verdict and the fix-loop is closed.

1. **Suggest `/consistency-check` mode B** (user command; the skill is
   explicit-only). It confirms BA validation, final Feature/ADR
   states, arc42 and plan-context coherence, and returns
   Release-Ready: yes/no.
2. **On Release-Ready: yes**, print the closing report: features
   implemented/deferred/removed, bugs resolved/open, security P0/P1
   state, test coverage, artifacts finalized. Then: "If you have a
   private release skill configured, run it now. The cycle is
   complete; iterate from `/business-analysis` or
   `/requirements-engineering`."
3. **Queue the post-release review as a BACKLOG row** under
   `## Deferred / Ideas`: type `BL-Item`, note
   `post-release BA review, revisit {date + scope window: Simple
   Test 1-3d, PoC 7-14d, MVP 14-30d}`, refs to the hypotheses to
   re-validate. No separate handoff file.
4. **On Release-Ready: no**, name the responsible skill and the items
   to fix. Cycle closure resumes after the fix.

---

## Artifact Directory Structure

```
_devprocess/
  analysis/                         <- flat: BA-*, EXPLORE-*, AUDIT-*, RESEARCH-* (+ sources/)
  requirements/
    epics/EPIC-{nn}-{slug}.md
    features/FEAT-{ee}-{ff}-{slug}.md
    fixes/FIX-*.md  improvements/IMP-*.md
    handoff/architect-handoff.md  plan-context.md
  architecture/
    ADR-{nn}-{slug}.md  arc42.md
    decisions/README.md             <- router table (lean profile)
  rules/                            <- full profile; lean consolidates into AGENTS.md
  implementation/plans/PLAN-*.md
  context/
    BACKLOG.md                      <- single source of truth for state and graph
    BACKLOG-HISTORY.md              <- append-only session history
    METRICS.md                      <- signal layer
  SYSTEM-MAP.md                     <- navigation map (lean profile)

src/
  ARCHITECTURE.map                  <- wayfinder: concept -> entry-point -> ADR
  {module}/README.md                <- optional module wayfinder
```

## Traceability Chain

```
BA document (Why?)
 -> Epic -> Feature -> ASR -> ADR -> plan-context.md (ref index)
 -> Critical Review -> PLAN (tasks, TDD gates)
 -> Code (commits cite PLAN + DIA trailers)
 -> Tests -> fix-loop -> Security Audit -> fix-loop
 -> Backlog -> Closing Handoff (mode B + optional /release)
```

Backchannel: changes in every phase flow back into the source
artifacts. At the end, the documentation reflects the actual state.

## Conventions

This workflow follows `/project-conventions`: file names with 2-digit
counters and kebab-case, English skill text with user-language
dialog, artifacts under `_devprocess/`, lifecycle BACKLOG -> SPEC ->
PLAN -> IMPL -> UPDATE.

## V-Model as a decision graph, not a straight path

The overview shows phases linearly for readability. In practice the V
is a decision graph with three cross-phase feedback triggers:

1. **Mid-course bug discovery** (in `/coding`): pause, FIX triage,
   root cause, backlog entry, then the fix. Commit cites both items.
2. **Mid-course design discovery** (in `/coding`): pause, amend or
   supersede the ADR, update dependent artifacts, then continue.
3. **Mid-course requirements discovery** (in `/architecture` or
   `/coding`): route the gap back to the FEATURE spec, re-run the
   Plan Coverage Gate, then continue.

Each trigger: STOP, triage, minimal root-cause note, backlog entry
BEFORE any change, change with a citing commit, final sync. When a
phase returns to an earlier phase, downstream phases do NOT re-run
automatically; the user decides, the backlog entry carries the
decision.

## Dialog handoff (RE -> Architecture)

`architect-handoff.md` carries a `## Dialog` section as a
bidirectional channel between RE and architecture. Rules: not a
blocker (only the dependent item waits); try to self-answer from
artifacts first; surface ALL unresolved entries in ONE
AskUserQuestion per session; append-only, answered entries get
`Status: Resolved`. Questions from the coder to the architect do NOT
use a Dialog section (plan-context is a pure ref index); they go into
the BACKLOG row's Notes column or a PR comment.

## Concurrent-agent coordination

When multiple human-agent pairs work in parallel, the backlog is the
single synchronization point. The `Claim` column encodes ownership:
`{pair-id} @ {YYYY-MM-DD}`; empty means free.

**Claim protocol:**

1. **Claim on phase start**, BEFORE any other write.
2. **Release on phase end or Status: Done.**
3. **Claim conflict:** never overwrite. Surface via AskUserQuestion:
   ask the other pair to release, take over with acknowledgement,
   work on a different item, or split the row. Takeovers append a
   dated note to the Notes column.
4. **Stale claims** (older than the phase-expected duration, e.g. 14
   days) get flagged in the next audit.
5. **Claim history is append-additive**: current claim in the cell,
   previous claims as dated notes.

Pair-id convention: `{human-handle}-{model}` (e.g.
`sebastian-opus-4.7`). No central lock service: the backlog is the
lock, and a merge conflict on the Claim column IS the collision
surfacing at the right moment.

## Signal layer

Lightweight signals live in `_devprocess/context/METRICS.md` (seeded
from `templates/METRICS-TEMPLATE.md`): cycle time per FEATURE and
drift count (written by `/coding`), hypothesis validation
(`/business-analysis`), phase transition and trigger counts (the
firing skill). Append-additive, written inside existing phase
actions, no separate ceremony. Consumers read it to decide whether a
reconciliation run or post-release review is due.

## User Interaction Protocol

Binding for this guide and every phase skill:
`skills/project-conventions/references/user-interaction-protocol.md`
(one question per turn, AskUserQuestion, Pro/Con per option,
recommended option first).

## Keywords

V-Model, workflow, full cycle, new project, development cycle, from
analysis to implementation, full run, guide, phase transitions,
closing handoff, orientation
