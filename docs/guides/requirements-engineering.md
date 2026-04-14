---
title: Requirements Engineering
description: Turn a validated Business Analysis into Epics, Features, and tech-agnostic Success Criteria. The bridge between WHY and HOW.
---

# Requirements Engineering

`/requirements-engineering` is the bridge between
[Business Analysis](./business-analyse) (the WHY) and
[Architecture](./architecture) (the HOW). It transforms the validated
business analysis into structured, measurable, tech-agnostic
requirements that an architect — human or AI — can actually design
against.

**Input:** `_devprocess/analysis/BA-{PROJECT}.md` (validated BA)
**Output:** Epics, Features, `architect-handoff.md`

## Why this phase exists at all

Most teams skip Requirements Engineering. The BA produces "what we
want to build", someone writes a Notion page, and the next day
engineers are picking a framework. This produces two recurring
failure modes:

- **Tech bleed** — non-functional requirements leak into the problem
  statement ("we need OAuth" instead of "users must prove identity")
- **Unmeasurable success** — features ship with DoDs like "users
  love it" that no test or gate can ever verify

Requirements Engineering exists to catch both, systematically, before
they contaminate the architecture. It is the *discipline layer*
between wanting something and designing it.

::: info The three languages of the V
Each phase of the V-Model speaks a different language:

- **BA** speaks user language: *users, needs, pains, insights*
- **RE** speaks capability language: *the system shall let a user
  do X, measurably, without coupling to any specific technology*
- **Architecture** speaks structural language: *ADRs, modules,
  interfaces, constraints*

The job of this phase is to translate cleanly from one to the next
without leaking vocabulary in either direction. No user stories in
the ADRs. No ORMs in the Success Criteria.
:::

## The translation chain

Every output of Requirements Engineering descends from something in
the BA. The skill enforces **traceability** — every requirement has
a source you can point to.

```
BA element                    →  RE element
──────────────────────────────────────────────────────
HMW question                  →  Epic Hypothesis Statement
Insights                      →  Benefits Hypothesis (per Feature)
Functional needs              →  User Stories (functional)
Emotional needs               →  User Stories (emotional)
Social needs                  →  User Stories (social)
Jobs to be Done (each level)  →  User Story motivation
Critical Hypotheses (BA)      →  Feature Validation section
Idea Potential axes           →  Priority label (P0/P1/P2)
Value Proposition             →  Definition of Done context
```

If a user story has no BA source, the skill flags it. RE does not
create *new* requirements out of thin air — it structures what the
BA already surfaced. New requirements go back to `/business-analyse`.

## Epic — the strategic container

An Epic is the largest unit of work in Requirements Engineering. It
is **not** "a big feature". It is a **hypothesis about value**, in
the Scaled Agile / SAFe sense.

### The Epic Hypothesis Statement

The skill writes Epics in this canonical format:

```markdown
## Epic: {short name}

### Hypothesis
For {target user}
who {problem / need from the BA}
the {solution concept}
is a {category / product type}
that {key value}.
Unlike {current alternative}
our solution {unfair advantage}.
```

This format is direct from the Playbook's Explore → Create bridge.
It forces six things into the same sentence:

- The user (not "everyone")
- The problem (not "an opportunity")
- The solution category (so the team knows what kind of thing they
  are building)
- The primary value (one sentence)
- The current alternative (even if it is "manual spreadsheet work")
- The unfair advantage (the Wow from the BA)

### The BA → Epic walkthrough

Concretely, the skill transforms the BA as follows:

1. **HMW → solution concept.** The How Might We question becomes the
   seed of the "the *solution* is a *category*" clause.
2. **Primary persona → target user.** Copied verbatim, with the key
   descriptor from the BA persona section.
3. **Top-ranked insight → problem clause.** The insight that was
   most consequential during Exploration.
4. **Value proposition → value clause.**
5. **Current alternative** comes from the BA's Competitors section.
6. **Unfair advantage** comes from the Evaluate Assessment Radar
   and the Wow.

## Feature — the unit of work

Under each Epic, Features are the units that get implemented. A
Feature is what a team can ship in one coherent increment. Each
Feature has a fixed structure:

```markdown
## FEATURE-XXX: {short name}

### Feature Description
{2-3 sentences: what the system will let a user do}

### Benefits Hypothesis
{We believe this feature creates value because <insight from BA>.
 We will know we were right if <measurable signal>.}

### User Stories
- **As a** {persona} **I want to** {action} **so that** {outcome}
- ...

### Success Criteria (tech-agnostic)
- Measurable, tech-free, user-observable
- ...

### Technical NFRs
- Concrete numbers (latency, throughput, data retention, ...)
- ...

### ASRs (Architecturally Significant Requirements)
- Critical / Moderate / Low
- Each one becomes (or constrains) an ADR in /architecture

### Definition of Done
- What must be true for this feature to ship
```

### Excursion — User Stories with three levels of need

::: details Method: User Stories layered on Jobs to be Done
The Playbook draws a sharp distinction between three levels of user
need, which maps cleanly onto three complementary user stories for
the same capability:

- **Functional need** — what the user is trying to *do*
- **Emotional need** — how they want to *feel* while doing it
- **Social need** — how they want to be *seen* while doing it

**Example — a shared expense splitter for roommates:**

- *Functional:* "As a roommate I want to record a shared purchase
  so that the split math is automatic."
- *Emotional:* "As a roommate I want the split to feel fair without
  awkward conversations so that the shared flat stays calm."
- *Social:* "As a roommate I want other flatmates to see I always
  pay my share so that my reputation stays intact."

A feature that serves *all three* levels is dramatically more
valuable than a feature that only serves the functional one — and
far stickier in the market. The skill probes explicitly for all
three levels when it drafts user stories from BA needs.

*Method origin: Jobs-to-be-Done theory (Christensen, Ulwick) as
applied in the Digital Innovation Playbook's Needs pyramid.*
:::

### Excursion — Tech-agnostic Success Criteria

This is the single most-violated rule in industry requirements
documents, and it is the one the skill is most aggressive about
enforcing.

::: details Rule: Success Criteria must be free of technology terms
**Bad:**
- "User authenticates via OAuth 2.0"
- "Data is stored in PostgreSQL with a 24h retention"
- "REST endpoint returns 200 OK within 300ms"
- "React component loads in under 2s"

**Good:**
- "A user can prove identity without entering a password more than
  once per week on the same device"
- "Data a user deletes becomes irrecoverable within 24 hours of
  deletion"
- "A user receives a visible response within 300ms of interacting
  with any list screen"
- "The first list view becomes interactive within 2s on a
  mid-range phone on 3G"

**Why it matters:** Success Criteria are the contract between the
user and the team. If the contract references OAuth, you cannot
later swap it for a magic-link flow without renegotiating. If the
contract references React, you have prematurely locked the stack
in the wrong document.

Technical details live in the **Technical NFRs** section of the same
Feature, clearly separated, and in the ADRs that follow in
`/architecture`. See
[Tech-agnostic Requirements](../concepts/tech-agnostic-requirements)
for the full ruleset.
:::

### Excursion — ASRs: Architecturally Significant Requirements

::: details Concept: ASRs (Architecturally Significant Requirements)
An **ASR** is a requirement whose realisation shapes the architecture
— that is, a requirement you cannot satisfy by editing one module in
isolation. Typical ASRs:

- Performance targets (latency, throughput, percentile budgets)
- Security constraints (data classification, auth model)
- Compliance constraints (GDPR, HIPAA, SOC2)
- Availability and recovery targets (SLA, RPO, RTO)
- Scale targets (concurrent users, data volume)
- Integration constraints (must talk to system X, must not talk to Y)

**Classification:**

- **Critical ASR** — one-for-one maps to an ADR in `/architecture`.
  The architect cannot decide the component structure without knowing
  this requirement.
- **Moderate ASR** — influences an ADR but does not force one.
- **Low ASR** — captured for completeness, no ADR required.

The skill labels every ASR with this classification, and the
`/architecture` quality gate later checks that every Critical ASR
has a matching ADR. This is the single most important traceability
link in the entire V-Model.
:::

### Excursion — Benefits Hypothesis (not "description")

::: details Rule: Every Feature has a Benefits Hypothesis, not a justification
Teams love to write feature descriptions. The skill forces a stricter
form: a **Benefits Hypothesis**, structured like a Learning Card from
the Evaluate phase of the BA.

> **We believe** this feature creates value
> **because** {insight from BA}.
> **We will know we were right if** {measurable signal}.

This form matters because it:

- Forces the feature to trace back to an Exploration insight
- Forces a success signal that is testable, not aspirational
- Makes it obvious which features are *based on evidence* and which
  are still unvalidated bets

The second category is not forbidden — in fact, validated features
are rare early in a product's life — but the distinction is
explicit on every feature card.

*Source: Strategyzer Learning Card structure, as used in the
Digital Innovation Playbook's Evaluate module.*
:::

## Priority: mapping BA Idea Potential to P0/P1/P2

The BA scores Idea Potential on three axes: **User Value**,
**Transferability (Scalability)**, and **Feasibility**. Requirements
Engineering collapses those three scores into a single priority
label per feature:

| Priority | Criteria | Meaning |
|---|---|---|
| **P0** | High User Value + High Feasibility | Must ship in v1 |
| **P1** | Moderate across axes, or high value with risk | Should ship in v1 if time allows |
| **P2** | Low value or blocked feasibility | Backlog / follow-up |

The scoring is explicit and visible on every Feature card so the
architect knows immediately which Features are load-bearing for the
MVP and which are stretch goals.

## Quality gates

Each Feature must pass **all** of these before the skill lets the
Epic hand off:

- ✅ Feature Description present (not a placeholder)
- ✅ Benefits Hypothesis with an Exploration insight source
- ✅ At least one User Story per level where the need exists
  (functional minimum, emotional and social where relevant)
- ✅ Tech-free, measurable Success Criteria (the skill greps each
  criterion against a technology blocklist)
- ✅ Technical NFRs with concrete numbers (not "fast" — `< 300ms p95`)
- ✅ ASRs identified and classified (Critical / Moderate / Low)
- ✅ Definition of Done
- ✅ Priority label traced to BA Idea Potential

See [Verification Gates](../concepts/verification-gates) for the
full gate mechanic and how failures are handled.

## The architect handoff document

The final artifact is `architect-handoff.md`, a single document that
`/architecture` will consume. It contains:

1. The Epic Hypothesis Statement
2. Feature summary table with priorities
3. The **full list of Critical ASRs** — the architect's contract
4. The **full list of Technical NFRs** with numbers
5. Open questions for the architect (decisions RE cannot make)
6. Critical Hypotheses from the BA that are still unvalidated

The skill ends with the standard 3-part
[Handoff Ritual](../concepts/handoff-rituals) and proposes
`/architecture` as the next phase.

## Read the skill file

[`skills/requirements-engineering/SKILL.md`](https://github.com/pssah4/digital-innovation-agents/blob/main/skills/requirements-engineering/SKILL.md)
on GitHub.

## Further reading

- [Tech-agnostic Requirements](../concepts/tech-agnostic-requirements)
  — the full ruleset for keeping technology out of requirements
- [Architecture guide](./architecture) — the next phase, where ASRs
  become ADRs
- [Digital Innovation Playbook lineage](../concepts/digital-innovation-playbook)
  — the methodological heritage
