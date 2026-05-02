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

## MANDATORY Pre-Phase 0: Branch and item check

RE writes the FEATURE / FIX / IMP spec for a specific backlog item.
Run the team-workflow check (full rules:
`skills/project-conventions/references/team-workflow.md`):

1. Identify the active item from the prompt or via AskUserQuestion.
   For new items, write the BACKLOG row first.
2. Verify the branch matches `feature/<item-id-lower>-<slug>` (or
   `fix/...` / `chore/...`). On a wrong branch, AskUserQuestion to
   switch.
3. Skill-triggered GitHub integration:

   ```
   python3 tools/github-integration/flow.py create-issue --item <ID>
   python3 tools/github-integration/flow.py open-draft-pr --item <ID>
   ```

4. At Handoff Ritual end, tag the phase:

   ```
   python3 tools/github-integration/flow.py tag-phase --item <ID> --phase re
   ```

5. Write `.git/dia-active-skill` so subsequent invocations stay silent.

## MANDATORY Phase 0: Artifact triage

Before any code, doc, or spec change, the skill determines which
artifact category the work falls into:

1. **New FEATURE** (user-facing capability that did not exist before).
2. **IMPROVEMENT (IMP)** on an existing feature (refactor, performance,
   doc drift, tests, config).
3. **FIX** for a bug or drift on an existing feature.
4. **ADR** when the work is an architecture decision.

**Rule:** if the assignment cannot be derived unambiguously from the
user prompt, the skill asks one short question before anything else
(in the user's working language; the English wording below is a
template):

> "Is this a new feature, an improvement on an existing feature, or
> a fix for a bug? If feature or IMP/FIX: which feature and which
> epic?"

No spec change without this assignment. FIX and IMP require
`feature:` and `epic:` in the frontmatter. Details:
`skills/project-conventions/references/graph-invariants.md`
(section "Artifact triage at entry point").


## MANDATORY: Backlog as single source of truth (no asking)

Whenever this skill creates or modifies a Feature, Epic, or
Improvement, it writes the backlog row in
`_devprocess/context/BACKLOG.md` BEFORE touching the artifact
body. Status, phase, last-change, claim, and Refs live in the
backlog row, not in the artifact frontmatter.

For every new FEATURE or IMP, a backlog row is mandatory output of
this skill. The row carries:

- Initial status (Planned)
- Initial phase (Building, or Candidates if early ideation)
- Epic link in Refs
- Source (BA, RE, REV, USER)
- Empty PLAN-refs and ADR-refs (filled later by /architecture and
  /coding)

**Defaults when no better value exists:**

- Feature: status Planned, phase Building
- Epic: phase Building (derived via worst-wins once features exist)
- IMP: status Planned, phase Candidates

**Sync chain (binding order):**

1. Update the backlog row (status, phase, claim, last-change, refs)
   FIRST
2. Update the artifact body with the substance change
3. Recompute the dashboard counts at the bottom of the backlog
4. Run `/consistency-check` mode A at the end of the skill phase


You are the bridge between Business Analyst and Architect. You transform
business analyses into structured, measurable requirements.

**Input:** Business Analysis from `_devprocess/analysis/BA-*.md`
**Output:** Epics + Features + `architect-handoff.md`


## MANDATORY: FIX/IMP, depends-on as a graph edge

**Chores are not a separate node type.** Every piece of work outside
of a Feature is either:

- **FIX-{ee}-{ff}-{nn}** (bug or issue follow-up) at
  `_devprocess/requirements/fixes/FIX-{ee}-{ff}-{nn}-{slug}.md`
- **IMPROVEMENT / IMP-{ee}-{ff}-{nn}** (technical or other change that is not a
  feature) at
  `_devprocess/requirements/improvements/IMP-{ee}-{ff}-{nn}-{slug}.md`

**Required frontmatter for FIX and IMP:**

```yaml
id: FIX-{ee}-{ff}-{nn}
feature: FEAT-{ee}-{ff}    # mandatory
epic: EPIC-{nn}                    # mandatory
adr-refs: []
plan-refs: []
depends-on: []
created: {YYYY-MM-DD}
```

FIX and IMP without `feature:` and `epic:` are invalid. Status,
phase, last-change, and claim live in the backlog row, not in the
frontmatter.

**Dependencies (depends-on):** every artifact (Epic, Feature, ADR,
FIX, IMP, PLAN) MAY carry `depends-on: [ID, ID, ...]` in the
frontmatter. The resulting graph is acyclic. Targets must be
existing artifact IDs. Details: graph-invariants.md section
"Dependencies and implementation order".

## MANDATORY: Hypothesis statements as full prose

Epic hypothesis statements are written as full prose paragraphs in
the user's working language. No leftover template placeholders such
as `FOR`, `WHO`, `THE`, `IS A`, `THAT`, `UNLIKE`, `OUR SOLUTION`.
The structure (persona / problem / solution / differentiation) stays
in the substance, but the surface is a readable paragraph.

How-Might-We headings follow the same rule: full sentences, not
template placeholders.

## MANDATORY: Writing style and humanizer rules

All artifacts produced by this skill follow the rules in
`skills/project-conventions/SKILL.md` under "Writing style for every
artifact". Zero em dashes (U+2014, U+2013, double-hyphen substitute).
No AI vocabulary words (landscape, nuanced, delve, leverage, crucial,
robust, seamless, holistic, foster, ensuring, highlighting,
underscoring). No negative parallelisms ("not X but Y"). Active
voice by default. Sentence case in headings. No rule-of-three padding.

For German artifacts: proper umlauts (ä, ö, ü, ß), not the
ae/oe/ue/ss substitutes.


## What You Create

- **Epics** in `_devprocess/requirements/epics/EPIC-{nn}-{slug}.md` (PoC/MVP)
- **Features** in `_devprocess/requirements/features/FEAT-{ee}-{ff}-{slug}.md`
 (epic-local counter, 2-digit on both sides: Epic 01 -> FEAT-01-01,
 FEAT-01-02, ...; Epic 13 -> FEAT-13-01, ...)
- **architect-handoff.md** in `_devprocess/requirements/handoff/`
- **Backlog entries** in `_devprocess/context/BACKLOG.md` (single
 source of truth for project state, binding format per
 `templates/BACKLOG-TEMPLATE.md`)

Templates are in `templates/` in this skill directory.

**Method catalog:** The BA skill ships a method catalog at `skills/business-analysis/references/innovation-methods.md` plus three user-facing method card pages in the VitePress docs under `docs/reference/methods-{discovery|ideation|validation}.md`. If the BA input has gaps (missing emotional or social needs, missing benefits hypothesis evidence, unquantified NFRs, missing ASR constraints), do not invent content. Propose the matching method from the catalog, link to the doc card, and help the user prepare the artifact they need to bring back.

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

## MANDATORY: Parent BA status promotion on successful handoff

After Quality Gates pass and before the Handoff Ritual runs, the skill
promotes the parent BA status if the BA is still at a draft marker. RE
just produced Epics, Features, and an architect-handoff from this BA,
so the BA has been exercised end-to-end. Leaving it at `Draft (...)`
makes the next reader wonder whether the BA is raw or content-bearing.

The check runs every time, but the promotion is gated and asks the
user once. On `Validated` it is silent.

### Trigger

Locate the parent BA. The BA is the file referenced as
`analysis-source:` in the new Epics' frontmatter, or the
`source-ba:` field in `_devprocess/requirements/handoff/architect-handoff.md`,
or the only `_devprocess/analysis/BA-*.md` file when the project has
exactly one.

If no parent BA can be located unambiguously, skip silently and log a
one-line notice in the Handoff Ritual artifact report
(`Parent BA: not located, status promotion skipped`). Do not block
the handoff.

### Status promotion gate

Read the parent BA frontmatter `status:` field:

- **`status: Draft (reverse-engineered, ...)` or `status: Draft`**: ask
  one confirmation turn via `AskUserQuestion`:

  > Title: "Promote parent BA status?"
  > Question: "RE derived Epics, Features, and an architect-handoff
  > from `BA-{NAME}.md`. The BA is still marked Draft. Promote it to
  > Validated as part of this handoff?"
  >
  > Options (each with Pro/Con per User Interaction Protocol):
  > 1. (Recommended) Promote to Validated
  >    + Pro: BA exercised end-to-end through RE, status reflects
  >      reality, downstream readers see a content-bearing artifact.
  >    - Con: marks the BA as validated even if you have not personally
  >      walked every section since the co-creation dialog.
  > 2. Keep Draft
  >    + Pro: explicit walkthrough via `/business-analysis` Validation
  >      Mode happens later; status change stays manual.
  >    - Con: BA stays at Draft while its derived Epics and Features
  >      are already in flight; later readers must guess the BA's
  >      reliability.
  > 3. Other (free text)

  On option 1: update the BA frontmatter:

  ```yaml
  status: Validated
  validated-by: /requirements-engineering on {YYYY-MM-DD}
  validated-via: handoff (Epics + Features + architect-handoff)
  ```

  Append a row to the BA's `## Validation Log` section (create the
  section if it does not exist, place it after the Executive Summary):

  ```
  | {YYYY-MM-DD} | /requirements-engineering | Validated through RE handoff: {N} epics, {M} features, architect-handoff at `_devprocess/requirements/handoff/architect-handoff.md` |
  ```

  Keep `created-by:` and `reverse-engineering-provenance:` (if set)
  in place as historical record.

  On option 2 or 3: leave the BA frontmatter untouched. Note the
  decline in the Handoff Ritual artifact report
  (`Parent BA status: kept at Draft per user request`).

- **`status: Validated` or any other non-Draft value**: skip silently.
  No prompt, no edit. The BA already passed validation through some
  other path (`/business-analysis` Validation Mode, manual edit, or a
  prior RE pass). Idempotent on the second and later runs.

### Output for the Handoff Ritual report

The artifact report (Part 1 of the Handoff Ritual) carries one of
three lines depending on what happened:

- `Parent BA: BA-{NAME}.md, promoted Draft -> Validated`
- `Parent BA: BA-{NAME}.md, kept at {status} per user request`
- `Parent BA: BA-{NAME}.md, already at status {status} (no change)`
- `Parent BA: not located, status promotion skipped`

This makes the promotion auditable in the phase-end commit.

### Companion: status-coherence invariant N-17

`/consistency-check` Mode A enforces N-17 (status coherence between
parent artifacts and their downstream evidence). The RE-side promotion
is the proactive path that prevents the breach in the first place; N-17
is the safety net that flags the breach if RE-side promotion was
declined or skipped, or if the BA was edited out-of-band. The two
checks are complementary, not redundant.

## Handoff Ritual (mandatory at end of phase)

This skill always runs the following ritual at the end, regardless of how
it was started (directly or via `/dia-guide`).

### Part 1: Artifact report

```
Produced / updated:
- _devprocess/requirements/epics/EPIC-*.md: {count} epics
- _devprocess/requirements/features/FEATURE-*.md: {count} features
- _devprocess/requirements/handoff/architect-handoff.md: aggregated input for architect
- _devprocess/context/BACKLOG.md: {count} FIX-{ee}-{ff}-{nn} oder IMP-{ee}-{ff}-{nn} entries added, dashboard updated
- ASRs identified: {critical count}, {moderate count}
```

### Part 2: Handoff context

Append a new entry to `_devprocess/context/HANDOFFS.md` with:

- **NFR summary**: key non-functional requirements (Performance, Security,
 Scalability, Availability) with quantified targets
- **Critical ASRs**: architecturally significant requirements that must
 each have an ADR
- **Open architecture questions**: uncertainties the architect should
 resolve (e.g. "should auth be federated or centralized?")
- **Constraints**: budget, timeline, compliance (GDPR, ISO 27001, etc.)
- **Forbidden-terms check**: confirmation that no tech terms leaked into
 Success Criteria (OAuth, REST, PostgreSQL, etc.)

### Part 3: Phase-end commit

Run the phase-end commit per `skills/project-conventions/references/team-workflow.md`
section "Phase-end commit (binding)". The block fires the binding
branch-and-item check, stages every artefact this phase produced
(epics, features, architect-handoff, BACKLOG row updates), commits
with the canonical message, sets the phase tag, and opens a draft PR
if one does not exist yet.

Canonical commit message for RE:

```
chore(re): <ITEM-ID> RE complete

<one-line summary: N epics, M features, K success criteria>

Refs: <ITEM-ID>[, additional epic/feature IDs touched]
```

After the commit lands, run:

```
python3 tools/github-integration/flow.py tag-phase --item <ID> --phase re
```

For long RE phases that span days and produce many features,
intermediate commits per cluster of features are encouraged. Each
intermediate commit follows the same template; only the final
phase-end commit gets the `<id>/re-done` tag.

Skip the commit silently if the working tree has no changes.

### Part 4: Transition question

Ask the user:

> "Requirements are ready. Saved to:
> - Epics: `_devprocess/requirements/epics/`
> - Features: `_devprocess/requirements/features/`
> - Handoff: `_devprocess/requirements/handoff/architect-handoff.md`
>
> Recommended next: `/architecture` -- creates ADR proposals,
> arc42 documentation, and plan-context.md.
>
> Shall I start `/architecture` now, or would you like to review the
> requirements first?"

**On agreement** ("yes" / "go" / "next") or when running inside
`/dia-guide`:
-> Start `/architecture` and pass the handoff context

**On rejection** ("no" / "stop" / "I want to check first"):
-> Pause and wait for user instruction

## Project Structure

This skill follows the conventions from `/project-conventions`.
Ensure that `_devprocess/requirements/{epics,features,handoff}/` and
`_devprocess/context/` exist.

Filenames:

- `EPIC-{nn}-{slug}.md` (2-digit epic number, kebab-case slug)
- `FEAT-{ee}-{ff}-{slug}.md` (epic-local; `{ee}` is the 2-digit
 epic number identical to the parent epic's filename number, `NNN`
 is the 2-digit feature counter local to that epic)

## Backlog Ownership

This skill owns `_devprocess/context/BACKLOG.md`. On first run in a
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
