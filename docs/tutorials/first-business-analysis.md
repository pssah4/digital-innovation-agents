---
title: Your first Business Analysis
description: Walk through a concrete business analysis with the /business-analyse skill, from scoping to handoff.
---

# Your first Business Analysis

Let's run a real business analysis. We take an idea, scope it, explore
the problem, design a solution, and end with a Business Analysis document
that hands off cleanly to Requirements Engineering.

## The example idea

> "I want to build a tool that helps distributed teams run better
> async retrospectives."

This is a typical starting point: a rough idea, no clear user, no
hypothesis, no scope. Exactly where `/business-analyse` is most useful.

## Step 1: Invoke the skill

In your AI coding tool (Claude Code, Cursor, Codex, OpenCode, or Gemini CLI):

```
/business-analyse

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
8-12 questions covering:

- **Users and personas**: who is affected? Who pays? Who blocks?
- **Needs**: what functional, emotional, and social needs exist?
- **Insights**: what did you learn from real user statements?
- **Trends and technology**: what is happening in the space?
- **How-Might-We**: the synthesis question that bridges problem and solution

Important: the skill co-creates artifacts with you. It proposes a
draft persona and asks you to confirm or correct. It cites which user
statement an insight comes from. Nothing is invented in the background.

At the end of Exploration, you get a How-Might-We question like:

> How might we help distributed product teams run retros that surface
> root causes, so action items actually ship?

## Step 4: Ideation phase

The skill now shifts from understanding the problem to designing a
solution. For a PoC, expect 8-10 questions:

- Solution description and object model
- **Idea potential** on 3 axes (Value, Transferability, Feasibility), 0-10
- **The Wow**: which feature would you want the press to celebrate?
- **Critical hypotheses**: what must be true for this to work?
- **Value proposition**: the formal statement

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

## Step 6: Produce the documents

The skill now creates two artifacts:

- `_devprocess/analysis/BA-retrospectives.md`: the full Business Analysis
- `_devprocess/analysis/EXPLORE-retrospectives.md`: the Exploration Board

Both follow the templates in `skills/business-analyse/templates/`.

## Step 7: Handoff ritual

`/business-analyse` ends with the mandatory 3-part Handoff Ritual:

1. **Artifact report**: lists the produced files and the HMW question
2. **Handoff context**: appends an entry to `_devprocess/context/30_handoffs.md`
   with scope, personas, critical hypotheses, and open assumptions
3. **Transition question**: "BA complete. Shall I start `/requirements-engineering` now?"

If you say "yes", the next phase starts automatically. If you say "stop",
the skill pauses and you can review the BA before moving on.

## What's next

- The BA document is the input for [`/requirements-engineering`](../guides/requirements-engineering),
  which turns it into Epics, Features, and tech-agnostic Success Criteria.
- Or run the entire cycle in one go with [`/v-model-workflow`](../guides/v-model-workflow).
  See the next tutorial: [A full V-Model run](./full-v-model-run).
