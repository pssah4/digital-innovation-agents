---
title: Your first Business Analysis
description: Walk through a concrete business analysis with the /business-analysis skill, from scoping to handoff.
---

# Your first Business Analysis

Let's run a real business analysis. We take an idea, scope it, explore
the problem, design a solution, and end with a Business Analysis document
that hands off cleanly to Requirements Engineering.

## The example idea

> "I want to build a tool that helps distributed teams run better
> async retrospectives."

This is a typical starting point: a rough idea, no clear user, no
hypothesis, no scope. Exactly where `/business-analysis` is most useful.

::: info Methods you will see referenced below
The agent's main job is to notice gaps in your understanding and propose
the right research or prototyping method to close them. The callouts
through this tutorial link straight to the method cards under
[Discovery methods](../reference/methods-discovery),
[Ideation methods](../reference/methods-ideation), and
[Validation methods](../reference/methods-validation). You can read
them now or wait until the tutorial walks you into the spot where one
becomes relevant.
:::

## Step 1: Invoke the skill

In your AI coding tool (Claude Code, Cursor, Codex, OpenCode, or Gemini CLI):

```
/business-analysis

I want to build a tool that helps distributed teams run better async
retrospectives.
```

## Step 2: Determine the project scope

The skill starts with a scope question:

```
Before we go into detail: what is your project purpose?

A) Simple Test / Feature
   -> Timeframe: hours to 1-2 days

B) Proof of Concept (PoC)
   -> Prove technical feasibility, 1-4 weeks

C) Minimum Viable Product (MVP)
   -> Functional product, 2-6 months
```

Pick **B) PoC** for this walkthrough. The skill now adapts the depth
of the analysis: shortened Exploration, full Ideation, hypothesis-based
Validation.

## Step 3: Exploration phase

The skill asks targeted questions, one at a time. For a PoC, expect
8 to 12 questions covering:

- **Users and personas**: who is affected? Who pays? Who blocks?
- **Needs**: what functional, emotional, and social needs exist?
- **Insights**: what did you learn from real user statements?
- **Trends and technology**: what is happening in the space?
- **How-Might-We**: the synthesis question that bridges problem and solution

Important: the skill co-creates artifacts with you. It proposes a
draft persona and asks you to confirm or correct. It cites which user
statement an insight comes from. Nothing is invented in the background.

::: tip If you cannot answer "who is the user"
Before drafting a persona, the agent will likely propose a field method
so you can come back with real evidence:

- [Explorative interviews](../reference/methods-discovery#explorative-interviews).
  7 to 10 short conversations, 20 to 30 minutes each, to map the problem
  space when you do not yet know which segment matters.
- [Qualitative interview](../reference/methods-discovery#qualitative-interview).
  One deep conversation, 60 to 90 minutes, when you already know who
  to talk to and need depth.
- [Stakeholder map](../reference/methods-discovery#stakeholder-map)
  when several departments or external parties are in the picture and
  you do not know who to interview first.
- [Extreme users](../reference/methods-discovery#extreme-users) when
  average-user interviews produce generic answers and the real driver
  has not surfaced yet.
:::

::: tip If you have interview notes but no pattern
The agent will help you move from raw notes to a usable persona:

- [User motivation analysis](../reference/methods-discovery#user-motivation-analysis)
  to pull functional needs, emotional needs, and obstacles out of a
  pile of transcripts.
- [Persona synthesis cluster](../reference/methods-discovery#persona-synthesis-cluster)
  to turn clusters of insights into persona seeds.
- [Persona](../reference/methods-discovery#persona) to finish each
  seed into a one-page reference everyone on the team can check
  decisions against.
:::

::: tip If users describe an ideal workflow instead of the real one
Interviews alone will not get you past this. Two observational
methods fit:

- [Fly on the wall](../reference/methods-discovery#fly-on-the-wall).
  Silent observation in the real context. You learn what users do,
  not what they say they do.
- [Self-test](../reference/methods-discovery#self-test). Walk the
  user's process yourself. Uncomfortable but fast.
:::

::: tip If you cannot name the competitors or the market context
- [Market and trend analysis](../reference/methods-discovery#market-and-trend-analysis).
  One day of desk research, two hours of clustering, four to six
  themes with one potential field each.
- [User journey](../reference/methods-discovery#user-journey) when
  the friction is really about the user's experience over time, not
  the market around it.
:::

At the end of Exploration, you get a How-Might-We question like:

> How might we help distributed product teams run retros that surface
> root causes, so action items actually ship?

## Step 4: Ideation phase

The skill now shifts from understanding the problem to designing a
solution. For a PoC, expect 8 to 10 questions:

- Solution description and object model
- **Idea potential** on three axes (Value, Transferability, Feasibility), scored 0 to 10
- **The Wow**: which feature would you want the press to celebrate?
- **Critical hypotheses**: what must be true for this to work?
- **Value proposition**: the formal statement

::: tip If the solution space feels empty or keeps repeating itself
The agent will suggest a short ideation exercise. Which one depends on
your team and the shape of the blockage:

- [Brainstorming](../reference/methods-ideation#brainstorming). A
  15 to 20 minute group session once you have a sharp HMW. Best when
  the team is willing to defer judgement and fast-talkers can be kept
  in check.
- [Brainwriting](../reference/methods-ideation#brainwriting). The
  silent 6-3-5 variant, useful when previous brainstorms were dominated
  by one or two voices.
- [Inspiration cards](../reference/methods-ideation#inspiration-cards)
  when the team keeps reproducing the same three or four variants and
  you need a jolt from outside the domain.
- [Idea tower](../reference/methods-ideation#idea-tower) when a seed
  idea is promising but too thin to prototype. Additive only, no
  removals, until the concept is coherent enough to sketch.
:::

::: tip If you cannot explain why users would switch
- [Jobs to be done](../reference/methods-ideation#jobs-to-be-done).
  Name the functional job, the emotional job, and the social job for
  the target user, along with hiring and firing criteria. This is
  also the method the RE skill will rely on when it drafts user
  stories for the functional, emotional, and social layer.
- [Kill your company](../reference/methods-ideation#kill-your-company)
  for the inverse lens. Pretend a startup is attacking you. The
  weaknesses they would target become the value proposition you
  need to defend.
:::

::: tip If you have too many ideas and no shortlist
- [Idea clustering and selection](../reference/methods-ideation#idea-clustering-and-selection).
  Cluster by theme first, then score the clusters against four
  criteria (User Value, Feasibility, Transferability, Risk), and
  pick the top three with evidence you can defend.
:::

Example output of Idea Potential:

```
Value/Urgency:    8/10 (retros are a well-known pain point)
Transferability: 9/10 (applies to any distributed team)
Feasibility:     6/10 (async UX is tricky)
```

## Step 5: Validation phase

For PoC scope, Validation is shortened to hypothesis prioritization and
feasibility. You list the critical hypotheses, prioritize them, and
define test methods.

::: tip If a critical hypothesis needs a test plan
The agent matches the hypothesis to the cheapest method that would
actually falsify it:

- [Wireframes, storyboards, and paper prototypes](../reference/methods-validation#wireframes-storyboards-and-paper-prototypes).
  Low-fidelity sketches of the risky flow. Best as a first test when
  the flow itself is the hypothesis.
- [Wizard of Oz](../reference/methods-validation#wizard-of-oz) when
  the feature is expensive to build (AI, automation, complex backend)
  and you want to see if users would even use it.
- [Appearance prototype](../reference/methods-validation#appearance-prototype)
  when the flow is clear and you are testing brand or visual trust.
- [Expert review](../reference/methods-validation#expert-review)
  when the question is "can this even exist" (regulation, technical
  feasibility, safety) rather than "do users want this".
:::

::: tip If you are unsure about the business side
- [Business plan](../reference/methods-validation#business-plan).
  A one-page Business Model Canvas with one sentence per cell and a
  number in every revenue and cost cell. Mark unsupported assumptions
  as the next hypotheses.
- [Value proposition quantification](../reference/methods-validation#value-proposition-quantification)
  to compare two or three candidate value propositions against
  evidence instead of gut feeling.
- [Pre-mortem](../reference/methods-validation#pre-mortem) before
  committing resources. "It is six months from now and the project
  has failed. Write down why." Five minutes silent per person, then
  cluster the reasons and assign owners to preventive actions.
:::

## Step 6: Produce the documents

The skill now creates two artifacts:

- `_devprocess/analysis/BA-retrospectives.md`: the full Business Analysis
- `_devprocess/analysis/EXPLORE-retrospectives.md`: the Exploration Board

Both follow the templates in `skills/business-analysis/templates/`.

## Step 7: Handoff ritual

`/business-analysis` ends with the mandatory 3-part Handoff Ritual:

1. **Artifact report**: lists the produced files and the HMW question
2. **Handoff context**: appends an entry to `_devprocess/context/HANDOFFS.md`
   with scope, personas, critical hypotheses, and open assumptions
3. **Transition question**: "BA complete. Shall I start `/requirements-engineering` now?"

If you say "yes", the next phase starts automatically. If you say "stop",
the skill pauses and you can review the BA before moving on.

## What's next

- The BA document is the input for [`/requirements-engineering`](../guides/requirements-engineering),
  which turns it into Epics, Features, and tech-agnostic Success Criteria.
- Or run the entire cycle in one go with [`/dia-orchestrator`](../guides/dia-orchestrator).
  See the next tutorial: [A full V-Model run](./full-v-model-run).
- The full set of method cards lives under
  [Discovery methods](../reference/methods-discovery),
  [Ideation methods](../reference/methods-ideation), and
  [Validation methods](../reference/methods-validation).
