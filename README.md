# Digital Innovation Agents

> **AI-augmented Innovation & Development Workflow** -- From raw idea to production-ready code through structured, quality-gated phases.

A system of specialized AI agents that guide digital innovation from initial business concept through requirements engineering, architecture design, implementation, testing, and security audit. Integrates proven innovation methods (EXPLORATION, IDEATION, VALIDATION) with structured software engineering. Available for **Claude Code** and **GitHub Copilot**.

---

## What This Is

**Digital Innovation Agents** provides a structured, agent-based workflow for building digital products. Instead of jumping straight into code, projects follow a systematic path through innovation and engineering phases:

```
EXPLORATION -> IDEATION -> VALIDATION -> Requirements -> Architecture -> Code -> Test -> Security
    |          |          |           |              |            |       |         |
  Understand  Design    Validate    Formalize     Decide      Build   Verify    Harden
  the problem the idea  the market  what to build  how         it      it        it
```

Each agent specializes in one phase, has built-in quality checks, and produces standardized outputs that feed into the next phase.

### Innovation Methods Built In

The Business Analysis agent uses structured innovation methods to deeply understand problems before solving them:

- **EXPLORE phase**: Qualitative interviews, persona synthesis, user motivation analysis, stakeholder mapping, market trend analysis, user journeys, and more -- with probing techniques when interview partners give thin answers
- **IDEATION phase**: Jobs to be Done, idea potential assessment (value, transferability, feasibility), critical hypotheses, the "Wow" feature, and value proposition synthesis
- **EVALUATE phase**: Value proposition scoring, 6-axis assessment radar, pricing analysis, channel strategy, unfair advantage, revenue streams, and business viability testing

All methods include concrete guidance on **how to conduct them** and **what to do when you get stuck** -- see [innovation-methods.md](claude-code-skills/business-analyse/references/innovation-methods.md).

---

## Quick Start

### Option A: Claude Code (Recommended)

Works in **Claude Code CLI**, **VS Code**, and **JetBrains**.

**Step 1 -- Download the repository**

If you have Git installed:
```bash
git clone https://github.com/pssah4/digital-innovation-agents.git
```

Or download as ZIP from GitHub: Click the green **"Code"** button, then **"Download ZIP"**, and unzip the folder.

**Step 2 -- Run the installer**

Open a terminal, navigate to the downloaded folder, and run:

```bash
cd digital-innovation-agents/claude-code-skills
chmod +x install-skills.sh
./install-skills.sh
```

This copies all skills to `~/.claude/skills/` where Claude Code picks them up automatically.

**Step 3 -- Verify**

Open Claude Code (terminal, VS Code, or JetBrains) and type `/`. Your skills should appear in the autocomplete dropdown. If they don't appear in VS Code or JetBrains, close and reopen the Claude Code panel.

**Step 4 -- Start using**

```
/business-analyse          -- Start a structured business analysis
/v-model-workflow          -- Full guided cycle from idea to security audit
```

### Option B: Claude Desktop App

**Step 1 -- Download the repository** (same as above)

**Step 2 -- Add skills via the UI**

1. Open the Claude Desktop App
2. Go to **Customize** (bottom-left gear icon) -> **Skills**
3. Click the **"+"** button
4. Upload each skill folder from `claude-code-skills/` (one at a time)

Alternatively, copy the skill folders manually to `~/.claude/skills/` -- the desktop app reads from the same location.

### Option C: Use Without Installing (Any Claude Environment)

You can use the templates and methods without installing skills. Simply:

1. Open any Claude conversation
2. Copy the content of [BA-TEMPLATE.md](claude-code-skills/business-analyse/templates/BA-TEMPLATE.md) or [EXPLORATION-BOARD.md](claude-code-skills/business-analyse/templates/EXPLORATION-BOARD.md) into your message
3. Ask Claude to help you fill it out based on your project

The [innovation-methods.md](claude-code-skills/business-analyse/references/innovation-methods.md) reference works as a standalone guide in any conversation.

### Option D: GitHub Copilot

**Step 1** -- Copy the `.github/` directory to your project root. Agents are automatically detected by Copilot.

**Step 2** -- Use agents in Copilot Chat:

```
@business-analyst I want to build a tool that helps teams run better retrospectives
@requirements-engineer Here is my BA document, create epics and features
@architect Design the architecture based on the requirements handoff
@developer Implement the first feature
@debugger Tests are failing, analyze the error log
```

The Copilot agents have the same EXPLORATION/IDEATION/VALIDATION innovation workflow, the same templates, and the same quality gates as the Claude Code skills.

---

## The Agents

| Phase | What It Does | Claude Code | Copilot |
|-------|-------------|-------------|---------|
| **Business Analysis** | EXPLORATION/IDEATION/VALIDATION innovation cycle, structured interviews, problem analysis | `/business-analyse` | `@business-analyst` |
| **Requirements** | Epics, features, tech-agnostic success criteria, jobs-to-be-done | `/requirements-engineering` | `@requirements-engineer` |
| **Architecture** | ADRs (MADR), arc42, plan-context.md | `/architecture` | `@architect` |
| **Implementation** | Context handoff, critical review, artifact writeback | `/coding` | `@developer` |
| **Testing** | Unit and integration tests with fix-loop | `/testing` | built-in |
| **Security Audit** | OWASP Top 10, LLM Top 10, SAST, SCA, Zero Trust | `/security-audit` | `@security-auditor` |
| **Debugging** | Root cause analysis, systematic error resolution | -- (default) | `@debugger` |
| **Orchestrator** | Guides through all phases step by step | `/v-model-workflow` | -- |
| **Conventions** | Project structure and naming standards | `/project-conventions` | -- |

---

## The Flow

### Innovation Phases (Business Analysis)

The BA agent guides you through three innovation phases before a single line of code is written:

```
/business-analyse
  Phase 1: EXPLORE -- Understand the problem space
    - Users, needs, insights, trends, competitors
    - Output: Exploration Board + How-Might-We question
    
  Phase 2: IDEATION -- Design the solution
    - Idea potential, the Wow, critical hypotheses, value proposition
    - Output: Solution concept with validation plan
    
  Phase 3: EVALUATE -- Test business viability
    - VP score, assessment radar, pricing, channels, revenue
    - Output: Market assessment

  Final: BA Document
    Output: _devprocess/analysis/BA-{PROJECT}.md
           _devprocess/analysis/EXPLORE-{PROJECT}.md
```

### Design Phases (Left Side of the V)

```
/requirements-engineering
  Input:  BA document (HMW, needs, jobs-to-be-done, hypotheses)
  Output: Epics, Features, architect-handoff.md
    |
    v
/architecture
  Input:  Features, ASRs, NFRs
  Output: ADRs, arc42, plan-context.md
```

### Implementation (Bottom of the V)

```
/coding
  Input:  plan-context.md + ADRs + Features
  1. Load context from design phases
  2. Critical review against real codebase
  3. Write changes back to artifacts
  4. Implementation
  5. Final sync -- artifacts reflect what was actually built
```

### Verification (Right Side of the V)

```
/testing
  Output: Unit tests, integration tests (with fix-loop)

/security-audit
  Output: Security report with remediation plan (with fix-loop)
```

---

## Key Design Principles

**Innovation Before Engineering**: Understand the problem deeply (EXPLORATION), design a validated solution (IDEATION), and test business viability (VALIDATION) before writing requirements.

**Codebase-Awareness**: Every agent reads the existing codebase before producing output. Your project's `CLAUDE.md` always takes precedence.

**Living Documents**: ADRs, features, and architecture docs are continuously updated during implementation. Documentation always reflects what was actually built.

**Tech-Agnostic Success Criteria**: Requirements separate *what* (measurable, technology-free) from *how* (technical NFRs). No OAuth, REST, or PostgreSQL in success criteria -- those go into Technical NFRs for the architect.

**Built-In Probing Techniques**: When interview partners give thin answers, the BA agent suggests concrete follow-up techniques: 5-Why, concretization, future projection, perspective shift, emotional probing, and analogy triggers.

**Quality Gates**: No phase proceeds until quality criteria are met. Each agent validates its own output before handoff.

---

## Scope Levels

The BA agent adapts its depth to your project scope:

| Scope | EXPLORATION | IDEATION | VALIDATION | Typical Duration |
|-------|---------|--------|----------|-----------------|
| **Simple Test** | Minimal (user + problem) | Describe solution | Skip | Hours to 1-2 days |
| **PoC** | Shortened (user, needs, HMW) | Full | Hypotheses + feasibility | 1-4 weeks |
| **MVP** | Full (all 10 sections) | Full | Full market assessment | 2-6 months |

---

## File Structure

```
digital-innovation-agents/
├── README.md
├── LICENSE
├── .gitignore
│
├── claude-code-skills/                         # Claude Code Skills
│   ├── install-skills.sh                       # Installer script
│   │
│   ├── project-conventions/                    # Directory structure & naming
│   │   ├── SKILL.md
│   │   └── references/
│   │       ├── codebase-awareness.md
│   │       ├── directory-structure.md
│   │       └── naming-conventions.md
│   │
│   ├── business-analyse/                       # EXPLORATION/IDEATION/VALIDATION cycle
│   │   ├── SKILL.md
│   │   ├── templates/
│   │   │   ├── BA-TEMPLATE.md                  # Full BA document (12 sections)
│   │   │   └── EXPLORATION-BOARD.md                # Exploration phase board (10 sections)
│   │   └── references/
│   │       └── innovation-methods.md           # 20+ methods with probing techniques
│   │
│   ├── requirements-engineering/               # Epics, features, success criteria
│   │   ├── SKILL.md
│   │   ├── templates/
│   │   │   ├── EPIC-TEMPLATE.md                # With HMW and hypothesis tracking
│   │   │   └── FEATURE-TEMPLATE.md             # With jobs-to-be-done and validation
│   │   └── references/
│   │       └── tech-agnostic-rules.md          # Forbidden terms + transformation guide
│   │
│   ├── architecture/                           # ADRs, arc42, plan-context.md
│   │   ├── SKILL.md
│   │   └── templates/
│   │       ├── ADR-TEMPLATE.md
│   │       ├── arc42-TEMPLATE.md
│   │       └── plan-context-TEMPLATE.md
│   │
│   ├── coding/                                 # Context handoff & artifact writeback
│   │   └── SKILL.md
│   │
│   ├── testing/                                # Unit & integration tests
│   │   ├── SKILL.md
│   │   └── references/
│   │       ├── test-checklist.md
│   │       └── test-anti-patterns.md
│   │
│   ├── security-audit/                         # OWASP, SAST, SCA
│   │   ├── SKILL.md
│   │   ├── templates/
│   │   │   └── AUDIT-TEMPLATE.md
│   │   └── references/
│   │       ├── cwe-patterns.md
│   │       ├── owasp-checklist.md
│   │       └── owasp-llm-checklist.md
│   │
│   └── v-model-workflow/                       # Orchestrator
│       └── SKILL.md
│
└── .github/                                    # GitHub Copilot Agents
    ├── copilot-instructions.md                 # Global instructions (auto-loaded)
    ├── agents/
    │   ├── business-analyst.agent.md           # EXPLORATION/IDEATION/VALIDATION cycle
    │   ├── requirements-engineer.agent.md      # HMW, JTBD, hypothesis tracking
    │   └── architect.agent.md                  # ADRs, arc42, system design
    ├── chatmodes/
    │   ├── business-analyst.chatmode.md        # Same as agent (chat mode format)
    │   ├── requirements-engineer.chatmode.md
    │   ├── developer.chatmode.md               # Test-driven implementation
    │   └── debugger.chatmode.md                # Root cause analysis
    ├── instructions/                           # Auto-validation quality rules
    │   ├── business-analyst.instructions.md    # EXPLORATION/IDEATION/VALIDATION validation
    │   ├── requirements-engineer.instructions.md # HMW, JTBD, hypothesis validation
    │   ├── architect.instructions.md           # ADR, arc42, issue validation
    │   ├── developer.instructions.md           # Test enforcement, code quality
    │   └── debugger.instructions.md            # Fix validation, regression checks
    └── templates/
        ├── EPIC-TEMPLATE.md                    # With HMW and hypothesis tracking
        ├── FEATURE-TEMPLATE.md                 # With JTBD and hypothesis validation
        ├── ISSUE-TEMPLATE.md                   # Atomic issues (1-3 days)
        ├── BUGFIX-TEMPLATE.md                  # Root cause analysis format
        └── IMPROVEMENT-TEMPLATE.md             # Enhancement with ROI
```

---

## Where It Works

| Environment | Skills Support | How to Install |
|-------------|---------------|----------------|
| **Claude Code CLI** | Full | Run `install-skills.sh` |
| **VS Code** (Claude Code extension) | Full | Same -- inherits from `~/.claude/skills/` |
| **JetBrains** (Claude Code plugin) | Full | Same -- inherits from `~/.claude/skills/` |
| **Claude Desktop App** | Supported | Upload via Customize > Skills > "+" |
| **Any Claude conversation** | Manual | Copy templates into your message |
| **GitHub Copilot** | Full (agents) | Copy `.github/` to your project |

---

## Adapt to Your Workflow

These agents reflect a specific workflow. You will want to adjust:

- **Templates**: Edit templates to match your document standards
- **Quality gates**: Tune validation thresholds
- **Naming conventions**: Change file naming patterns in `project-conventions`
- **Testing patterns**: Swap framework examples for your stack
- **Scope levels**: Adjust Simple Test / PoC / MVP complexity settings
- **Innovation methods**: Add or remove methods in `innovation-methods.md`
- **Language**: Skills are in English; your `CLAUDE.md` controls conversation language

---

## Migration Notes: Copilot -> Claude Code

| Copilot Concept | Claude Code Equivalent |
|----------------|----------------------|
| `.github/agents/*.agent.md` | `~/.claude/skills/*/SKILL.md` |
| `.github/instructions/*.instructions.md` | Integrated as Quality Gates in SKILL.md |
| `.github/templates/*.md` | `~/.claude/skills/*/templates/*.md` |
| `@agent-name` | `/skill-name` or natural language |
| `tools:` in frontmatter | Not needed (Claude Code has own tool system) |
| `model:` in frontmatter | Not needed (always current model) |
| `applyTo:` file patterns | Skill description for auto-invocation |

---

## License

MIT License -- Copyright (c) 2025 Sebastian Hanke

See [LICENSE](LICENSE) for details.

---

## Acknowledgments

Built with:
- Claude Code Skills and GitHub Copilot Agents
- Innovation methods inspired by design thinking and lean startup practices
- SAFe Framework (Epics, Features)
- Jobs to be Done Framework
- arc42 Architecture Documentation
- MADR (Markdown Architectural Decision Records)
- OWASP Top 10 and LLM Top 10
- AAA Pattern and FIRST Principles for Testing
