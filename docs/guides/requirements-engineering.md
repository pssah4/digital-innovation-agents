---
title: Requirements Engineering
description: Transform a Business Analysis into Epics, Features, and tech-agnostic Success Criteria.
---

# Requirements Engineering

`/requirements-engineering` is the bridge between Business Analysis and
Architecture. It transforms the business analysis into structured,
measurable requirements.

**Input:** `_devprocess/analysis/BA-{PROJECT}.md`
**Output:** Epics, Features, `architect-handoff.md`

## Key features

- **HMW -> Epic Hypothesis**: the How-Might-We question from the BA
  becomes the Epic Hypothesis Statement
- **Needs -> User Stories**: functional, emotional, and social needs
  from the BA are transformed into user stories
- **Jobs to be Done -> User Stories**: each job level adds motivation
  to a user story
- **Critical Hypotheses -> Feature Validation**: features based on
  critical hypotheses get a dedicated Validation section
- **Idea Potential -> Feature Prioritization**: the 3 axes from the BA
  (Value, Transferability, Feasibility) flow into P0/P1/P2 labeling
- **Tech-agnostic Success Criteria**: Success Criteria must be free of
  technology terms (no OAuth, REST, PostgreSQL, ...). Technical details
  go into the separate "Technical NFRs" section. See
  [Tech-agnostic Requirements](../concepts/tech-agnostic-requirements)
  for the full rules.

## Quality gates

Each feature must have: Feature Description, Benefits Hypothesis,
User Stories, tech-free measurable Success Criteria, Technical NFRs
with numbers, identified ASRs (Critical/Moderate), and Definition of Done.

## Handoff

Ends with the 3-part Handoff Ritual. Next phase: `/architecture`.

## Read the skill file

[`skills/requirements-engineering/SKILL.md`](https://github.com/pssah4/digital-innovation-agents/blob/main/skills/requirements-engineering/SKILL.md) on GitHub.
