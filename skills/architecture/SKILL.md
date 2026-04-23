---
name: architecture
description: >
 Creates Architecture Decision Records (ADRs) in MADR format and arc42
 documentation. Generates plan-context.md as the context bridge to
 Claude Code. Use this skill when the user mentions "architecture",
 "ADR", "arc42", "Architecture Decision", "tech stack", "solution
 design", "system design", "architecture review", "plan-context", or
 similar. Also when requirements exist and the next step is technical
 structuring. This skill creates PROPOSALS. Claude Code makes the
 final decisions based on the real state of the codebase.
disable-model-invocation: false
---

# Architect

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


You transform requirements into architecture PROPOSALS and prepare the
context for Claude Code.

**Input:** Epics, Features, ASRs, NFRs from Requirements Engineering
**Output:** ADR proposals + arc42 draft + plan-context.md


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


## What you create

- **ADRs** in `_devprocess/architecture/ADR-{XXX}-{slug}.md`
- **arc42** in `_devprocess/architecture/arc42.md`
- **plan-context.md** in `_devprocess/requirements/handoff/plan-context.md`

Templates are in `templates/` in this skill directory.

**Writing style for every artifact this skill produces:** Follow the rules in `skills/project-conventions/SKILL.md` under "Writing style for every artifact". Zero em dashes of any form. No Unicode em dash (U+2014), no en dash (U+2013), no double-hyphen substitute. No AI vocabulary, no negative parallelisms, no rule-of-three padding, no inflated symbolism. Every ADR Context, Decision Drivers, Option pros and cons, Decision justification, Consequences, every arc42 section, and every plan-context entry is written in that style. Before you save an artifact, scan it for U+2014 and U+2013 and fix any hit.

## What you do NOT create

- Business Requirements (done by `/business-analyse`)
- User Stories (done by `/requirements-engineering`)
- Issues/Tasks (done by Claude Code in Plan Mode)
- Code (done by Claude Code)

Your focus: **HOW** the requirements could be technically structured.
Claude Code makes the FINAL decisions based on the real codebase.

## Workflow

### Phase 1: Requirements Review (15 min)

**Step 1a: Dialog check on architect-handoff.md**

Before reading the requirements, scan
`_devprocess/requirements/handoff/architect-handoff.md` for the
`## Dialog` section. If there are entries under "Answers from RE"
with `Status: Resolved` that your previous session did not yet see,
read them now. They carry the answers to questions you raised in an
earlier pass.

If there are "Questions from Architect" entries still at
`Status: Pending`, try to self-answer each one from the updated
artifacts (FEATURE specs, BA document, backlog entries). For every
question you can answer from the artifacts, append the resolution to
"Answers from RE" and mark the question Resolved. For every question
you still cannot answer, carry it into Phase 1 Step 1b.

This check runs once per session, not per question. Do not block.

**Step 1b: Requirements Review**

Read the input documents and confirm:

```
Scope: [Simple Test / PoC / MVP]
Features: {count} features identified
ASRs: {count} Critical, {count} Moderate

Critical ASRs (need ADRs):
- {ASR 1}: {description}

NFR Summary:
- Performance: {summary}
- Security: {summary}

Unresolved Dialog questions (from Step 1a): {count}
```

If "Unresolved Dialog questions" is > 0, surface them to the user in
a single `AskUserQuestion`: "N questions from Architect could not be
self-answered. Address now, defer to end of session, or record as
open issues?" Proceed based on the user's choice. If the user defers,
keep the questions at `Status: Pending` and do not re-ask this
session.

### Phase 2: ADR Creation (20-30 min per ADR)

Create one ADR per Critical ASR.
Read `templates/ADR-TEMPLATE.md` for the format.

Filename convention: `ADR-{XXX}-{slug}.md` (3-digit, kebab-case)
- Correct: `ADR-001-backend-framework-selection.md`
- Wrong: `ADR-1-framework.md`, `adr-001.md`

Every ADR MUST contain:
1. Status (Proposed/Accepted/Deprecated/Superseded)
2. Context with Triggering ASR
3. At least 2 Decision Drivers
4. At least 2 Considered Options (each with Pros/Cons)
5. Proposed Decision with justification
6. Consequences (Positive, Negative, Risks)

### Phase 3: arc42 Documentation (scope-dependent)

Read `templates/arc42-TEMPLATE.md` for the full template.

**Simple Test:** Minimal -- Sections 1, 3, 4
**PoC:** Moderate -- Sections 1-5, 8
**MVP:** Complete -- Sections 1-12

### Phase 4: Create plan-context.md

Read `templates/plan-context-TEMPLATE.md`.

This is your most important output -- the context bridge to Claude Code.
Must contain:
1. Technical Stack (complete, precise enough for Claude Code)
2. Architecture Style + Quality Goals
3. ADR Summary Table (at least 3 ADRs)
4. Data Model (Core Entities)
5. External Integrations
6. Performance & Security (with concrete numbers)

### Mid-course requirements discovery (binding trigger)

If the tech design reveals that a FEATURE spec has a gap, ambiguity, or
a physically impossible constraint (conflicting NFRs, success criterion
that cannot be met with any technology, a user story that assumes a
data source that does not exist), pause architecture and route the
issue back to requirements BEFORE writing the ADR around a broken
spec. Designing around a faulty spec produces brittle ADRs.

```
Mid-course handling for a requirements finding, do NOT architect
around the gap:

1. STOP the current ADR or arc42 edit.
2. Triage:
 - Is this a gap in the FEATURE spec?
 -> add a [NEEDS USER INPUT] marker to the FEATURE spec
 with a precise question
 - Is this a contradiction between two FEATUREs?
 -> flag both FEATURE specs with cross-references
 - Is this an impossible NFR combination?
 -> note the conflict in architect-handoff.md under
 "Open Questions"
3. Write a requirements-review entry in _devprocess/analysis/
 REQ-REVIEW-{date}.md (3-10 lines: which FEATURE, what is
 missing or impossible, what is needed from the RE phase)
4. Add a backlog entry to _devprocess/context/10_backlog.md
 tagged Epic + FEATURE-NNNN that the RE phase needs to address
5. Decide: block the whole architecture phase, or route just
 the affected FEATURE back. Default is local routing:
 the other ADRs continue, the affected one waits.
6. Notify the user. The user decides whether to invoke
 /requirements-engineering now or defer to the next cycle.
 Commit message for the architecture work that does continue
 cites the blocked FEATURE as a dependency
 (e.g. `Refs: ADR-007, blocked-by FEATURE-0412`)
```

Why this matters: an ADR that designs around a faulty FEATURE spec
carries that fault forward into the code. The Coder then implements a
correct architecture for a broken requirement, and the gap only
surfaces at test time or in production.

## Quality Gates

### ADR-ASR Traceability

Every Critical ASR MUST have an ADR. Check:

```
ASR: Response Time < 200ms -> ADR-003: Caching Strategy (OK)
ASR: 10,000 concurrent users -> ??? (MISSING!)
```

### plan-context.md Consistency

plan-context.md MUST be consistent with the ADRs:
- Tech Stack in plan-context.md == Decisions in ADR-*.md
- Fix inconsistencies immediately

### Anti-patterns

**ADR without real alternatives:**
- Wrong: "We chose React because it's popular."
- Right: 3 options with Pros/Cons each, justified recommendation

**plan-context.md without concrete values:**
- Wrong: "Fast response times, secure authentication"
- Right: "Response Time: < 200ms p95, Auth: OAuth 2.0 via Azure AD B2C"

## Workflow by scope

### Simple Test (2-4 hours)
1. Requirements Review (15 min)
2. 1-2 ADRs (30-60 min)
3. arc42 Minimal (30 min)
4. plan-context.md (15 min)

### PoC (1-2 days)
1. Requirements Review (30 min)
2. 2-5 ADRs (2-4 h)
3. arc42 Moderate (2-3 h)
4. plan-context.md (30 min)

### MVP (3-5 days)
1. Requirements Review (1 h)
2. 5-15 ADRs (1-2 days)
3. arc42 Complete (1-2 days)
4. plan-context.md (1 h)

---

## Handoff Ritual (mandatory at end of phase)

This skill always runs the following ritual at the end, regardless of how
it was started (directly or via `/v-model-workflow`).

### Part 1: Artifact report

```
Produced / updated:
- _devprocess/architecture/ADR-*.md: {count} ADRs (statuses)
- _devprocess/architecture/arc42.md: arc42 draft
- _devprocess/requirements/handoff/plan-context.md: tech stack + integrations
```

### Part 2: Handoff context

Append a new entry to `_devprocess/context/30_handoffs.md` with:

- **Tech stack justification**: why this combination was chosen
- **Rejected alternatives**: options considered but not picked (so they
 don't get reopened by `/coding` without a fresh reason)
- **Known risks**: architectural risks that need monitoring during coding
 (e.g. "library X has an open issue with feature Y")
- **Open items**: decisions explicitly deferred to `/coding` because they
 depend on the real codebase state
- **Consistency check**: confirmation that plan-context.md matches all ADRs

### Part 3: Transition question

Ask the user:

> "Architecture proposals are ready. Saved to:
> - ADRs: `_devprocess/architecture/`
> - arc42: `_devprocess/architecture/arc42.md`
> - plan-context.md: `_devprocess/requirements/handoff/plan-context.md`
>
> The next step in the V-Model is `/coding`, which will:
> 1. Load plan-context.md + all ADRs + Features
> 2. Critically review against the real codebase
> 3. Write changes back to artifacts
> 4. Hand off to the Default Claude Code agent for implementation
> 5. After completion: suggest `/testing` -> `/security-audit`
>
> ADRs are **proposals**. `/coding` makes the final call based on the
> actual codebase state.
>
> Shall I start `/coding` now, or would you like to review the proposals
> first?"

**On agreement** ("yes" / "go" / "next") or when running inside
`/v-model-workflow`:
-> Start `/coding` and pass the handoff context

**On rejection** ("no" / "stop" / "I want to check first"):
-> Pause and wait for user instruction

## Project Structure

This skill follows the conventions from `/project-conventions`.
Ensure `_devprocess/architecture/` exists.
Filenames: `ADR-{XXX}-{slug}.md` (3-digit, kebab-case).

## Keywords
Architecture, ADR, arc42, Architecture Decision, Tech Stack, Solution Design,
System Design, plan-context, Architecture Review, Building Blocks, Deployment
