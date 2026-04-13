# Digital Innovation Agents

> **AI-augmented Innovation & Development Workflow.** From raw idea to production-ready code through structured, quality-gated phases.

A system of specialized AI agents that guide digital innovation from initial business concept through requirements engineering, architecture design, implementation, testing, and security audit. Integrates proven innovation methods (Exploration, Ideation, Validation) with structured software engineering. Works across **Claude Code**, **Cursor**, **Codex**, **OpenCode**, **Gemini CLI**, and **GitHub Copilot**.

---

## Versions

| Version | Status | Install |
|---------|--------|---------|
| **v2** (main) | Active, recommended | See Installation below |
| **v1.0.0** | Stable, frozen (legacy) | `./scripts/install-skills.sh --version v1.0.0` |

See [CHANGELOG.md](CHANGELOG.md) for details. v1 is installable as a legacy
snapshot for historical reference but is not actively maintained.

---

## What this is

**Digital Innovation Agents** provides a structured, agent-based workflow for building digital products. Instead of jumping straight into code, projects follow a systematic path through innovation and engineering phases:

<img width="1317" height="675" alt="image" src="https://github.com/user-attachments/assets/c12e5e6d-e46a-4c65-8042-0f82c18db16a" />

Each agent specializes in one phase, has built-in quality checks, and produces standardized outputs that feed into the next phase.

### Innovation methods built in

The Business Analysis agent uses structured innovation methods to deeply understand problems before solving them:

- **Exploration phase**: Qualitative interviews, persona synthesis, user motivation analysis, stakeholder mapping, market trend analysis, user journeys. Includes probing techniques for when interview partners give thin answers.
- **Ideation phase**: Jobs to be Done, idea potential assessment (value, transferability, feasibility), critical hypotheses, the "Wow" feature, and value proposition synthesis
- **Validation phase**: Value proposition scoring, 6-axis assessment radar, pricing analysis, channel strategy, unfair advantage, revenue streams, and business viability testing

All methods include concrete guidance on how to conduct them and what to do when you get stuck. See [innovation-methods.md](skills/business-analyse/references/innovation-methods.md).

<img width="800" height="513" alt="image" src="https://github.com/user-attachments/assets/43ed2ff6-e59e-497f-9f89-cd79267cdd18" />

---

## Installation

Digital Innovation Agents works on multiple AI coding platforms. Install
via the plugin mechanism of your choice:

### Claude Code (recommended)

```bash
/plugin marketplace add pssah4/digital-innovation-agents
/plugin install digital-innovation-agents@pssah4-skills
```

Start a new session and type `/` -- the V-Model skills appear in autocomplete. The `using-digital-innovation-agents` skill is loaded automatically at session start as a brief orientation.

### Cursor

In Cursor Agent chat:

```
/add-plugin digital-innovation-agents
```

Or search for "digital-innovation-agents" in the Cursor plugin marketplace.

### GitHub Copilot CLI

```bash
copilot plugin marketplace add pssah4/digital-innovation-agents
copilot plugin install digital-innovation-agents@pssah4-skills
```

### Codex

Tell Codex:

```
Fetch and follow instructions from https://raw.githubusercontent.com/pssah4/digital-innovation-agents/main/.codex/INSTALL.md
```

Detailed docs: [.codex/INSTALL.md](.codex/INSTALL.md)

### OpenCode

Tell OpenCode:

```
Fetch and follow instructions from https://raw.githubusercontent.com/pssah4/digital-innovation-agents/main/.opencode/INSTALL.md
```

Detailed docs: [.opencode/INSTALL.md](.opencode/INSTALL.md)

### Gemini CLI

```bash
gemini extensions install https://github.com/pssah4/digital-innovation-agents
```

To update:

```bash
gemini extensions update digital-innovation-agents
```

### GitHub Copilot Chat (VS Code)

Copy the `.github/` directory to your project root. Agents are automatically detected by Copilot. Use them in Copilot Chat:

```
@business-analyst I want to build a tool that helps teams run better retrospectives
@requirements-engineer Here is my BA document, create epics and features
@architect Design the architecture based on the requirements handoff
@developer Implement the first feature
@debugger Tests are failing, analyze the error log
```

The Copilot agents have the same Exploration/Ideation/Validation innovation workflow, the same templates, and the same quality gates as the Claude Code skills.

### Legacy: Shell Script Install

For users without plugin marketplace support or with special setup needs:

```bash
git clone https://github.com/pssah4/digital-innovation-agents.git
cd digital-innovation-agents
./scripts/install-skills.sh
```

Install a specific version (e.g. v1.0.0 frozen snapshot):

```bash
./scripts/install-skills.sh --version v1.0.0
```

---

## Verify Installation

Start a new session in your chosen platform and try one of these:

```
/v-model-workflow          Full guided cycle from idea to security audit
/business-analyse          Start a structured business analysis
```

Or ask a natural-language question like "help me analyze this business problem". The agent should invoke the relevant skill.

If a skill does not appear:

- **Claude Code / Cursor:** Restart the session; the SessionStart hook loads the skill overview automatically
- **Codex:** Verify the symlink with `ls -la ~/.agents/skills/digital-innovation-agents`
- **OpenCode:** Check logs with `opencode run --print-logs "hello" 2>&1 | grep -i digital-innovation`
- **Gemini CLI:** Run `gemini extensions list`

---

## The agents

| Phase | What It Does | Claude Code | Copilot |
|-------|-------------|-------------|---------|
| **Business Analysis** | Exploration, Ideation, Validation cycle with structured interviews and probing techniques | `/business-analyse` | `@business-analyst` |
| **Requirements** | Epics, features, tech-agnostic success criteria, jobs-to-be-done | `/requirements-engineering` | `@requirements-engineer` |
| **Architecture** | ADRs (MADR), arc42, plan-context.md | `/architecture` | `@architect` |
| **Implementation** | Context handoff, critical review, artifact writeback | `/coding` | `@developer` |
| **Testing** | Unit and integration tests with fix-loop | `/testing` | built-in |
| **Security Audit** | OWASP Top 10, LLM Top 10, SAST, SCA, Zero Trust | `/security-audit` | `@security-auditor` |
| **Debugging** | Root cause analysis, systematic error resolution | -- (default) | `@debugger` |
| **Orchestrator** | Guides through all phases step by step | `/v-model-workflow` | -- |
| **Conventions** | Project structure and naming standards | `/project-conventions` | -- |

---

## The flow

### Innovation phases (business analysis)

The BA agent guides you through three innovation phases before a single line of code is written:

```
/business-analyse
  Phase 1: Exploration -- Understand the problem space
    - Users, needs, insights, trends, competitors
    - Output: Exploration Board + How-Might-We question
    
  Phase 2: Ideation -- Design the solution
    - Idea potential, the Wow, critical hypotheses, value proposition
    - Output: Solution concept with validation plan
    
  Phase 3: Validation -- Test business viability
    - VP score, assessment radar, pricing, channels, revenue
    - Output: Market assessment

  Final: BA Document
    Output: _devprocess/analysis/BA-{PROJECT}.md
           _devprocess/analysis/EXPLORATION-{PROJECT}.md
```

### Design phases (left side of the V)

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

### Implementation (bottom of the V)

```
/coding
  Input:  plan-context.md + ADRs + Features
  1. Load context from design phases
  2. Critical review against real codebase
  3. Write changes back to artifacts
  4. Implementation
  5. Final sync: artifacts reflect what was actually built
```

### Verification (right side of the V)

```
/testing
  Output: Unit tests, integration tests (with fix-loop)

/security-audit
  Output: Security report with remediation plan (with fix-loop)
```

---

## Design principles

The agents explore the problem (Exploration), design a solution (Ideation), and test business viability (Validation) before any requirements are written. Every agent reads the existing codebase before producing output, and your project's `CLAUDE.md` always takes precedence.

ADRs, features, and architecture docs are updated continuously during implementation. At the end, documentation reflects what was actually built, not what was originally planned.

Requirements separate *what* (measurable, technology-free) from *how* (technical NFRs). No OAuth, REST, or PostgreSQL in success criteria. Those go into Technical NFRs for the architect.

When interview partners give thin answers, the BA agent suggests concrete follow-up techniques: 5-Why, concretization, future projection, perspective shift, emotional probing, analogy triggers.

No phase proceeds until its quality criteria are met. Each agent validates its own output before handoff.

---

## Scope levels

The BA agent adapts its depth to your project scope:

| Scope | Exploration | Ideation | Validation | Typical Duration |
|-------|---------|--------|----------|-----------------|
| **Simple Test** | Minimal (user + problem) | Describe solution | Skip | Hours to 1-2 days |
| **PoC** | Shortened (user, needs, HMW) | Full | Hypotheses + feasibility | 1-4 weeks |
| **MVP** | Full (all 10 sections) | Full | Full market assessment | 2-6 months |

---

## File structure

```
digital-innovation-agents/
├── README.md
├── CHANGELOG.md
├── CLAUDE.md                                    # Repo-level agent instructions
├── AGENTS.md -> CLAUDE.md                       # Codex convention (symlink)
├── LICENSE
├── .gitignore
│
├── .claude-plugin/                              # Claude Code plugin
│   ├── plugin.json                              # Plugin manifest
│   └── marketplace.json                         # Marketplace manifest (pssah4-skills)
│
├── .cursor-plugin/plugin.json                   # Cursor plugin manifest
├── .codex/INSTALL.md                            # Codex installation guide
├── .opencode/                                   # OpenCode plugin
│   ├── INSTALL.md
│   └── plugins/digital-innovation-agents.js    # JS plugin (adapted from superpowers)
├── gemini-extension.json                        # Gemini CLI extension manifest
├── GEMINI.md                                    # Gemini CLI context file
│
├── hooks/                                       # SessionStart hooks
│   ├── hooks.json                               # Claude Code hook config
│   ├── hooks-cursor.json                        # Cursor hook config
│   ├── session-start                            # Shared bootstrap script
│   └── run-hook.cmd                             # Windows polyglot wrapper
│
├── skills/                                      # V-Model skills (loaded by all platforms)
│   │
│   ├── using-digital-innovation-agents/         # Bootstrap orientation (loaded by hook)
│   │   └── SKILL.md
│   │
│   ├── project-conventions/                     # Directory structure & naming
│   │   ├── SKILL.md
│   │   └── references/
│   │       ├── codebase-awareness.md
│   │       ├── directory-structure.md
│   │       └── naming-conventions.md
│   │
│   ├── business-analyse/                        # Exploration/Ideation/Validation cycle
│   │   ├── SKILL.md
│   │   ├── templates/
│   │   │   ├── BA-TEMPLATE.md                   # Full BA document (12 sections)
│   │   │   └── EXPLORATION-BOARD.md             # Exploration phase board (10 sections)
│   │   └── references/
│   │       └── innovation-methods.md            # 20+ methods with probing techniques
│   │
│   ├── requirements-engineering/                # Epics, features, success criteria
│   │   ├── SKILL.md
│   │   ├── templates/
│   │   │   ├── EPIC-TEMPLATE.md                 # With HMW and hypothesis tracking
│   │   │   └── FEATURE-TEMPLATE.md              # With jobs-to-be-done and validation
│   │   └── references/
│   │       └── tech-agnostic-rules.md           # Forbidden terms + transformation guide
│   │
│   ├── architecture/                            # ADRs, arc42, plan-context.md
│   │   ├── SKILL.md
│   │   └── templates/
│   │       ├── ADR-TEMPLATE.md
│   │       ├── arc42-TEMPLATE.md
│   │       └── plan-context-TEMPLATE.md
│   │
│   ├── coding/                                  # Context handoff & artifact writeback
│   │   └── SKILL.md
│   │
│   ├── testing/                                 # Unit & integration tests
│   │   ├── SKILL.md
│   │   └── references/
│   │       ├── test-checklist.md
│   │       └── test-anti-patterns.md
│   │
│   ├── security-audit/                          # OWASP, SAST, SCA
│   │   ├── SKILL.md
│   │   ├── templates/
│   │   │   └── AUDIT-TEMPLATE.md
│   │   └── references/
│   │       ├── cwe-patterns.md
│   │       ├── owasp-checklist.md
│   │       └── owasp-llm-checklist.md
│   │
│   └── v-model-workflow/                        # Orchestrator
│       └── SKILL.md
│
├── scripts/
│   └── install-skills.sh                        # Legacy shell installer (fallback)
│
└── .github/                                     # GitHub Copilot Chat agents
    ├── copilot-instructions.md                 # Global instructions (auto-loaded)
    ├── agents/
    │   ├── business-analyst.agent.md           # Exploration/Ideation/Validation cycle
    │   ├── requirements-engineer.agent.md      # HMW, JTBD, hypothesis tracking
    │   └── architect.agent.md                  # ADRs, arc42, system design
    ├── chatmodes/
    │   ├── business-analyst.chatmode.md        # Same as agent (chat mode format)
    │   ├── requirements-engineer.chatmode.md
    │   ├── developer.chatmode.md               # Test-driven implementation
    │   └── debugger.chatmode.md                # Root cause analysis
    ├── instructions/                           # Auto-validation quality rules
    │   ├── business-analyst.instructions.md    # Exploration/Ideation/Validation quality rules
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

## Where it works

| Environment | Skills Support | Primary Install |
|-------------|---------------|------------------|
| **Claude Code** (CLI, VS Code, JetBrains) | Full | `/plugin install digital-innovation-agents@pssah4-skills` |
| **Cursor** | Full | `/add-plugin digital-innovation-agents` |
| **GitHub Copilot CLI** | Full | `copilot plugin install digital-innovation-agents@pssah4-skills` |
| **Codex** | Full | Clone + symlink (see `.codex/INSTALL.md`) |
| **OpenCode** | Full | `opencode.json` plugin entry (see `.opencode/INSTALL.md`) |
| **Gemini CLI** | Full | `gemini extensions install https://github.com/pssah4/digital-innovation-agents` |
| **GitHub Copilot Chat** (VS Code) | Full (agents) | Copy `.github/` to your project |
| **Claude Desktop App** | Supported | Upload via Customize > Skills > "+" |
| **Any platform, no install** | Manual | Copy templates into your message |

---

## Adapt to your workflow

These agents reflect a specific workflow. You will want to adjust:

- **Templates**: Edit templates to match your document standards
- **Quality gates**: Tune validation thresholds
- **Naming conventions**: Change file naming patterns in `project-conventions`
- **Testing patterns**: Swap framework examples for your stack
- **Scope levels**: Adjust Simple Test / PoC / MVP complexity settings
- **Innovation methods**: Add or remove methods in `innovation-methods.md`
- **Language**: Skills are in English; your `CLAUDE.md` controls conversation language

---

## License

MIT License. Copyright (c) 2025 Sebastian Hanke.

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
