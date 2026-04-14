---
title: The Digital Innovation Playbook heritage
description: Where the BA / RE / Architecture methodology comes from — Dark Horse Innovation's Digital Innovation Playbook, etventure's innovation framework, Strategyzer, Design Thinking, and Lean Startup.
---

# The Digital Innovation Playbook heritage

The left side of the V-Model in this skill set — Business Analysis,
Requirements Engineering, Architecture — is not invented from
scratch. It is a specific adaptation of an established,
battle-tested methodology for a new medium: the one-on-one
conversation between a human and an AI coding agent. This page
traces the heritage so you know what you are standing on and where
to go if you want to dig deeper.

## The primary source: Dark Horse Innovation's Digital Innovation Playbook

The **Digital Innovation Playbook** (Dark Horse Innovation, Murmann
Verlag, multiple German editions) is a 600-page, open-licensed
toolkit for running digital innovation projects end-to-end. It
describes a six-module innovation process — Frame, Explore, Create,
Evaluate, PoC, MVP — with several hundred methods, canvases, and
templates that teams can mix and match.

The book is the single largest source of methods used in
[`/business-analyse`](../guides/business-analyse). Specifically:

- The three-phase **Explore → Create → Evaluate** cycle
- The **Digital Innovation Board** canvas structure (users, needs,
  insights, touchpoints, idea potential, value proposition, etc.)
- The **Assessment Radar** (Brand Fit, Investment, Market Size,
  Asset Fit, Viral Potential, New Customer)
- The **Value Proposition Score** (activation, preference,
  willingness to pay, recommendation)
- The staged depth model (Simple Test → PoC → MVP) that every
  skill's scope adaptation descends from

::: info Licensing
The Digital Innovation Playbook is published under Creative Commons
(CC BY-SA) and its templates are explicitly designed to be reused,
adapted, and integrated into other workflows — which is exactly
what this skill set does. Full book:
[digital-innovation-playbook.de](https://digital-innovation-playbook.de).
:::

## The secondary source: etventure's innovation framework

Dark Horse's playbook is complemented in this skill set by the
**etventure Innovation Framework** — specifically the set of
one-page method cards ("methoden-onepagers") that document
individual techniques in a tight, practitioner-ready format. Many
of the method excursions in the
[Business Analysis guide](../guides/business-analyse) are directly
derived from these one-pagers:

- **Explorative Interviews** — the 2-person, transcribe-don't-interpret
  discipline
- **Observation** — open, hidden, shadowing
- **Immersion** — stepping into the user's shoes first-hand
- **Persona** — built from interview synthesis, not imagination
- **Point of View** — the `User / Need / Insight` sentence template
- **How Might We** — POV reframed as open question
- **Stakeholder Mapping** — influence / power grids
- **Classic Brainstorming** — with the 11 Design Thinking rules
- **Idea Canvas** — compact single-page idea summary
- **Prototype** (low-res to high-res)
- **Feedback Grid** — What worked / Could be improved / Questions /
  Ideas / Conclusion
- **Landing Page Test** — fastest real-market hypothesis test

The etventure framework itself sits inside a wider workflow —
Setup & Kick Off → Market & Client Discovery → Exploration &
Ideation → Prototype Test & Validation → Business Proposal → MVP
Marktstart → Roll Out — which is another version of the same
innovation backbone the V-Model's left side implements.

## The tertiary sources: Strategyzer, Design Thinking, Lean Startup

Woven through both of the above are the classic innovation-method
sources most developers have brushed up against at some point:

### Strategyzer

- **Business Model Canvas** (Osterwalder, Pigneur) — the nine-block
  business model visualisation
- **Value Proposition Canvas** — the Customer Profile / Value Map
  fit test used in
  [Business Analysis](../guides/business-analyse#excursion-value-proposition-canvas-strategyzer)
- **Test Card** and **Learning Card** — the hypothesis-testing
  templates used in the
  [Critical Hypotheses section](../guides/business-analyse#excursion-critical-hypotheses-and-the-test-card)
  of the BA and in the Benefits Hypothesis block of every Feature
  in [Requirements Engineering](../guides/requirements-engineering#excursion-benefits-hypothesis-not-description)

### Design Thinking (IDEO / Stanford d.school)

- The **Empathise → Define → Ideate → Prototype → Test** loop
- The **11 rules of brainstorming** that govern every ideation
  session
- The **human-centred design** principle — every artifact traces
  back to a real person with a real need

### Lean Startup (Eric Ries)

- **Build-Measure-Learn** as the tight iteration loop for
  hypothesis testing
- **Minimum Viable Product** as the smallest thing that can teach
  you something real
- **Pivot** as a legitimate outcome of validation, not a failure
- **Innovation Accounting** — treating learning as a measurable
  output of experimentation

### Jobs to be Done (Christensen, Ulwick)

- The **functional / emotional / social** layering of user needs
  that drives the three-story pattern in
  [Requirements Engineering](../guides/requirements-engineering#excursion-user-stories-with-three-levels-of-need)
- The "hire a product to do a job" metaphor that reframes features
  as service relationships rather than feature checklists

## How the heritage maps onto the skill set

| Playbook module / concept | Skill / phase | Where it shows up |
|---|---|---|
| Frame (setup, stakeholders, team, milestones) | `/business-analyse` (pre-Exploration) | Scope selection, stakeholder mapping |
| Explore | `/business-analyse` Phase 1 | Users, needs, insights, touchpoints, trends |
| Create | `/business-analyse` Phase 2 | Idea description, VP, Wow, high-level concept |
| Evaluate | `/business-analyse` Phase 3 | Hypotheses, VP score, assessment radar |
| PoC | `/requirements-engineering` + `/architecture` + `/coding` | Small-scope variant of the full V |
| MVP | Full V-Model run | Largest scope, full rigor |
| Explorative Interviews, Observation, Immersion, Stakeholder Map | BA methodology excursions | 20+ method references |
| Persona, POV, HMW | BA bridge sections | Output of Explore, input of Create |
| Idea Canvas, VP Canvas | BA Create phase | Condensation step before Evaluate |
| Test Card, Learning Card | BA Evaluate + RE Benefits Hypothesis | Critical Hypotheses + Feature justification |
| Assessment Radar | BA Evaluate | Viability scoring |
| Build-Measure-Learn | Living documents + `/coding` loop | Verification Gates + iteration |

## What has been adapted, and why

The Digital Innovation Playbook assumes a **workshop setting**: a
room of 4–8 people, Post-its, flipcharts, several hours of facilitated
conversation. This skill set runs the same methodology in a
fundamentally different medium — **a 1:1 interview with an AI coding
agent**, often asynchronously, often in short sessions.

The adaptations:

1. **Co-creation replaces group divergence.** The agent proposes
   drafts and the user confirms; there is no "vote with three dot
   stickers" step, because there is only one voter.

2. **Transcription replaces note-taking.** Because the conversation
   is text-based, every response is already captured. The interview
   discipline shifts from "transcribe accurately" to "probe
   persistently."

3. **Scope tiers replace workshop length.** Instead of "full-day
   workshop vs. half-day workshop," the tiers are Simple Test / PoC /
   MVP, scaled to match the weight of the question.

4. **Evidence rules replace facilitator judgement.** In a workshop,
   a facilitator decides when an insight is strong enough to be
   carried forward. In a 1:1 AI session, explicit evidence rules
   replace facilitator judgement — which is why
   [`/reverse-engineering`](../guides/reverse-engineering) refuses
   to invent personas from route names and why every Critical
   Hypothesis carries a Test Card structure.

5. **Living documents replace whiteboards.** The Digital Innovation
   Board is a physical A3 canvas in the Playbook; here it becomes
   `EXPLORE-{PROJECT}.md`, version-controlled alongside the code,
   evolving with the project instead of being photographed and
   archived at the end of the workshop.

6. **Handoff rituals replace demo days.** The Playbook uses formal
   handoffs between teams; the skill set uses
   [Handoff Rituals](./handoff-rituals) between phases, each
   producing a structured context file for the next phase's agent.

## Further reading

### Primary sources (books)

- Dark Horse Innovation, *Digital Innovation Playbook*, Murmann
  Verlag. Book site:
  [digital-innovation-playbook.de](https://digital-innovation-playbook.de)
- Osterwalder, Pigneur, *Business Model Generation*, Wiley
- Osterwalder et al., *Value Proposition Design*, Wiley
- Eric Ries, *The Lean Startup*, Crown Business
- Tim Brown, *Change by Design*, HarperBusiness (Design Thinking)
- Clayton Christensen, *Competing Against Luck* (Jobs to be Done)

### Templates and canvases

- [Strategyzer canvases](https://www.strategyzer.com/library/) — Test Card,
  Learning Card, Business Model Canvas, Value Proposition Canvas
- [arc42 templates](https://arc42.org/download) — used in
  `/architecture`
- [MADR](https://adr.github.io/madr/) — the ADR format used by
  `/architecture`

### Where this skill set lives

- [Business Analysis guide](../guides/business-analyse) — the
  primary home of the Playbook methodology
- [Requirements Engineering guide](../guides/requirements-engineering) —
  Jobs to be Done + Learning Card structure
- [Architecture guide](../guides/architecture) — MADR + arc42
- [Reverse Engineering guide](../guides/reverse-engineering) —
  brownfield entry that produces the same artifacts from existing
  code
