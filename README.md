Digital Innovation Agents

AI-Powered Software Development Workflow - From idea to production-ready code through structured, quality-gated phases.

A comprehensive system of specialized AI agents that guide software development from initial business concept through requirements engineering, architecture design, implementation, and debugging. Built for GitHub Copilot with automated quality gates and validation.

🎯 What This Is
Digital Innovation Agents transforms how software is built by providing a structured, agent-based workflow that ensures quality at every stage. Instead of jumping straight into code, projects follow a systematic path:
Business Idea → Requirements → Architecture → Implementation → Quality Assurance
     ↓              ↓              ↓              ↓                ↓
   BA Agent    RE Agent    Architect Agent  Developer Agent  Debugger Agent
Each agent specializes in one phase, has built-in quality checks, and produces standardized outputs that feed into the next phase.

🤖 The Five Agents
1. Business Analyst (@business-analyst)
Role: Transform raw ideas into structured business requirements
When to use:

Starting a new project from scratch
Have a problem but unclear on the solution
Need to explore requirements systematically

Input: Raw project idea or problem description
Output: docs/business-analysis/BA-[PROJECT].md
Key Features:

Scope detection (Simple Test / PoC / MVP)
Structured interviews (5-50 questions based on scope)
Jobs-to-be-Done analysis
Value proposition development
Success metrics definition


2. Requirements Engineer (@requirements-engineer)
Role: Convert business analysis into architect-ready requirements
When to use:

Have a business analysis document
Need structured epics and features
Ready to define technical requirements

Input: Business Analysis document OR direct user input
Output:

requirements/epics/EPIC-*.md
requirements/features/FEATURE-*.md
requirements/handoff/architect-handoff.md

Key Features:

Epic creation with hypothesis statements
Feature breakdown with acceptance criteria
NFR quantification (Performance, Security, Scalability)
ASR identification (Architecture-Significant Requirements)
Comprehensive architect handoff package

Quality Gate 1 (QG1):

✅ All NFRs quantified (with numbers!)
✅ All ASRs identified and marked (🔴/🟡)
✅ Acceptance criteria testable
✅ Architect handoff complete


3. Architect (@architect)
Role: Design technical architecture and create developer-ready issues
When to use:

Requirements are complete (QG1 passed)
Need architectural decisions documented
Ready to plan implementation

Input: requirements/handoff/architect-handoff.md
Output:

docs/decisions/ADR-*.md (Architecture Decision Records in MADR format)
docs/arc42/ARC42-DOCUMENTATION.md (arc42 architecture docs)
backlog/ISSUE-*.md (Developer-ready issues)
backlog/Backlog.md (Single source of truth for work breakdown)

Key Features:

Adaptive complexity (Simple Test / PoC / MVP)
ADR creation with research (web_search + @azure)
arc42 documentation (sections 1-7 for MVP)
Atomic issue creation (1-3 days each)
System design with Mermaid diagrams

Quality Gate 2 (QG2):

✅ ADRs for all major decisions (MADR format, 3+ options)
✅ arc42 complete for scope
✅ Atomic issues created (clear single responsibility)
✅ Backlog.md created (work overview)
✅ Developer handoff complete


4. Developer (@developer)
Role: Implement atomic tasks with mandatory testing
When to use:

Architecture complete (QG2 passed)
Ready to write code
Have developer-ready issues in backlog

Input: Issues from backlog/ISSUE-*.md
Output:

Production code (src/**/*)
Test code (tests/**/*)
Error logs if tests fail (logs/ERROR-TASK-*.md)

Key Features:

5-Phase Streamlined Workflow:

Task Analysis & Setup
Implementation (code + tests)
Testing & Validation (ALL tests MANDATORY)
Validation & Commit
Completion & Metrics



Quality Gate 3 (QG3):

✅ ALL tests written (from task test plan)
✅ ALL tests executed (full suite)
✅ ALL tests passing OR error log created
✅ Coverage ≥90%
✅ Clean code principles applied
✅ No TODOs or placeholders

Critical Rule: Tests are MANDATORY, not optional!

5. Debugger (@debugger)
Role: Systematic error analysis and resolution
When to use:

Tests failed after implementation
Have error log from Developer
Need root cause analysis

Input: logs/ERROR-TASK-*.md
Output:

Fixed code
Updated tests
Resolution documentation

Key Features:

Fast Path: Simple fixes in minutes (typos, missing imports)
Systematic Path: Complex issues with full analysis

Root cause identification (not symptoms!)
Fix strategy with multiple options
Comprehensive testing
No regressions



Quality Gate Debug (QGD):

✅ Root cause identified (not symptom)
✅ Clean fix (no workarounds)
✅ ALL tests run and passing
✅ No regressions
✅ Resolution documented


📁 Repository Structure
digital-innovation-agents/
├── .github/
│   ├── chatmodes/                    # Agent definitions
│   │   ├── business-analyst.chatmode.md
│   │   ├── requirements-engineer.chatmode.md
│   │   ├── architect.chatmode.md
│   │   ├── developer.chatmode.md
│   │   └── debugger.chatmode.md
│   │
│   ├── instructions/                 # Auto-validation rules
│   │   ├── architect.instructions.md
│   │   ├── developer.instructions.md
│   │   ├── debugger.instructions.md
│   │   └── requirements-engineer.instructions.md
│   │
│   ├── templates/                    # Document templates
│   │   ├── EPIC-TEMPLATE.md
│   │   ├── FEATURE-TEMPLATE.md
│   │   ├── ISSUE-TEMPLATE.md
│   │   ├── BUGFIX-TEMPLATE.md
│   │   └── IMPROVEMENT-TEMPLATE.md
│   │
│   └── copilot-instructions.md       # Global agent overview
│
├── docs/                             # Documentation outputs
│   ├── business-analysis/            # BA outputs
│   ├── decisions/                    # ADRs from Architect
│   └── arc42/                        # Architecture docs
│
├── requirements/                     # RE outputs
│   ├── epics/                        # EPIC-*.md
│   ├── features/                     # FEATURE-*.md
│   └── handoff/                      # architect-handoff.md
│
├── backlog/                          # Architect outputs
│   ├── Backlog.md                    # THE single source of truth
│   └── ISSUE-*.md                    # Developer-ready issues
│
├── src/                              # Developer outputs (code)
├── tests/                            # Developer outputs (tests)
└── logs/                             # Error logs (when tests fail)

🚀 Getting Started
Prerequisites

GitHub Copilot with Chat enabled
Project with .github/chatmodes/ directory
Understanding of your project scope (Simple Test / PoC / MVP)

Quick Start
Option 1: Starting from Scratch (No Requirements)
Step 1: Use @business-analyst
→ Conducts structured discovery interview
→ Creates business analysis document

Step 2: Use @requirements-engineer  
→ Reads BA document
→ Creates epics, features, architect handoff

Step 3: Use @architect
→ Creates ADRs, arc42 docs, issues
→ Prepares backlog

Step 4: Use @developer
→ Implements issues with mandatory tests

Step 5: Use @debugger (if tests fail)
→ Fixes issues systematically
Option 2: Starting with Requirements
Skip @business-analyst

Step 1: Use @requirements-engineer directly
→ Conducts scope-specific intake
→ Creates epics, features, handoff

[Continue with Steps 3-5 above]
Option 3: Starting with Architecture
Skip @business-analyst and @requirements-engineer

Step 1: Use @architect with your requirements
→ Creates architecture artifacts

[Continue with Steps 4-5 above]

💡 Example Usage
Starting a New Project
markdownUser: I want to build a Notion importer that processes markdown files

AI: [Detects @business-analyst should be used]

@business-analyst:
🎯 What are you developing?
A) Simple Test/Quick Script
B) Proof of Concept (PoC)  
C) Minimum Viable Product (MVP)
D) Own description

User: B - I want to validate technical feasibility

@business-analyst: [Conducts 15-25 questions interview]
→ Creates: docs/business-analysis/BA-notion-importer.md

---

User: Create requirements based on the BA document

@requirements-engineer: [Reads BA document]
→ Creates: requirements/epics/EPIC-001-content-migration.md
→ Creates: requirements/features/FEATURE-001-markdown-import.md
→ Creates: requirements/features/FEATURE-002-asset-upload.md
→ Creates: requirements/handoff/architect-handoff.md

Quality Gate 1 ✅ PASSED

---

User: Design the architecture

@architect: [Reads architect-handoff.md]
→ Creates: docs/decisions/ADR-001-markdown-parser-choice.md
→ Creates: docs/arc42/ARC42-DOCUMENTATION.md (sections 1,3,4 for PoC)
→ Creates: backlog/Backlog.md
→ Creates: backlog/ISSUE-001-markdown-parser.md
→ Creates: backlog/ISSUE-002-frontmatter-extractor.md
[... 10-30 atomic issues total]

Quality Gate 2 ✅ PASSED

---

User: Implement ISSUE-001

@developer: [Reads ISSUE-001-markdown-parser.md]
→ Phase 1: Analyzes task
→ Phase 2: Implements code + writes tests
→ Phase 3: Runs ALL tests
  → Result: 2 tests failing ❌
→ Creates: logs/ERROR-TASK-001-2025-11-05-1430.md
→ Notifies: @debugger
→ STOPS task execution

---

User: @debugger fix the error

@debugger: [Reads ERROR-TASK-001-2025-11-05-1430.md]
→ Root Cause Analysis: Missing import statement
→ Fast Path: Simple fix in 5 minutes
→ Fixes code, runs ALL tests
→ All tests passing ✅
→ Updates error log with resolution
→ Notifies: @developer can continue

Quality Gate Debug ✅ PASSED

---

User: Continue implementation

@developer: [Resumes from Phase 3]
→ All tests passing ✅
→ Phase 4: Validates acceptance criteria
→ Phase 5: Commits with informative message
→ Task ISSUE-001 complete ✅

Quality Gate 3 ✅ PASSED
```

---

## 🎯 Key Principles

### 1. **Adaptive Complexity**
Architecture depth matches project scope:
- **Simple Test:** Minimal (hours-days)
- **PoC:** Focused (1-4 weeks)
- **MVP:** Comprehensive (2-6 months)

### 2. **Quality Gates**
No phase proceeds until quality criteria met:
- **QG1:** Requirements ready for architecture
- **QG2:** Architecture ready for development
- **QG3:** Code ready for production
- **QGD:** Bugs fixed without regressions

### 3. **Test-First Development**
- Write tests AS you code (not after)
- Execute ALL tests (not just affected)
- 100% pass rate OR error log created
- Coverage ≥90% maintained

### 4. **Clean Separation**
- **BA:** WHAT problem (business view)
- **RE:** WHAT to build (requirements view)
- **Architect:** HOW to structure (architectural view)
- **Developer:** HOW to implement (code view)
- **Debugger:** WHY it failed (root cause view)

### 5. **Atomic Work Units**
- Issues are small (1-3 days max)
- Single responsibility per issue
- Clear acceptance criteria
- Independent and testable

---

## 📊 Quality Standards

### Requirements Engineering
- ✅ All NFRs quantified (no vague "fast" or "secure")
- ✅ All ASRs identified and marked (🔴 Critical / 🟡 Moderate)
- ✅ Acceptance criteria testable (pass/fail)
- ✅ Traceability to business goals

### Architecture
- ✅ ADRs in MADR format (3+ options, pros/cons, research links)
- ✅ arc42 complete for scope (Simple Test: skip, PoC: 1,3,4, MVP: 1-7)
- ✅ Issues atomic (1-3 days each)
- ✅ Backlog.md as single source of truth

### Development
- ✅ Tests written during implementation
- ✅ ALL tests executed (full suite)
- ✅ Clean code (type hints, docstrings, no TODOs)
- ✅ Coverage ≥90%

### Debugging
- ✅ Root cause identified (not symptom)
- ✅ Clean fix (no workarounds)
- ✅ Comprehensive testing (no regressions)
- ✅ Learnings documented

---

## 🔧 Configuration

### Enable Agents in Your Project

1. **Copy the `.github/` directory** to your project root

2. **Customize chatmodes** (optional):
   - Edit `.github/chatmodes/*.chatmode.md` for your needs
   - Adjust complexity levels
   - Add/remove tools

3. **Use in GitHub Copilot Chat:**
```
   @business-analyst [your request]
   @requirements-engineer [your request]
   @architect [your request]
   @developer [your request]
   @debugger [your request]
Agent Selection in Copilot
GitHub Copilot automatically detects available agents from .github/chatmodes/ and presents them in the agent picker.

📚 Documentation

Global Overview - Complete workflow and agent integration
Business Analyst Guide - Discovery and ideation
Requirements Engineer Guide - Epics and features
Architect Guide - ADRs and system design
Developer Guide - Test-driven implementation
Debugger Guide - Systematic debugging

Validation Rules

Architect Instructions - ADR and arc42 validation
Developer Instructions - Test enforcement
Debugger Instructions - Error log validation
RE Instructions - NFR and ASR validation

Templates

Epic Template
Feature Template
Issue Template
Bugfix Template
Improvement Template


🎓 Best Practices
When to Use Which Agent
Use @business-analyst when:

❓ Starting with a vague idea
🆕 New project from scratch
🤔 Need to explore problem space

Use @requirements-engineer when:

📄 Have business analysis document
✍️ Have clear requirements but need structure
🎯 Want to skip discovery and jump to features

Use @architect when:

🏗️ Requirements complete (QG1 passed)
📋 Need technical design decisions
🔧 Ready to plan implementation

Use @developer when:

💻 Architecture complete (QG2 passed)
📝 Have developer-ready issues
🧪 Ready to implement with tests

Use @debugger when:

🐛 Tests failing
📋 Have error log from Developer
🔍 Need systematic root cause analysis

Common Pitfalls to Avoid
❌ DON'T:

Skip quality gates (they catch problems early!)
Write code without tests
Use vague NFRs ("fast", "secure")
Create oversized issues (>3 days)
Commit with failing tests

✅ DO:

Follow the workflow sequentially
Let each agent do its job
Quantify all NFRs with numbers
Keep issues atomic (1-3 days)
Run ALL tests before commit


🤝 Contributing
This is an evolving system. Contributions welcome for:

New agent types
Improved validation rules
Additional templates
Documentation improvements
Bug fixes


📄 License
[Add your license here]

🙏 Acknowledgments
Built with:

GitHub Copilot Chat Modes
Inspired by SAFe Framework (Epics, Features)
arc42 Architecture Documentation
MADR (Markdown Architectural Decision Records)
Clean Code Principles
Test-Driven Development
