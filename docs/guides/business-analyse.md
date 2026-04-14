---
title: Business Analysis
description: Explore, Ideate, Validate. Understand the problem before you design the solution. Based on Dark Horse Innovation's Digital Innovation Playbook.
---

# Business Analysis

`/business-analyse` is the first phase of the V-Model — and, honestly,
the most important one. It prevents the single most common failure
mode of AI coding sessions: **jumping to solutions before the problem
is clear**. A Claude Code agent is extraordinarily good at producing
code. It is catastrophically fast at producing the wrong code if the
problem was never properly framed.

This skill is not a form. It is a structured innovation interview
based on the three-phase innovation cycle from the
[Digital Innovation Playbook](../concepts/digital-innovation-playbook)
by Dark Horse Innovation, adapted for a one-on-one session with an AI
agent instead of a workshop room full of Post-its.

## The innovation cycle, one level up

Before diving into the mechanics of the skill, it is worth
understanding the method it implements. The Digital Innovation
Playbook describes three innovation modules that every digital
product idea has to pass through, in order:

```
EXPLORE ──▶  CREATE  ──▶  EVALUATE
  WHO?        WHAT?         WORTH IT?
  problem     solution      viability
   space       space         test
```

**Explore** is about *understanding*. You look at users, their needs,
the jobs they are trying to get done, their touchpoints, the trends
shaping the market, and the competitors already solving parts of the
problem. The output is an **insight**: a non-obvious statement about
why the current situation falls short for a real user.

**Create** is about *framing a response*. Given the problem you just
framed, what might solve it? Here you ideate, sketch, condense ideas
into a value proposition, and pick the one combination of features
that has the best chance of earning its place in the user's life.

**Evaluate** is about *testing viability*. Is this idea worth
building? Not "can we build it" but "should we." This is where
hypothesis-based testing, prototype feedback, landing pages, business
model canvases, and assessment matrices live.

::: info Why three phases and not two
Most teams conflate Explore and Create. They hear a problem, their
brain fires off three solutions, and they sprint to build them. This
is human. It is also how you end up with a feature that solves the
wrong problem for the wrong user. The Explore → Create separation
forces a beat between *framing* and *solving*. That beat is the
single most valuable discipline the Playbook teaches.
:::

`/business-analyse` walks you through all three phases in one
session, at a depth that matches your scope.

## Scope adaptation — three tiers

The skill asks at the start which scope applies. The rest of the
session scales to match:

| Scope | Exploration | Ideation | Validation | Typical duration |
|---|---|---|---|---|
| **Simple Test** | Minimal (user + problem) | Describe solution | Skip | Hours to 1-2 days |
| **Proof of Concept** | Shortened (user, needs, HMW) | Full | Hypotheses + feasibility | 1-4 weeks |
| **MVP** | Full 10-section Exploration Board | Full | Full market assessment | 2-6 months |

The rule: **do not over-produce for a small target; do not
under-produce for a full onboarding**. A Simple Test does not need
a stakeholder map. An MVP does not get away without one.

## Phase 1 — Exploration: understand the problem

Exploration is the part most people want to skip. They already "know"
the users; they already "know" the problem. In practice, "knowing"
almost always means *holding an assumption the team has never
challenged*. The skill treats every claim as a draft until you
explicitly confirm it.

The Exploration Board sections the skill walks through (full at MVP
scope, shortened below):

- **Users** — who is affected, in 1–3 concrete segments
- **Needs** — functional, emotional, and social
- **Insights** — the "aha" statements that reframe the problem
- **Touchpoints** — where the user currently encounters the problem
- **Trends & Technology** — shaping forces
- **Facts** — data, sizing, market context
- **Potential partners & competitors** — who is already in the space
- **Potential fields** — adjacent opportunities

### The key mechanic: ask before you ask

Before asking you about users, markets, or competitors, the skill
first checks whether you already have that data — from prior
research, existing documents, customer support logs, CRM exports.
If yes, it ingests what you have and builds on it. If no, it
suggests one or two research methods and continues.

This matters because the biggest waste in a BA session is the agent
re-asking questions you could have answered from existing evidence
in five seconds flat.

### Excursion — Explorative Interviews

::: details Method: Explorative Interviews (30–90 min per user)
**Goal:** Identify pain points, needs, and routines of a target group.

An explorative interview is an open but guided conversation with a
user. You ask a lot of open-ended questions and **let the user talk**.
Most important rule: transcribe, do not interpret yet. Quotes will
help later during synthesis.

**Classic rhythm:**

1. Define the target group based on the problem framing
2. Draft an interview guideline with topics you want to cover
3. Find 5–10 users (rule of thumb: ~7 interviews surface the patterns)
4. Interview in pairs — one moderator, one note-taker
5. Transcribe in the moment; do not paraphrase
6. Extract 4–5 key insights directly after each interview while
   your memory is fresh
7. After every few interviews, hold a short result session to shift
   focus for upcoming ones

**Probing techniques** when an interview partner gives thin answers:

- **5-Why** — ask "why is that a problem?" five times
- **Concretization** — "can you give a concrete example?"
- **Future projection** — "imagine the problem was solved, what changes?"
- **Perspective shift** — "what would your customer or boss say?"
- **Emotional level** — "how does it feel when that happens?"
- **Analogy trigger** — "do you know something similar from another domain?"

The skill uses the same probes during your BA interview whenever
your own answers go too thin to be actionable.

*Source: Digital Innovation Playbook, Explore methoden-onepager "Explorative Interviews"*
:::

### Excursion — Observation

::: details Method: Observation (field, > 1 h)
**Goal:** Observe users to infer what's not being said.

Interviews often fail to reveal actual behavior — users *tell* you
what they think they do, not what they really do. Observation puts
you in their environment and lets you watch the real sequence.

**Steps:**

1. Define a research question and a plan (topics, contexts, places,
   users to observe)
2. Go into the field. Observe. Ask clarifying questions sparingly.
   Document observations and direct quotes.
3. Secure impressions immediately after the session in a reflection
   round. Post-it note the most important findings.

**Variants:**

- **Open observation** — the user knows you are watching
- **Hidden observation** — you blend in (only where ethical)
- **Shadowing** — common in B2B: follow the user through a shift

Observation is most useful when interview responses feel rehearsed
or when users describe a workflow that "should" happen instead of
the workflow that actually does.

*Source: Digital Innovation Playbook, Explore methoden-onepager "Observation"*
:::

### Excursion — Immersion

::: details Method: Immersion (1 h to several days)
**Goal:** Establish empathy by taking on the user's worldview.

Conversations and observations are often insufficient to fully
understand a user. Immersion means experiencing the service or
interaction first-hand: visiting the shop, calling the hotline,
temporarily doing the user's job.

**Steps:**

1. Pick a situation to examine in more detail
2. Put yourself in the situation — do it for real, not as a mental
   exercise
3. Document what you observe and feel
4. Recall your experience and go through your notes
5. Verify your assumptions by interviewing real customers

This is the method you reach for when a product has to serve a user
type you personally do not belong to. It is uncomfortable — that is
the point.

*Source: Digital Innovation Playbook, Explore methoden-onepager "Immersion"*
:::

### Excursion — Stakeholder Mapping

::: details Method: Stakeholder Mapping (45–60 min)
**Goal:** Map all internal and external stakeholders of a project
and identify their impact and expectations.

Stakeholder Mapping provides an overview of everyone directly or
indirectly affected by the project: owners, customers, employees,
industry, regulators, community. It helps you understand how
stakeholders interact, the mechanics of internal politics, and
strategies for influence.

**Steps:**

1. Identify internal and external stakeholders on Post-its, pin them
   to the board
2. Analyse each stakeholder's contribution, willingness to engage,
   influence, and necessity of involvement
3. Map the key stakeholders spatially (e.g. power/interest grid)
4. Draw connections between Post-its and describe each connection
   in one word
5. Rank stakeholders by relevance for the project

Use this early in an MVP-scope BA whenever the product touches
multiple departments or external regulators. For a Simple Test it
is usually overkill.

*Source: Digital Innovation Playbook, Explore methoden-onepager "Stakeholder Mapping"*
:::

### From insights to a Point of View

Once the Exploration sections are filled, the skill synthesises a
**Point of View (POV)** statement. This is the single sentence that
condenses everything you learned into an actionable problem frame.

::: details Method: Point of View
**Format:**

> [User . . . (descriptive)] **needs/wants/has to** [need/pain . . .
> (verb)] **because/but** [insight . . . (compelling)].

**Classic example:**

> Harriet, a mother of three rushing through the airport, needs a
> way to entertain her children because she feels uncomfortable
> when they disturb other passengers.

A good POV is:

- **Specific about the user.** "Mothers of three rushing through
  the airport" beats "travelers."
- **Verb-driven in the need.** "Entertain her children" is
  actionable; "better experience" is not.
- **Insightful in the because.** The insight is the non-obvious
  part — the emotional pressure of social judgement, not the
  functional lack of entertainment.

You will spend more time on this one sentence than you think, and
it will earn back every minute during Ideation.

*Source: Digital Innovation Playbook, Explore methoden-onepager "Point of View"*
:::

### The bridge: How Might We

The POV becomes a **How Might We (HMW) question** — the bridge from
Exploration to Ideation.

::: details Method: HMW Questions
**Purpose:** Reframe the POV into an open question that opens a
solution space instead of closing it.

Good HMW questions are neither too wide nor too narrow. From
Harriet's POV, all of these are valid HMWs, each opening a
different solution space:

- *"How might we use the energy of the children to entertain other
  passengers?"* (turn bad into good)
- *"How might we separate the children from other passengers?"*
  (delete the bad)
- *"How might we delete the waiting time at the airport?"*
  (challenge propositions)
- *"How might we turn the airport into a playground?"*
  (analogies)

Notice how the same POV produces radically different HMWs. Each one
steers the creative team into a different ideation direction. The
skill proposes 3–5 candidates and asks which direction you want to
carry forward.

**Workshop rhythm:**

1. Take one problem statement (POV) as the starting point
2. Ideate HMW questions for 3 minutes — one per Post-it
3. Read each question aloud and stick it on the wall
4. Cluster similar questions
5. Vote on favourites (3–5 dot votes per person)
6. Start ideation on the winning HMW

In the 1:1 AI session the skill runs a compressed version: it
drafts candidate HMWs, you pick one.

*Source: Digital Innovation Playbook, Explore methoden-onepager "HMW Questions"*
:::

## Phase 2 — Ideation (Create): design the response

Once the HMW is set, the skill moves into Create mode. The sections
(full at MVP scope):

- **Idea description** — the core concept in 2–3 sentences
- **Addressed users** — which users from Exploration are served
- **Addressed needs** — which needs the idea hits
- **Problems solved** — what specifically becomes easier
- **Idea Potential** — scored on three axes (User Value,
  Scalability / Transferability, Feasibility)
- **The Wow** — the one feature that makes the idea memorable
- **High-Level Concept** — the "for X, this is like Y but Z" line
- **Value Proposition** — the formal synthesis that closes Create

The three Idea Potential axes feed directly into priority labelling
later: a high-User-Value / high-Feasibility idea becomes a P0
feature in [Requirements Engineering](./requirements-engineering).

### Excursion — Classic Brainstorming

::: details Method: Classic Brainstorming (15 min)
**Goal:** Generate many new ideas on a specific HMW.

The Playbook ships 11 Design Thinking rules that govern every
ideation session. They are non-negotiable:

1. **Go for quantity** — volume first, quality later
2. **Go for wild ideas** — the crazier the seed, the better the
   branch
3. **Build on ideas of others** — "yes, and" beats "yes, but"
4. **Defer judgement** — no critique in the generative phase
5. **Only one person speaks** — no cross-talk
6. **Stay focused** — one HMW at a time
7. **Work visual** — sketches beat sentences
8. **Work multidisciplinary** — invite people outside your function
9. **Fail early and often** — quick and rough is better than slow
   and polished
10. **Think user-centric** — every idea loops back to the POV
11. **Take the fun serious** — play is part of the method

The skill enforces these during the 1:1 session: it generates wide
before narrowing, it never critiques your ideas in the generative
phase, and it asks "what if the constraint was removed?" to push
for wild variants.

*Source: Digital Innovation Playbook, Create methoden-onepager "Classic Brainstorming"*
:::

### Excursion — Idea Canvas

::: details Method: Idea Canvas (15–35 min)
**Goal:** Condense an idea to its core by focusing on the target
group and their pain points.

The Idea Canvas is a one-page checklist that wraps up ideation.
Sections:

- **Slogan** — the idea in one catchy sentence
- **Persona / Target group** — who is addressed
- **Pain points & Point of View** — the pains this idea solves
- **Concept** — what the idea is about
- **3 most important features** — how the idea works
- **Value Proposition** — the benefits for the customer
- **Visualisation** — a sketch says more than a thousand words

The skill produces this structure as part of the BA output so the
handoff to Requirements Engineering has a compact idea summary that
is not buried in prose.

*Source: Digital Innovation Playbook, Create methoden-onepager "Idea Canvas"*
:::

### Excursion — Value Proposition Canvas (Strategyzer)

::: details Method: Value Proposition Canvas (1–3 h)
**Goal:** Set customer jobs, pains, and gains against products and
services, pain relievers, and gain creators.

The Value Proposition Canvas is a zoom-in on two blocks of the
Business Model Canvas — Customer Segments and Value Proposition.
You fit them together and find blind spots.

**Customer Profile (right side):**

- **Jobs** — what customers are trying to get done in their work
  and lives (in their own words)
- **Pains** — bad outcomes, risks, obstacles related to those jobs
- **Gains** — outcomes customers want to achieve, concrete benefits

**Value Map (left side):**

- **Products & Services** — the list your value proposition is
  built around
- **Pain Relievers** — how your products alleviate customer pains
- **Gain Creators** — how your products create customer gains

**The fit test:** for each Pain Reliever and Gain Creator, check
whether it matches a specific Job, Pain, or Gain. Those without a
match may be nice features but are not creating customer value.

The skill produces a compact version of this as part of the Value
Proposition synthesis. For MVP scope it asks you to validate each
fit explicitly.

*Source: Digital Innovation Playbook, Create methoden-onepager "Value Proposition Canvas" (Strategyzer)*
:::

## Phase 3 — Validation (Evaluate): is it worth building?

The final phase tests the business viability of the idea. At MVP
scope this is the longest section in the BA; at PoC scope it is
short; at Simple Test scope it is skipped entirely.

Sections from the Digital Innovation Board:

- **Value Proposition Score** — 4 scales 0–10 (activation,
  preference over substitutes, willingness to pay, recommendation)
- **Pricing & willingness to pay**
- **User Experience** — emotional response scale
- **Assessment Radar** — 6 axes (Brand Fit, Investment, Market
  Size, Asset Fit, Viral Potential, New Customer)
- **Channels** — how the idea reaches users
- **Unfair Advantage** — what makes this hard to copy
- **KPI** — what will be measured after launch
- **Revenue Stream** — how money flows

### Excursion — Critical Hypotheses and the Test Card

::: details Method: Hypothesis-Based Testing (Strategyzer Test Card)
**Goal:** Test assumptions in a fast, iterative, build-measure-learn
cycle.

Every BA surfaces critical hypotheses — assumptions the team needs
to test before investing. The Playbook uses two Strategyzer
templates to keep this rigorous.

**Test Card — a single experiment:**

> **STEP 1 — Hypothesis:** We believe that [assumption]
> **STEP 2 — Test:** To verify that, we will [method]
> **STEP 3 — Metric:** And measure [indicator]
> **STEP 4 — Criteria:** We are right if [threshold]

**Example:**

> *We believe that small teams will pay 29€/month for a private
> Git mirror with audit logs. To verify that, we will run a
> 14-day landing page test with a "Start trial" CTA. And measure
> the signup rate. We are right if signups / visitors ≥ 3%.*

**Rules:**

- **Prioritise by risk.** Start with the hypothesis that could
  kill the business if wrong. Not the easiest — the deadliest.
- **One hypothesis can have multiple tests.** Start cheap, progress
  to more expensive ones as evidence stacks up.
- **Run tests in build-measure-learn iterations** — short loops.

**Learning Card — the result of one experiment:**

> **We believed that** [hypothesis]
> **We observed** [data]
> **From that we learned that** [insight]
> **Therefore, we will** [decision: validated / invalidated / learn more]

The skill produces critical hypotheses at the end of the BA in
exactly this test-card structure, so `/requirements-engineering`
can pick them up and attach them to specific features.

*Source: Digital Innovation Playbook, Evaluate onepager "Hypothesis-based Testing" + Strategyzer Test Card and Learning Card*
:::

### Excursion — Assessment Radar

The Assessment Radar is a quick-and-dirty 6-axis viability score.
Each axis is rated 0–5:

| Axis | Question |
|---|---|
| **Brand Fit** | Does this idea reinforce the brand or pull it off-course? |
| **Investment** | How much does it cost relative to expected return? |
| **Market Size** | How big is the reachable market? |
| **Asset Fit** | Do we already have the key assets (data, partners, infra)? |
| **Viral Potential** | Will users pull other users in? |
| **New Customer** | Does this reach customers we could not reach before? |

The skill scores each axis with you explicitly and calls out the
weakest axis as the primary risk to validate. A radar with one
collapsed axis is far more useful than a balanced mediocre one —
you see the real bottleneck instead of averaging it away.

## The co-creation rule

Every persona, insight, need, and touchpoint the skill writes is
**proposed as a draft** and confirmed by you before it becomes part
of the artifact. Example:

> "Based on what you described, here is a persona sketch: [draft].
> Does this fit, or should we adjust something?"

The skill does not generate personas, HMWs, or value propositions
"in the background." Co-creation is the whole point — if you wanted
autonomous generation, you would get a hallucinated BA that reads
well and fails silently.

## Key outputs

- `_devprocess/analysis/BA-{PROJECT}.md` — the full Business Analysis
- `_devprocess/analysis/EXPLORE-{PROJECT}.md` — the Exploration Board
  (PoC and MVP scope only)
- **HMW question** — the bridge from Exploration to Ideation
- **Value Proposition** — the formal synthesis at the end of Create
- **Critical Hypotheses** — in test-card structure, ready for Evaluate
- **Idea Potential** — scored on User Value / Transferability /
  Feasibility

## Quality gates

Before handoff to Requirements Engineering, the skill checks quality
gates adapted to scope:

| Scope | Gate threshold |
|---|---|
| **Simple Test** | ≥ 3 of 4 criteria (problem, user, functionality, DoD) |
| **PoC** | ≥ 6 of 8 criteria (HMW, hypothesis, persona, risks, …) |
| **MVP** | ≥ 10 of 13 criteria (full Exploration Board, 2+ personas, …) |

If a gate fails, the skill returns to the relevant section instead
of handing off with a half-finished BA. See
[Verification Gates](../concepts/verification-gates) for the full
mechanic.

## Handoff

`/business-analyse` ends with the mandatory 3-part
[Handoff Ritual](../concepts/handoff-rituals):

1. **Artifact report** — which sections were filled, which were
   deferred, which hypotheses are still open
2. **Handoff context entry** in `_devprocess/context/30_handoffs.md`
3. **Transition question** — shall I start `/requirements-engineering` now?

## Validation Mode (from reverse engineering)

When `/business-analyse` detects a BA draft created by
`/reverse-engineering`, it enters **Validation Mode**:

- Walks through each section one by one
- Confirms evidence-backed claims with the user
- Fills `[NEEDS USER INPUT]` placeholders through the normal
  interview cycle
- Promotes each section status from `Draft` to `Validated` on
  confirmation

See the [Reverse Engineering guide](./reverse-engineering) for how
this flow gets triggered.

## Read the skill file

Want to see the exact instructions the agent follows?
[`skills/business-analyse/SKILL.md`](https://github.com/pssah4/digital-innovation-agents/blob/main/skills/business-analyse/SKILL.md)
on GitHub. The skill ships with 20+ innovation methods and their
probing techniques in
[`skills/business-analyse/references/innovation-methods.md`](https://github.com/pssah4/digital-innovation-agents/blob/main/skills/business-analyse/references/innovation-methods.md).

## Further reading

- [Digital Innovation Playbook lineage](../concepts/digital-innovation-playbook)
  — the method heritage this skill builds on
- [Your first Business Analysis tutorial](../tutorials/first-business-analysis)
- [Requirements Engineering](./requirements-engineering) — the next phase
- [Tech-agnostic Requirements](../concepts/tech-agnostic-requirements)
  — why the BA must never reference specific technologies
