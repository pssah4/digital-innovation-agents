---
name: Architect Quality Standards
description: "Automatische Validierungsregeln für Architektur-Outputs - ADRs, arc42, Issues"
applyTo: "architecture/**/*.md, docs/ARC42-DOCUMENTATION.md, docs/architect-handoff.md, backlog/ISSUE-*.md"
---

# Architect Mode - Quality Standards & Validation Rules

Diese Instructions werden automatisch angewendet beim Arbeiten mit Architektur-Dateien. Sie stellen Qualitätsstandards für ADRs, arc42 Dokumentation und Issue-Spezifikationen sicher.

> **Ziel:** Developer kann sofort mit Implementation starten, ohne Rückfragen an den Architekten.

---

## 📁 Unterstützte Dateitypen

```
✅ architecture/**/*.md (Analysis, Intake, ADRs)
✅ docs/ARC42-DOCUMENTATION.md
✅ docs/architect-handoff.md
✅ backlog/ISSUE-*.md
```

---

## ⚙️ Prerequisites Check (Phase 1)

**Vor Architektur-Arbeit validieren:**

```markdown
✅ Requirements handoff existiert?
   Location: requirements/handoff/architect-handoff.md

✅ Handoff enthält ASRs?
   → Critical ASRs (🔴)
   → Moderate ASRs (🟡)

✅ Handoff enthält NFRs?
   → NFR Summary Table (quantifiziert)

✅ Handoff enthält Constraints?
   → Technical, Business, Functional

✅ Handoff enthält Open Questions?
   → High Priority (blocking)
   → Medium Priority (non-blocking)

If ANY missing:
  ❌ Return to Requirements Engineer
  ❌ Request completion

If ALL present:
  ✅ Proceed with Phase 1
```

---

## 📋 ADR (Architecture Decision Record) Validation

### Dateinamen-Pattern

```javascript
// Pattern: ADR-NNN-descriptive-title.md
const adrPattern = /^ADR-\d{3}-[a-z0-9-]+\.md$/;

// ✅ ADR-001-backend-framework-selection.md
// ✅ ADR-023-event-driven-architecture.md
// ❌ 0001-backend-framework.md (missing ADR prefix)
// ❌ adr-1-title.md (wrong format)
```

### Pflicht-Sections

```markdown
MANDATORY in jedem ADR:

✅ # [Title]
✅ **Status:** Accepted/Proposed/Deprecated
✅ **Date:** YYYY-MM-DD
✅ ## Context and Problem Statement (2-3 Sätze)
✅ ## Decision Drivers (min. 2)
✅ ## Considered Options (min. 3!)
✅ ## Decision Outcome
✅ ### Consequences (Good AND Bad)
✅ ### Confirmation (wie verifizieren?)
✅ ## Pros and Cons of Options (für jede Option)
✅ ## Research Links (min. 2)
```

### Content Quality Checks

```markdown
CHECK:
✅ Context ist prägnant (2-3 Sätze)?
✅ Decision Drivers sind spezifisch?
✅ Options sind realistische Alternativen (keine Strohmänner)?
✅ Decision Outcome nennt Wahl + Begründung?
✅ Consequences enthält POSITIVE UND NEGATIVE?
✅ Research Links sind relevant und aktuell?

FORBIDDEN:
❌ Vager Context ("We need a database")
❌ Nur 2 Options (braucht 3+ für echte Evaluation)
❌ Nur positive Consequences
❌ Keine Research Links
❌ Placeholders [TODO], [TBD]
```

### Fehlermeldung bei ADR-Problemen

```
❌ ADR Quality Issues

File: architecture/ADR-015-database-choice.md
Issues: 3

1. ❌ Insufficient Options
   Found: 2 options
   Required: Minimum 3
   → Add realistic alternative with pros/cons

2. ❌ Missing Research Links
   Found: 0 links
   Required: Minimum 2
   → Include web_search findings
   → Reference official documentation

3. ❌ No Negative Consequences
   Found: Only positive
   Required: Both good AND bad
   → Be honest about trade-offs
```

---

## 📐 arc42 Documentation Validation

### Scope-spezifische Sections

```markdown
Simple Test:
- Kein arc42 erforderlich
- README.md mit Setup-Instructions

PoC:
- Required: Sections 1, 3, 4
- Minimum: 2-3 Diagrams

MVP:
- Required: Sections 1-7
- Minimum: 5-8 Diagrams
```

### Section Validation

**Section 1: Introduction and Goals**
```markdown
CHECK:
✅ Requirements overview (top 3-5)?
✅ Quality goals mit Priorities?
✅ Stakeholder table?

FORBIDDEN:
❌ Copy-paste entire requirements
❌ Vage quality goals ("should be fast")
```

**Section 3: Context and Scope**
```markdown
CHECK:
✅ Business context diagram (Mermaid)?
✅ External systems identified?
✅ Technical context (protocols, interfaces)?

FORBIDDEN:
❌ Internal implementation details
```

**Section 4: Solution Strategy**
```markdown
CHECK:
✅ Fundamental decisions listed?
✅ Links zu ADRs?
✅ Technology choices mit Rationale?

FORBIDDEN:
❌ Detailed design (zu früh)
❌ Keine ADR references
```

**Sections 5-7 (MVP only)**
```markdown
CHECK:
✅ Building blocks mit Responsibilities?
✅ Component diagrams?
✅ Key scenarios mit Sequence diagrams?
✅ Deployment view?
```

### Diagram Quality

```markdown
CHECK Mermaid Diagrams:
✅ Valid Mermaid syntax?
✅ Minimum 5 nodes?
✅ Descriptive labels (nicht nur A, B, C)?
✅ Relationships labeled?

Minimum Diagrams:
- PoC: 2-3 (Context, Components)
- MVP: 5-8 (Context, Container, Component, Sequence, Deployment)

FORBIDDEN:
❌ Trivial diagrams (< 5 nodes)
❌ Unlabeled relationships
❌ ASCII art statt Mermaid
```

---

## 📝 Issue Specification Validation

### Dateinamen-Pattern

```javascript
// Pattern: ISSUE-NNN-descriptive-title.md
const issuePattern = /^ISSUE-\d{3}-[a-z0-9-]+\.md$/;

// Location: backlog/ISSUE-*.md

// ✅ backlog/ISSUE-001-user-authentication.md
// ❌ issues/ISSUE-001-auth.md (wrong directory)
```

### Atomic Issue Requirement (KRITISCH!)

```markdown
ATOMIC ISSUE = 1-3 Tage Effort Maximum

| Size | Effort | Example |
|------|--------|---------|
| Tiny | 2-4h | Add field to model |
| Small | 4-8h | Single endpoint |
| Medium | 1-2d | Profile with validation |
| Large | 2-3d | Third-party integration |

If Issue > 3 days → SPLIT IT!

❌ TOO LARGE:
"ISSUE-001: Implement User Auth System" (2-3 weeks)

✅ ATOMIC:
"ISSUE-001: Create User Model" (4-6h)
"ISSUE-002: User Registration Endpoint" (6-8h)
"ISSUE-003: Email Validation" (4-6h)
"ISSUE-004: Password Hashing" (4-6h)
"ISSUE-005: Login Endpoint" (6-8h)
```

### Pflicht-Sections

```markdown
MANDATORY in jedem Issue:

✅ # ISSUE-XXX: [Title]
✅ Metadata (Type, Priority, Effort, Status)
✅ ## Context (Why this Issue exists)
✅ ## Requirements (Functional & Non-Functional)
✅ ## 🏗️ Architectural Context (ADR links)
✅ ## Implementation Guidance (high-level)
✅ ## ✅ Acceptance Criteria (min. 3, testbar)
✅ ## Testing Requirements (mandatory)
✅ ## Definition of Done
✅ ## Architectural Constraints (MUST/MUST NOT)
✅ ## Dependencies
```

### Content Quality Checks

```markdown
CHECK Issue Quality:

Architectural Context:
✅ Links zu relevanten ADRs?
✅ References arc42 sections?
✅ Decision summary vorhanden?

Acceptance Criteria:
✅ Minimum 3 Criteria?
✅ Jedes Kriterium testbar?
✅ Verification method specified?

Constraints:
✅ Clear MUST statements?
✅ Clear MUST NOT (anti-patterns)?
✅ Performance requirements quantified?

Developer Autonomy:
✅ Implementation details offen gelassen?
✅ HOW nicht vorgeschrieben?

FORBIDDEN:
❌ Step-by-step implementation tasks
❌ Code snippets (unless mandated pattern)
❌ Specific algorithms (unless performance-critical)
❌ Missing ADR references
❌ Vage acceptance criteria ("works well")
```

### Fehlermeldung bei Issue-Problemen

```
❌ Issue Specification Issues

File: backlog/ISSUE-023-order-processing.md
Issues: 3

1. ❌ Issue Too Large
   Found: ~15 days effort
   Required: 1-3 days maximum
   → Split into 5-8 atomic Issues

2. ❌ No ADR References
   Required: Links to relevant ADRs
   → Link ADR-015 (Event-Driven)
   → Explain architectural decision

3. ❌ Implementation Tasks Included
   Found: Step-by-step HOW
   Problem: Tasks are Developer's job
   → Remove implementation steps
   → Keep architectural constraints only
```

---

## 🎯 Scope-Specific Validation

### Simple Test

```markdown
CHECK:
✅ README.md mit Setup?
✅ 3-8 atomic Issues?
✅ Each Issue 1-3 days?
✅ Clear single responsibility?

SKIP:
- arc42 (overkill)
- Multiple ADRs
- Complex diagrams
```

### PoC

```markdown
CHECK:
✅ Requirements analysis complete?
✅ 2-5 ADRs (MADR, 3+ options)?
✅ arc42 sections 1, 3, 4?
✅ 2-3 diagrams?
✅ 10-30 atomic Issues?
✅ Handover document?
```

### MVP

```markdown
CHECK:
✅ Requirements analysis comprehensive?
✅ 5-15 ADRs?
✅ arc42 sections 1-7?
✅ 5-8 diagrams?
✅ 30-100 atomic Issues?
✅ All Issues link to ADRs?
✅ Dependencies mapped?
✅ Performance/Security quantified?
✅ Handover comprehensive?
```

---

## 🚨 Critical Validation Failures (Blocker)

```markdown
1. ❌ Wrong Project Scope
   BLOCK: MVP complexity for Simple Test
   ACTION: Scale back appropriately

2. ❌ Missing ADR for Major Decision
   BLOCK: Architectural choice without ADR (PoC/MVP)
   ACTION: Create ADR using MADR template

3. ❌ Issues with Implementation Tasks
   BLOCK: Step-by-step HOW in Issues
   ACTION: Remove tasks, keep constraints

4. ❌ Issues Too Large
   BLOCK: Issue > 3 days effort
   ACTION: Split into atomic Issues

5. ❌ Insufficient Options in ADR
   BLOCK: ADR has < 3 options
   ACTION: Add realistic alternatives

6. ❌ arc42 Sections Missing
   BLOCK: MVP missing sections 1-7
   ACTION: Complete all required sections
```

---

## ✅ Quality Gate Checklists

### Simple Test QG

```markdown
- [ ] README with setup exists
- [ ] Tech stack chosen
- [ ] 3-8 atomic Issues created
- [ ] Each Issue has clear requirements
- [ ] Each Issue has acceptance criteria
```

### PoC QG

```markdown
- [ ] Requirements analysis complete
- [ ] 2-5 ADRs (MADR format, 3+ options)
- [ ] arc42 sections 1,3,4 complete
- [ ] 2-3 diagrams
- [ ] 10-30 atomic Issues
- [ ] Issues have architectural context
- [ ] Handover document complete
```

### MVP QG

```markdown
- [ ] Requirements analysis comprehensive
- [ ] 5-15 ADRs for all major decisions
- [ ] arc42 sections 1-7 complete
- [ ] 5-8 diagrams
- [ ] 30-100 atomic Issues
- [ ] All Issues link to ADRs
- [ ] Dependencies mapped
- [ ] Performance/security quantified
- [ ] Handover comprehensive
```

---

## 📤 Handover Document Validation

**File:** `docs/architect-handoff.md`

```markdown
MANDATORY Sections:

✅ # Architecture → Developer Handoff
✅ **Status:** ✅ Architecture Approved
✅ ## Project Summary (scope, pattern, tech stack)
✅ ## Architecture Overview
✅ ## System Architecture (diagram + components)
✅ ## Getting Started (setup + first issue)
✅ ## Architecture Artifacts (doc locations)
✅ ## Quality Standards
✅ ## Developer Autonomy (clear boundaries)
✅ ## Priority Order (issue sequence)
```

---

## 💬 Validation Message Formats

### Success

```
✅ {DOCUMENT TYPE} Validation Passed

File: {filepath}
Scope: {Simple Test / PoC / MVP}

Validations:
  ✅ {Check 1}
  ✅ {Check 2}

Status: Ready for next step
```

### Warning

```
⚠️ {DOCUMENT TYPE} Quality Warnings

File: {filepath}
Non-Blocking: {count}

⚠️ {Warning 1}
   Recommendation: {suggestion}

Status: Acceptable but could improve
```

### Critical Block

```
❌ CRITICAL: {DOCUMENT TYPE} BLOCKED

File: {filepath}
Blocking Issues: {count}

1. ❌ {Issue Title}
   Found: {what was found}
   Required: {what's needed}
   → Action: {specific fix}

CANNOT PROCEED until resolved!
```

---

## 📚 Reference Templates

- **MADR Template:** https://adr.github.io/madr/
- **arc42 Template:** https://arc42.org/
- **C4 Model:** https://c4model.com/
- **Mermaid Diagrams:** https://mermaid.js.org/

---

## 📝 Summary

Diese Instructions stellen sicher:

✅ **Appropriate Complexity** - Match depth to scope
✅ **ADR Quality** - MADR format, 3+ options, research links
✅ **arc42 Completeness** - Required sections per scope
✅ **Atomic Issues** - 1-3 days max, single responsibility
✅ **Clear Boundaries** - Architect defines WHAT, Developer defines HOW
✅ **Quality Gates** - Validation before handover

**Ziel:** Developer kann sofort mit atomaren Issues starten, ohne Rückfragen.

---

**Version:** 2.0
**Integration:** Works with architect.agent.md
**Key Features:** Atomic Issues (1-3 days), scope-adaptive validation
