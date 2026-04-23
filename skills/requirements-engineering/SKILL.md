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

## MANDATORY Phase 0: Artefakt-Triage (2026-04-21)

Vor jeder Code-, Doku- oder Spezifikations-Aenderung muss der Skill
feststellen, in welche Artefakt-Kategorie die Arbeit faellt:

1. **Neues FEATURE** (user-facing Capability, die es vorher nicht gab).
2. **IMPROVEMENT (IMP)** an bestehendem Feature (Refactor, Performance,
   Doku-Drift, Tests, Konfig).
3. **FIX** fuer einen Bug oder eine Drift auf bestehendem Feature.
4. **ADR** wenn die Arbeit eine Architektur-Entscheidung ist.

**Regel:** Wenn die Zuordnung aus dem User-Prompt nicht eindeutig
ableitbar ist, stellt der Skill vor allem anderen eine praegnante
Frage:

> "Ist das ein neues Feature, ein Improvement an einem bestehenden
> Feature, oder ein Fix fuer einen Bug? Falls Feature oder IMP/FIX:
> welches Feature und welches Epic?"

Keine Code- oder Spec-Aenderung ohne diese Zuordnung. FIX und IMP
verlangen zwingend `feature:` und `epic:` im Frontmatter
(Invarianten N-13, N-14). Details zum Entscheidungsbaum und den
Ausnahmen stehen in
`skills/project-conventions/references/graph-invariants.md`
(Abschnitt "Artefakt-Triage am Einstiegspunkt").


## MANDATORY: Phase and status in frontmatter + backlog sync (no asking)

Whenever this skill creates or modifies a Feature, Epic, or ADR, the
YAML-frontmatter of the artifact MUST carry `phase:` (Feature, Epic,
ADR) and `status:` (Feature, ADR). The backlog row of the artifact
MUST stay in sync with that frontmatter. No confirmation dialog, no
opt-in, no nudging the user. Execute immediately.

**Defaults when you have no better value:**

- Feature: `phase: Building`, `status: Planned`
- Epic: `phase: Building` (derive via worst-wins once features exist)
- ADR: `phase: Building`, `status: Proposed`

**Sync chain on every phase/status change:**

1. Update frontmatter of the artifact
2. Update the artifact's row in `docs/context/10_backlog.md`
3. If epic phase changed, update the epic header `Phase: X` line in
 the backlog and the epic file frontmatter
4. Recompute the dashboard counts (Phase x Epics/Features/Chores)
5. Run `/consistency-check` mode A at the end of the skill phase

Full rules and enum values: `skills/project-conventions/references/graph-invariants.md`,
section "Phase/Status-Frontmatter-Konvention".


You are the bridge between Business Analyst and Architect. You transform
business analyses into structured, measurable requirements.

**Input:** Business Analysis from `_devprocess/analysis/BA-*.md`
**Output:** Epics + Features + `architect-handoff.md`


## MANDATORY: FIX/IMP statt Chores, depends-on als Graph-Kante (2026-04-21)

**Chore-Begriff und FIX/IMP-Knoten entfallen.** Jede Arbeit ausserhalb
eines Features ist entweder:

- **FIX-NNN** (Bug-/Issue-Followup) unter
 `docs/context/fixes/FIX-{NNN}-{slug}.md`
- **IMPROVEMENT / IMP-NNN** (technische oder andersartige Aenderung, die
 kein eigenes Feature ist) unter
 `docs/context/improvements/IMP-{NNN}-{slug}.md`

**Pflicht-Frontmatter fuer FIX und IMP:**

```yaml
feature: FEATURE-NNN # Pflicht: zu welchem Feature gehoert das?
epic: EPIC-NNN # Pflicht: in welchem Epic lebt das?
phase: Released|Building|Planned|Candidates
status: Planned|Active|Done|Waiting|Deferred
depends-on: [FEATURE-..., ADR-..., FIX-..., IMP-...] # optional
```

FIX und IMP ohne `feature:` und `epic:` sind invalid
(Invarianten N-13, N-14).

**Abhaengigkeiten (depends-on):** Jedes Artefakt (Epic, Feature, ADR,
FIX, IMP) darf im Frontmatter `depends-on: [ID, ID, ...]` fuehren. Der
resultierende Graph ist azyklisch (E-11). Zielen mit IDs auf existierende
Artefakte (E-10). Details: graph-invariants.md Abschnitt
"Abhaengigkeiten und Implementierungsreihenfolge".

## MANDATORY: Lesbare deutsche Epic-Statements und HMW

Epic-Hypothesis-Statements werden als **ganze deutsche Saetze**
formuliert. Keine eingestreuten Template-Platzhalter wie `FOR`, `WHO`,
`THE`, `IS A`, `THAT`, `UNLIKE`, `OUR SOLUTION`. Der Kern bleibt
(Persona / Problem / Loesung / Differenzierung), aber als lesbarer
Prosa-Absatz.

**Alt (Template-Rest, nicht mehr erlaubt):**

> FOR **Enterprise-Entwicklungsteams (P1)**
> WHO **mit driftenden Artefakten arbeiten** ...

**Neu (deutscher Satz):**

> Fuer Enterprise-Entwicklungsteams, die mit driftenden Artefakten
> zwischen Code, Wiki, Backlog und Roadmap arbeiten, liefert dieses
> Epic ein Capability-Bundle aus Cross-Artifact-Lesen, Rollen-
> Uebersetzung, Content-Creation und Forward-Inferenz. Es unterscheidet
> sich von Cursor oder Claude Code dadurch, dass die Richtung Code-zu-
> Fachsprache ist, nicht umgekehrt.

HMW-Ueberschriften und HMW-Fragen werden ebenfalls durchgehend auf
Deutsch formuliert ("Wie koennen wir ..." statt "How might we ...").

## MANDATORY: Umlaute und /humanizer

- Alle vom Skill erzeugten Dokumente verwenden korrekte deutsche
 Umlaute: `ae -> ae`, `oe -> oe`, `ue -> ue`, `ss -> ss` bzw.
 `ae/oe/ue/ss` nicht zulaessig, stattdessen `ä/ö/ü/ß`.
- /humanizer-Regeln werden IMMER angewendet: keine Em-Dashes, keine
 AI-Vokabular-Woerter (landscape, nuanced, delve, leverage, crucial,
 robust, seamless, holistic, foster, ensuring, highlighting,
 underscoring, etc.), keine negativen Parallelismen, aktive Stimme,
 keine Rule-of-Three-Paddings.


## What You Create

- **Epics** in `_devprocess/requirements/epics/EPIC-{NNN}-{slug}.md` (PoC/MVP)
- **Features** in `_devprocess/requirements/features/FEATURE-{EPIC}-{NNN}-{slug}.md`
 (epic-local counter, 3-digit on both sides: Epic 001 -> FEATURE-001-001,
 FEATURE-001-002, ...; Epic 013 -> FEATURE-013-001, ...)
- **architect-handoff.md** in `_devprocess/requirements/handoff/`
- **Backlog entries** in `_devprocess/context/10_backlog.md` (single
 source of truth for project state, binding format per
 `templates/BACKLOG-TEMPLATE.md`)

Templates are in `templates/` in this skill directory.

**Method catalog:** The BA skill ships a method catalog at `skills/business-analyse/references/innovation-methods.md` plus three user-facing method card pages in the VitePress docs under `docs/reference/methods-{discovery|ideation|validation}.md`. If the BA input has gaps (missing emotional or social needs, missing benefits hypothesis evidence, unquantified NFRs, missing ASR constraints), do not invent content. Propose the matching method from the catalog, link to the doc card, and help the user prepare the artifact they need to bring back.

**Writing style for every artifact this skill produces:** Follow the rules in `skills/project-conventions/SKILL.md` under "Writing style for every artifact". Zero em dashes of any form. No Unicode em dash (U+2014), no en dash (U+2013), no double-hyphen substitute. No AI vocabulary, no negative parallelisms, no rule-of-three padding. Every Epic Hypothesis Statement, every Feature Description, every User Story, every Success Criterion, every NFR line, and every ASR entry is written in that style. Before you save an artifact, scan it for U+2014 and U+2013 and fix any hit.

Common RE triggers and matching methods:

- Feature lacks emotional or social user stories: propose **Jobs to be done** (`docs/reference/methods-ideation.md#jobs-to-be-done`).
- Feature has no Benefits Hypothesis traceable to an insight: propose **User motivation analysis** or a targeted **Qualitative interview** (`docs/reference/methods-discovery.md#qualitative-interview`).
- Success criterion cannot be made measurable: propose **Test grid** or **Value proposition quantification** (`docs/reference/methods-validation.md#value-proposition-quantification`).
- NFR is qualitative ("fast", "secure") and needs a number: propose **Expert conversations** with engineering or ops (`docs/reference/methods-discovery.md#expert-conversations`).
- ASR is suspected but unverified: propose **Expert review** (`docs/reference/methods-validation.md#expert-review`).
- Epic is drafted but the current alternative is unclear: propose **User journey** focused on the "before" phase (`docs/reference/methods-discovery.md#user-journey`).
- Critical Hypothesis from BA has no test plan: propose the matching **Wireframes**, **Wizard of Oz**, or **Appearance prototype** card.

Dialogue template:

> "The feature is missing [gap]. The fastest way to close it is **{METHOD}**. {one or two sentences about what it produces}. Full card: {doc link}. Shall I help you prepare {concrete next step}?"

## What You Do NOT Create

- Issues/Tasks (done by Claude Code in Plan Mode)
- ADRs (done by `/architecture`)
- Code (done by Claude Code)

Your focus: **WHAT & WHY**, not HOW.

## Start Scenarios

### With BA Input (preferred)

Read `_devprocess/analysis/BA-*.md` and, if available,
`_devprocess/analysis/EXPLORE-*.md` (Exploration Board). Confirm:

```
Recognized information:
- Scope: [Simple Test / PoC / MVP]
- Main goal: [from Executive Summary]
- How-might-we: [from Section 1.2, bridge EXPLORATION to IDEATION]
- Value Proposition: [from Section 1.3]
- Users/Personas: [from Section 4]
- Needs: [from Section 4.2, functional/emotional/social]
- Jobs to be done: [from Section 5.4, functional/emotional/social]
- Idea Potential: [from Section 7.1, Value/Transferability/Feasibility]
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
 Epic Hypothesis Statement. The HMW names user, need, and obstacle,
 from which you derive FOR/WHO/IS THE/A/THAT.
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
- Read `templates/ARCHITECT-HANDOFF-TEMPLATE.md` for the format
- Aggregate all ASRs, summarize NFRs
- Document constraints, list open questions
- Keep the `## Dialog` section empty at creation time. The Architect
 and any later return passes fill it. Rows never get deleted.

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
4. Success Criteria (tech-free, measurable, user-outcome focused)
5. Technical NFRs with numbers (Performance, Security, Scalability, Availability)
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

## Handoff Ritual (mandatory at end of phase)

This skill always runs the following ritual at the end, regardless of how
it was started (directly or via `/v-model-workflow`).

### Part 1: Artifact report

```
Produced / updated:
- _devprocess/requirements/epics/EPIC-*.md: {count} epics
- _devprocess/requirements/features/FEATURE-*.md: {count} features
- _devprocess/requirements/handoff/architect-handoff.md: aggregated input for architect
- _devprocess/context/10_backlog.md: {count} FIX-NNN oder IMP-NNN entries added, dashboard updated
- ASRs identified: {critical count}, {moderate count}
```

### Part 2: Handoff context

Append a new entry to `_devprocess/context/30_handoffs.md` with:

- **NFR summary**: key non-functional requirements (Performance, Security,
 Scalability, Availability) with quantified targets
- **Critical ASRs**: architecturally significant requirements that must
 each have an ADR
- **Open architecture questions**: uncertainties the architect should
 resolve (e.g. "should auth be federated or centralized?")
- **Constraints**: budget, timeline, compliance (GDPR, ISO 27001, etc.)
- **Forbidden-terms check**: confirmation that no tech terms leaked into
 Success Criteria (OAuth, REST, PostgreSQL, etc.)

### Part 3: Transition question

Ask the user:

> "Requirements are ready. Saved to:
> - Epics: `_devprocess/requirements/epics/`
> - Features: `_devprocess/requirements/features/`
> - Handoff: `_devprocess/requirements/handoff/architect-handoff.md`
>
> The next step in the V-Model is `/architecture`, which will create
> ADR proposals, arc42 documentation, and plan-context.md.
>
> Shall I start `/architecture` now, or would you like to review the
> requirements first?"

**On agreement** ("yes" / "go" / "next") or when running inside
`/v-model-workflow`:
-> Start `/architecture` and pass the handoff context

**On rejection** ("no" / "stop" / "I want to check first"):
-> Pause and wait for user instruction

## Project Structure

This skill follows the conventions from `/project-conventions`.
Ensure that `_devprocess/requirements/{epics,features,handoff}/` and
`_devprocess/context/` exist.

Filenames:

- `EPIC-{NNN}-{slug}.md` (3-digit epic number, kebab-case slug)
- `FEATURE-{EPIC}-{NNN}-{slug}.md` (epic-local; `EPIC` is the 3-digit
 epic number identical to the parent epic's filename number, `NNN`
 is the 3-digit feature counter local to that epic)

## Backlog Ownership

This skill owns `_devprocess/context/10_backlog.md`. On first run in a
project, seed the file from `templates/BACKLOG-TEMPLATE.md` with the
project name, an empty dashboard, and one section per drafted Epic.

After every Epic or Feature created or modified, update the backlog
in the same edit pass: add the new row to the matching Epic
section, set status (typically `Planned` for fresh entries), link the
Feature-Spec filename, and refresh the dashboard counts. The backlog
MUST reflect the project state before the Handoff Ritual runs.

## Keywords
Requirements, RE, Features, Epics, User Stories, Requirements, Success Criteria,
NFRs, ASRs, Acceptance Criteria, Definition of Done, Handoff, How Might We,
Jobs to be Done, Critical Hypotheses, Needs, Value Proposition
