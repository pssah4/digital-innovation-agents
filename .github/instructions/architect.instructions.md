---
description: "Automatic validation rules for Architect Mode - ensures quality standards for ADRs, arc42 docs, and issues"
applyTo: "architecture/**/*.md, docs/**/*.md, issues/**/*.md, docs/decisions/**/*.md"
autoLoad: true
---

# Architect Mode - Automatic Validation & Quality Rules

These instructions apply automatically when working with architecture files. They enforce quality standards for Architecture Decision Records (ADRs), arc42 documentation, and issue specifications.

> **Integration:** Works with `architect.chatmode.md` to ensure all architectural outputs meet quality standards.

## 🎯 Supported File Types

These validation rules apply to:

```
✅ architecture/**/*.md (Architecture analysis, intake, handover)
✅ docs/ARC42-DOCUMENTATION.md (arc42 documentation)
✅ docs/decisions/*.md (Architecture Decision Records)
✅ issues/ISSUE-*.md (Developer-ready issues)
✅ README.md (For Simple Test projects)
```

---

## ⚙️ Prerequisites Check

### Phase 1 Validation

**Check Prerequisites before starting architecture work:**

```
✅ Requirements handoff exists?
   Location: requirements/handoff/architect-handoff.md
✅ Handoff contains ASRs?
   → Critical ASRs (🔴) listed
   → Moderate ASRs (🟡) listed
✅ Handoff contains NFRs?
   → NFR Summary Table with quantified targets
✅ Handoff contains Constraints?
   → Technical Constraints
   → Business Constraints
   → Functional Constraints
✅ Handoff contains Open Questions?
   → High Priority (blocking)
   → Medium Priority (non-blocking)
✅ Handoff contains Tech Stack Recommendations?
✅ Handoff contains System Context?
   → System Context Diagram
   → Data Flow description

If ANY missing:
  ❌ Return to Requirements Engineer
  ❌ Request architect-handoff.md completion
  ❌ List specific missing sections
  
If ALL present:
  ✅ Proceed with Phase 1: Requirements Handoff Analysis
```

---

## 📋 Validation Rules by Document Type

### 1. ADR (Architecture Decision Record) Validation

**Pattern Validation:**
```javascript
// ADR File Pattern - MUST include "ADR" prefix
const adrPattern = /^ADR-\d{3}-[a-z0-9-]+\.md$/;

// Examples:
// ✅ ADR-001-backend-framework-selection.md
// ✅ ADR-023-event-driven-architecture.md
// ❌ 0001-backend-framework.md (missing ADR prefix)
// ❌ adr-1-title.md (wrong format)
```

**Required Sections:**
```markdown
MANDATORY Sections in every ADR:

✅ # [Title]
✅ ## Context and Problem Statement
✅ ## Decision Drivers (min 2)
✅ ## Considered Options (min 3!)
✅ ## Decision Outcome
✅ ### Consequences (Good AND Bad)
✅ ### Confirmation
✅ ## Pros and Cons of Options (for each option)
✅ ## Research Links (min 2 from web_search/@azure)

OPTIONAL:
○ ## More Information
○ ## References
```

**Error Message Format:**

```
❌ ADR Quality Issues

File: architecture/ADR-015-database-choice.md
Issues Found: 4

1. ❌ Filename Format
   Found: ADR-015-database.md
   Expected: 0015-database-choice.md
   
   Format: NNNN-title-with-dashes.md
   - NNNN = 4-digit sequential number
   - Title = lowercase-with-dashes

2. ❌ Insufficient Options
   Found: 2 options
   Required: Minimum 3 options
   
   → Add at least one more considered option
   → Include pros/cons for each

3. ❌ Missing Decision Drivers
   Found: 1 driver
   Required: Minimum 2 drivers
   
   → What forces influenced this decision?
   → What concerns needed addressing?

4. ❌ No Research Links
   Found: 0 links
   Required: Minimum 2 research sources
   
   → Include web_search findings
   → Reference @azure best practices
   → Link official documentation

Action Required:
Fix these issues before marking ADR as "Accepted".
Use MADR template: https://adr.github.io/madr/
```

**Content Quality Checks:**
```markdown
CHECK during ADR creation:

✅ Context is 2-3 sentences (not too long)?
✅ Decision drivers are specific (not vague)?
✅ Options are realistic alternatives (not strawmen)?
✅ Decision outcome clearly states choice + rationale?
✅ Consequences include BOTH positive AND negative?
✅ Confirmation describes how to verify?
✅ Each option has pros AND cons?
✅ Research links are relevant and current?

FORBIDDEN:
❌ Vague context ("We need a database")
❌ Only 2 options (need 3+ for true evaluation)
❌ Only positive consequences (be honest about trade-offs)
❌ No research links (decisions must be informed)
❌ Placeholders like [TODO], [TBD], [To be determined]
```

---

### 2. arc42 Documentation Validation

**Project Scope Determines Required Sections:**

```markdown
Simple Test:
- No arc42 required
- Use README.md instead
- Validation: Basic setup instructions exist

PoC:
- Required: Sections 1, 3, 4
- Minimum: 2-3 diagrams
- Validation: Sections present, no placeholders

MVP:
- Required: Sections 1-7
- Minimum: 5-8 diagrams
- Validation: All sections complete, comprehensive
```

**Section Validation (for PoC/MVP):**

**Section 1: Introduction and Goals**
```markdown
CHECK:
✅ Requirements overview (top 3-5)?
✅ Quality goals with priorities (top 3-5)?
✅ Stakeholder table with roles?

FORBIDDEN:
❌ Copy-paste entire requirements doc
❌ Vague quality goals ("should be fast")
❌ Missing stakeholder interests
```

**Section 3: Context and Scope**
```markdown
CHECK:
✅ Business context diagram (Mermaid)?
✅ External systems identified?
✅ User groups defined?
✅ Technical context (protocols, interfaces)?

FORBIDDEN:
❌ Internal implementation details (save for Section 5)
❌ Missing external boundary
```

**Section 4: Solution Strategy**
```markdown
CHECK:
✅ Fundamental decisions listed?
✅ Links to ADRs for major decisions?
✅ Technology choices with rationale?
✅ Top-level decomposition?

FORBIDDEN:
❌ Detailed design (too early)
❌ No ADR references
```

**Section 5: Building Block View (MVP)**
```markdown
CHECK:
✅ Level 1: High-level components?
✅ Responsibilities for each component?
✅ Interfaces defined?
✅ Component diagram (Mermaid)?

OPTIONAL:
○ Level 2+ refinement (if complex)

FORBIDDEN:
❌ Code-level classes (too detailed)
❌ Missing interfaces
```

**Sections 6-7: Runtime & Deployment (MVP)**
```markdown
CHECK:
✅ Key scenarios with sequence diagrams?
✅ Main workflows documented?
✅ Deployment view with infrastructure?
✅ Deployment strategy explained?

FORBIDDEN:
❌ Every possible scenario (pick key ones)
❌ Missing deployment view
```

**Error Message Format:**

```
❌ arc42 Documentation Incomplete

File: docs/ARC42-DOCUMENTATION.md
Project Scope: MVP
Issues Found: 3

1. ❌ Section 1: Missing Quality Goals
   Found: Requirements listed
   Missing: Top 3-5 quality goals with priorities
   
   → Add quality goals table:
     | Goal | Priority | Justification |

2. ❌ Section 5: No Component Diagram
   Found: Text description only
   Required: Mermaid diagram
   
   → Add C4 component diagram
   → Show component boundaries
   → Include interfaces

3. ❌ Section 4: ADRs Not Referenced
   Found: Technology choices listed
   Missing: Links to ADR files
   
   → Link to ADR-XXX for each major decision
   → Add rationale from ADRs

Action Required:
Complete missing sections and diagrams.
Reference: https://arc42.org/
```

**Diagram Quality Validation:**

```markdown
CHECK Mermaid Diagrams:

✅ Valid Mermaid syntax (renders correctly)?
✅ Minimum 5 nodes (not trivial)?
✅ Descriptive labels (not just "A", "B", "C")?
✅ Relationships clearly labeled?
✅ Readable layout?

Minimum Diagrams by Scope:
- PoC: 2-3 diagrams
  - Context diagram (C4)
  - Component diagram
  
- MVP: 5-8 diagrams
  - Context diagram (C4)
  - Container diagram (C4)
  - Component diagram (C4)
  - 2-3 sequence diagrams (key scenarios)
  - Deployment diagram
  - ERD or data model (if applicable)

FORBIDDEN:
❌ Hand-drawn diagrams (use Mermaid)
❌ Trivial diagrams (< 5 nodes)
❌ Unlabeled relationships
❌ ASCII art instead of proper diagrams
```

---

### 3. Issue Specification Validation

**Location:** All Issues MUST be in `backlog/` directory

**Pattern Validation:**
```javascript
// Issue File Pattern
const issuePattern = /^ISSUE-\d{3}-[a-z0-9-]+\.md$/;

// Examples:
// ✅ backlog/ISSUE-001-user-authentication.md
// ✅ backlog/ISSUE-042-payment-gateway-integration.md
// ❌ issues/ISSUE-001-auth.md (wrong directory)
// ❌ backlog/issue-1-auth.md (wrong format)
```

**Terminology & Hierarchy:**
```markdown
CONSISTENT TERMINOLOGY (Critical!):

Issues = Developer-implementable work units
  - Located in: issues/ISSUE-XXX-*.md
  - Scope: What can be completed in 1-2 weeks max
  - Contains: Architecture context, constraints, acceptance criteria
  - Developer breaks down into tasks

Modules/Components = Technical implementation units
  - Part of an Issue's implementation
  - Example: wiki_links.py, frontmatter.py, etc.
  - Documented within Issue or separate module spec
  - Multiple modules can be grouped into one Issue (for Simple Test)

HIERARCHY:
Epic (optional) → Issues → Modules/Tasks
Example:
  Epic: Content Migration
    → ISSUE-001: Migration Orchestrator
    → ISSUE-002: Content Transformation (contains 5 modules)
    → ISSUE-003: User Interface

FORBIDDEN:
❌ Calling modules "features" (creates confusion)
❌ Mixing Feature/Issue terminology inconsistently
❌ Creating Issue for every tiny module (over-engineering Simple Test)
```

**Required Sections:**
```markdown
MANDATORY in every Issue:

✅ # ISSUE-XXX: [Title]
✅ Metadata block (Type, Priority, Effort, Status, Sprint)
✅ ## Context (Why this Issue exists, what problem it solves)
✅ ## Requirements (Functional & Non-Functional)
✅ ## 🏗️ Architectural Context (ADR links, patterns)
✅ ## Implementation (Structure, modules, approach)
✅ ## Acceptance Criteria (min 3, testable)
✅ ## Definition of Done
✅ ## 📚 Related Documentation (ADR links, arc42 refs)

OPTIONAL:
○ ## Dependencies (other Issues)
○ ## Notes for Developer
○ Architecture diagrams
○ ## 🔓 Open for Developer Decision (what's flexible)
```

**Content Quality Checks:**
```markdown
CHECK Issue Quality:

Architectural Context:
✅ Links to relevant ADRs?
✅ References arc42 sections?
✅ Decision summary present?

Business Objective:
✅ WHY this matters clearly stated?
✅ Contribution to feature explained?
✅ User impact described?

Architectural Constraints:
✅ Clear MUST statements (non-negotiable)?
✅ Clear MUST NOT (anti-patterns)?
✅ Performance requirements quantified (if applicable)?
✅ Security requirements specific (if applicable)?

Acceptance Criteria:
✅ Minimum 3 criteria?
✅ Each criterion testable?
✅ Verification method specified?
✅ Links to Gherkin scenarios from requirements?

Open for Developer Decision:
✅ Implementation details explicitly left open?
✅ Developer autonomy preserved?
✅ Clear what's constrained vs. open?

FORBIDDEN:
❌ Step-by-step implementation tasks (Developer breaks down)
❌ Code snippets (unless mandated pattern)
❌ Specific algorithms (unless performance-critical)
❌ Low-level decisions (variable names, internal structure)
❌ Missing ADR references for architectural choices
❌ Vague acceptance criteria ("works well")
```

**Error Message Format:**

```
❌ Issue Specification Issues

File: issues/ISSUE-023-order-processing.md
Issues Found: 4

1. ❌ No ADR References
   Section: Architectural Context
   Found: Generic description
   Required: Links to relevant ADRs
   
   → Link ADR-015 (Event-Driven Architecture)
   → Link ADR-022 (Message Queue Choice)
   → Explain architectural decision

2. ❌ Vague Acceptance Criteria
   Found: "System should handle orders quickly"
   Required: Specific, measurable criteria
   
   → Specify: "Process orders within 2 seconds (p95)"
   → Add: "Support 100 orders/second in load test"
   → Include: Verification method

3. ❌ Implementation Tasks Included
   Found: Section with step-by-step tasks
   Problem: Tasks are Developer's responsibility
   
   → Remove: Implementation steps
   → Keep: Architectural constraints only
   → Add: "Open for Developer Decision" section

4. ❌ Missing "Open for Developer" Section
   Problem: No clarity on developer autonomy
   Required: Explicitly state what's open
   
   → Add section: "Open for Developer Decision"
   → List: Internal structure, libraries, etc.
   → Clarify: Developer owns the HOW

Action Required:
Fix issues to properly balance architectural guidance
with developer autonomy. Issues define WHAT, not HOW.
```

---

### 4. Backlog Overview Validation

**File:** `backlog/Backlog.md` (MANDATORY for ALL projects)

**Required Sections:**
```markdown
MANDATORY in backlog.md:

✅ # Project Backlog
✅ ## Project Overview (one-liner, scope)
✅ ## Issues Overview Table
   | Issue | Title | Priority | Effort | Status | Dependencies |
✅ ## Issue Details (for each Issue)
   - What it implements
   - Modules/components included
   - Dependencies on other Issues
✅ ## Implementation Roadmap (Sprint plan)
✅ ## Progress Tracking (checkboxes)
✅ ## Related Documentation (links)

PURPOSE:
- Single source of truth for work breakdown
- Clear hierarchy: Issues → Modules
- No confusion about terminology
- Easy progress tracking
```

**Error Message Format:**

```
❌ Missing Backlog.md

File: backlog/Backlog.md
Status: NOT FOUND
Required: YES (for all projects)

Action Required:
Create backlog/Backlog.md with:
1. Issues Overview Table (all Issues listed)
2. Detailed breakdown (what each Issue contains)
3. Clear hierarchy (Epics → Features → Issues)
4. Sprint planning with implementation order
5. Progress tracking sections

Purpose:
Single source of truth for Developer to track all work.
Shows complete hierarchy from business goals to implementation.
```

---

### 5. Handover Document Validation

**File:** `docs/architect-handoff.md`

**Required Sections:**
```markdown
MANDATORY Sections:

✅ # Architecture → Developer Handoff
✅ Status: ✅ Architecture Approved
✅ ## 📊 Project Summary (scope, pattern, tech stack)
✅ ## 🎯 Architecture Overview (from arc42 Section 1)
✅ ## 🏗️ System Architecture (diagram + components)
✅ ## 🚀 Getting Started (setup + first issue)
✅ ## 📁 Architecture Artifacts (doc locations)
✅ ## ✅ Quality Standards
✅ ## 🤝 Developer Autonomy (clear boundaries)
✅ ## 📞 Support (how to get help)
✅ ## 📋 Reference to backlog/Backlog.md (PRIMARY work tracking document)
```

**Error Message Format:**

```
❌ Handover Document Incomplete

File: docs/architect-handoff.md
Issues Found: 2

1. ❌ Missing "Getting Started" Section
   Required: Environment setup instructions
   Required: First issue to implement
   
   → Add setup commands or script reference
   → Identify priority issue to start
   → List issue priority order

2. ❌ No Developer Autonomy Section
   Problem: Unclear boundaries
   Required: Explicit architect/developer split
   
   → Add "Developer Autonomy" section
   → Clarify: Developer owns task breakdown
   → Clarify: Developer owns implementation details

Action Required:
Complete handover document for smooth transition.
```

---

## 🎯 Scope-Specific Validation

### Simple Test Validation

```markdown
CHECK for Simple Test:

✅ README.md exists with:
  - What it does
  - How to run it
  - Basic tech stack

✅ backlog.md created (MANDATORY):
  - Lists all atomic Issues (3-8 typically)
  - Shows clear single responsibility per Issue
  - Issues are small (1-3 days each)
  - Implementation order with dependencies

✅ 3-8 ATOMIC Issues created:
  - Clear title (ISSUE-XXX-name.md format)
  - Single responsibility per Issue
  - 1-3 days effort maximum
  - Context & requirements
  - Implementation guidance (high-level)
  - Acceptance criteria (testable)
  - Testing requirements (mandatory)
  - Definition of Done checklist

OPTIONAL:
○ 0-1 ADR (if reusable decision)

SKIP:
- Full arc42 (overkill)
- Multiple ADRs (unnecessary)
- Complex diagrams

STRUCTURE RULES (ATOMIC ISSUES):
✅ Break down complex features into multiple Issues
✅ Each Issue = 1-3 days implementation
✅ Typical Simple Test: 5-8 atomic Issues (not 1-3 large ones!)
✅ Example: "5 modules" → 5 separate Issues (one per module)
❌ DON'T create Issues >3 days (Developer can't complete atomically)
❌ DON'T group unrelated modules into one Issue
```

### PoC Validation

```markdown
CHECK for PoC:

✅ Requirements analysis complete

✅ backlog.md created (MANDATORY):
  - Lists all atomic Issues (10-30 typical)
  - Dependencies clearly mapped
  - Sprint breakdown with story points
  - Priority ordering

✅ 2-5 critical ADRs:
  - All use MADR format
  - Each has 3+ options
  - Research links present

✅ arc42 sections 1, 3, 4:
  - Minimal but complete
  - No placeholders
  - 2-3 diagrams

✅ 10-30 ATOMIC Issues:
  - Each 1-3 days effort
  - Single responsibility
  - Clear architectural context
  - Testable acceptance criteria
  - Testing requirements included
  - Implementation guidance (not step-by-step)

✅ Handover document complete
  - References backlog.md
```

### MVP Validation

```markdown
CHECK for MVP:

✅ Requirements analysis comprehensive

✅ backlog.md created (MANDATORY):
  - Complete atomic Issues overview (30-100 typical)
  - Clear single responsibility per Issue
  - Dependencies fully mapped
  - Detailed Sprint breakdown with story points
  - Progress tracking structure

✅ 5-15 ADRs:
  - All major decisions documented
  - MADR format strictly followed
  - 3+ options each
  - Pros/cons detailed
  - Research links (2+ per ADR)

✅ arc42 sections 1-7:
  - All sections complete
  - No placeholders
  - 5-8 diagrams
  - Cross-references to ADRs

✅ 30-100 ATOMIC Issues:
  - Each 1-3 days effort
  - Single, focused responsibility
  - Full architectural context
  - ADR references
  - Quantified constraints
  - Detailed acceptance criteria
  - Testing requirements mandatory
  - Dependencies mapped

✅ Handover document comprehensive
  - References backlog.md
  - Clear work breakdown
✅ Quality standards clearly defined
```

---

## 🚨 Critical Validation Failures

**Instant Blocks (Cannot Proceed):**

1. **❌ Wrong Project Scope**
   ```
   BLOCK: Applying MVP complexity to Simple Test
   REASON: Over-engineering kills speed
   ACTION: Scale back to appropriate complexity
   ```

2. **❌ Missing ADR for Major Decision**
   ```
   BLOCK: Architectural choice without ADR (for PoC/MVP)
   REASON: Decisions must be documented
   ACTION: Create ADR using MADR template
   ```

3. **❌ Issues with Implementation Tasks**
   ```
   BLOCK: Issues contain step-by-step HOW
   REASON: Developer breaks down, not Architect
   ACTION: Remove tasks, keep constraints only
   ```

4. **❌ Missing backlog.md**
   ```
   BLOCK: No backlog.md file created
   REASON: Single source of truth required for work breakdown
   ACTION: Create backlog.md with Issues overview table
   ```

5. **❌ Issues Too Large (Not Atomic)**
   ```
   BLOCK: Issue requires >3 days effort or groups unrelated modules
   REASON: Developer needs atomic tasks (1-3 days each)
   ACTION: Break down into smaller, focused Issues
   EXAMPLE: Split "ISSUE-002: 5 modules" into 5 separate Issues
   PRINCIPLE: Each Issue = single responsibility, completable in 1-3 days
   ```

6. **❌ Insufficient Options in ADR**
   ```
   BLOCK: ADR has < 3 options
   REASON: Need true evaluation of alternatives
   ACTION: Add more options with trade-offs
   ```

7. **❌ arc42 Sections Missing (for scope)**
   ```
   BLOCK: MVP missing required sections 1-7
   REASON: Incomplete architecture documentation
   ACTION: Complete all required sections
   ```

8. **❌ Over-Granular Issues (Simple Test)**
   ```
   BLOCK: 10+ Issues for Simple Test project
   REASON: Over-engineering, too much overhead
   ACTION: Group related modules into fewer Issues (1-3 typical)
   EXAMPLE: One Issue can contain 5 modules (parser, resolver, uploader, etc.)
   ```

---

## 💬 Validation Message Formats

### Success Format:

```
✅ {DOCUMENT TYPE} Validation Passed

File: {filepath}
Project Scope: {Simple Test / PoC / MVP}

Validations Passed:
  ✅ {Check 1}
  ✅ {Check 2}
  ✅ {Check 3}

Status: Ready for {next step}
```

### Warning Format:

```
⚠️ {DOCUMENT TYPE} Quality Warnings

File: {filepath}
Non-Blocking Issues: {count}

⚠️ {Warning 1 - description}
   Recommendation: {suggestion}

⚠️ {Warning 2 - description}
   Recommendation: {suggestion}

Status: Acceptable but could improve
Consider addressing warnings for better quality.
```

### Critical Block Format:

```
❌ CRITICAL: {DOCUMENT TYPE} BLOCKED

File: {filepath}
Blocking Issues: {count}

{Issue Number}. ❌ {Issue Title}
   Found: {what was found}
   Required: {what's needed}
   
   → Action: {specific fix}

CANNOT PROCEED until all blocking issues resolved!
```

---

## 🔄 Integration with Chatmode

**Architect Chatmode triggers these validations automatically when:**

1. Creating ADRs → ADR validation
2. Generating arc42 → arc42 validation
3. Creating issues → Issue validation
4. Creating handover → Handover validation

**Validation Flow:**

```
Architect creates document
  ↓
Automatic validation triggered
  ↓
If validation fails ❌
  → Show specific errors
  → Provide fix suggestions
  → BLOCK until fixed
  
If validation passes ✅
  → Continue to next phase
```

**Self-Checks at Each Phase:**

Architect chatmode includes self-check sections at end of each phase:
- Phase 1: Requirements analysis
- Phase 2: Architecture intake
- Phase 3: ADRs
- Phase 4: arc42
- Phase 5: Issues
- Phase 6: Handover & QG

These instructions provide the validation logic for those self-checks.

---

## 📊 Quality Gate Automation

### Quality Gate Checklist Generation

Based on project scope, automatically generate appropriate checklist:

**Simple Test QG:**
```markdown
- [ ] ✅ README with setup exists
- [ ] ✅ backlog.md created with Issues overview
- [ ] ✅ Tech stack chosen
- [ ] ✅ 1-3 Issues created (not over-split)
- [ ] ✅ Issues have clear requirements
- [ ] ✅ Consistent terminology (Issue = work unit)
- [ ] ✅ Grouping strategy clear (if Issue contains multiple modules)
```

**PoC QG:**
```markdown
- [ ] ✅ Requirements analysis complete
- [ ] ✅ backlog.md created with full breakdown
- [ ] ✅ 2-5 ADRs (MADR format, 3+ options)
- [ ] ✅ arc42 sections 1,3,4 (minimal complete)
- [ ] ✅ 2-3 diagrams
- [ ] ✅ 5-15 Issues (context + constraints)
- [ ] ✅ Consistent terminology throughout
- [ ] ✅ Handover document complete (refs backlog.md)
```

**MVP QG:**
```markdown
- [ ] ✅ Requirements analysis comprehensive
- [ ] ✅ backlog.md with complete work breakdown
- [ ] ✅ 5-15 ADRs (all major decisions)
- [ ] ✅ arc42 sections 1-7 (complete)
- [ ] ✅ 5-8 diagrams (all key views)
- [ ] ✅ 15-50 Issues (full context, appropriate granularity)
- [ ] ✅ Dependencies mapped in backlog.md
- [ ] ✅ Performance/security quantified
- [ ] ✅ Consistent terminology (Issue vs Module)
- [ ] ✅ Handover comprehensive (refs backlog.md)
```

---

## 📚 Reference Templates

### MADR Template Location
Full template: https://adr.github.io/madr/

### arc42 Template Location
Full template: https://arc42.org/

### Best Practices Resources
- ADR Best Practices: https://github.com/joelparkerhenderson/architecture-decision-record
- C4 Model: https://c4model.com/
- Mermaid Diagrams: https://mermaid.js.org/

---

## 📝 Summary

These instructions ensure:

✅ **Appropriate Complexity** - Match architecture depth to project scope
✅ **Decision Documentation** - ADRs in MADR format with 3+ options
✅ **Comprehensive Docs** - arc42 sections appropriate to scope
✅ **Clear Boundaries** - Issues define WHAT, preserve developer autonomy
✅ **Consistent Terminology** - Issue = work unit, Module = technical unit
✅ **Single Source of Truth** - backlog.md required for all projects
✅ **Appropriate Granularity** - Don't over-split Simple Test into 10+ Issues
✅ **Quality Gates** - Automatic validation before handover
✅ **Consistency** - All architects follow same standards

**Goal:** Enable Architect to produce high-quality, scope-appropriate architecture with clear work breakdown that Developer can immediately execute on.

**Critical Rules:**
- ✅ ALWAYS create backlog.md (single overview document)
- ✅ Use consistent terminology (Issue = work unit, not Feature)
- ✅ Simple Test: 1-3 Issues (can group modules), not 10+ Issues
- ✅ Each Issue can contain multiple modules (reduces overhead)
- ✅ Backlog.md shows clear hierarchy and grouping strategy

---

**Version:** 1.1
**Last Updated:** 2025-11-02
**Integration:** Works with architect.chatmode.md
**Critical Features:** 
  - Adaptive validation based on project scope
  - Mandatory backlog.md creation
  - Consistent Issue/Module terminology
