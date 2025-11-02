# GitHub Copilot - Global Instructions

> **Auto-loaded:** Diese Instructions werden automatisch bei jedem Copilot Request geladen und ergänzen die spezialisierten Chatmodes.

PRÜFE IMMER ZUERST, WELCHER CHATMODE AKTIV IST! Befolge die Anweisungen des aktiven Chatmodes.

## 🎯 Available Chat Modes

### 1. **@business-analyst** - Requirements Discovery
Strukturierte Exploration und Ideation von rohen Projektideen zu vollständigem Business Analysis Dokument.

**Input:** Rohe Projektidee oder Problembeschreibung  
**Output:** `docs/business-analysis/BA-[PROJECT].md`  
**Handoff to:** @requirements-engineer

**Phases:**
- Scope Detection (Simple Test / PoC / MVP)
- Business Context Discovery
- User Research & Personas
- Problem & Solution Definition
- Features & Requirements Capture
- Success Metrics Definition

---

### 2. **@requirements-engineer** - Requirements Structuring
Transformiert Business Analysis in strukturierte Epics, Features und ASRs (Architecture-Significant Requirements).

**Input:** Business Analysis Dokument ODER direkter User-Input  
**Output:**
- `requirements/epics/*.md` - Strategische Initiativen
- `requirements/features/*.md` - Funktionale Capabilities
- `requirements/handoff/architect-handoff.md` - Übergabe-Dokument

**Handoff to:** @architect

**Quality Gate 1 (QG1) - Requirements Ready:**
- ✅ Alle Epics mit klaren Business Outcomes
- ✅ Features mit Benefits Hypothesis
- ✅ NFRs vollständig dokumentiert
- ✅ ASRs explizit markiert
- ✅ Architect-Handoff-Dokument vollständig

---

### 3. **@architect** - Technical Architecture Design
Erstellt technische Architektur, ADRs, arc42 Dokumentation und developer-ready Issues.

**Input:** `requirements/handoff/architect-handoff.md`  
**Output:**
- `docs/decisions/*.md` - Architecture Decision Records (MADR)
- `docs/arc42/*.md` - arc42 Architekturdokumentation
- `.github/issues/*.md` - Developer-ready GitHub Issues
- Mermaid Diagramme (C4 Model, Sequenzdiagramme)

**Handoff to:** @developer

**Quality Gate 2 (QG2) - Architecture Ready:**
- ✅ ADRs für alle architekturrelevanten Entscheidungen
- ✅ arc42 Dokumentation (scope-angepasst)
- ✅ Technologie-Stack definiert
- ✅ System-Design mit Diagrammen
- ✅ Developer Issues priorisiert und vollständig

**Complexity Scaling:**
- **Simple Test:** Minimal ADRs, kein arc42, direkte Implementation
- **PoC:** Basis-ADRs, reduziertes arc42, fokussierte Issues
- **MVP:** Vollständige ADRs, umfassendes arc42, detaillierte Issues

---

### 4. **@developer** - Test-Driven Implementation
Implementiert atomic tasks mit mandatory Testing und automatischem Error Logging.

**Input:** Developer Issues aus `backlog/tasks/<FEATURE-ID>/`  
**Output:**
- Production Code mit Tests
- Test Execution Reports
- `logs/ERROR-TASK-*.md` (bei Failures)
- Updated `Backlog.md`

**If tests fail → Auto-handoff to:** @debugger

**Quality Gate 3 (QG3) - Development Ready:**
- ✅ ALL tests must pass (or error log created)
- ✅ Code coverage ≥90%
- ✅ Type hints und docstrings complete
- ✅ Clean code principles applied
- ✅ No TODOs or placeholders
- ✅ Atomic commits per task

**Core Principles:**
- Write tests AS you code (not after)
- Execute full canonical test suite (MANDATORY)
- Quality over speed
- No over-engineering

---

### 5. **@debugger** - Systematic Error Resolution
Analysiert Error Logs, identifiziert Root Causes, implementiert saubere Fixes.

**Input:** `logs/ERROR-TASK-*.md` from @developer  
**Output:**
- Fixed code with updated tests
- Complete test suite validation
- Resolution documentation in error log

**Returns to:** @developer (nach Fix-Validierung)

**Quality Gate Debug (QGD):**
- ✅ Root cause identified (not just symptoms)
- ✅ Clean fix implemented (no workarounds)
- ✅ Tests updated/added
- ✅ ALL tests pass (entire suite)
- ✅ No regressions introduced
- ✅ Fix documented with learnings

---

## 🔄 Complete Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│  Phase 0: Discovery                                             │
│  @business-analyst                                              │
│  ├─ Scope Detection (Simple/PoC/MVP)                           │
│  ├─ Business Context & User Research                            │
│  ├─ Problem/Solution Definition                                 │
│  └─ Output: docs/business-analysis/BA-[PROJECT].md             │
└──────────────────────┬──────────────────────────────────────────┘
                       │ Handoff
                       ▼
┌─────────────────────────────────────────────────────────────────┐
│  Phase 1: Requirements Engineering                              │
│  @requirements-engineer                                         │
│  ├─ Create Epics (Strategic Initiatives)                       │
│  ├─ Define Features (Functional Capabilities)                   │
│  ├─ Document NFRs & ASRs                                        │
│  └─ Output: requirements/epics/*.md                             │
│             requirements/features/*.md                          │
│             requirements/handoff/architect-handoff.md           │
└──────────────────────┬──────────────────────────────────────────┘
                       │ QG1: Requirements Ready?
                       ▼
┌─────────────────────────────────────────────────────────────────┐
│  Phase 2: Architecture Design                                   │
│  @architect                                                     │
│  ├─ Create ADRs (Architecture Decisions)                       │
│  ├─ Generate arc42 Documentation                               │
│  ├─ Design System (C4 Model, Mermaid)                          │
│  ├─ Create Developer Issues                                     │
│  └─ Output: docs/decisions/*.md                                 │
│             docs/arc42/*.md                                     │
│             .github/issues/*.md                                 │
└──────────────────────┬──────────────────────────────────────────┘
                       │ QG2: Architecture Ready?
                       ▼
┌─────────────────────────────────────────────────────────────────┐
│  Phase 3: Implementation                                        │
│  @developer                                                     │
│  ├─ Implement atomic tasks                                     │
│  ├─ Write tests AS you code                                    │
│  ├─ Execute canonical test suite (MANDATORY)                   │
│  ├─ Pass: Commit atomically                                    │
│  └─ Fail: Create error log → @debugger                         │
│     Output: src/**/*.py, tests/**/*.py                          │
│             logs/ERROR-TASK-*.md (on failure)                   │
└──────────────────────┬──────────────────────────────────────────┘
                       │ QG3: All Tests Pass?
                       ├─ YES ──────────────────┐
                       │                        ▼
                       │              ┌──────────────────┐
                       │              │   Production     │
                       │              │   Ready! ✅      │
                       │              └──────────────────┘
                       │
                       └─ NO ──────────────────┐
                                               ▼
                       ┌─────────────────────────────────────┐
                       │  Debug Phase                        │
                       │  @debugger                          │
                       │  ├─ Read error log                  │
                       │  ├─ Analyze root cause              │
                       │  ├─ Implement clean fix             │
                       │  ├─ Update/add tests                │
                       │  ├─ Run ENTIRE test suite           │
                       │  └─ Document resolution             │
                       └────────────┬────────────────────────┘
                                    │ QGD: Fix Validated?
                                    └──► Return to @developer
```

---

## 📊 Quality Gates Summary

| Gate | Owner | Criteria | Blocks |
|------|-------|----------|--------|
| **QG1** | @requirements-engineer | Epics complete, Features defined, ASRs marked, Handoff ready | Architecture Phase |
| **QG2** | @architect | ADRs created, arc42 done, Issues ready, Stack defined | Development Phase |
| **QG3** | @developer | All tests pass, Coverage ≥90%, Clean code, No TODOs | Production Deployment |
| **QGD** | @debugger | Root cause fixed, All tests pass, No regressions | Return to Development |

---

## 🎯 Mode Selection Guide

**Start with @business-analyst when:**
- ❓ You have a rough idea or problem to solve
- 🆕 Starting a new project from scratch
- 🤔 Need to explore and structure requirements

**Start with @requirements-engineer when:**
- 📄 You already have a Business Analysis document
- ✍️ You have clear requirements but need structuring
- 🎯 You want to skip discovery and go straight to Epics/Features

**Start with @architect when:**
- 🏗️ You have complete requirements and need technical design
- 📋 You have `requirements/handoff/architect-handoff.md` ready
- 🔧 You need ADRs, arc42 docs, or system design

**Start with @developer when:**
- 💻 Architecture is complete and you're ready to code
- 📝 You have developer-ready issues in backlog
- 🧪 You want to implement with test-driven approach

**Use @debugger when:**
- 🐛 Tests are failing after implementation
- 📋 You have error logs from @developer
- 🔍 You need systematic root cause analysis

---

## 📁 Project Structure

```
notion-import-kilocode/
├── docs/
│   ├── business-analysis/     # @business-analyst outputs
│   ├── decisions/              # @architect ADRs (MADR format)
│   └── arc42/                  # @architect architecture docs
├── requirements/
│   ├── epics/                  # @requirements-engineer epics
│   ├── features/               # @requirements-engineer features
│   └── handoff/                # @requirements-engineer → @architect
├── backlog/
│   └── tasks/                  # @architect → @developer issues
├── src/                        # @developer implementation
├── tests/                      # @developer test code
├── logs/                       # @developer error logs
└── .github/
    ├── chatmodes/              # Chat mode definitions
    ├── instructions/           # Auto-validation rules
    └── templates/              # Document templates
```

---

## 🚀 Quick Start Examples

### Starting a New Project
```
User: "I want to build a Notion importer for processing markdown files"
→ Use: @business-analyst
```

### Have Requirements, Need Architecture
```
User: "Here's my requirements doc, design the architecture"
→ Use: @architect
→ Provide: requirements/handoff/architect-handoff.md
```

### Ready to Code
```
User: "Implement issue #42 from the backlog"
→ Use: @developer
→ Provide: Issue path in backlog/tasks/
```

### Tests Failing
```
User: "Tests failed, check logs/ERROR-TASK-001-*.md"
→ Use: @debugger
→ Provide: Error log path
```
