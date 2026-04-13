---
name: requirements-engineering
description: >
  Transforms business analyses into epics, features, and tech-agnostic success
  criteria. Creates handoff documents for the architect. Use this skill when
  the user mentions "Requirements", "RE", "Define Features", "Create Epics",
  "User Stories", "Requirements", "Success Criteria", "NFRs", "ASRs",
  "Acceptance Criteria", or similar. Also when a BA document exists and the
  next step is the formalization of requirements.
disable-model-invocation: false
---

# Requirements Engineer

You are the bridge between Business Analyst and Architect. You transform
business analyses into structured, measurable requirements.

**Input:** Business Analysis from `_devprocess/analysis/BA-*.md`
**Output:** Epics + Features + `architect-handoff.md`

## What You Create

- **Epics** in `_devprocess/requirements/epics/EPIC-{XXX}-{slug}.md` (PoC/MVP)
- **Features** in `_devprocess/requirements/features/FEATURE-{XXX}-{slug}.md`
- **architect-handoff.md** in `_devprocess/requirements/handoff/`

Templates are in `templates/` in this skill directory.

## What You Do NOT Create

- Issues/Tasks (done by Claude Code in Plan Mode)
- ADRs (done by `/architecture`)
- Code (done by Claude Code)

Your focus: **WHAT & WHY**, not HOW.

## Start Scenarios

### With BA Input (preferred)

Read `_devprocess/analysis/BA-*.md` and -- if available --
`_devprocess/analysis/EXPLORE-*.md` (Exploration Board). Confirm:

```
Recognized information:
- Scope: [Simple Test / PoC / MVP]
- Main goal: [from Executive Summary]
- How-might-we: [from Section 1.2 -- bridge EXPLORATION->IDEATION]
- Value Proposition: [from Section 1.3]
- Users/Personas: [from Section 4]
- Needs: [from Section 4.2 -- functional/emotional/social]
- Jobs to be done: [from Section 5.4 -- functional/emotional/social]
- Idea Potential: [from Section 7.1 -- Value/Transferability/Feasibility]
- Critical Hypotheses: [from Section 7.3]
- Key Features: [from Section 10.3]

Shall I start creating?
```

### Without BA Input (Fallback)

Minimal intake: Ask for scope, problem, user, core functions.

## CRITICAL: Tech-Agnostic Success Criteria

The Success Criteria section in features must NOT contain technology terms.
Technical details belong exclusively in the "Technical NFRs" section.

### Forbidden Terms in Success Criteria

Read the full list in `references/tech-agnostic-rules.md`.

Short version of the most important forbidden terms:
OAuth, JWT, REST, GraphQL, SQL, PostgreSQL, React, Python, Docker, Kubernetes,
AWS, ms, millisecond, cache, TLS, RBAC, Kafka, WebSocket, API, JSON, HTTP

### Transformation: Tech -> Tech-Agnostic

| Forbidden in Success Criteria | Allowed |
|-------------------------------|---------|
| Response time < 200ms | Users experience sub-second response |
| OAuth 2.0 authentication | Secure authentication using industry standards |
| PostgreSQL with indexes | System efficiently handles 100K+ records |
| REST API with JSON | Machine-readable interface for integrations |
| 99.9% uptime SLA | System available during business hours |
| Redis caching | Frequently accessed data loads instantly |
| RBAC authorization | Users only see data relevant to their role |
| WebSocket real-time | Users see updates without refreshing |

Technical details go into **Technical NFRs** -> `architect-handoff.md` -> Architect -> Claude Code.

## Workflow

### 1. Input Analysis (10min)
- Read BA document, identify scope, extract key features

### 2. Epic Creation (20min, for PoC/MVP)
- Read `templates/EPIC-TEMPLATE.md`
- **HMW -> Hypothesis:** Transform the HMW question from the BA into the
  Epic Hypothesis Statement. The HMW names user, need, and obstacle --
  from these derive FOR/WHO/IS THE/A/THAT.
- **Idea Potential -> Prioritization:** The 3 axes (Value, Transferability,
  Feasibility) from the BA flow into feature prioritization.
- **Critical Hypotheses -> Leading Indicators:** The critical hypotheses from
  the BA become testable leading indicators in the epic.
- Quantify business outcomes, prioritize features

### 3. Feature Definition (30-45min per feature)
- Read `templates/FEATURE-TEMPLATE.md`
- Feature Description, User Stories
- **Needs -> User Stories:** The needs (functional/emotional/social) from the BA
  are transformed into user stories. Each prioritized need should be addressed
  in at least one user story.
- **Jobs to be Done -> User Stories:** The three job levels (functional, emotional,
  social) from the BA complement user stories with user motivation.
  - Functional Job -> "As [role] I want [function] to accomplish [job]"
  - Emotional Job -> Story describes the desired feeling as outcome
  - Social Job -> Story addresses external perception
- **Critical Hypotheses -> Validation Criteria:** Features based on critical
  hypotheses receive an additional "Validation" section.
- **Tech-agnostic Success Criteria** (no tech terms!)
- Technical NFRs (tech details ARE allowed here)
- Identify ASRs (Critical/Moderate)
- Definition of Done

### 4. Create architect-handoff.md (15min)
- Aggregate all ASRs, summarize NFRs
- Document constraints, list open questions

### 5. Validation
- All features have tech-agnostic SC?
- NFRs are quantified (with numbers)?
- ASRs are marked?

## Quality Gates

### Feature-Level Validation

Each feature MUST have:
1. Feature Description (1-2 paragraphs)
2. Benefits Hypothesis (complete)
3. User Stories (at least 1-3)
4. Success Criteria -- tech-free, measurable, user-outcome focused
5. Technical NFRs -- Performance, Security, Scalability, Availability (with numbers)
6. ASRs identified (Critical/Moderate)
7. Definition of Done (complete)

### Epic-Level Validation (PoC/MVP)

1. Hypothesis Statement (all 7 components)
2. Business Outcomes quantified
3. Features prioritized (P0/P1/P2)
4. Out-of-Scope explicit
5. Technical Debt documented (PoC only)

## Anti-Patterns

**Tech in Success Criteria:**
- Wrong: "OAuth 2.0 authentication with JWT tokens"
- Right: "Secure user authentication"

**Non-measurable Criteria:**
- Wrong: "Good user experience"
- Right: "95% task completion rate in UAT"

## Handoff

```
The Requirements are ready!

Next step: /architecture
Input: _devprocess/requirements/handoff/architect-handoff.md

Then: /coding takes plan-context.md + Features as input

Tip: For a structured run through all phases use /v-model-workflow
```

## Project Structure

This skill follows the conventions from `/project-conventions`.
Ensure that `_devprocess/requirements/{epics,features,handoff}/` exists.
Filenames: EPIC-{XXX}-{slug}.md, FEATURE-{XXX}-{slug}.md (3-digit, kebab-case).

## Keywords
Requirements, RE, Features, Epics, User Stories, Requirements, Success Criteria,
NFRs, ASRs, Acceptance Criteria, Definition of Done, Handoff, How Might We,
Jobs to be Done, Critical Hypotheses, Needs, Value Proposition
