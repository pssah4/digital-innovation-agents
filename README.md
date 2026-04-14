# Digital Innovation Agents

> **When code costs almost nothing, the plan becomes the product.**
>
> A V-Model workflow that walks your AI coding assistant through Business
> Analysis, Requirements Engineering, Architecture, Coding, Testing, and
> a Security Audit, with quality-gated handoffs between every phase.

**Full documentation:** [pssah4.github.io/digital-innovation-agents](https://pssah4.github.io/digital-innovation-agents/)

Shipping code is a solved problem. What most teams still lack is evidence
that the features they ship matter to a real user. Digital Innovation
Agents pair a battle-tested innovation methodology with a state-of-the-art
coding workflow, so your AI never builds the wrong thing at speed. Works
across **Claude Code**, **Cursor**, **Codex**, **OpenCode**, **Gemini CLI**,
and **GitHub Copilot**.

<p align="center">
  <img src="https://raw.githubusercontent.com/pssah4/digital-innovation-agents/main/docs/public/v-model-overview.svg" alt="V-Model workflow: Business Analysis, Requirements Engineering, Architecture, Coding, Testing, Security Audit" width="100%" />
</p>

---

## What this is

The project ships ten specialised skills that run inside your AI coding
assistant. Each skill owns one phase of the V-Model, has its own quality
gates, and hands off a structured artifact to the next phase. The result
is a workflow where every decision is traceable from a real user problem
through requirements, architecture, code, tests, and a security audit.

Two entry points cover greenfield and brownfield projects:

- **Greenfield:** `/business-analyse` starts with structured discovery
  (users, needs, insights, critical hypotheses) and walks forward
  through the V-Model.
- **Brownfield:** `/reverse-engineering` walks the V backwards over an
  existing codebase and produces plan-context, ADRs, an arc42 snapshot,
  a FEATURE inventory, a backlog seed, and an evidence-based BA draft.
  Every claim is sourced to a file path or doc section. Nothing invented.

## Innovation methodology, not just automation

The BA and RE agents ship a catalog of 32 innovation methods (qualitative
interviews, extreme users, fly on the wall, cultural probes, persona
synthesis, stakeholder maps, jobs to be done, brainwriting, TRIZ, wizard
of oz, pre-mortem, value proposition quantification, and more) organised
as [method cards in the docs](https://pssah4.github.io/digital-innovation-agents/reference/methods-discovery).

During a BA or RE session, when your answers go thin, the agent stops
the interview and proposes the matching field method with a one-page
card: what it produces, when to reach for it, how to run it, team and
time, things that go wrong, and what to bring back to the session. The
actual research work stays human-to-human: interviews with real users,
observations in the real context, prototypes on real hands. The agent's
job is to spot the gap and pick the right method, not to replace the
work.

## Quick start

Pick your platform. Each installer drops the same ten skills with the
same templates and quality gates into your tool of choice.

### Claude Code (recommended)

```bash
/plugin marketplace add pssah4/digital-innovation-agents
/plugin install digital-innovation-agents@pssah4-skills
```

Start a new session and type `/` to see the V-Model skills in
autocomplete. The `using-digital-innovation-agents` skill loads
automatically at session start as a brief orientation.

### Cursor

```
/add-plugin digital-innovation-agents
```

Or search for "digital-innovation-agents" in the Cursor plugin
marketplace.

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

Copy the `.github/` directory into your project root. Copilot picks the
agents up automatically. In Copilot Chat:

```
@business-analyst I want to build a tool that helps teams run better retrospectives
@requirements-engineer Here is my BA document, create epics and features
@architect Design the architecture based on the requirements handoff
@developer Implement the first feature
@debugger Tests are failing, analyze the error log
```

The Copilot agents run the same Exploration / Ideation / Validation
cycle, the same templates, and the same quality gates as the Claude
Code skills.

### Legacy shell install

For users without plugin marketplace support:

```bash
git clone https://github.com/pssah4/digital-innovation-agents.git
cd digital-innovation-agents
./scripts/install-skills.sh
```

## Verify the install

Start a session in your chosen platform and try one of these:

```
/v-model-workflow          Full guided cycle from idea to security audit
/business-analyse          Start a structured business analysis
/reverse-engineering       Brownfield entry for an existing codebase
```

Or ask a natural-language question like "help me analyse this business
problem". The agent should invoke the matching skill.

Troubleshooting:

- **Claude Code or Cursor:** restart the session, the SessionStart hook
  loads the skill overview automatically.
- **Codex:** verify the symlink with `ls -la ~/.agents/skills/digital-innovation-agents`.
- **OpenCode:** check logs with `opencode run --print-logs "hello" 2>&1 | grep -i digital-innovation`.
- **Gemini CLI:** run `gemini extensions list`.

## The skills

| Phase | What it does | Claude Code | Copilot |
|---|---|---|---|
| **Reverse Engineering** | Brownfield entry. Walks the V backwards over an existing codebase and produces plan-context, ADRs, arc42, FEATURE inventory, backlog seed, and an evidence-based BA draft with every claim sourced. | `/reverse-engineering` | `@reverse-engineer` |
| **Business Analysis** | Exploration, Ideation, and Validation cycle with structured interviews, probing techniques, and the method catalog. | `/business-analyse` | `@business-analyst` |
| **Requirements Engineering** | Epics, features, tech-agnostic success criteria, user stories across functional / emotional / social levels, critical hypotheses. | `/requirements-engineering` | `@requirements-engineer` |
| **Architecture** | ADRs in MADR format, arc42 snapshot, plan-context bridge to implementation. | `/architecture` | `@architect` |
| **Coding** | Context handoff, critical review against the real codebase, artifact writeback during implementation. | `/coding` | `@developer` |
| **Testing** | Unit and integration tests with a fix-loop until green. | `/testing` | built-in |
| **Security Audit** | OWASP Top 10, LLM Top 10, SAST, SCA, Zero Trust review with a fix-loop. | `/security-audit` | `@security-auditor` |
| **Debugging** | Root-cause analysis, systematic error resolution, causal chain documentation. | default agent | `@debugger` |
| **V-Model Workflow** | Orchestrator that guides through every phase step by step. | `/v-model-workflow` | built-in |
| **Project Conventions** | Directory structure, naming standards, writing-style rules for every artifact. | `/project-conventions` | built-in |

## Scope levels

The skills adapt their depth to your project scope. Match the tier to
the size of the question.

| Scope | Exploration | Ideation | Validation | Typical duration |
|---|---|---|---|---|
| **Simple Test** | Minimal (user and problem) | Describe the solution | Skip | Hours to 1-2 days |
| **Proof of Concept** | Shortened (user, needs, HMW) | Full | Hypotheses and feasibility | 1-4 weeks |
| **MVP** | Full 10-section Exploration board | Full | Full market assessment | 2-6 months |

A Simple Test does not need a stakeholder map. An MVP does not get away
without one.

## Tech-agnostic requirements

Success Criteria stay free of technology vocabulary. No OAuth, REST,
PostgreSQL, or React in the contract between the user and the team.
Technical details live in a separate Technical NFRs section and in the
ADRs that follow in `/architecture`. See the
[Tech-agnostic Requirements](https://pssah4.github.io/digital-innovation-agents/concepts/tech-agnostic-requirements)
page in the docs for the full ruleset.

## Living documents

ADRs, features, architecture docs, and the backlog update continuously
during implementation. At release time, documentation reflects what was
actually built, not what was originally planned. The
`_devprocess/context/10_backlog.md` file is the single source of truth
for project state, and every phase skill touches it in the same edit
pass as the code it affects.

## Design principles

1. Understand the problem before designing the solution.
2. Separate what the system does (user-observable, tech-free) from how
   it does it (ADRs, NFRs).
3. Propose the right research method instead of grinding through a
   question list when your answers go thin.
4. No phase proceeds until its quality gate is met.
5. Every agent reads the real codebase before producing output. The
   project's `CLAUDE.md` always takes precedence over generic skill
   instructions.

## Documentation

Every guide, tutorial, concept page, and method card lives at
[pssah4.github.io/digital-innovation-agents](https://pssah4.github.io/digital-innovation-agents/).

Start here:

- [Your first Business Analysis tutorial](https://pssah4.github.io/digital-innovation-agents/tutorials/first-business-analysis)
- [A full V-Model run](https://pssah4.github.io/digital-innovation-agents/tutorials/full-v-model-run)
- [Discovery methods](https://pssah4.github.io/digital-innovation-agents/reference/methods-discovery),
  [Ideation methods](https://pssah4.github.io/digital-innovation-agents/reference/methods-ideation),
  [Validation methods](https://pssah4.github.io/digital-innovation-agents/reference/methods-validation)
- [Reverse Engineering guide](https://pssah4.github.io/digital-innovation-agents/guides/reverse-engineering)

## Versions

| Version | Status | Install |
|---|---|---|
| **v2** (main) | Active, recommended | See Quick start above |
| **v1.0.0** | Frozen snapshot (legacy) | `./scripts/install-skills.sh --version v1.0.0` |

See [CHANGELOG.md](CHANGELOG.md) for details. v1 is installable as a
historical snapshot and is not actively maintained.

## License

MIT License. Copyright (c) 2025 Sebastian Hanke. See [LICENSE](LICENSE).

## Acknowledgments

Built with:

- Claude Code Skills, Claude Agent SDK, and GitHub Copilot Agents
- Innovation methodology from design thinking and lean startup practice
- Jobs-to-be-Done framework
- arc42 architecture documentation template
- MADR (Markdown Architectural Decision Records)
- OWASP Top 10 and LLM Top 10
- AAA pattern and FIRST principles for testing
