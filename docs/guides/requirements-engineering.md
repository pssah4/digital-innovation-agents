---
title: Requirements Engineering
description: Turn a validated Business Analysis into Epics, Features, and tech-agnostic Success Criteria. The bridge between the Why and the How.
---

# Requirements Engineering

`/requirements-engineering` is the bridge between [Business Analysis](./business-analysis) (the Why) and [Architecture](./architecture) (the How). It transforms the validated business analysis into structured, measurable, tech-agnostic requirements that a human or AI architect can actually design against.

**Input:** `_devprocess/analysis/BA-{PROJECT}.md` (validated BA)
**Output:** Epics, Features, `architect-handoff.md`

## Why this phase exists

Most teams skip Requirements Engineering. The BA produces "what we want to build," someone writes a Notion page, and the next day engineers are picking a framework. Two failure modes follow from that shortcut.

Tech bleeds into the problem statement. "We need OAuth" gets written instead of "users must prove identity." Now the requirement is coupled to a technology before anyone has decided whether that technology fits.

Success becomes unmeasurable. Features ship with Definition-of-Done lines like "users love it" that no test, gate, or agent can ever verify. The result is a backlog full of items nobody can say are finished.

Requirements Engineering exists to catch both, systematically, before they contaminate the architecture.

## The translation chain

Every output of RE descends from something in the BA. The skill enforces traceability. If a user story has no BA source, the skill flags it and sends you back to `/business-analysis` rather than inventing new requirements on the fly.

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

The Epic is the strategic container. It is not a "big feature." It is a hypothesis about value, written as full prose. The skill rejects fill-in-the-blank templates because they reduce a strategic decision to a Mad Libs exercise.

```markdown
---
id: EPIC-01
title: AI agent core
created: 2026-04-30
---

# EPIC-01: AI agent core

## Hypothesis

For solo founders running a B2B SaaS support inbox, who currently
spend two to four hours each day triaging tickets that mostly say
"how do I reset my password?", the AI agent core is a context-aware
ticket triage layer that auto-resolves the top ten password and
billing scenarios so the founder gets back at least an hour a day.
Unlike Zendesk macros, which the founder has to author and maintain
by hand, the agent core learns from the founder's resolution
history without configuration.
```

The hypothesis is one paragraph of prose, not a six-line template.
The skill rejects formats like `For {x} who {y} the {z} is a ...`
because they hide thin reasoning behind structure. A real
hypothesis explains the user, the problem, the solution category,
the primary value, the current alternative, and the unfair
advantage in actual sentences.

**Epic ID format.** 2-digit counter with leading zeros (`EPIC-01`,
not `EPIC-001`). Filename: `EPIC-{nn}-{slug}.md` in
`_devprocess/requirements/epics/`. Status, phase, last-change live
in the **backlog row**, not in the frontmatter.

## Feature structure

Under each Epic, Features are the units that get implemented. A
Feature is what a team can ship in one coherent increment. Features
are **scoped to a single epic** and numbered locally. The format
is `FEAT-{ee}-{ff}-{slug}.md`, where `{ee}` is the parent epic
number and `{ff}` is the feature counter inside that epic. Example:
`EPIC-01` owns `FEAT-01-01`, `FEAT-01-02`, ...; `EPIC-13` owns
`FEAT-13-01`, ....

```markdown
---
id: FEAT-01-02
title: Auto-resolve password reset tickets
created: 2026-04-30
epic: EPIC-01
adr-refs: []
feature-refs: []
depends-on: [FEAT-01-01]
---

# FEAT-01-02: Auto-resolve password reset tickets

## Feature Description
{2-3 sentences: what the system will let a user do}

## Benefits Hypothesis
We believe this feature creates value because {insight from BA}.
We will know we were right if {measurable signal}.

## User Stories
- As a {persona} I want to {action} so that {outcome}
- ...

## Success Criteria (tech-agnostic)
- Measurable, tech-free, user-observable
- ...

## Technical NFRs
- Concrete numbers (latency, throughput, retention, uptime)
- ...

## ASRs (Architecturally Significant Requirements)
- Critical / Moderate / Low
- Each Critical ASR becomes an ADR in /architecture

## Definition of Done
- What must be true for the feature to ship
```

**Frontmatter rule.** Status, phase, last-change, claim, and
commit SHA do **not** live in the frontmatter. They live in the
**backlog row** for `FEAT-01-02`. The frontmatter carries identity
(`id`, `title`, `created`) and graph edges (`epic`, `adr-refs`,
`feature-refs`, `depends-on`) only. See the
[Three-layer documentation model](../concepts/three-layer-documentation).

**FIX and IMP scope.** Bug fixes are
`FIX-{ee}-{ff}-{nn}-{slug}.md` files (rows in `BACKLOG.md`, detail
files in `_devprocess/requirements/fixes/`), with each Fix scoped to
the parent feature. Improvements use the same scheme as
`IMP-{ee}-{ff}-{nn}` in `_devprocess/requirements/improvements/`.

### User stories across three levels of need

Human needs stack in three layers. The skill writes user stories on all three layers where the need exists, because a feature that serves only the functional layer is dramatically less sticky than one that serves the emotional and social layers too. The method that surfaces these three layers is the [Jobs to be done](../reference/methods-ideation#jobs-to-be-done) card.

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

Like the BA, this skill spots gaps in your input and suggests the method that will close them. You run the method, you come back with data, the skill continues. Common triggers and the matching cards:

- **Epic Hypothesis missing the current alternative.** [User journey](../reference/methods-discovery#user-journey) focused on the "before" phase, so you can see how the user solves the problem today without your product.
- **Feature has only functional user stories.** [Jobs to be done](../reference/methods-ideation#jobs-to-be-done) to surface the emotional and social layers so the stories stop feeling hollow.
- **Benefits Hypothesis has no Exploration source.** [Qualitative interview](../reference/methods-discovery#qualitative-interview) or [User motivation analysis](../reference/methods-discovery#user-motivation-analysis) to anchor the hypothesis in real evidence.
- **Technical NFR reads "fast" or "secure" without a number.** [Expert conversations](../reference/methods-discovery#expert-conversations) with the engineering or operations team to get a concrete target.
- **ASR is suspected but unverified.** [Expert review](../reference/methods-validation#expert-review) so you can confirm feasibility before writing the ADR.
- **Success Criterion cannot be made measurable.** [Test grid](../reference/methods-validation#test-grid) or [Value proposition quantification](../reference/methods-validation#value-proposition-quantification) for a baseline you can test against.
- **Critical Hypothesis from BA has no test plan.** Pick the cheapest falsifier: [Wireframes, storyboards, and paper prototypes](../reference/methods-validation#wireframes-storyboards-and-paper-prototypes), [Wizard of Oz](../reference/methods-validation#wizard-of-oz), or [Appearance prototype](../reference/methods-validation#appearance-prototype).
- **Risk blind spots before commit.** [Pre-mortem](../reference/methods-validation#pre-mortem) before the team locks resources.

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

The skill ends with the standard four-part [Handoff Ritual](../concepts/handoff-rituals): artifact report, handoff context appended to `HANDOFFS.md`, phase-end commit (`feat(re): {ITEM-ID} RE complete`) plus `tag-phase --phase re`, transition question. The guide runs `/consistency-check` Mode A on the changed artifacts at the boundary. The next phase is `/architecture`.

## Read the skill file

[`skills/requirements-engineering/SKILL.md`](https://github.com/pssah4/digital-innovation-agents/blob/main/skills/requirements-engineering/SKILL.md) on GitHub.

## Further reading

- [Tech-agnostic Requirements](../concepts/tech-agnostic-requirements). Full ruleset for keeping technology out of requirements.
- [Architecture](./architecture). The next phase, where ASRs become ADRs.
- [Discovery methods](../reference/methods-discovery), [Ideation methods](../reference/methods-ideation), [Validation methods](../reference/methods-validation). Method cards the agent references when you have gaps in the BA.
