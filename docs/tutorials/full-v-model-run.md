---
title: A full V-Model run
description: End-to-end walkthrough of the V-Model workflow from raw idea to release closure, showing all phases and handoffs.
---

# A full V-Model run

This tutorial takes a rough idea through **all 7 phases** of the V-Model
workflow, from first conversation to final release closure. You'll see
every phase, every handoff, and every artifact. Think of it as the
reference trip -- once you've done this, you understand the whole system.

Timeframe to follow along: about 30-45 minutes of reading, plus another
1-2 hours if you actually run it for a PoC project.

## The setup

Start with a plain project directory and invoke the orchestrator:

```
/v-model-workflow

I want to build X. Help me go through the full cycle.
```

The orchestrator asks where you are in the V-Model. For a new project,
pick **A) Starting from scratch**. It launches `/business-analyse`.

## Phase 1: Business Analysis

See the [first Business Analysis tutorial](./first-business-analysis) for
the detailed walkthrough. For this overview, the key outputs are:

- `BA-{PROJECT}.md` (Business Analysis document)
- `EXPLORE-{PROJECT}.md` (Exploration Board for PoC/MVP)
- HMW question, personas, critical hypotheses

At the end, the skill asks: **"Start `/requirements-engineering` now?"**
Say "yes". The orchestrator passes the handoff context automatically.

## Phase 2: Requirements Engineering

`/requirements-engineering` reads the BA and produces:

- **Epics** (`EPIC-{XXX}-{slug}.md`) with Hypothesis Statements derived
  from the HMW question
- **Features** (`FEATURE-{XXX}-{slug}.md`) with tech-agnostic Success
  Criteria and Technical NFRs
- **Architect handoff** (`architect-handoff.md`) aggregating ASRs and NFRs

Key rule: Success Criteria must be **technology-neutral**. No "OAuth",
"REST", "PostgreSQL" -- those go into Technical NFRs. See [Tech-agnostic
Requirements](../concepts/tech-agnostic-requirements).

Handoff ritual ends with: **"Start `/architecture` now?"** -> yes.

## Phase 3: Architecture

`/architecture` transforms requirements into proposals:

- **ADRs** (`ADR-{XXX}-{slug}.md`) in MADR format, one per Critical ASR
- **arc42** documentation (scope-dependent section count)
- **plan-context.md** as the context bridge to implementation

Each ADR must have **at least 2 alternatives with pros/cons** plus a
justified recommendation. "We chose React because it's popular" is not
acceptable.

Handoff: **"Start `/coding` now?"** -> yes.

## Phase 4: Coding

This is the most involved phase. `/coding` has four steps:

### Step 1: Load context

Reads `plan-context.md`, all ADRs, Features, `CLAUDE.md`, and optionally
the backlog, bug log, and last handoff entry.

### Step 2: Critical review

**Reviews the design proposals against the real codebase.** This is the
v1 differentiator that Digital Innovation Agents never lost. ADRs that
conflict with existing patterns are flagged. Changes are written back
into the source artifacts **before** implementation begins.

### Step 3: Implementation (delegated to Default agent)

Hands off to the Default Claude Code agent with a precise briefing:

- **Phase 3a:** Task-breakdown guidelines (bite-size tasks, no placeholders)
- **Phase 3b:** Optional TDD mode (activate with "enable TDD")
- **Phase 3c:** Debugging protocol if a bug appears (4-phase root-cause
  process, "architecture alarm" after 3+ failed fixes)

### Step 4: Completion and final sync

- **Phase 4a:** Verification gate -- no completion claims without fresh
  evidence. "Tests pass" requires actual test command output with 0 failures.
- **Phase 4b:** Regression test cycle for bug fixes (Red-Green-Red verify)
- Final synchronization: Feature specs, ADRs, backlog, and bug log updated

Bugs found during implementation land in `_devprocess/context/20_bugs.md`
with FIX-NN IDs, causal chains, and priority.

Handoff: **"Start `/testing` now?"** -> yes.

## Phase 5: Testing

`/testing` has two modes depending on whether `/coding` ran in TDD mode:

- **With TDD:** Focus on integration tests, unit-test gaps, coverage check
- **Without TDD:** Takes over unit test creation (fallback mode)

Failing tests trigger a **fix-loop** with 4 user options (fix all / approve
one-by-one / adjust tests only / abort). The loop runs until all tests
are green or the user aborts.

Handoff: **"Start `/security-audit` now?"** -> yes.

## Phase 6: Security Audit

`/security-audit` runs 6 phases:

1. Reconnaissance (tech stack identification)
2. SAST (static code analysis, CWE-based)
3. OWASP Top 10 (A01-A10)
4. OWASP LLM Top 10 (LLM01-LLM10, if applicable)
5. SCA (software composition analysis, dependency vulnerabilities)
6. Zero Trust & Code Quality

Findings are prioritized (Critical/High/Medium/Low) and a fix-loop
identical to the testing fix-loop runs. Deferred findings land in the
backlog with full traceability.

Handoff: **"Start Phase 7 Release Closure now?"** -> yes.

## Phase 7: Release Closure

The final phase. `/v-model-workflow` runs 5 steps:

1. **Final artifact synchronization** (cross-phase): BA, Features, ADRs,
   arc42, plan-context all reflect the actual implemented state
2. **Release notes generation**: implemented features, fixed bugs from
   `20_bugs.md`, security findings, breaking changes
3. **CHANGELOG update**: `[Unreleased]` -> `[{version}] - {date}`, semver bump
4. **Backlog cleanup**: open items referenced, future ideas captured
5. **Closing report** to the user with a full summary

## Artifact trail after a full run

```
_devprocess/
  analysis/
    BA-{PROJECT}.md
    EXPLORE-{PROJECT}.md
    security/AUDIT-{PROJECT}-{DATE}.md
  requirements/
    epics/EPIC-001-*.md
    features/FEATURE-001-*.md, FEATURE-002-*.md, ...
    handoff/architect-handoff.md, plan-context.md
  architecture/
    ADR-001-*.md, ADR-002-*.md, ...
    arc42.md
  context/
    10_backlog.md
    20_bugs.md
    30_handoffs.md   (full audit trail of phase transitions)
```

Plus the actual source code under `src/` and tests under `tests/`.

## Opting out mid-workflow

At any handoff, if you don't want the orchestrator to proceed, just say
"stop" or "I want to check first" or ask an unrelated question. The
workflow pauses immediately. You can resume later by re-invoking
`/v-model-workflow`.

## What's next

- [V-Model workflow guide](../guides/v-model-workflow) -- details on the
  orchestrator and phase transitions
- [The V-Model concept](../concepts/v-model) -- why this shape?
- [Living Documents pattern](../concepts/living-documents) -- how artifacts
  stay in sync with reality
