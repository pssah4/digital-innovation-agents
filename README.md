# Digital Innovation Agents

> **AI-Powered Software Development Workflow** -- From idea to production-ready code through structured, quality-gated phases.

A comprehensive system of specialized AI agents that guide software development from initial business concept through requirements engineering, architecture design, implementation, testing, and security audit. Available for **GitHub Copilot** and **Claude Code**.

---

## What This Is

**Digital Innovation Agents** transforms how software is built by providing a structured, agent-based workflow that ensures quality at every stage. Instead of jumping straight into code, projects follow a systematic path:

```
Business Idea -> Requirements -> Architecture -> Implementation -> Testing -> Security Audit
      |               |              |               |              |             |
   BA Agent      RE Agent     Architect Agent   Coding Agent   Test Agent   Security Agent
```

Each agent specializes in one phase, has built-in quality checks, and produces standardized outputs that feed into the next phase.

---

## Two Platforms, One Workflow

### GitHub Copilot (`.github/`)

The original implementation using Copilot's custom agents, instructions, and templates. Activate agents with `@agent-name` in Copilot Chat.

See [GitHub Copilot Setup](#github-copilot-setup) below.

### Claude Code (`claude-code-skills/`)

Migrated to Claude Code's skill system. Activate with `/skill-name` slash commands or let Claude auto-detect the right skill. Works in Claude Code terminal, VS Code extension, and JetBrains.

See [Claude Code Setup](#claude-code-setup) below.

---

## The Agents

| Phase | Role | Copilot | Claude Code |
|-------|------|---------|-------------|
| Business Analysis | Problem and stakeholder analysis | `@business-analyst` | `/business-analyse` |
| Requirements | Epics, features, success criteria | `@requirements-engineer` | `/requirements-engineering` |
| Architecture | ADRs, arc42, plan-context.md | `@architect` | `/architecture` |
| Implementation | Context handoff, critical review, coding | `@developer` | `/coding` |
| Testing | Unit and integration tests | `@developer` (built-in) | `/testing` |
| Security Audit | OWASP, SAST, SCA, Zero Trust | `@security-auditor` | `/security-audit` |
| Debugging | Root cause analysis | `@debugger` | -- (default agent) |
| Orchestrator | Guides through all phases | -- | `/v-model-workflow` |
| Conventions | Project structure and naming | -- | `/project-conventions` |

---

## The Flow

### Entwurfsphasen (Left Side of the V)

```
/business-analyse
  Output: _devprocess/analysis/BA-{PROJECT}.md
    |
    v
/requirements-engineering
  Input:  BA document
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
  3. Write changes back to artifacts BEFORE coding
  4. Implementation (default coding agent)
  5. Continuous writeback during implementation
  6. Final sync -- artifacts reflect what was actually built
```

### Verification (Right Side of the V)

```
/testing
  Input:  Implemented codebase
  Output: Unit tests, integration tests

/security-audit
  Input:  Implemented codebase
  Output: Security report with remediation plan
```

---

## Key Design Principles

**Codebase-Awareness**: Every agent reads the existing codebase before producing output. No agent works in a vacuum. Your project's `CLAUDE.md` always takes precedence.

**Living Documents**: ADRs, features, and architecture docs are continuously updated during implementation. At the end, documentation always reflects what was actually built -- not what was originally planned.

**Tech-Agnostic Success Criteria**: Requirements separate *what* (measurable, technology-free) from *how* (technical NFRs). No OAuth, REST, or PostgreSQL in success criteria -- those go into Technical NFRs for the architect.

**Lightweight Coding Bridge**: The `/coding` skill doesn't replace your coding agent. It handles context loading, critical review, and artifact writeback. You code the way you always do.

**Quality Gates**: No phase proceeds until quality criteria are met. Each agent validates its own output before handoff.

---

## Claude Code Setup

### Install

```bash
cd claude-code-skills
chmod +x install-skills.sh
./install-skills.sh
```

Skills are copied to `~/.claude/skills/` and available immediately in Claude Code (terminal, VS Code extension, JetBrains).

### Verify

Type `/` in Claude Code -- your skills should appear in the autocomplete dropdown.

In VS Code: if skills don't appear after install, close and reopen the Claude Code session.

### Usage

**Explicit** -- type `/business-analyse` or `/testing` to start a specific phase. Deterministic and reliable.

**Automatic** -- say "I need a stakeholder analysis" and Claude loads the right skill based on the description. Works most of the time, but `/slash-command` is the safe bet.

**Full cycle** -- type `/v-model-workflow` to be guided through each phase step by step.

### Claude Code Skills Overview

| Skill | Slash-Command | Auto | Description |
|-------|---------------|------|-------------|
| Project Conventions | `/project-conventions` | Yes | Directory structure, naming, codebase-awareness |
| Business Analyse | `/business-analyse` | Yes | Structured interview, problem analysis |
| Requirements Engineering | `/requirements-engineering` | Yes | Epics, features, tech-agnostic success criteria |
| Architecture | `/architecture` | Yes | ADRs (MADR), arc42, plan-context.md |
| Coding | `/coding` | Yes | Critical review, context handoff, artifact writeback |
| Testing | `/testing` | Yes | Unit and integration tests (AAA, FIRST) |
| Security Audit | `/security-audit` | Manual only | OWASP Top 10, LLM Top 10, SAST, SCA |
| V-Model Workflow | `/v-model-workflow` | Manual only | Orchestrator for the full cycle |

### Claude Code File Structure

```
claude-code-skills/
  install-skills.sh
  project-conventions/
    SKILL.md
    references/directory-structure.md, naming-conventions.md, codebase-awareness.md
  business-analyse/
    SKILL.md
    templates/BA-TEMPLATE.md
  requirements-engineering/
    SKILL.md
    templates/EPIC-TEMPLATE.md, FEATURE-TEMPLATE.md
    references/tech-agnostic-rules.md
  architecture/
    SKILL.md
    templates/ADR-TEMPLATE.md, arc42-TEMPLATE.md, plan-context-TEMPLATE.md
  coding/
    SKILL.md
  testing/
    SKILL.md
    references/test-checklist.md, test-anti-patterns.md
  security-audit/
    SKILL.md
    templates/AUDIT-TEMPLATE.md
    references/cwe-patterns.md, owasp-checklist.md, owasp-llm-checklist.md
  v-model-workflow/
    SKILL.md
```

---

## GitHub Copilot Setup

### Prerequisites

- GitHub Copilot with Chat enabled
- Project with `.github/` directory from this repo

### Install

Copy the `.github/` directory to your project root. Agents are automatically detected by Copilot.

### Usage

```
@business-analyst [your request]
@requirements-engineer [your request]
@architect [your request]
@developer [your request]
@debugger [your request]
```

### Copilot Agents Overview

| Agent | Input | Output |
|-------|-------|--------|
| `@business-analyst` | Raw idea | `BA-[PROJECT].md` |
| `@requirements-engineer` | BA document | Epics, Features, architect-handoff.md |
| `@architect` | architect-handoff.md | ADRs, arc42, Issues, Backlog.md |
| `@developer` | Issues from Backlog | Code + Tests |
| `@debugger` | Error logs | Fixed code + resolution docs |

### Quality Gates

- **QG1** (RE -> Architect): All NFRs quantified, all ASRs identified
- **QG2** (Architect -> Developer): ADRs complete, atomic issues created
- **QG3** (Developer): All tests passing, coverage >= 90%
- **QGD** (Debugger): Root cause fixed, no regressions

### Copilot File Structure

```
.github/
  agents/                     # Agent definitions
    business-analyst.agent.md
    requirements-engineer.agent.md
    architect.agent.md
    security-auditor.agent.md
  instructions/               # Auto-validation rules
    architect.instructions.md
    business-analyst.instructions.md
    requirements-engineer.instructions.md
  templates/                  # Document templates
    EPIC-TEMPLATE.md
    FEATURE-TEMPLATE.md
```

---

## Adapt to Your Workflow

These agents reflect my workflow. You'll want to adjust:

- **Templates**: Edit templates to match your document standards
- **Quality gates**: Tune validation thresholds
- **Naming conventions**: Change file naming patterns in `project-conventions`
- **Testing patterns**: Swap framework examples for your stack
- **Scope levels**: Adjust Simple Test / PoC / MVP complexity settings

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
- GitHub Copilot Chat Modes and Claude Code Skills
- SAFe Framework (Epics, Features)
- arc42 Architecture Documentation
- MADR (Markdown Architectural Decision Records)
- OWASP Top 10 and LLM Top 10
- AAA Pattern and FIRST Principles for Testing
