---
title: A full V-Model run
description: End-to-end walkthrough of the V-Model workflow from raw idea to release closure, showing all phases and handoffs.
---

# A full V-Model run

This tutorial takes a rough idea through all 7 phases of the V-Model
workflow, from first conversation to final release closure. You see
every phase, every handoff, and every artifact. Think of it as the
reference trip. Once you have done this, you understand the whole system.

Timeframe to follow along: about 30-45 minutes of reading, plus another
1-2 hours if you actually run it for a PoC project.

## The setup

Start with a plain project directory and invoke the guide:

```
/dia-guide

I want to build X. Help me go through the full cycle.
```

The guide asks where you are in the V-Model. For a new project,
pick **A) Starting from scratch**. It launches `/business-analysis`.

## Phase 1: Business Analysis

See the [first Business Analysis tutorial](./first-business-analysis) for
the detailed walkthrough. For this overview, the key outputs are:

- `BA-{PROJECT}.md` (Business Analysis document)
- `EXPLORE-{PROJECT}.md` (Exploration Board for PoC/MVP)
- HMW question, personas, critical hypotheses

::: tip Methods the BA agent will propose
During this phase the agent stops the interview whenever a gap appears
and points you at the matching field method. Most common entry points:

- [Explorative interviews](../reference/methods-discovery#explorative-interviews)
  and [Qualitative interview](../reference/methods-discovery#qualitative-interview)
  when the user is still abstract.
- [Fly on the wall](../reference/methods-discovery#fly-on-the-wall)
  and [Self-test](../reference/methods-discovery#self-test) when
  interviews keep producing the ideal workflow instead of the real one.
- [Persona synthesis cluster](../reference/methods-discovery#persona-synthesis-cluster)
  and [Persona](../reference/methods-discovery#persona) to turn
  notes into a usable persona.
- [Brainstorming](../reference/methods-ideation#brainstorming),
  [Brainwriting](../reference/methods-ideation#brainwriting), or
  [Jobs to be done](../reference/methods-ideation#jobs-to-be-done)
  during Ideation.
- [Wireframes, storyboards, and paper prototypes](../reference/methods-validation#wireframes-storyboards-and-paper-prototypes)
  and [Pre-mortem](../reference/methods-validation#pre-mortem)
  during Validation.

Full catalog under [Discovery methods](../reference/methods-discovery),
[Ideation methods](../reference/methods-ideation), and
[Validation methods](../reference/methods-validation).
:::

At the end, the skill asks: "Start `/requirements-engineering` now?"
Say "yes". The guide passes the handoff context automatically.

## Phase 2: Requirements Engineering

`/requirements-engineering` reads the BA and produces:

- **Epics** (`EPIC-{nn}-{slug}.md`, 2-digit counter) with full-prose
  Hypothesis Statements derived from the HMW question
- **Features** (`FEAT-{ee}-{ff}-{slug}.md`, epic-local numbering
  with 2-digit epic and feature numbers) with tech-agnostic Success
  Criteria and Technical NFRs
- **Architect handoff** (`architect-handoff.md`) aggregating ASRs
  and NFRs

Key rule: Success Criteria must be technology-neutral. No "OAuth",
"REST", "PostgreSQL". Those go into Technical NFRs. See
[Tech-agnostic Requirements](../concepts/tech-agnostic-requirements).

::: tip Methods the RE agent will propose
If the BA input has gaps, the RE agent does not invent content. It
sends you back to the user with the matching method:

- [Jobs to be done](../reference/methods-ideation#jobs-to-be-done)
  when a feature has only functional user stories and the emotional
  and social layers are missing.
- [Expert conversations](../reference/methods-discovery#expert-conversations)
  when a Technical NFR reads "fast" or "secure" and needs an actual
  number before it can become an ASR.
- [Expert review](../reference/methods-validation#expert-review)
  when an ASR is suspected but unverified and a full test would be
  too expensive.
- [User journey](../reference/methods-discovery#user-journey) focused
  on the "before" phase when the Epic Hypothesis cannot name the
  current alternative.
- [Test grid](../reference/methods-validation#test-grid) and
  [Value proposition quantification](../reference/methods-validation#value-proposition-quantification)
  when a Benefits Hypothesis needs a measurable success signal.
:::

Handoff ritual ends with: "Start `/architecture` now?" -> yes.

## Phase 3: Architecture

`/architecture` transforms requirements into proposals:

- **ADRs** (`ADR-{nn}-{slug}.md`, 2-digit counter) in MADR format,
  one per Critical ASR. ADR core sections carry no code paths
  (the ADR abstraction rule).
- **arc42** documentation (scope-dependent section count)
- **plan-context.md** as the context bridge to implementation
- **Wayfinder layer** seeded: `src/ARCHITECTURE.map` rows for every
  new concept, JSDoc / docstring header proposals for entry points

Each ADR must have at least 2 alternatives with pros and cons plus a
justified recommendation. "We chose React because it's popular" is
not acceptable.

Handoff: "Start `/coding` now?" -> yes.

## Phase 4: Coding

This is the most involved phase. `/coding` has four phases:

### Phase 1: Triage and load context

Confirms the inbound item type (FEAT / IMP / FIX / ADR). Reads
`plan-context.md`, all ADRs, FEAT specs, `CLAUDE.md`,
`src/ARCHITECTURE.map`, the relevant module READMEs, and the rule
sets under `_devprocess/rules/`.

### Phase 2: Critical review

Reviews the design proposals against the real codebase. This is the
core differentiator that Digital Innovation Agents has carried since
v1. ADRs that conflict with existing patterns are flagged. Changes
are written back into the source artifacts (substance) and the
backlog rows (state) before implementation begins. The drift count
goes into `METRICS.md`.

### Phase 3: Plan persistence and implementation

- **Phase 3a**: Plan persisted as `PLAN-{nn}-{slug}.md` in
  `_devprocess/implementation/plans/`, with the Plan Coverage Gate
  (SC coverage, ADR alignment, codebase anchoring, verify commands)
- **Phase 3b**: Task-breakdown guidelines (bite-size tasks, no
  placeholders, every file path anchored in the wayfinder)
- **Phase 3c**: Optional TDD mode (activate with "enable TDD")
- **Phase 3d**: Debugging protocol if a bug appears (4-phase
  root-cause process, "architecture alarm" after 3+ failed fixes).
  Bugs land as `FIX-{ee}-{ff}-{nn}` rows in `BACKLOG.md` plus
  detail files in `_devprocess/requirements/fixes/`
- **Phase 3e**: Mid-course discoveries pause work and route back
  (design / requirements / capability)

### Phase 4: Completion and final sync

- **Phase 4a**: Verification gate. No completion claims without
  fresh evidence. "Tests pass" requires actual test command output
  with 0 failures.
- **Phase 4b**: Regression test cycle for bug fixes
  (red-green-red verify). The FIX detail file gets a
  `## Regression test` section.
- **Phase 4c**: Final synchronisation. State first (backlog rows),
  substance second (FEAT, ADR, PLAN, FIX detail files), then the
  wayfinder, `plan-context.md`, `arc42.md`, `MEMORY.md`, and
  `METRICS.md`.

Handoff: "Start `/testing` now?" -> yes.

## Phase 5: Testing

`/testing` has two modes depending on whether `/coding` ran in TDD mode:

- **With TDD**: focus on integration tests, unit-test gaps, coverage check
- **Without TDD**: takes over unit test creation (fallback mode)

Failing tests trigger a fix-loop with 4 user options (fix all, approve
one-by-one, adjust tests only, abort). The loop runs until all tests
are green or the user aborts.

Handoff: "Start `/security-audit` now?" -> yes.

## Phase 6: Security Audit

`/security-audit` runs 6 phases:

1. Reconnaissance (tech stack identification)
2. SAST (static code analysis, CWE-based)
3. OWASP Top 10 (A01-A10)
4. OWASP LLM Top 10 (LLM01-LLM10, if applicable)
5. SCA (software composition analysis, dependency vulnerabilities)
6. Zero Trust & Code Quality

Findings are prioritised (`H-N` / `M-N` / `L-N`) and a fix-loop
runs. Deferred findings land in the backlog with full traceability,
each carrying `Status: Deferred` and a written reason.

Handoff: "Start the Closing Handoff now?" -> yes.

## Closing Handoff

The cycle closes with the guide's three-step Closing Handoff:

1. **Suggest `/consistency-check` mode B** (semantic). Mode B
   confirms BA Validation is filled, all Feature/ADR statuses are
   final, arc42 reflects the actual decisions, and `plan-context.md`
   matches the real tech stack. State changes go through the
   backlog row first. Mode B returns a Release-Ready verdict.
2. **On Release-Ready: yes**: closing report (Feature / bug /
   security counts, finalised artifacts) plus the `release-to-ba`
   HANDOFFS template that queues the BA Post-Release Review for the
   next BA session.
3. **On Release-Ready: yes**: optional run of a project-specific
   release skill (version bump, merge, tag, publish). The public
   DIA plugin does not own a release mechanism, since release
   pipelines are project-specific. The cycle is complete with or
   without the release act.

## Artifact trail after a full run

```
src/
  ARCHITECTURE.map
  {module}/README.md
_devprocess/
  analysis/
    BA-{PROJECT}.md
    EPIC-01-ba.md
    EXPLORE-{PROJECT}.md
    AUDIT-{PROJECT}-2026-04-30.md       (flat, no analysis/security/)
  requirements/
    epics/EPIC-01-*.md
    features/FEAT-01-01-*.md, FEAT-01-02-*.md, FEAT-02-01-*.md, ...
    fixes/FIX-01-02-03-*.md
    improvements/IMP-01-02-01-*.md
    handoff/architect-handoff.md, plan-context.md
  architecture/
    ADR-01-*.md, ADR-02-*.md, ...
    arc42.md
  rules/
    technical.md
    domain.md
    design.md          (only if UI surface)
  implementation/plans/
    PLAN-04-*.md
  context/
    BACKLOG.md         (single source of truth for state)
    HANDOFFS.md        (full audit trail of phase transitions)
    METRICS.md         (signal layer: cycle time, drift, hypothesis status)
```

Plus the actual source code under `src/` and tests under `tests/`.

## Opting out mid-workflow

At any handoff, if you do not want the guide to proceed, just say
"stop" or "I want to check first" or ask an unrelated question. The
workflow pauses immediately. You can resume later by re-invoking
`/dia-guide`.

## What's next

- [V-Model workflow guide](../guides/dia-guide): details on the
  guide and phase transitions
- [The V-Model concept](../concepts/v-model): why this shape?
- [Living Documents pattern](../concepts/living-documents): how artifacts
  stay in sync with reality
