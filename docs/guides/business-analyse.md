---
title: Business Analysis
description: The Exploration / Ideation / Validation cycle. Understand the problem before designing the solution.
---

# Business Analysis

`/business-analyse` is the **first phase of the V-Model** and arguably
the most important. It prevents the number-one failure mode of AI coding
sessions: jumping to solutions before the problem is clear.

## What it does

The skill guides you through three innovation phases:

1. **Exploration** -- understand the problem space (users, needs, insights,
   trends, competitors, touchpoints)
2. **Ideation** -- design the solution (value proposition, idea potential,
   the "Wow" feature, jobs to be done, critical hypotheses)
3. **Validation** -- test business viability (VP score, assessment radar,
   pricing, channels, revenue streams)

All three phases are **co-created** with the user. The skill never
invents personas, insights, or assumptions in the background. It
proposes, cites sources, and waits for confirmation.

## Scope adaptation

The skill asks at the start which scope applies:

| Scope | Exploration | Ideation | Validation | Typical duration |
|---|---|---|---|---|
| **Simple Test** | Minimal (user + problem) | Describe solution | Skip | Hours to 1-2 days |
| **Proof of Concept** | Shortened (user, needs, HMW) | Full | Hypotheses + feasibility | 1-4 weeks |
| **MVP** | Full (10 sections) | Full | Full market assessment | 2-6 months |

The depth of questions, the number of personas, and the rigor of
validation all scale with scope.

## Interview rules

### Co-creation, not autonomous generation

Every persona, insight, need, and touchpoint is proposed as a draft and
confirmed by the user before becoming part of the artifact. Example:

> "Here is a persona based on what you described: [draft]. Does this
> fit, or should we adjust something?"

### Ask before you ask

Before asking about users, market, or competitors, the skill first
checks whether the user already has that data. If yes: let them share
it. If no: suggest 1-2 research methods and continue.

### Probing techniques

When an interview partner gives thin answers, the skill uses:

- **5-Why** -- ask "why is that a problem?" five times
- **Concretization** -- "can you give a concrete example?"
- **Future projection** -- "imagine the problem was solved -- what would change?"
- **Perspective shift** -- "what would your customer/boss say about this?"
- **Emotional level** -- "how does it feel when that happens?"
- **Analogy trigger** -- "do you know something similar from another domain?"

Plus ethnographic suggestions when appropriate: Fly on the Wall,
Self-Immersion, Extreme Users.

## Key outputs

- `_devprocess/analysis/BA-{PROJECT}.md` -- the full Business Analysis
- `_devprocess/analysis/EXPLORE-{PROJECT}.md` -- the Exploration Board (PoC/MVP)
- **HMW question** -- the bridge from Exploration to Ideation
- **Value Proposition** -- the formal synthesis
- **Critical Hypotheses** -- what must be validated
- **Idea Potential** -- scored on 3 axes (Value, Transferability, Feasibility)

## Innovation methods

The skill ships with 20+ innovation methods and their probing techniques
in `skills/business-analyse/references/innovation-methods.md`. Examples:

- Jobs to be Done (functional, emotional, social job levels)
- Kill your Company -- "how would a startup attack you?"
- Evaluation Matrix -- compare and prioritize ideas
- Assessment Radar (6 axes for business viability)
- Value Proposition Score (4 scales 0-10)

All methods include concrete guidance on how to conduct them and what
to do when you get stuck.

## Quality gates

Before handoff to Requirements Engineering, the skill checks quality
gates adapted to scope:

- **Simple Test**: at least 3 of 4 criteria (problem, user, functionality, DoD)
- **PoC**: at least 6 of 8 criteria (HMW, hypothesis, persona, risks, ...)
- **MVP**: at least 10 of 13 criteria (full Exploration Board, 2+ personas, ...)

If a gate fails, the skill returns to the relevant section instead of
handing off with a half-finished BA.

## Handoff

`/business-analyse` ends with the mandatory 3-part Handoff Ritual
(Artifact report, Handoff context in `30_handoffs.md`, Transition
question for `/requirements-engineering`). See
[Handoff Rituals](../concepts/handoff-rituals).

## Source

The canonical skill content is in
[`skills/business-analyse/SKILL.md`](https://github.com/pssah4/digital-innovation-agents/blob/main/skills/business-analyse/SKILL.md).

## What's next

- [Your first Business Analysis tutorial](../tutorials/first-business-analysis)
- [Requirements Engineering guide](./requirements-engineering) -- the next phase
- [Tech-agnostic Requirements concept](../concepts/tech-agnostic-requirements)
