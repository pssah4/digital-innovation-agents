---
title: Three-layer documentation model
description: Why DIA splits documentation into wayfinder, rule sets, backlog, and detail artifacts. The structural fix for doc-vs-code drift.
---

# Three-layer documentation model

DIA v3 splits project documentation into three layers plus a fourth
group of detail artifacts. Each layer has a different update cadence,
a different owner, and a different audience. Mixing the layers is the
dominant source of doc-vs-code drift, so the boundaries are binding.

## The four locations

| Layer | Purpose | Lives in | Owner |
|---|---|---|---|
| Wayfinder | Concept-to-file lookup, navigational, grep-friendly | `src/ARCHITECTURE.map`, JSDoc headers in entry-point files, `src/{module}/README.md` | `/coding` (every code edit that creates or renames an entry-point updates this layer) |
| Rule sets | Stable truths: stack, conventions, design rules, domain glossary. Hard cap **500 lines total** | `_devprocess/rules/technical.md`, `_devprocess/rules/design.md` (only if UI), `_devprocess/rules/domain.md` | `/architecture`, `/coding` |
| Backlog | Single source of truth for status of every artifact, plus the relation graph (Epic -> Feature -> Plan -> Fix) | `_devprocess/context/BACKLOG.md` | Every status-changing skill writes the backlog row BEFORE touching the artifact body |
| Detail artifacts | Audit trail of the engineering process: BA, Epics, Features, Plans, Fixes, Improvements, ADRs | `_devprocess/analysis/`, `_devprocess/requirements/{epics,features,fixes,improvements,handoff}/`, `_devprocess/architecture/`, `_devprocess/implementation/plans/` | `/business-analysis`, `/requirements-engineering`, `/architecture`, `/coding` |

## The structural fix for drift

The most common drift class in project documentation is **status
fields stuck at "Planned" while the code shipped**. It happens
because state lives in two places: the ADR frontmatter says
`Status: Proposed`, the FEATURE spec says `Status: Planned`, and
nobody updates them when the code lands.

DIA v3 says: **state lives in one place only, the backlog row**.
Status, phase, last-change, and claim of every artifact live in the
`BACKLOG.md` row. Artifact frontmatter carries identity (`id`,
`title`, `created`) and relations (`epic`, `adr-refs`,
`feature-refs`) only. A status change touches the backlog row first,
then the artifact body. The body changes only if the substance of
the artifact changes (problem, decision, success criteria,
reasoning).

That single rule eliminates the most expensive drift class. It also
makes the backlog the only file you need to read to know where every
item stands.

## Why the wayfinder

The other expensive drift class is **stale code paths in detail
artifacts**. An ADR written in Phase 3 lists "the embedding provider
is configured in `src/embed/provider.ts:42`". Two refactors later,
the file is `src/services/embedding/index.ts` and the line is `87`.
The ADR is silently wrong. A new agent reading it walks the wrong
path.

DIA v3 says: **detail artifacts do not list current code paths in
core sections**. Code-level hints belong in optional, explicitly
stale-tolerant appendices (`## Implementation Notes` for ADRs,
`## Code Pointer` for FEATUREs). The canonical answer to "where does
X live?" is the wayfinder:

- `src/ARCHITECTURE.map` is a one-line-per-concept table:
  `concept | entry-point | adr | how-to-extend`
- The entry-point file carries a JSDoc / docstring header with
  one-line purpose, the ADRs it implements, and the feature it serves
- Module READMEs at `src/{module}/README.md` describe what the module
  owns

The wayfinder updates with every code edit that creates or renames an
entry-point. It is never out of date because the agent that edited
the code is the same agent that updates the wayfinder, in the same
edit pass.

## Why the rule sets

The third expensive drift class is **conventions stuck in CLAUDE.md
or in a long ADR**. The rule sets isolate stable truths in a small
number of files (`technical.md`, `design.md`, `domain.md`) with a
hard cap of 500 lines total. If you cross the cap, condense or move
detail to an ADR.

The cap forces discipline. A 2000-line rules file is unread; a
400-line set of three focused files is loaded into the agent's
context every session.

## ADR abstraction rule

ADR core sections (Context, Decision Drivers, Considered Options,
Decision, Consequences) contain **no code paths, file names, line
numbers, or method signatures**. Code-level hints belong in the
optional `## Implementation Notes` appendix at the bottom, which is
allowed to go stale. The wayfinder is the canonical source for
current paths.

This is the same rule applied to ADRs specifically. ADRs age slower
than code; when they list code, they age at code speed. Keeping ADRs
abstract keeps them readable years after the decision.

## ADR / FEATURE / PLAN separation

The three artifact types answer three different questions:

- **ADR** answers "what is the architectural decision and why?". No
  tasks, no code paths in core sections.
- **FEATURE** answers "what should the user be able to do?". No
  tasks, no implementation details.
- **PLAN** answers "how is it concretely implemented?". Tasks with
  file paths and verify commands live HERE and only here.

Plans are explicitly the place for concrete code paths and verify
commands. Plans are short-lived (Draft / Active / Done) and
acceptable to be detailed. ADRs and FEATUREs are long-lived and must
stay abstract.

## What this looks like in practice

A request like "let's reindex the vault when notes change" produces:

| Artifact | What it contains |
|---|---|
| `BACKLOG.md` row `FEAT-01-02` | Status (Active), phase (code), claim, refs to ADR-07 and PLAN-04, commit SHA when done |
| `_devprocess/requirements/features/FEAT-01-02-reindex-on-change.md` | Problem, success criteria, hypothesis, scope. No tasks, no code paths |
| `_devprocess/architecture/ADR-07-reindex-trigger.md` | Decision drivers, considered options (cron / file watcher / queue), decision (file watcher), consequences. No file paths in core sections |
| `_devprocess/implementation/plans/PLAN-04-reindex-mvp.md` | Task list with `src/index/watcher.ts` paths, verify commands, plan coverage gate |
| `src/ARCHITECTURE.map` | One row: `reindex-trigger \| src/index/watcher.ts:export class \| ADR-07 \| Add a new TriggerSource in src/index/triggers/` |
| `src/index/watcher.ts` | JSDoc header pointing to ADR-07 and FEAT-01-02 |

A new agent reading this can:

1. Open `BACKLOG.md` to see what is in flight (`FEAT-01-02 Active code`)
2. Open `ARCHITECTURE.map` to see where reindex lives
3. Open `ADR-07` to see why it is a file watcher
4. Open `PLAN-04` to see the concrete task list

Each layer answers exactly one question.

## See also

- [Conventions](../reference/conventions): the binding rules
- [Artifacts](../reference/artifacts): full directory tree and file
  catalog
- [Living Documents](./living-documents): the writeback pattern that
  keeps the layers in sync
- [Project Conventions guide](../guides/project-conventions): the
  skill that owns the model
