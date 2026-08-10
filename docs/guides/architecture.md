---
title: Architecture
description: Transform tech-agnostic requirements into Architecture Decision Records, the arc42 constraints doc, navigation artifacts, and the plan-context ref index.
---

# Architecture

`/architecture` transforms requirements into architecture proposals. The final decisions get made during `/coding` when the actual codebase state is known. This distinction matters because a greenfield ADR written against an abstract RE document is a hypothesis about how to build. A `/coding` decision is a commitment against real constraints.

**Input:** Epics, Features, ASRs, NFRs from [`/requirements-engineering`](./requirements-engineering) (full profile), or the running codebase (lean profile, post-hoc)
**Output:** ADRs, the arc42 constraints doc, `plan-context.md` as a ref index, navigation artifacts (`SYSTEM-MAP.md`, `decisions/README.md`)

## The role of Architecture in the V-Model

Architecture sits at the bottom of the left side of the V. It is the last phase before code and the first phase where technology is allowed to enter the vocabulary. Everything upstream ([BA](./business-analysis) and [RE](./requirements-engineering)) was tech-agnostic on purpose. Here, the lid comes off.

Three things happen in this phase.

Every Critical ASR from Requirements Engineering gets turned into a proposed Architecture Decision Record. The system structure gets documented in arc42 format at a depth matching the scope. A plan-context bridge gets written to hand off to `/coding`, as a compact AI-readable summary of the stack and the decisions an implementer needs to know.

The output is not a binding document. It is a proposal that `/coding` critically reviews against the real codebase before committing. This separation is deliberate. It avoids the classic waterfall failure mode where an architecture designed against imagined constraints discovers at implementation time that reality disagrees.

## ADRs and their kinds

Every ADR carries a `kind` field in its frontmatter, and the kind
determines how much MADR ceremony the record needs:

- **`post-hoc` (the normal case):** the decision is documented AFTER
  the implementation that embodies it. Sections: Context, Decision,
  Consequences, Sources (code paths allowed there). Short, like a
  commit-style decision record. Considered Options are omitted; the
  code already chose.
- **`choice`:** a real pre-code choice. Adds Decision Drivers;
  Considered Options are recommended.
- **`constraint` (the exception):** pre-decided (compliance, hard to
  reverse). Full MADR with a mandatory Considered Options table.

Every ADR additionally carries `reversal-cost`, `applies-to`, and
`read-when` router fields. The router fields feed the
`decisions/README.md` router table (from
`DECISIONS-README-TEMPLATE.md`), which tells agents WHEN a decision
file is relevant without reading it. The skill keeps the router
table in sync with the frontmatter.

A missing `kind` on a legacy ADR means `choice`; old ADRs are never
rewritten just to add the field.

### The full MADR structure (constraint kind)

```markdown
---
id: ADR-NN
title: {short title of the decision}
created: 2026-04-30
kind: constraint
reversal-cost: high
applies-to: {module or concern}
read-when: {trigger condition for reading this ADR}
adr-refs: [ADR-MM]
feature-refs: [FEAT-EE-FF]
---

# ADR-NN: {short title of the decision}

## Context
Triggering ASR: {link to ASR from RE}
{Why this decision is needed, what forces apply, what constraints bind it.}
No code paths, file names, line numbers, or method signatures here.

## Decision Drivers
- {Driver 1, e.g. p95 latency < 300ms}
- {Driver 2, e.g. team knows Python, not Go}
- {Driver 3, e.g. must run in existing AWS account}

## Considered Options
### Option A: {name}
- Pros: ...
- Cons: ...

### Option B: {name}
- Pros: ...
- Cons: ...

### Option C: {name}
- Pros: ...
- Cons: ...

## Decision
We propose {Option X}, because {justification linking back to drivers}.

## Consequences
- Positive: ...
- Negative: ...
- Risks: ...

## Implementation Notes (optional, may go stale)
{Concept names from src/ARCHITECTURE.map, hints for the agent that
will implement the decision. This appendix is the only place inside
an ADR where code-level hints are tolerated.}
```

**Status, phase, last-change.** ADR status (Proposed / Accepted /
Superseded by ADR-MM) lives in the **backlog row**, not in the ADR
frontmatter. The `BACKLOG.md` row for `ADR-NN` carries Status,
phase, last-change, and the commit SHA when it lands.

**ADR ID format.** 2-digit counter with leading zeros (`ADR-03`,
`ADR-12`, not `ADR-003`).

### Why ADRs beat architecture diagrams

Architecture diagrams rot the moment they are drawn. A box-and-line PNG showing "the system" in 2024 tells you nothing about why the lines are drawn that way. As the system changes, the diagram becomes a lie faster than anyone updates it.

ADRs rot differently. An ADR is a snapshot of a decision at a moment in time: the forces that existed, the alternatives that were considered, the reasoning that won. Even if the decision is later reversed, the original ADR stays in the repo with `Status: Superseded by ADR-NNN` so future readers can follow the thread.

This turns the architecture folder into institutional memory instead of a stale visualisation. When a new engineer asks "why Postgres and not MongoDB?", the answer is a file, not a Slack thread from two years ago.

The MADR format was chosen because it is:

- Markdown. Renders everywhere, greps easily, reviews cleanly in PRs.
- Structured. The sections force you to name the drivers and alternatives instead of hand-waving.
- Short. One decision per file. You can read an ADR in under five minutes.

Further reading: [adr.github.io](https://adr.github.io), [MADR template](https://adr.github.io/madr/).

### ADR abstraction rule

ADR core sections (Context, Decision Drivers, Considered Options,
Decision, Consequences) contain **no code paths, file names, line
numbers, or method signatures**. Code-level hints belong in the
optional `## Implementation Notes` appendix at the bottom, which is
allowed to go stale. The wayfinder is the canonical source for
current paths.

This is the structural fix for the second-most-common drift class:
ADRs that age at code speed because they list code. An ADR written
abstractly stays readable years after the decision; an ADR written
concretely is silently wrong after the next refactor. See the
[Three-layer documentation model](../concepts/three-layer-documentation).

### Wayfinder maintenance

`/architecture` opens the wayfinder layer for every concept the new
ADR introduces or renames:

- A new row in `src/ARCHITECTURE.map`:
  `concept | entry-point | adr | how-to-extend`. The entry-point may
  be `(planned)` until `/coding` lands the first implementation.
- The ADR's optional `## Implementation Notes` appendix references
  the concept by name, not by file path.

`/coding` then fills in the concrete entry-point when the
implementation lands and adds the JSDoc / docstring header that
links back to the ADR. The wayfinder is never out of date because
the agent that edits the code is the same agent that edits the
wayfinder, in the same edit pass.

### ADR consolidation duty

An exploding ADR count is itself a smell. Thirty thematic ADRs are
better than ninety per-decision ADRs. `/architecture` consolidates
when it sees:

- Multiple ADRs that share a concept and disagree on detail. Combine
  them into one ADR with explicit Considered Options.
- ADRs that have been Superseded twice. Replace the chain with one
  current ADR and archive the old ones with `Status: Superseded`.
- ADRs that exist only to document a library upgrade. Move the
  rationale to `_devprocess/rules/technical.md` and delete the ADR.

### Rule-set maintenance

Stable truths live in `_devprocess/rules/{technical,design,domain}.md`
with a hard cap of **500 lines total** across the three files.
`/architecture` updates the rule sets when:

- The technical stack changes (technical.md)
- The UI design system changes (design.md, only if UI surface)
- The domain glossary needs a new term (domain.md)

If you cross the cap, condense or move detail to an ADR. The cap
forces the rules to stay focused.

### No choice ADR without real alternatives

For `constraint` and `choice` ADRs the skill enforces a hard rule: real alternatives with pros and cons each. "We chose React because it's popular" is not a decision, it is a default. If you cannot name two alternatives you seriously considered, you did not make a decision at all, and the ADR gets sent back. `post-hoc` ADRs are exempt: they record a decision the code already made, and inventing alternatives after the fact would be fiction.

### ASR to ADR traceability

An ASR from [Requirements Engineering](./requirements-engineering) classified as **Critical** has to produce at least one ADR. This is the single most important traceability link in the whole V-Model, and the skill's quality gate will refuse to hand off if any Critical ASR is orphaned.

Why: a Critical ASR is, by definition, a requirement you cannot satisfy without shaping the system. If no ADR addresses it, one of two things is true. Either the requirement is not actually Critical, and it needs to go back to RE for reclassification. Or an ADR is missing and needs to be written. There is no third option where a Critical ASR floats free without a corresponding design decision.

The traceability goes both directions:

- **RE to Architecture:** every Critical ASR gets at least one ADR.
- **Architecture to RE:** every ADR's `Context` section cites the triggering ASR.

## arc42, split into constraints and reference

arc42 is a 12-section template from Gernot Starke and Peter Hruschka, widely used in the German-speaking software architecture community. It is not a process, it is a table of contents that lets teams document what they know and deliberately leave blank what they do not.

Since v4, the single arc42 document is split into two artifacts with different cadences:

- **`arc42.md` (CONSTRAINTS, pre-code, always).** Written from
  `arc42-CONSTRAINTS-TEMPLATE.md` before implementation: quality
  goals, constraints, quality scenarios, risks. Hard cap of 40
  lines, `scope: constraints` in frontmatter. This is the part of
  arc42 that shapes code that does not exist yet, so it must exist
  before `/coding` starts.
- **`arc42-REFERENCE.md` (post-code, optional, cap-exempt).**
  Written from `arc42-REFERENCE-TEMPLATE.md` only when an auditor
  or customer audience needs the formal 12-section document. It is
  allowed to lag behind the code; the wayfinder and the ADR catalog
  stay canonical for current structure. `/dia-realign` produces this
  document when it reverse-engineers an existing codebase.

The split fixes a drift problem: the pre-code sections of arc42 age
slowly (constraints rarely change), while the descriptive sections
age at code speed. Keeping them in one file meant the whole document
was always partially stale. Legacy single-file arc42 documents keep
their old scope caps and stay valid.

Further reading: [arc42.org](https://arc42.org), [arc42 template download](https://arc42.org/download).

## plan-context.md: a 20-line ref index

`plan-context.md` is the handoff artifact from `/architecture` to `/coding`. Since v4 it is a pure reference index with a hard cap of 20 lines: stack refs, ADR impact, quality refs, and a read-next pointer. It names WHERE decisions live and never restates them.

- Stack facts live in `_devprocess/rules/technical.md`, not in
  plan-context.
- Decisions live in the ADRs; plan-context lists which ADRs affect
  the item.
- Current code paths live in the wayfinder
  (`src/ARCHITECTURE.map`).

Earlier versions carried a prose summary and a `## Dialog` section
for coder questions. Both are gone: restated facts drifted from
their sources, and questions now travel via BACKLOG-row notes or PR
comments. The ADR floor is gated by scope: 1 ADR for Simple Test, 2
for PoC, 3 for MVP.

See also: [Living Documents](../concepts/living-documents).

## Navigation artifacts

Two templates support the navigation layer:

- **`SYSTEM-MAP.md`** (`SYSTEM-MAP-TEMPLATE.md`): a compact
  navigation file with fast paths into the code, read before any
  formal architecture document. Mandatory in the lean profile,
  recommended in full.
- **`decisions/README.md`** (`DECISIONS-README-TEMPLATE.md`): the
  router table over all ADRs with *Applies when* and *Read when*
  columns, generated from the ADRs' `applies-to`/`read-when`
  frontmatter.

In the lean profile (see [Three modes](../concepts/three-modes#mode-vs-profile)) these two artifacts replace the three rules files as the primary structure seed, and `/architecture` becomes the core skill of the workflow: it owns the rules in AGENTS.md, `SYSTEM-MAP.md`, and the post-hoc decision records behind `decisions/README.md`.

## Rejected Alternatives

One of the most valuable sections in plan-context.md is **Rejected Alternatives**. It captures the options `/architecture` considered and deliberately did not pick, with the reason for rejection.

Why: without it, `/coding` will re-propose the same alternatives the next time a similar decision comes up. The team then spends thirty minutes re-running the same argument, with a higher chance of flipping the decision for no new reason. Recording the rejection stops the thrash.

Example:

```markdown
### Rejected: GraphQL for the public API
Reason: The client workload is read-heavy with predictable shapes.
REST and JSON matches the team's existing skill set and fits behind
CloudFront caching. Re-evaluate if a mobile client appears with
materially different query patterns. (ADR-004)
```

## Quality gates

The skill checks all four of the following before handing off.

1. **ADR to ASR traceability.** Every Critical ASR from RE has a matching ADR. No orphans.
2. **Ref integrity.** Every Accepted ADR appears exactly once in `plan-context.md`, and every ref there resolves to an existing ADR.
3. **No choice ADR without real alternatives.** `constraint` and `choice` ADRs offer real alternatives with Pros and Cons, not single-option rationalisation.
4. **Router consistency.** The `decisions/README.md` rows match the ADRs' `applies-to`/`read-when` frontmatter.

Gate failures are never suppressed. The skill reopens the failing section instead of handing off with a silently-broken link. See [Verification Gates](../concepts/verification-gates) for the full mechanic.

## Handoff

`/architecture` ends with the standard three-part [Handoff Ritual](../concepts/handoff-rituals): artifact report, phase-end commit (`chore(arch): {ITEM-ID} ARCH complete` with the `DIA-Phase: arch-done` and `DIA-Handoff: {ITEM-ID} -> coding` trailers) plus `tag-phase --phase arch` and `sync-status --item {ITEM-ID}` (no-op outside `mode = "github-sync"`), transition question. Between phase boundaries the pre-commit hook enforces the graph invariants.

The commit body is particularly rich because it captures decisions the next phase must not re-litigate:

- Rejected alternatives worth remembering.
- Known architectural risks that `/coding` should watch for during implementation.
- Open items deferred to `/coding`, and ADR consolidation moves.

The next phase is [`/coding`](./coding), which will critically review plan-context.md and the wayfinder against the real codebase and either confirm the proposal, adjust it, or (in the rare case) push back to architecture with new evidence. When `/coding` discovers a capability the architecture never planned (a new library, a new infrastructure component), the **mid-course capability discovery** trigger pauses implementation and routes back here for an ADR before the code continues.

## Read the skill file

[`skills/architecture/SKILL.md`](https://github.com/pssah4/digital-innovation-agents/blob/main/skills/architecture/SKILL.md) on GitHub.

## Further reading

- [MADR template](https://adr.github.io/madr/). The ADR format.
- [arc42](https://arc42.org). The structural documentation template.
- [Living Documents concept](../concepts/living-documents). Why architecture artifacts are meant to evolve.
- [Coding guide](./coding). The next phase.
- [DIA Realign guide](./dia-realign). How this same structure is reached from an existing codebase.
