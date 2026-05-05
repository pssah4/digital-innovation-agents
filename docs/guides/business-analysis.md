---
title: Business Analysis
description: The first phase of the V-Model. Understand the problem before you design the solution. The agent runs the dialog, you run the field work.
---

# Business Analysis

`/business-analysis` is the first phase of the V-Model. It exists to stop the single most common failure mode of AI-assisted software projects: jumping straight to code before the problem is understood. A modern AI coding agent will happily build the wrong thing, fast, if nobody slowed it down to ask who the user is and what they actually struggle with.

This skill is the slowdown. It runs an innovation interview with you, spots the gaps in your understanding of the user and the problem, and tells you which research method will close each gap fastest. The actual field work stays with you. No agent can replace a real conversation with a real user.

## What the skill actually does

The session walks through three internal phases:

1. **Exploration** to understand the problem space. Users, needs, insights, touchpoints, trends, competitors.
2. **Ideation** to design a response. Idea description, value proposition, Wow feature, high-level concept, critical hypotheses.
3. **Validation** to test whether the idea is worth building. VP score, assessment radar, pricing, channels, revenue streams.

Every persona, insight, need, and touchpoint is proposed as a draft and confirmed by you before it becomes part of the artifact. The agent does not invent users in the background. It proposes, cites the source, and waits for your confirmation.

## Scope adaptation

The skill asks at the start which tier applies. The rest of the session scales to match.

| Scope | Exploration | Ideation | Validation | Typical duration |
|---|---|---|---|---|
| Simple Test | Minimal: user and problem | Describe the solution | Skip | Hours to 1 or 2 days |
| Proof of Concept | Shortened: user, needs, HMW | Full | Hypotheses and feasibility | 1 to 4 weeks |
| MVP | Full 10-section Exploration board | Full | Full market assessment | 2 to 6 months |

A Simple Test does not need a stakeholder map. An MVP does not get away without one. Match depth to scope.

## How the agent proposes methods in the dialog

The core behaviour of this skill is method matchmaking. During the interview, the agent notices where your answers go thin, where you sound certain without evidence, or where entire sections of the Exploration board are empty. When that happens, it stops asking questions and suggests a method instead.

Example moment inside a real session:

> **Agent:** Who exactly is affected by this problem?
>
> **You:** Probably our B2B customers. Maybe also their end users.
>
> **Agent:** That's a guess, not evidence. Before we draft a persona, we need a few real conversations. The fastest way at this stage is [explorative interviews](../reference/methods-discovery#explorative-interviews): seven to ten short conversations, 20 to 30 minutes each, to map the problem space. If you already suspect the real pain is with power users or non-users, [extreme users](../reference/methods-discovery#extreme-users) is a better fit. Which one do you want me to prep a question list for?

The agent then helps you build the question list or the stakeholder map or the interview guide, you run the method in the field, and you come back with notes. The session continues from where you paused.

The full set of methods the agent can suggest is documented as method cards on three reference pages:

- [Discovery methods](../reference/methods-discovery) for user research, observation, synthesis, and mapping
- [Ideation methods](../reference/methods-ideation) for generating and sharpening ideas
- [Validation methods](../reference/methods-validation) for prototyping, testing, and business viability

Each card has the same structure: what the method produces, when the agent brings it up, how to run it, team and time, things that go wrong in practice, and what to bring back to the session.

## Where the methods fit into the session

The BA session walks through Exploration, Ideation, and Validation. Each phase has a natural set of methods the agent reaches for when your answers go thin. The mapping below is the practical answer to "what should I actually do next if I am stuck on this step".

**Exploration, understanding users and the problem.**

- Fuzzy user group: [Explorative interviews](../reference/methods-discovery#explorative-interviews), [Qualitative interview](../reference/methods-discovery#qualitative-interview), [Extreme users](../reference/methods-discovery#extreme-users).
- Users describe the ideal instead of the real: [Fly on the wall](../reference/methods-discovery#fly-on-the-wall), [Self-test](../reference/methods-discovery#self-test).
- Notes exist but no pattern: [User motivation analysis](../reference/methods-discovery#user-motivation-analysis), [Persona synthesis cluster](../reference/methods-discovery#persona-synthesis-cluster), [Persona](../reference/methods-discovery#persona).
- Political or multi-department project: [Stakeholder map](../reference/methods-discovery#stakeholder-map).
- B2B with several intermediaries: [Value proposition chain](../reference/methods-discovery#value-proposition-chain).
- Broad fuzzy problem: [Research mind map](../reference/methods-discovery#research-mind-map).
- Unknown market or competitors: [Market and trend analysis](../reference/methods-discovery#market-and-trend-analysis).
- Experience spans several touchpoints: [User journey](../reference/methods-discovery#user-journey).
- Private or self-censored behaviour: [Cultural probes](../reference/methods-discovery#cultural-probes).

**Ideation, designing a response.**

- Empty solution space: [Brainstorming](../reference/methods-ideation#brainstorming), [Brainwriting](../reference/methods-ideation#brainwriting).
- Seed idea too thin to prototype: [Idea tower](../reference/methods-ideation#idea-tower).
- Repeating the same variants: [Inspiration cards](../reference/methods-ideation#inspiration-cards).
- Cannot explain why users would switch: [Jobs to be done](../reference/methods-ideation#jobs-to-be-done).
- Team too close to the product: [Kill your company](../reference/methods-ideation#kill-your-company).
- Too many ideas, no shortlist: [Idea clustering and selection](../reference/methods-ideation#idea-clustering-and-selection).
- Genuine technical contradiction: [TRIZ](../reference/methods-ideation#triz).

**Validation, testing whether it is worth building.**

- A risky flow needs user feedback: [Wireframes, storyboards, and paper prototypes](../reference/methods-validation#wireframes-storyboards-and-paper-prototypes).
- Expensive feature, unclear demand: [Wizard of Oz](../reference/methods-validation#wizard-of-oz).
- Visual direction unclear: [Appearance prototype](../reference/methods-validation#appearance-prototype).
- Environment matters more than the product: [Context and system prototypes](../reference/methods-validation#context-and-system-prototypes).
- Feasibility question: [Expert review](../reference/methods-validation#expert-review).
- Business model unclear: [Business plan](../reference/methods-validation#business-plan).
- Multiple competing VPs: [Value proposition quantification](../reference/methods-validation#value-proposition-quantification).
- Team too optimistic: [Pre-mortem](../reference/methods-validation#pre-mortem).
- Menu or taxonomy confuses users: [Card sorting](../reference/methods-validation#card-sorting).

## The interview discipline

A few rules that the skill follows consistently across every session.

### Co-creation, not autonomous generation

The agent proposes drafts and you confirm. A typical exchange:

> "Here is a persona sketch based on what you just told me: [draft]. Does this fit your real users, or does it need adjustment?"

If you wanted autonomous generation, you would get a plausible BA that reads well and fails silently. Co-creation is the point.

### Ask before you ask

Before asking you about users, markets, or competitors, the agent checks whether you already have that data. Existing interviews, customer support logs, CRM exports, prior research. If you have it, the agent ingests it. If not, the agent proposes a method and you go into the field.

### Probing when answers get thin

When your answers become generic, the agent reaches for a handful of probing techniques.

- 5-Why. Ask "why is that a problem" until you hit something surprising.
- Concretisation. "Give me a concrete example." "When did this last happen?"
- Future projection. "Imagine the problem was solved tomorrow. What changes?"
- Perspective shift. "What would your customer or your boss say?"
- Emotional level. "How did that feel?"
- Analogy trigger. "Do you know something similar from another domain?"

These are the same probes the field methods use. They work in both directions: you use them on the users during field work, the agent uses them on you during the session.

## The bridge out of Exploration: Point of View and HMW

Once Exploration fills up, the agent synthesises a **Point of View** statement. The canonical form:

> [User, descriptive] needs/wants/has to [verb describing the need] because/but [insight that reframes the problem].

Example:

> Harriet, a mother of three rushing through the airport, needs a way to entertain her children because she feels uncomfortable when they disturb other passengers.

A good POV is specific about the user, verb-driven in the need, and insightful in the because. You spend more time on this one sentence than you expect, and it earns the time back in Ideation.

The POV then becomes a **How Might We** question that opens a solution space. The agent drafts three or four HMW variants from the same POV, each steering ideation in a different direction. You pick one and Ideation starts from there.

## The bridge out of Ideation: Value Proposition and Critical Hypotheses

Ideation closes with a Value Proposition and a set of Critical Hypotheses. Every hypothesis is written in the test-card form:

> We believe that [assumption]. To verify that, we will [method]. We will measure [indicator]. We are right if [threshold].

These hypotheses become the validation agenda. The agent prioritises them by risk, not by ease. The hypothesis that would kill the idea if wrong gets tested first.

## Quality gates

Before the skill hands off to Requirements Engineering, it checks quality gates adapted to scope.

| Scope | Gate threshold |
|---|---|
| Simple Test | At least 3 of 4 criteria (problem, user, functionality, DoD) |
| PoC | At least 6 of 8 criteria (HMW, hypothesis, persona, risks and more) |
| MVP | At least 10 of 13 criteria (full Exploration board, two or more personas, and so on) |

If a gate fails, the skill returns to the relevant section instead of handing off a half-finished BA. See [Verification Gates](../concepts/verification-gates) for the full mechanic.

## BA layers: Project-BA and Item-BA

A real project does not collapse into one Business Analysis. The BA
is a two-layer artifact that lives entirely in `_devprocess/analysis/`.
Item-BAs feed the corresponding EPIC / FEAT / IMP / FIX artefact via a
`ba-ref:` in the artefact frontmatter. They are NOT siblings of the
backlog item.

- **Project-BA** (`BA-{PROJECT}.md`) is the singleton product layer.
  Personas, value dimensions, nordstern, project-wide constraints
  and KPIs. Created once, referenced by every Item-BA.
- **Item-BA** is one BA per new backlog item that needs discovery
  depth. The file name carries the target id:

  | Item type | BA file (in `analysis/`) | Promoted to | Required? |
  |-----------|--------------------------|-------------|-----------|
  | Epic | `BA-EPIC-{nn}-{slug}.md` | `requirements/epics/EPIC-{nn}-{slug}.md` | yes |
  | Feature | `BA-FEAT-{ee}-{ff}-{slug}.md` | `requirements/features/FEAT-{ee}-{ff}-{slug}.md` | yes |
  | Improvement | `BA-IMP-{ee}-{ff}-{nn}-{slug}.md` | `requirements/improvements/IMP-{ee}-{ff}-{nn}-{slug}.md` | optional |
  | Fix | `BA-FIX-{ee}-{ff}-{nn}-{slug}.md` | `requirements/fixes/FIX-{ee}-{ff}-{nn}-{slug}.md` | optional |

The Item-BA's id matches the future backlog item's id. When
`/requirements-engineering` (or `/coding` for FIX) promotes the
artefact, it writes `ba-ref:` into the EPIC/FEAT/IMP/FIX frontmatter
pointing at the BA file. The BA stays in `analysis/` as audit trail
and is never inlined into the backlog artefact.

**Inheritance.** Item-BA frontmatter carries `project-ba-ref:`
pointing at the Project-BA (or `null` for single-item projects).
Personas are referenced by ID, never redefined. KPIs map upward via
`project-kpi-ref:`. The same invariants live in
`skills/project-conventions/references/graph-invariants.md` (N-8
and N-9).

**Templates:**

- Full discovery (Project-BA, EPIC and FEAT Item-BAs):
  `templates/BA-TEMPLATE.md`
- Mini discovery (IMP and FIX Item-BAs, capped at 80 lines):
  `templates/BA-MINI-TEMPLATE.md`

**Scope mapping per item type:**

| BA type | Default scope | Sections used |
|---------|---------------|---------------|
| Project-BA | PoC or MVP | full template |
| BA-EPIC | PoC or MVP | full template |
| BA-FEAT | Simple Test or PoC | reduced (1, 4, 5, 7, 8) |
| BA-IMP | Simple Test | mini template |
| BA-FIX | Simple Test | mini template |

Long research raw material lives in `BA-{PROJECT}-v{N}-full.md`
archives, not in the active Project-BA.

## Handoff

`/business-analysis` ends with the mandatory four-part
[Handoff Ritual](../concepts/handoff-rituals):

1. Artifact report. Which sections filled, which deferred, which
   hypotheses still open.
2. Handoff context entry in `_devprocess/context/HANDOFFS.md`.
3. Phase-end commit (`chore(ba): {ITEM-ID} BA complete`) plus
   `tag-phase --phase ba`.
4. Transition question. "Shall I start `/requirements-engineering`
   now?"

The guide runs `/consistency-check` Mode A on the changed
artifacts at the boundary.

## Phase 8: Post-Release Review (BA as living document)

The BA is not done when the first release ships. Once a feature is in
front of real users, the Critical Hypotheses formulated in Ideation
become testable against actual usage.

Phase 8 walks each Critical Hypothesis and classifies it against
real-world evidence:

- **Confirmed by usage**: the hypothesis held up. The metric in the
  test card was met or exceeded.
- **Contradicted by usage**: the hypothesis was wrong. The data tells
  a different story. A backlog entry is created so the team can react
  (pivot the feature, change the value proposition, drop it).
- **Inconclusive**: not enough data yet, or the metric is ambiguous.
  Stays open, gets re-reviewed at the next release.

The hypothesis status is also written to
`_devprocess/context/METRICS.md` so the signal layer accumulates a
trace of what the team predicted versus what actually happened.

Phase 8 is queued automatically. `/dia-guide` the Closing Handoff (
Closure) appends a `release-to-ba` entry to `HANDOFFS.md`. The
next time `/business-analysis` runs, it picks up that handoff and runs
Phase 8 before any new exploration work.

This closes the BA-to-release loop. The BA file ages with the product
instead of becoming a stale document from the first sprint.

## Validation Mode for brownfield projects

When `/business-analysis` detects a BA draft created by [`/reverse-engineering`](./reverse-engineering), it enters Validation Mode. Instead of starting a new interview from scratch, it walks through each section of the existing draft, confirms the evidence-backed claims with you, and fills the `[NEEDS USER INPUT]` placeholders through the normal interview cycle. Each section gets promoted from `Draft` to `Validated` as you confirm it.

This is how the backward walk through the V joins the forward walk. Same file, same path, same downstream phases.

## Read the skill file

Want to see the exact instructions the agent follows? [`skills/business-analysis/SKILL.md`](https://github.com/pssah4/digital-innovation-agents/blob/main/skills/business-analysis/SKILL.md) on GitHub. The method catalog the agent draws from lives at [`skills/business-analysis/references/innovation-methods.md`](https://github.com/pssah4/digital-innovation-agents/blob/main/skills/business-analysis/references/innovation-methods.md).

## Further reading

- [Discovery methods](../reference/methods-discovery), [Ideation methods](../reference/methods-ideation), [Validation methods](../reference/methods-validation). The full method cards the agent references during the dialog.
- [Your first Business Analysis tutorial](../tutorials/first-business-analysis).
- [Requirements Engineering](./requirements-engineering). The next phase.
- [Tech-agnostic Requirements](../concepts/tech-agnostic-requirements). Why the BA must stay free of technology vocabulary.
