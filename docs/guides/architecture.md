---
title: Architecture
description: Transform tech-agnostic requirements into Architecture Decision Records, arc42 documentation, and the plan-context bridge to implementation.
---

# Architecture

`/architecture` transforms requirements into architecture proposals. The final decisions get made during `/coding` when the actual codebase state is known. This distinction matters because a greenfield ADR written against an abstract RE document is a hypothesis about how to build. A `/coding` decision is a commitment against real constraints.

**Input:** Epics, Features, ASRs, NFRs from [`/requirements-engineering`](./requirements-engineering)
**Output:** ADRs, arc42, `plan-context.md`

## The role of Architecture in the V-Model

Architecture sits at the bottom of the left side of the V. It is the last phase before code and the first phase where technology is allowed to enter the vocabulary. Everything upstream ([BA](./business-analyse) and [RE](./requirements-engineering)) was tech-agnostic on purpose. Here, the lid comes off.

Three things happen in this phase.

Every Critical ASR from Requirements Engineering gets turned into a proposed Architecture Decision Record. The system structure gets documented in arc42 format at a depth matching the scope. A plan-context bridge gets written to hand off to `/coding`, as a compact AI-readable summary of the stack and the decisions an implementer needs to know.

The output is not a binding document. It is a proposal that `/coding` critically reviews against the real codebase before committing. This separation is deliberate. It avoids the classic waterfall failure mode where an architecture designed against imagined constraints discovers at implementation time that reality disagrees.

## ADRs in MADR format

The skill uses the MADR (Markdown Architecture Decision Records) format. Every Critical ASR from RE produces exactly one ADR.

### The MADR structure

```markdown
# ADR-NNN: {short title of the decision}

## Status
Proposed | Accepted | Superseded by ADR-MMM | Inferred from codebase

## Context
Triggering ASR: {link to ASR from RE}
{Why this decision is needed, what forces apply, what constraints bind it.}

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
```

### Why ADRs beat architecture diagrams

Architecture diagrams rot the moment they are drawn. A box-and-line PNG showing "the system" in 2024 tells you nothing about why the lines are drawn that way. As the system changes, the diagram becomes a lie faster than anyone updates it.

ADRs rot differently. An ADR is a snapshot of a decision at a moment in time: the forces that existed, the alternatives that were considered, the reasoning that won. Even if the decision is later reversed, the original ADR stays in the repo with `Status: Superseded by ADR-NNN` so future readers can follow the thread.

This turns the architecture folder into institutional memory instead of a stale visualisation. When a new engineer asks "why Postgres and not MongoDB?", the answer is a file, not a Slack thread from two years ago.

The MADR format was chosen because it is:

- Markdown. Renders everywhere, greps easily, reviews cleanly in PRs.
- Structured. The sections force you to name the drivers and alternatives instead of hand-waving.
- Short. One decision per file. You can read an ADR in under five minutes.

Further reading: [adr.github.io](https://adr.github.io), [MADR template](https://adr.github.io/madr/).

### No ADR without real alternatives

The skill enforces a hard rule on every ADR: at least two considered options with pros and cons each. "We chose React because it's popular" is not a decision, it is a default. If you cannot name two alternatives you seriously considered, you did not make a decision at all, and the ADR gets sent back.

### ASR to ADR traceability

An ASR from [Requirements Engineering](./requirements-engineering) classified as **Critical** has to produce at least one ADR. This is the single most important traceability link in the whole V-Model, and the skill's quality gate will refuse to hand off if any Critical ASR is orphaned.

Why: a Critical ASR is, by definition, a requirement you cannot satisfy without shaping the system. If no ADR addresses it, one of two things is true. Either the requirement is not actually Critical, and it needs to go back to RE for reclassification. Or an ADR is missing and needs to be written. There is no third option where a Critical ASR floats free without a corresponding design decision.

The traceability goes both directions:

- **RE to Architecture:** every Critical ASR gets at least one ADR.
- **Architecture to RE:** every ADR's `Context` section cites the triggering ASR.

## arc42 snapshot

The skill produces an arc42-formatted architecture document, tailored to the project scope. arc42 is a 12-section template from Gernot Starke and Peter Hruschka, widely used in the German-speaking software architecture community. It is not a process, it is a table of contents that lets teams document what they know and deliberately leave blank what they do not.

### The 12 arc42 sections

| # | Section | Purpose |
|---|---|---|
| §1 | Introduction and Goals | Why does this system exist? Primary quality goals. |
| §2 | Architecture Constraints | Technical, organisational, political, legal constraints. |
| §3 | System Scope and Context | Black-box view: users, neighbouring systems, interfaces. |
| §4 | Solution Strategy | The high-level approach. Usually a set of ADR references. |
| §5 | Building Block View | White-box decomposition into components and modules. |
| §6 | Runtime View | Sequence and collaboration views for important scenarios. |
| §7 | Deployment View | Where does this run? Environments, infrastructure. |
| §8 | Crosscutting Concepts | Auth, logging, error handling, i18n. Things that touch every module. |
| §9 | Architecture Decisions | Back-references to all ADRs. |
| §10 | Quality Requirements | The quality tree and scenarios. |
| §11 | Risks and Technical Debt | Known pain that will hurt us later. |
| §12 | Glossary | Project-specific terms. |

### Scope-dependent depth

arc42 lets you leave sections empty when you have nothing to say. The skill matches the depth to the scope.

| Scope | arc42 sections filled |
|---|---|
| Simple Test | §1, §3, §4 |
| Proof of Concept | §1 to §5 and §8 |
| MVP | §1 to §12 (full template) |

A Simple Test scope project does not need a Risks section. An MVP absolutely does. Over-producing arc42 on a small project is a common waste. The skill is aggressive about preventing it.

### Why arc42 instead of a single Architecture.md

Teams usually reach for a single `ARCHITECTURE.md` file, which turns into a 5,000-word wall of prose nobody reads. arc42 is different in three ways.

It is a checklist, not a narrative. You know when you are done: all 12 sections have either content or an explicit "N/A."

It separates views. The Building Block View (static structure) is in §5. The Runtime View (dynamic collaboration) is in §6. A reader looking for one of them does not have to wade through the other.

It is standard. Two teams using arc42 can swap documents and find what they need immediately. A custom structure makes every handoff cost context-switching tax.

The skill writes arc42 in the same repository as the code, under `_devprocess/architecture/arc42.md`, so the architecture stays version-controlled alongside the implementation it describes.

Further reading: [arc42.org](https://arc42.org), [arc42 template download](https://arc42.org/download).

## plan-context.md

`plan-context.md` is the handoff artifact from `/architecture` to `/coding`. It is not a summary of arc42. It is the minimum AI-readable context a `/coding` agent needs to make correct implementation decisions on day one.

### What plan-context.md contains

| Section | What it holds |
|---|---|
| Technical Stack | Runtime, language, framework, DB, auth, testing, CI, with versions |
| Architecture Style | Monolith, modulith, microservices, serverless, hybrid |
| ADR summary table | ID, title, status, one-line decision |
| Data Model | Entities, relationships, key constraints |
| External Integrations | APIs, queues, third-party services |
| Performance and Security | Concrete numbers from NFRs |
| Conventions | Naming, error handling, logging, testing style |
| Existing Patterns | How the codebase currently does X (if not greenfield) |
| Rejected Alternatives | What `/coding` should NOT reopen without new reasons |

### Why a separate plan-context.md

arc42 is a human document. It has prose, diagrams, and sections that only make sense if you read them in order. An AI coding agent reading arc42 as its only context has to extract structured facts from sections written for a human audience, which is expensive and error-prone.

plan-context.md is the machine counterpart. It holds the same information as arc42, compressed into structured, scannable form: tables, lists, explicit name-value pairs. A `/coding` agent can parse it in one pass and know immediately which language and framework to write in, which libraries are already blessed, which patterns the existing code follows, which alternatives were rejected, and which numbers it must hit for latency, security, and data model.

This dual representation (arc42 for humans, plan-context.md for agents) is a deliberate structural choice. It is why `/architecture` ends with two artifacts instead of one.

See also: [Living Documents](../concepts/living-documents).

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

The skill checks all three of the following before handing off.

1. **ADR to ASR traceability.** Every Critical ASR from RE has a matching ADR. No orphans.
2. **plan-context.md consistency.** The tech stack in plan-context matches the Decisions in the ADRs. If ADR-002 says "Postgres" and plan-context says "MongoDB," the gate fails.
3. **No ADR without real alternatives.** Every ADR has at least two Considered Options with Pros and Cons. "We chose React because it's popular" is rejected.

Gate failures are never suppressed. The skill reopens the failing section instead of handing off with a silently-broken link. See [Verification Gates](../concepts/verification-gates) for the full mechanic.

## Handoff

`/architecture` ends with the standard three-part [Handoff Ritual](../concepts/handoff-rituals). The handoff context entry in `_devprocess/context/30_handoffs.md` is particularly rich because it captures decisions the next phase must not re-litigate:

- Tech-stack justification, which helps `/coding` understand why without re-reading all ADRs.
- Rejected alternatives with reasons.
- Known risks that `/coding` should watch for during implementation.

The next phase is [`/coding`](./coding), which will critically review plan-context.md against the real codebase and either confirm the proposal, adjust it, or (in the rare case) push back to architecture with new evidence.

## Read the skill file

[`skills/architecture/SKILL.md`](https://github.com/pssah4/digital-innovation-agents/blob/main/skills/architecture/SKILL.md) on GitHub.

## Further reading

- [MADR template](https://adr.github.io/madr/). The ADR format.
- [arc42](https://arc42.org). The structural documentation template.
- [Living Documents concept](../concepts/living-documents). Why architecture artifacts are meant to evolve.
- [Coding guide](./coding). The next phase.
- [Reverse Engineering guide](./reverse-engineering). How this same structure is reached from an existing codebase.
