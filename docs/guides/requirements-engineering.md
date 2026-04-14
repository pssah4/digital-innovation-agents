---
title: Requirements Engineering
description: Turn a validated Business Analysis into Epics, Features, and tech-agnostic Success Criteria. The bridge between the Why and the How.
---

# Requirements Engineering

`/requirements-engineering` is the bridge between [Business Analysis](./business-analyse) (the Why) and [Architecture](./architecture) (the How). It transforms the validated business analysis into structured, measurable, tech-agnostic requirements that a human or AI architect can actually design against.

**Input:** `_devprocess/analysis/BA-{PROJECT}.md` (validated BA)
**Output:** Epics, Features, `architect-handoff.md`

## Why this phase exists

Most teams skip Requirements Engineering. The BA produces "what we want to build," someone writes a Notion page, and the next day engineers are picking a framework. Two failure modes follow from that shortcut.

Tech bleeds into the problem statement. "We need OAuth" gets written instead of "users must prove identity." Now the requirement is coupled to a technology before anyone has decided whether that technology fits.

Success becomes unmeasurable. Features ship with Definition-of-Done lines like "users love it" that no test, gate, or agent can ever verify. The result is a backlog full of items nobody can say are finished.

Requirements Engineering exists to catch both, systematically, before they contaminate the architecture.

## The translation chain

Every output of RE descends from something in the BA. The skill enforces traceability. If a user story has no BA source, the skill flags it and sends you back to `/business-analyse` rather than inventing new requirements on the fly.

```
BA element                    →  RE element
──────────────────────────────────────────────────────
HMW question                  →  Epic Hypothesis Statement
Insights                      →  Benefits Hypothesis per feature
Functional needs              →  User Stories (functional)
Emotional needs               →  User Stories (emotional)
Social needs                  →  User Stories (social)
Jobs to be Done per level     →  User Story motivation
Critical Hypotheses           →  Feature Validation section
Idea Potential axes           →  Priority label P0 / P1 / P2
Value Proposition             →  Definition of Done context
```

RE does not create new requirements out of thin air. It structures what the BA already surfaced.

## Epic Hypothesis Statement

The Epic is the strategic container. It is not a "big feature." It is a hypothesis about value, and the skill writes Epics in a canonical format:

```markdown
## Epic: {short name}

### Hypothesis
For {target user}
who {problem or need from the BA}
the {solution concept}
is a {category or product type}
that {key value}.
Unlike {current alternative}
our solution {unfair advantage}.
```

The format forces six things into one sentence:

- The user, not "everyone."
- The problem, not "an opportunity."
- The solution category, so the team knows what kind of thing they are building.
- The primary value, in one sentence.
- The current alternative the user has today, even if that is "a messy spreadsheet."
- The unfair advantage, the thing that makes this hard to copy.

## Feature structure

Under each Epic, Features are the units that get implemented. A Feature is what a team can ship in one coherent increment. Every Feature uses the same structure:

```markdown
## FEATURE-XXX: {short name}

### Feature Description
{2-3 sentences: what the system will let a user do}

### Benefits Hypothesis
We believe this feature creates value because {insight from BA}.
We will know we were right if {measurable signal}.

### User Stories
- As a {persona} I want to {action} so that {outcome}
- ...

### Success Criteria (tech-agnostic)
- Measurable, tech-free, user-observable
- ...

### Technical NFRs
- Concrete numbers (latency, throughput, retention, uptime)
- ...

### ASRs (Architecturally Significant Requirements)
- Critical / Moderate / Low
- Each Critical ASR becomes an ADR in /architecture

### Definition of Done
- What must be true for the feature to ship
```

### User stories across three levels of need

Human needs stack in three layers. The skill writes user stories on all three layers where the need exists, because a feature that serves only the functional layer is dramatically less sticky than one that serves the emotional and social layers too.

Functional is what the user is trying to do. Emotional is how they want to feel while doing it. Social is how they want to be seen while doing it.

For a shared-expense app inside a roommate household:

- Functional. "As a roommate I want to record a shared purchase so that the split math is automatic."
- Emotional. "As a roommate I want the split to feel fair without awkward conversations so that the shared flat stays calm."
- Social. "As a roommate I want other flatmates to see I always pay my share so that my reputation stays intact."

The third line is where retention comes from. The agent probes explicitly for the emotional and social layer when it drafts user stories from BA needs. If the BA did not capture those layers, the agent sends you back to the [Jobs to be Done](../reference/methods-ideation#jobs-to-be-done) method card to fill them.

### Tech-agnostic Success Criteria

This is the rule the skill is most aggressive about. Success Criteria must be free of technology vocabulary.

Bad:

- "User authenticates via OAuth 2.0."
- "Data is stored in PostgreSQL with 24h retention."
- "REST endpoint returns 200 OK within 300ms."
- "React component loads in under 2s."

Good:

- "A user can prove identity without entering a password more than once a week on the same device."
- "Data a user deletes becomes irrecoverable within 24 hours."
- "A user receives a visible response within 300ms of any list interaction."
- "The first list view becomes interactive within 2s on a mid-range phone on 3G."

Why the rule matters: Success Criteria are the contract between the user and the team. If the contract references OAuth, you cannot swap it for a magic-link flow without renegotiating. If the contract references React, you have locked the stack before the architect has seen the problem.

Technical details live in the Technical NFRs section of the same Feature, clearly separated, and in the ADRs that follow in `/architecture`. See [Tech-agnostic Requirements](../concepts/tech-agnostic-requirements) for the full ruleset.

### ASRs: Architecturally Significant Requirements

An ASR is a requirement whose realisation shapes the architecture. You cannot satisfy it by editing one module in isolation. Common examples:

- Performance targets (latency, throughput, percentile budgets)
- Security constraints (data classification, auth model)
- Compliance constraints (GDPR, HIPAA, SOC2)
- Availability and recovery targets (SLA, RPO, RTO)
- Scale targets (concurrent users, data volume)
- Integration constraints (must talk to system X, must not talk to Y)

The skill labels every ASR as Critical, Moderate, or Low. A Critical ASR maps one-to-one to an ADR in `/architecture`, and the architecture quality gate will refuse to hand off if any Critical ASR has no matching ADR. This is the single most important traceability link in the whole V-Model.

### Benefits Hypothesis, not "description"

Teams love to write feature descriptions. The skill forces a stricter form: a Benefits Hypothesis, shaped like the test cards from validation.

> We believe this feature creates value because {insight from BA}.
> We will know we were right if {measurable signal}.

The form does three things. It forces the feature to trace back to an Exploration insight. It forces a success signal that is testable. It makes it obvious which features are based on evidence and which are still unvalidated bets. The second category is not forbidden, but the distinction has to be explicit on the feature card.

## How the agent proposes methods in the dialog

Like the BA, this skill spots gaps in your input and suggests the method that will close them. If the BA did not capture emotional needs, the agent points you at the [Jobs to be Done](../reference/methods-ideation#jobs-to-be-done) card. If you cannot articulate the current alternative for the Epic Hypothesis, it suggests [User journey](../reference/methods-discovery#user-journey) work focused on the "before" phase. If a Critical ASR has no number attached, it sends you to [Expert conversations](../reference/methods-discovery#expert-conversations) with the engineering or operations team.

You run the method, you come back with data, the skill continues.

## Priority: from Idea Potential to P0 / P1 / P2

The BA scored Idea Potential on three axes: User Value, Transferability (Scalability), and Feasibility. Requirements Engineering collapses those three scores into a single priority label per feature.

| Priority | Criteria | Meaning |
|---|---|---|
| P0 | High User Value and High Feasibility | Must ship in v1 |
| P1 | Moderate across axes, or high value with risk | Should ship in v1 if time allows |
| P2 | Low value or blocked feasibility | Backlog or follow-up |

The label is visible on every Feature card so the architect knows immediately which features are load-bearing for the MVP.

## Quality gates

Each Feature has to pass all of these before the Epic hands off:

- Feature Description present and specific
- Benefits Hypothesis traced to an Exploration insight
- At least one User Story per level where the need exists
- Success Criteria are tech-free and measurable (the skill greps each criterion against a technology blocklist)
- Technical NFRs have concrete numbers, not adjectives
- ASRs identified and classified
- Definition of Done present
- Priority label traced to BA Idea Potential

See [Verification Gates](../concepts/verification-gates) for the full gate mechanic.

## The architect handoff

The final artifact is `architect-handoff.md`, a single document that `/architecture` will consume. It contains the Epic Hypothesis, the Feature summary table with priorities, the full list of Critical ASRs, the Technical NFRs with numbers, the open questions for the architect, and the Critical Hypotheses from the BA that are still unvalidated.

The skill ends with the standard three-part [Handoff Ritual](../concepts/handoff-rituals) and proposes `/architecture` as the next phase.

## Read the skill file

[`skills/requirements-engineering/SKILL.md`](https://github.com/pssah4/digital-innovation-agents/blob/main/skills/requirements-engineering/SKILL.md) on GitHub.

## Further reading

- [Tech-agnostic Requirements](../concepts/tech-agnostic-requirements). Full ruleset for keeping technology out of requirements.
- [Architecture](./architecture). The next phase, where ASRs become ADRs.
- [Discovery methods](../reference/methods-discovery), [Ideation methods](../reference/methods-ideation), [Validation methods](../reference/methods-validation). Method cards the agent references when you have gaps in the BA.
