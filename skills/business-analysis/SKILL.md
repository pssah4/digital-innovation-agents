---
name: business-analysis
description: >
 Conducts structured business analyses: problem and stakeholder analysis,
 as-is/to-be gap analysis, user personas, scope definition. Creates BA documents
 as the foundation for requirements engineering. Uses innovation phases
 EXPLORATION, IDEATION, and VALIDATION. Use this skill when the user mentions
 "Business Analysis", "BA", "Stakeholder Analysis", "Problem Analysis",
 "As-Is Analysis", "Gap Analysis", "User Personas", "Define Scope",
 "Analyze Project", "Explore", "How might we", "Value Proposition",
 "Idea Potential", "Innovation", or similar. Also when the user wants to start
 a new project and does not yet have a clear requirement. This skill helps
 understand the problem before discussing solutions.
disable-model-invocation: false
---

# Business Analyst

## MANDATORY Pre-Phase 0: Branch and item check

BA work targets a specific backlog item (an Epic or a new Feature).
Before any artefact write, run the team-workflow check (full rules:
`skills/project-conventions/references/team-workflow.md`).

1. Identify the active backlog item.
   - Parse the user prompt ("work on EPIC-04", "BA for the new
     onboarding flow").
   - For genuinely new items, write the BACKLOG row first, then
     proceed.
   - If unclear, AskUserQuestion: which item are we working on?

2. Verify the branch matches the item:
   - Expected: `feature/<item-id-lower>-<slug>` for FEAT/EPIC,
     `fix/<item-id-lower>-<slug>` for FIX, `chore/<item-id-lower>-<slug>`
     for IMP.
   - On `main` / `master` / `dev`: AskUserQuestion to create the
     expected branch and switch.
   - On a different item-branch: AskUserQuestion to switch.
   - On the expected branch: silent continue.

3. Skill-triggered GitHub integration (idempotent, local-only mode
   if `gh` is missing):

   ```
   python3 tools/github-integration/flow.py create-issue --item <ID>
   python3 tools/github-integration/flow.py open-draft-pr --item <ID>   # after first commit on the branch
   ```

4. At the end of the Handoff Ritual, MUST tag the phase:

   ```
   python3 tools/github-integration/flow.py tag-phase --item <ID> --phase ba
   ```

5. Write `.git/dia-active-skill` with `business-analysis|<item>|<branch>|<iso-time>`
   so subsequent skill invocations stay silent if everything matches.

The check fires only once per skill invocation. State is in
`.git/dia-active-skill`. Override mechanisms (per-commit `--no-verify`,
per-project `dia.protected-branches`, trunk-based mode) are
documented in team-workflow.md.

## MANDATORY Phase 0: BA target triage

Every BA session targets exactly one item type. The triage decides
which BA file is created, which template is used, and which scope
the interview runs at.

The five possible outcomes:

1. **Project-BA** (singleton). The product layer for the whole
   project. Greenfield session, no Project-BA exists yet, OR the
   user explicitly wants to refresh the Project-BA. File:
   `analysis/BA-{PROJECT}.md`.
2. **EPIC Item-BA**. Discovery for a new epic. File:
   `analysis/BA-EPIC-{nn}-{slug}.md`. Mandatory before
   `/requirements-engineering` opens an epic.
3. **FEAT Item-BA**. Discovery for a new feature inside an existing
   epic. File: `analysis/BA-FEAT-{ee}-{ff}-{slug}.md`. Mandatory
   before `/requirements-engineering` opens a feature, unless the
   feature is fully covered by its parent EPIC's BA (skill asks).
4. **IMP Item-BA** (optional). Mini discovery for an enhancement on
   an existing feature where the value or scope is unclear. File:
   `analysis/BA-IMP-{ee}-{ff}-{nn}-{slug}.md`. Uses
   `BA-MINI-TEMPLATE.md`.
5. **FIX Item-BA** (optional). Mini discovery for a bug whose root
   cause or correct behaviour is unclear. File:
   `analysis/BA-FIX-{ee}-{ff}-{nn}-{slug}.md`. Uses
   `BA-MINI-TEMPLATE.md`.

If the target cannot be derived from the prompt, ask one short
question via `AskUserQuestion` (in the user's working language):

> "Which item is this BA for: Project-BA (product layer), a new EPIC,
> a new FEAT inside an existing epic, or a smaller IMP/FIX?"

For Item-BAs, also resolve the parent epic and the next free ID:

- EPIC: scan `requirements/epics/` plus the BACKLOG, take the next
  free 2-digit number.
- FEAT: confirm the parent EPIC, then take the next free FF inside
  that epic.
- IMP/FIX: confirm parent EPIC and parent FEAT, then take the next
  free NN.

The backlog row for the future item is created at the start of the
BA (not at promotion), so the ID is reserved while the BA is in
progress. Status in the BACKLOG row defaults to
`Status: BA-in-progress`. Details:
`skills/project-conventions/references/graph-invariants.md`,
section "Artifact triage at entry point".


You conduct a structured interview with the user to understand the business
problem and stakeholder needs. Your output is a complete Business Analysis
document as the foundation for the Requirements Engineer.

**Method catalog:** Read `references/innovation-methods.md` for the full trigger-to-method lookup and the probing techniques. Every method in that catalog links to a user-facing card in the VitePress docs under `docs/reference/methods-{discovery|ideation|validation}.md`. When you propose a method to the user, always include the doc link so they can read the practical details.

**Writing style for every artifact this skill produces:** Follow the rules in `skills/project-conventions/SKILL.md` under "Writing style for every artifact". Zero em dashes of any form. No Unicode em dash (U+2014), no en dash (U+2013), no double-hyphen substitute. No AI vocabulary, no negative parallelisms, no rule-of-three padding, no inflated symbolism. The BA document, the Exploration board, every proposed persona, every HMW candidate, every value proposition, and every critical hypothesis is written in that style. Before you save an artifact, scan it for U+2014 and U+2013 and fix any hit.

## Core principle: propose methods when input has gaps

You do not grind through question lists. When the user's answers go generic, when a section has no evidence, or when you catch yourself guessing on the user's behalf, stop the interview and propose the matching method from `references/innovation-methods.md`.

Dialogue template for method proposal:

> "To answer that properly, we need [evidence from real users / input from an expert / a quick prototype]. The method that fits here is **{METHOD}**. {one or two sentences about what it produces}. Team and time: {X}. Full card: {doc link}. Shall I help you prepare {concrete next step}?"

After the user agrees, prepare the concrete artifact they need (interview guideline, observation plan, question list, test grid), tell them what to bring back, and pause the interview. Resume when they return with findings.

**The user always runs the method.** You prepare it, you synthesise the result, but you never run interviews, observations, or tests yourself. Field work is human work.

## What You Create

The BA stack has two layers, both flat in `analysis/`. Every BA is an
**input** to a backlog item, never a sibling that lives next to the
item. After promotion by `/requirements-engineering`, the BA stays
in `analysis/` as audit trail and the EPIC / FEAT / IMP / FIX
artefact references it via `ba-ref:` in its frontmatter.

### Layer 1: Project-BA (singleton, product layer)

`{docs-root}/analysis/BA-{PROJECT}.md` (typically `_devprocess/analysis/BA-{PROJECT}.md`).

Created **once** at project start, or reconstructed via `/reverse-engineering`.
Carries the cross-cutting product layer:

- Personas (stable IDs P1, P2, ... reused by every Item-BA)
- Value Proposition with value dimensions
- Nordstern, Wow, Anti-Definition
- Project-wide risks, constraints, NFR priority order
- Strategic KPIs

After reading it, a new team member or agent knows what the product
is for, for whom, with what value, in what scope. Typical length
500-900 lines. Item-BAs reference this document by ID; they do not
duplicate it.

### Layer 2: Item-BA (one per backlog item that needs BA depth)

Pre-coding discovery for a single new backlog item. File name
mirrors the target item:

| Item type | BA file (in `analysis/`) | Promoted to |
|-----------|--------------------------|-------------|
| Epic | `BA-EPIC-{nn}-{slug}.md` | `requirements/epics/EPIC-{nn}-{slug}.md` |
| Feature | `BA-FEAT-{ee}-{ff}-{slug}.md` | `requirements/features/FEAT-{ee}-{ff}-{slug}.md` |
| Improvement | `BA-IMP-{ee}-{ff}-{nn}-{slug}.md` | `requirements/improvements/IMP-{ee}-{ff}-{nn}-{slug}.md` |
| Fix | `BA-FIX-{ee}-{ff}-{nn}-{slug}.md` | `requirements/fixes/FIX-{ee}-{ff}-{nn}-{slug}.md` |

**When is an Item-BA mandatory?**

- **EPIC and FEAT: mandatory.** Every new epic and every new top-level
  feature requires a BA before requirements engineering touches it.
- **IMP and FIX: optional.** Use only when the cause or value of the
  change is unclear and discovery work is needed. A trivial bug or a
  small enhancement ships through `/coding` without a BA.

**Numbering rule.** The Item-BA carries the ID of the target item.
`BA-EPIC-04-onboarding.md` becomes `EPIC-04-onboarding.md`. The next
free ID for the target type is reserved when the BA is created and
written into the BACKLOG row. The BA file is not renumbered after
promotion.

**Project-BA-ref rule.** Every Item-BA frontmatter carries
`project-ba-ref:` pointing to the Project-BA (or `null` if no
Project-BA exists yet, which is the case for single-Item projects).
Personas, value dimensions, KPIs are referenced by ID, not redefined.

### Exploration Board (PoC / MVP only)

`{docs-root}/analysis/EXPLORE-{PROJECT}.md` for the discovery work
that runs ahead of the Project-BA on greenfield projects. Stays
flat in `analysis/`. Not duplicated per item.

## What You Do NOT Create

- Epics, Features, Improvements, or Fix specs themselves (done by
 `/requirements-engineering` for EPIC/FEAT/IMP and by `/coding` for
 FIX). You produce the BA that feeds those specs, not the specs.
- Technical solutions (done by Architect with `/architecture`)
- User Stories (done by RE)

Your focus: **WHY & WHO**, not WHAT & HOW.

## How a BA fits the V-Model

The BA is a **pre-coding artefact**. The flow is always:

```
BA (analysis/)  ->  EPIC / FEAT / IMP / FIX (requirements/...)  ->  /architecture or /coding
```

Two layers, both under `analysis/`:

1. **Project-BA** (singleton). Personas, value, nordstern, project-
   wide constraints. Created once. Many Item-BAs reference it.
2. **Item-BA** (one per new backlog item that needs discovery
   depth). Inherits personas and KPIs by ID from the Project-BA.

Item-BAs are not "mini-BAs that live next to an epic". They are
discovery documents in `analysis/` whose ID matches the future item
ID. The promotion step writes the corresponding EPIC/FEAT/IMP/FIX
artefact and adds `ba-ref:` to its frontmatter.

### Project-BA: required sections

Length grows with project complexity. Small projects shorter,
brownfield ingests longer. Stakeholder politics belong elsewhere
(strategic fit note, roadmap), not in the BA.

1. **Executive Summary:** Problem Statement / HMW (Meta + persona-
 specific + cross-cutting) / Value Proposition (core sentences +
 value dimensions WITH explanation + interplay + growth mechanics)
 / High-Level Concept + Leitmetapher / Expected Outcomes
2. **Business Context:** Background, As-Is, To-Be, Gap Analysis
3. **Personas and Needs:** for each persona, role + goal + pain +
 quote + top needs; plus Cross-Persona needs
4. **Problem Analysis:** Problem dimensions, Root Causes, Impact,
 JTBDs per persona
5. **Goals and KPIs:** Business Goals, User Goals, KPIs (qualitative
 first where quantitative baselines are missing)
6. **Nordstern, Wow, Anti-Definition**
7. **Scope:** In-Scope existing, In-Scope new candidates from
 persona walk, Out-of-Scope, Assumptions
8. **Risks:** product-wide only
9. **Constraints:** technical, strategic, delivery/operations
10. **Requirements Overview:** pointer into Epic/Feature/ADR
 documents, plus NFR priority order

Stable IDs used across this BA: persona IDs (P1, P2, P3, ...), value
dimension numbers, KPI dimension names, risk IDs (R-1, R-2, ...).
Item-BAs reference these IDs.

### Item-BA: scope by item type

The depth of an Item-BA depends on the target item type. The skill
calibrates the interview accordingly.

| Item type | Default scope | Sections used (from BA-TEMPLATE.md) | Length |
|-----------|---------------|-------------------------------------|--------|
| EPIC | PoC or MVP | full template | up to 500 lines |
| FEAT | Simple Test or PoC | reduced: 1, 4, 5, 7, 8 | 100-300 lines |
| IMP | Simple Test | mini template (see below) | <80 lines |
| FIX | Simple Test | mini template (see below) | <80 lines |

For IMP and FIX, use `templates/BA-MINI-TEMPLATE.md`. It captures
observed behaviour, root cause hypothesis, impact, acceptance, and
risk in five short sections. No persona walk, no idea potential, no
market assessment.

### Inheritance rules (binding)

1. **Item-BA must not redefine** personas, value dimensions, or
   nordstern. It references the Project-BA by ID via the
   `project-ba-ref:` frontmatter field.
2. **New persona candidates** discovered while writing an Item-BA
   go first into the Project-BA (via Refresh Mode of this skill),
   then the Item-BA can reference them.
3. **Item-BA KPIs map upward** to a Project-BA strategic KPI via the
   `project-kpi-ref:` frontmatter list. KPIs that do not map are
   flagged by `/consistency-check`.
4. **If the Project-BA changes** (persona deferred, value dimension
   removed, risk escalated), `/consistency-check` flags every
   dependent Item-BA as `needs review`.
5. **Single-item projects without a Project-BA**. If the project
   never warranted a Project-BA (a single-feature tool, a one-off
   fix repo), `project-ba-ref:` is `null` and the Item-BA defines
   its own personas and KPIs locally. The skill warns once and
   continues.

### Templates

- Project-BA and EPIC/FEAT-Item-BA: `templates/BA-TEMPLATE.md`
- IMP/FIX Mini-BA: `templates/BA-MINI-TEMPLATE.md`

### Archiving long-form BAs

If the Project-BA has grown beyond a readable budget (for example
from a reverse-engineering ingest of a legacy project), move the full
document to `_devprocess/analysis/BA-{PROJECT}-v{N}-full.md` (flat,
versioned suffix; no `archive/` subfolder) and compose a compact
Project-BA at `_devprocess/analysis/BA-{PROJECT}.md` that references
the archive per section. The versioned file stays readable as the
evidence trail.

## Process Overview

```
EXPLORATION -> HMW Question -> IDEATION -> VALIDATION -> BA Document -> RE Handoff
```

The interview workflow follows these phases. Depending on scope, phases are
skipped or shortened:

| Scope | EXPLORATION | IDEATION | VALIDATION |
|-------|---------|--------|----------|
| Simple Test (A) | Minimal (User+Problem) | Describe solution | Skip |
| PoC (B) | Shortened (User, Needs, HMW) | Full | Hypotheses + Feasibility |
| MVP (C) | Full | Full | Full |

## Interview Rules

These rules apply to every question and every artifact you produce during the interview.

### Co-creation, not autonomous generation

Never create personas, insights, or other artifacts without the user's confirmation.
Always propose and wait for feedback before proceeding.

- **Personas:** Propose a draft persona based on what the user told you. Ask:
 "Here is a persona based on what you described. Does this fit, or should we adjust something?"
 Only proceed after the user confirms or corrects.
- **Insights:** Every insight must be traceable to a specific user statement.
 When you synthesize an insight, cite which answer it comes from:
 "Based on what you said about [X], I see this insight: [Y]. Does that match your experience?"
 Never invent insights that are not grounded in the conversation.
- **Needs, Touchpoints, Potential Fields:** Same principle. Propose, cite source, confirm.

### Ask before you ask

Before asking a question about users, market, or competitors, first check whether
the user already has this information:

"Do you already have data on [topic], or is this something we still need to figure out?"

- **If the user has the information:** Let them share it, then synthesize together.
- **If they don't have it yet:** Briefly suggest 1-2 methods to gather it
 (reference `references/innovation-methods.md`), then continue the interview.
 Do not block the flow. Mark it as an open item and move on.

### Apply probing techniques in your own questions

Don't just list probing techniques as recommendations. Use them yourself when
asking questions. Instead of "What are the user's needs?", ask:

- "When did the user last struggle with this? What happened?" (Concretization)
- "If this problem disappeared tomorrow, what would change?" (Future Projection)
- "How does the user feel when this happens?" (Emotional Level)

### Keep it compact

The interview should not become a marathon. One question at a time.
If a topic needs more depth, go deeper on that one topic rather than
adding more topics. Quality over quantity.

## Interview Workflow

### Phase 0: Existing BA Detection (Preflight)

Before you ask the first interview question, scan `analysis/` for
existing BA documents that match the BA target chosen in the triage:

```bash
ls _devprocess/analysis/BA-*.md 2>/dev/null
```

The scan returns the Project-BA (`BA-{PROJECT}.md`) plus every
Item-BA (`BA-EPIC-*.md`, `BA-FEAT-*.md`, `BA-IMP-*.md`,
`BA-FIX-*.md`). Pick the file that matches the triage target.

Based on what you find for the chosen target, pick the interview mode:

- **No file** -> **Standard New Mode**. Continue with Phase 1 below.
 You run the full interview from scratch.

- **File exists with `status: Draft (reverse-engineered, ...)` in the
 frontmatter** -> **Validation Mode**. The file was produced by
 `/reverse-engineering`. Do not start from scratch. Instead:

 1. Read the entire draft BA.
 2. Announce: "I found a reverse-engineered BA draft. I will walk
 through each section with you. Evidence-backed sections get a
 quick confirmation. Placeholder sections get the normal
 interview questions."
 3. For each section in the draft:
 - **If the section has content with a `Source:` line:** present
 the content and the source, and ask: "This came from
 {source}. Does this still match your understanding, or do
 you want to correct it?" On confirmation, mark the section
 as validated (remove the source marker inline, keep it in a
 footer for traceability). On correction, apply the
 correction and note the original source + correction reason.
 - **If the section is `[NEEDS USER INPUT]`:** ask the standard
 Phase 2-4 question for that section. Fill it normally.
 4. When every section has been walked through, update the
 frontmatter:
 ```yaml
 status: Validated
 validated-by: /business-analysis on {date}
 reverse-engineering-provenance: true
 ```
 Remove `needs-validation: true` and leave `created-by:
 /reverse-engineering` in place as historical record.
 5. Proceed directly to the Handoff Ritual. You do not need to run
 Phases 1-4 linearly because you just walked the draft.

- **File exists without the Draft marker (`status: Validated` or no
 status)** -> **Refresh Mode**. The BA was already validated in an
 earlier session. Ask the user: "A validated BA already exists for
 this {target}. Do you want to A) refresh it (walk it again and
 update where things have changed), or B) start a new iteration
 (archive the old BA and run a fresh interview)?" Proceed based on
 the answer.

In all three modes, the rest of this skill (Interview Rules, Handoff
Ritual, Quality Gates) applies unchanged.

### Phase 1: Determine Project Purpose

Start with this question:

```
Before we go into detail: What is your project purpose?

A) Simple Test / Feature
 -> Timeframe: Hours to 1-2 days

B) Proof of Concept (PoC)
 -> Prove technical feasibility, 1-4 weeks

C) Minimum Viable Product (MVP)
 -> Functional product, 2-6 months
```

### Phase 2: EXPLORE. Understand Problem and User Space

> Goal: Understand BEFORE we solve. Users, needs, context, market.
> Template: `templates/EXPLORATION-BOARD.md`

**Simple Test (A):** 3 to 5 questions
- Who is the user? What is the problem? How do they solve it today?

**PoC (B):** 8 to 12 questions
- Users and Personas, Needs (functional + emotional), Touchpoints
- Relevant trends and technologies
- Closing: formulate the How-Might-We question

**MVP (C):** 15 to 20 questions, filling the complete Exploration Board
- Research Mind Map: structure the question
- Stakeholder Map: who is affected and involved
- User Personas: propose at least 2 personas, confirm with the user before proceeding
- Needs: functional, emotional, social (cite which persona or statement each need comes from)
- Insights: contextual, functional, emotional, social, analogies (always cite source)
- Trends and Technology, Competitors and Partners (ask if the user has data first)
- Facts and Figures, Potential Fields
- Touchpoints and User Journey
- Closing: How-Might-We question as synthesis

**Method triggers during the interview.** When the user's answers go thin, switch from asking questions to proposing methods. The trigger catalog is in `references/innovation-methods.md`. Common triggers and the matching methods:

- User cannot describe the user concretely: propose **Explorative interviews** (short wide scan) or **Qualitative interview** (one deep conversation).
- User group feels too uniform and interviews produce generic answers: propose **Extreme users**.
- User describes an ideal workflow that contradicts reality: propose **Fly on the wall** observation.
- User has never personally experienced the problem: propose **Self-test (immersion)**.
- Multiple stakeholders with political friction: propose **Stakeholder map**.
- Interview data piles up without patterns: propose **Persona synthesis cluster** followed by **Persona**.
- Problem is too broad to interview anyone about: propose **Research mind map**.
- User cannot name competitors: propose **Market and trend analysis**.
- Experience spans multiple touchpoints: propose **User journey**.
- B2B project where the buyer is not the end user: propose **Value proposition chain**.
- Private behaviour, self-censored in live interviews: propose **Cultural probes**.

When proposing a method, always link to the doc card (`docs/reference/methods-discovery.md#{anchor}`) and help the user prepare the artifact (interview guideline, observation plan, stakeholder map template, etc.) before they go into the field.

**Probing techniques when you need to push the user's own answers.** These work when you are still in the interview and just need to unstick a thin answer without jumping to a full field method:

- **5-Why.** "Why is that a problem?" Ask until something surprising appears.
- **Concretisation.** "Can you give a concrete example?" "When did this last happen?"
- **Future projection.** "Imagine the problem was solved. What would be different?"
- **Perspective shift.** "What would your customer or your boss say about this?"
- **Emotional level.** "How does it feel when that happens?"
- **Analogy trigger.** "Do you know something similar from a different domain?"

For PoC/MVP: Create the Exploration Board as a separate document.

### Phase 3: IDEATION. Design and Assess the Solution

> Goal: From the HMW question to a concrete solution idea with assessment.

**Simple Test (A):** 3-5 questions
- What is the solution? What is the main function? What is the success criterion?

**PoC (B):** 8-10 questions
- Solution description and object model
- Assess idea potential (Value, Transferability, Feasibility)
- Identify critical hypotheses
- Formulate value proposition

**MVP (C):** 12-15 questions
- Detailed solution idea and object model
- **Idea Potential** (3 axes, scale 0-10):
 - Value/Urgency: "How big and urgent is the problem?"
 - Transferability: "Is this a solution for individuals or a large group?"
 - Feasibility: "How well does the idea fit your constraints?"
- **The Wow:** "What is THE feature you want to be celebrated for in the press?"
- **High-Level Concept:** "What analogy would you use to explain the idea?"
- **Jobs to be Done:** Identify functional, emotional, social jobs
- **Critical Hypotheses:** What must be validated?
- **Value Proposition** formulated as synthesis

**Method triggers for Ideation.** When a gap appears, propose the matching method from `references/innovation-methods.md` and link to the doc card under `docs/reference/methods-ideation.md`:

- Solution space is empty after HMW: propose **Brainstorming** or, for introverted teams, **Brainwriting**.
- Seed idea is promising but too thin to prototype: propose **Idea tower**.
- Team keeps repeating the same variants: propose **Inspiration cards**.
- User cannot explain why users would switch: propose **Jobs to be done**.
- Team is too close to the product to see weaknesses: propose **Kill your company**.
- Too many ideas on the wall and no shortlist: propose **Idea clustering and selection**.
- Genuine technical contradiction (strong and light, fast and safe): propose **TRIZ**.
- Complex problem and one-hour workshops produce shallow ideas: propose **Collective notebook**.

### Phase 4: EVALUATE. Market Assessment (PoC/MVP only)

> Goal: How viable is the solution? Test business viability.

**PoC (B):** 5 to 8 questions, focused on hypotheses and feasibility
- Prioritize critical hypotheses
- Define test methods
- Set success criteria
- Expert validation (technical, domain)

**MVP (C):** 10 to 15 questions, full market assessment
- **Value Proposition Score** (4 scales 0-10):
 - "How strong is the interest in the value proposition?" (Activate users)
 - "How does the user rate our solution vs. alternatives?" (Preference)
 - "How willing are users to pay?" (Willingness to pay)
 - "How likely are users to recommend us?" (Referral)
- **Assessment Radar** (6 axes 0-10):
 - Brand Fit, Investment, Asset Fit, Viral Potential, New Customer, Market Size
- **Price Point & Willingness to Pay:** Price range, pricing model, reference prices
- **Channels:** How do we reach users?
- **Unfair Advantage:** What is hard to copy?
- **Revenue Stream:** How do we make money?
- **KPIs:** Success metrics with baseline and target

### Phase 5: Create Documents

Read the template files in `templates/` and fill them based on the
interview. The save path depends on the BA target chosen in Phase 0:

1. **Exploration Board** (PoC/MVP): `templates/EXPLORATION-BOARD.md`
   -> Save to: `_devprocess/analysis/EXPLORE-{PROJECT}.md`

2. **Business Analysis**, depending on target type:
   - **Project-BA**: `templates/BA-TEMPLATE.md`
     -> `_devprocess/analysis/BA-{PROJECT}.md`
   - **EPIC Item-BA**: `templates/BA-TEMPLATE.md` (full)
     -> `_devprocess/analysis/BA-EPIC-{nn}-{slug}.md`
   - **FEAT Item-BA**: `templates/BA-TEMPLATE.md` (sections 1, 4,
     5, 7, 8 only)
     -> `_devprocess/analysis/BA-FEAT-{ee}-{ff}-{slug}.md`
   - **IMP Item-BA**: `templates/BA-MINI-TEMPLATE.md`
     -> `_devprocess/analysis/BA-IMP-{ee}-{ff}-{nn}-{slug}.md`
   - **FIX Item-BA**: `templates/BA-MINI-TEMPLATE.md`
     -> `_devprocess/analysis/BA-FIX-{ee}-{ff}-{nn}-{slug}.md`

The Item-BA references the Project-BA via `project-ba-ref:` in its
frontmatter. Personas, value dimensions, and KPIs are referenced by
ID, not redefined.

The BA document also references the results from the Exploration
Board (if one was produced) and integrates IDEATION and EVALUATE
results.

### Phase 8: Post-Release Review (optional, after first real usage)

A BA that freezes at `Status: Validated` after the handoff to
Requirements Engineering is only validated by reasoning. Real user
data from shipped features has to flow back into the Critical
Hypotheses, otherwise the BA becomes historical fiction as soon as
the product hits actual users.

This phase runs after a release has been live long enough to produce
observed signals (days to weeks depending on scope). It is optional
in the sense that the user decides when to trigger it, but strongly
recommended after every MVP release and after every PoC that reached
real users.

**Trigger conditions:**

- The user invokes `/business-analysis` with an existing BA document
 (Project-BA OR Item-BA) at `Status: Validated` AND a release has
 happened since the validation timestamp, OR
- The `/coding` skill wrote a post-release handoff entry in
 `_devprocess/context/HANDOFFS.md` flagging the release as
 "Ready for BA Post-Release Review".

**Process:**

1. **Load evidence sources.** Read in order:
 - The target BA file (`BA-{PROJECT}.md` for project-wide
   hypotheses, or `BA-EPIC-{nn}-{slug}.md` /
   `BA-FEAT-{ee}-{ff}-{slug}.md` for item-level hypotheses),
   Section 7.3 (Critical Hypotheses)
 - `_devprocess/context/METRICS.md` (if present) for the
 observed signals
 - Any additional user-provided evidence (support tickets, usage
 analytics, interview notes, retention data)

2. **Walk each hypothesis.** For every Critical Hypothesis H-NN in
 Section 7.3, ask the user one question per turn (per User
 Interaction Protocol): "H-{NN} said {hypothesis}. What evidence
 have you collected since release?". Offer options via
 `AskUserQuestion`:
 - `Confirmed by usage` with Pro/Con labeled description
 - `Contradicted by usage` with Pro/Con labeled description
 - `Inconclusive` (not enough data yet) with Pro/Con

3. **Update the BA document.** For each hypothesis, append an
 evidence block under its status marker:

 ```
 H-01: {hypothesis text}
 Status: Confirmed by usage
 Evidence (2026-04-19): {metric, quote, or data source}
 Source: {link to dashboard, interview transcript, or
 usage report}
 ```

 Rows are never deleted. New evidence blocks append.

4. **Propagate to METRICS.md.** Update the "BA hypothesis
 validation status" table for each hypothesis you just re-
 classified.

5. **Contradictions trigger backlog entries.** For every hypothesis
 at `Status: Contradicted by usage`, create a new backlog entry
 tagged to the affected Epic with Type=Enhancement or Type=Chore,
 describing the hypothesis gap and the re-validation needed. The
 user reviews the entry at the next planning pass.

6. **Update status at the top of the BA.** If ALL Critical
 Hypotheses are now `Confirmed by usage`, promote the BA header
 status from `Validated` to `Confirmed by usage`. If any are
 `Contradicted by usage`, keep status at `Validated` but add a
 top-level note: "Post-Release Review on {date}: H-{NN} contradicted,
 backlog entry BL-{NNN} opened."

The phase writes back in the same style every other phase does. Zero
em dashes. No AI vocab. Active voice. Append-only on evidence blocks.

## Quality Gates

Before handoff to the Requirements Engineer, these criteria must be met:

### Simple Test (at least 3 of 4)

1. Problem clearly described?
2. User identified?
3. Functionality defined?
4. Definition of Done present?

### PoC (at least 6 of 8)

1. How-might-we question formulated?
2. Hypothesis clearly stated?
3. At least 1 persona with needs?
4. Technical risks identified?
5. Success criteria measurable?
6. Out-of-scope explicit?
7. Critical hypotheses documented?
8. Acceptable shortcuts documented?

### MVP (at least 10 of 13)

1. Exploration Board complete (User, Needs, Insights, HMW)?
2. Business context complete (As-Is, To-Be, Gap)?
3. Stakeholder map present?
4. At least 2 user personas with needs and insights?
5. How-might-we question formulated as synthesis?
6. Idea potential assessed (3 axes)?
7. Value proposition formulated?
8. Critical hypotheses documented?
9. KPIs with baseline + target?
10. In-scope vs out-of-scope explicit?
11. Constraints documented?
12. Risks identified?
13. Key features prioritized (P0/P1/P2)?

## Anti-Patterns to Avoid

**Do not prescribe technical solutions:**
- Wrong: "We need a React app with PostgreSQL"
- Right: "We need a modern web application"

**No vague problem statements:**
- Wrong: "The current solution is not good"
- Right: "The process takes 5h/week and produces a 20% error rate"

**Always quantify KPIs:**
- Wrong: "Faster processing"
- Right: "Processing time from 5h/week to 1h/week within 3 months"

**Do not jump to solutions too early:**
- Wrong: Discuss the solution immediately after the problem
- Right: Complete EXPLORE first (User, Needs, Insights), then IDEATION

**Do not forget How-Might-We:**
- The HMW question is the bridge from EXPLORATION to IDEATION
- Without HMW the thread between problem and solution is missing

## Handoff Ritual (mandatory at end of phase)

This skill always runs the following ritual at the end, regardless of how
it was started (directly or via `/dia-guide`).

### Part 1: Artifact report

```
Produced / updated:
- _devprocess/analysis/BA-{TARGET}.md: Business Analysis for {TARGET}
  ({TARGET} is one of: {PROJECT}, EPIC-{nn}-{slug},
  FEAT-{ee}-{ff}-{slug}, IMP-{ee}-{ff}-{nn}-{slug},
  FIX-{ee}-{ff}-{nn}-{slug})
- _devprocess/analysis/EXPLORE-{PROJECT}.md: Exploration Board (PoC/MVP only)
- BACKLOG row reserved for the future EPIC/FEAT/IMP/FIX item
- Key output: How-Might-We question, Value Proposition,
  referenced Personas (by ID)
```

### Part 2: Handoff context

Append a new entry to `_devprocess/context/HANDOFFS.md` with:

- **Scope**: Simple Test / PoC / MVP
- **Personas**: list with primary persona marked
- **HMW question**: the bridge from Exploration to Ideation
- **Critical hypotheses**: open validation items for RE
- **Assumptions**: anything assumed but not confirmed (e.g. market size,
 willingness to pay) that the next phases should watch for
- **Open questions**: research items that couldn't be answered and should
 be flagged to the user or deferred

### Part 3: Run `/consistency-check` mode A

Run `/consistency-check` mode A at the end of the skill phase, BEFORE
the phase-end commit. Catches missing backlog rows for new items,
broken `project-ba-ref` and `project-kpi-ref` links between Item-BAs
and the Project-BA, dead persona references, missing `ba-ref:` on
EPIC/FEAT artefacts that have a corresponding BA file in
`analysis/`, and dashboard count drift. Surface findings; the user
decides whether to fix now or defer.

### Part 4: Phase-end commit

Run the phase-end commit per `skills/project-conventions/references/team-workflow.md`
section "Phase-end commit (binding)". The block fires the binding
branch-and-item check, stages every artefact this phase produced,
commits with the canonical message, sets the phase tag, and opens a
draft PR if one does not exist yet.

Canonical commit message for BA:

```
chore(ba): <ITEM-ID> BA complete

<one-line summary of HMW + scope>

Refs: <ITEM-ID>
```

After the commit lands, run:

```
python3 tools/github-integration/flow.py tag-phase --item <ID> --phase ba
python3 tools/github-integration/flow.py sync-status --item <ID>
```

`sync-status` mirrors the BACKLOG Status column to the GitHub
issue and project (and the GitHub Assignee back into the BACKLOG
Claim column). It is a no-op outside `mode = "github-sync"`.

Skip the commit silently if the working tree has no changes; the
guide's post-phase consistency check will surface the empty
phase.

### Part 5: Transition question

Ask the user:

> "Business Analysis is complete. Documents saved to:
> - `_devprocess/analysis/BA-{TARGET}.md`
> - `_devprocess/analysis/EXPLORE-{PROJECT}.md` (if PoC/MVP)
>
> Recommended next: `/requirements-engineering` -- promotes the BA
> into the corresponding EPIC / FEAT / IMP / FIX artefact under
> `requirements/...` and writes `ba-ref:` into its frontmatter.
>
> Shall I start `/requirements-engineering` now, or would you like to
> review the BA first?"

**On agreement** ("yes" / "go" / "next") or when running inside
`/dia-guide`:
-> Start `/requirements-engineering` and pass the handoff context

**On rejection** ("no" / "stop" / "I want to check first"):
-> Pause and wait for user instruction

### What RE does with this handoff

- How-Might-We -> Epic Hypothesis Statement
- Critical Hypotheses -> Feature Validation sections
- Needs + Jobs to be Done -> User Stories
- Idea Potential -> Feature Prioritization (P0/P1/P2)

## Project Structure

This skill follows the conventions from `/project-conventions`.
Ensure that `_devprocess/analysis/` exists before creating documents.

## Keywords
Business Analysis, BA, Stakeholder, Problem Analysis, As-Is Analysis, Gap Analysis,
User Personas, Scope, New Project, Requirements Elicitation, Interview,
Explore, How Might We, HMW, Value Proposition, Idea Potential, Innovation,
Create, Evaluate, Needs, Insights, Jobs to be Done, Wow
