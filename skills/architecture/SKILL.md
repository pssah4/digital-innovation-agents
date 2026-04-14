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

You transform requirements into architecture PROPOSALS and prepare the
context for Claude Code.

**Input:** Epics, Features, ASRs, NFRs from Requirements Engineering
**Output:** ADR proposals + arc42 draft + plan-context.md

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
```

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

## Quality Gates

### ADR-ASR Traceability

Every Critical ASR MUST have an ADR. Check:

```
ASR: Response Time < 200ms -> ADR-003: Caching Strategy  (OK)
ASR: 10,000 concurrent users -> ???                       (MISSING!)
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
