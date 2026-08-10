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
  <img src="https://raw.githubusercontent.com/pssah4/digital-innovation-agents/main/docs/public/v-model-overview.svg" alt="V-Model workflow for AI coding assistants: six phases (Business analysis, Requirements engineering, Architecture, Coding, Testing, Security audit) plus a Closing handoff. Two consistency buses run beneath the phases: BACKLOG.md as status source of truth and ARCHITECTURE.map as code source of truth. Four dashed feedback loops show test fix, mid-course discovery, security fix, and living-documents writeback." width="100%" />
</p>

---

## What this is

The project ships thirteen skills that run inside your AI coding
assistant. Six are V-Model phase skills (business analysis,
requirements engineering, architecture, coding, testing, security
audit). One is the entry point for non-greenfield projects
(`/dia-realign`). One is the on-demand workflow guide (`/dia-guide`,
an explicit command the model never auto-invokes). Five are
foundation skills (project conventions, consistency check, humanizer,
dia-setup, dia-bootstrap). Every phase skill owns one part of the
V-Model, has its own quality gates, and hands off a structured
artifact to the next phase; the transition record lives as DIA
trailers (`DIA-Phase`, `DIA-Handoff`, `DIA-Triage`) on the phase-end
commits, readable with plain git. Every decision stays traceable
from a real user problem through requirements, architecture, code,
tests, and a security audit.

Two entry points cover greenfield and everything else:

- **Greenfield:** `/business-analysis` starts with structured discovery
  (users, needs, insights, critical hypotheses) and walks forward
  through the V-Model.
- **Brownfield and legacy DIA:** `/dia-realign` detects the repo state
  and picks the fitting mode. For a codebase without artifacts it
  walks the V backwards and produces a wayfinder, post-hoc ADRs, an
  arc42 reference, a FEATURE inventory, a backlog seed, and an
  evidence-based BA draft (every claim sourced to a file path or doc
  section, nothing invented). For an older DIA project it runs the
  idempotent migration script pass (status drift, ID schemas,
  analysis/ flattening, backlog regeneration) and then fills the
  remaining gaps.

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

Pick your platform. Each installer drops the same thirteen skills with
the same templates and quality gates into your tool of choice.

### Claude Code (recommended)

`/plugin` lives in the **Claude Code CLI**, not in the VS Code or
JetBrains extensions. If `claude --version` returns
`command not found`, install the CLI first:

```bash
curl -fsSL https://claude.ai/install.sh | bash    # official installer
# or: brew install --cask claude-code              # macOS Homebrew
# or: npm install -g @anthropic-ai/claude-code     # any OS with Node
```

Reopen your shell (`source ~/.zshrc` or `~/.bashrc`), then install the
plugin:

```bash
claude
```

```
/plugin marketplace add https://github.com/pssah4/digital-innovation-agents.git
/plugin install digital-innovation-agents@pssah4-skills
```

Type `/` in any new session to see the skills in autocomplete. The
`dia-bootstrap` skill loads automatically at session
start as a brief orientation.

**VS Code, JetBrains, and Cursor extensions cannot install plugins.**
Running `/plugin marketplace add ...` inside the VS Code Claude Code
extension returns `/plugin isn't available in this environment`.
Install once through the CLI as above. The skills land under
`~/.claude/skills/` and the IDE extension picks them up from the same
global directory on the next session start. On Windows without WSL,
the CLI is experimental; install through WSL or copy the manually:

The manual install copies the **complete plugin bundle** (skills,
tools, hooks, scripts) under a stable path and symlinks the skills
into `~/.claude/skills/`. Skills invoke tooling at
`${DIA_PLUGIN_ROOT}/tools/...`, so `DIA_PLUGIN_ROOT` is exported
from the install location. Re-run the block to update; it pulls
the latest commit and rewrites the bundle in place. Skills
renamed or removed in newer DIA versions (for example
`dia-orchestrator` from v2) are deleted explicitly so no stale
skill folders survive the upgrade.

```bash
# Stable plugin location. Override with DIA_PLUGIN_ROOT env if needed.
DIA_PLUGIN_ROOT="${DIA_PLUGIN_ROOT:-$HOME/.local/share/dia-plugin}"

# Clone or update the plugin bundle
if [ -d "$DIA_PLUGIN_ROOT/.git" ]; then
  git -C "$DIA_PLUGIN_ROOT" fetch --tags --prune
  git -C "$DIA_PLUGIN_ROOT" reset --hard origin/main
else
  mkdir -p "$(dirname "$DIA_PLUGIN_ROOT")"
  rm -rf "$DIA_PLUGIN_ROOT"
  git clone https://github.com/pssah4/digital-innovation-agents.git "$DIA_PLUGIN_ROOT"
fi

mkdir -p ~/.claude/skills

# Remove legacy DIA skills that were renamed or dropped
for legacy in dia-orchestrator reverse-engineering dia-migration; do
  rm -rf "$HOME/.claude/skills/$legacy"
done

# Symlink the current DIA skill set (covers future renames automatically)
for skill in project-conventions dia-realign business-analysis \
             requirements-engineering architecture coding testing \
             security-audit consistency-check humanizer dia-guide \
             dia-setup dia-bootstrap; do
  rm -rf "$HOME/.claude/skills/$skill"
  ln -sfn "$DIA_PLUGIN_ROOT/skills/$skill" "$HOME/.claude/skills/$skill"
done

# Persist DIA_PLUGIN_ROOT so skills can resolve tools/ at runtime
shell_rc="$HOME/.zshrc"
[ -f "$HOME/.bashrc" ] && shell_rc="$HOME/.bashrc"
if ! grep -q "DIA_PLUGIN_ROOT=" "$shell_rc" 2>/dev/null; then
  echo "export DIA_PLUGIN_ROOT=\"$DIA_PLUGIN_ROOT\"" >> "$shell_rc"
fi
export DIA_PLUGIN_ROOT
```

After the first install, open a new shell so `DIA_PLUGIN_ROOT` is
set, then start `claude`. Skills resolve their helper scripts at
`$DIA_PLUGIN_ROOT/tools/...` regardless of the user-project cwd.

### Cursor

```
/add-plugin digital-innovation-agents
```

Or search for "digital-innovation-agents" in the Cursor plugin
marketplace.

### GitHub Copilot (CLI and VS Code)

GitHub Copilot has no marketplace command. Install by copying the
`.github/` directory plus the helper tools into your project. The
agents call `flow.py`, `anchor.py`, the migration scripts, and the
consistency check, so `tools/` and `scripts/` must be available
locally.

Re-run the block to update; the source checkout is pulled to the
latest commit and each target subfolder is wiped before copy, so
no stale Copilot agents, chat modes, or helper scripts survive an
upgrade.

```bash
# Clone or update the source checkout
if [ -d /tmp/dia/.git ]; then
  git -C /tmp/dia fetch --tags --prune
  git -C /tmp/dia reset --hard origin/main
else
  rm -rf /tmp/dia
  git clone https://github.com/pssah4/digital-innovation-agents.git /tmp/dia
fi

mkdir -p .github

# Wipe old DIA copies before installing the current set
for sub in agents chatmodes instructions templates; do
  rm -rf ".github/$sub"
  cp -r "/tmp/dia/.github/$sub" ".github/$sub"
done
cp /tmp/dia/.github/copilot-instructions.md .github/copilot-instructions.md

# Install the helper tools (flow.py, anchor.py, migration, hooks)
# at the project root so the agents can invoke them
for sub in tools scripts hooks; do
  rm -rf "$sub"
  cp -r "/tmp/dia/$sub" "$sub"
done

# Skills resolve tools/ relative to the project root in this layout,
# so DIA_PLUGIN_ROOT points at the project itself
echo 'export DIA_PLUGIN_ROOT="$(pwd)"' >> .envrc 2>/dev/null || true
```

The Copilot install brings the helper tools into the project rather
than to a global location because Copilot agents run with the
project as their working directory and have no plugin-bundle path
to fall back on.

Copilot Chat picks the agents up automatically on the next session. In
Copilot Chat:

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

## Verify the install

Start a session in your chosen platform and try one of these:

```
/dia-setup                 Activate the workflow in this project
/dia-guide                 Orientation read: state audit and next-phase recommendation
/business-analysis         Start a structured business analysis
/dia-realign               Brownfield entry and legacy DIA upgrade
```

`/dia-setup` is the first call in any new project. It asks for the
mode (`off`, `git-only`, or `github-sync`) and the profile (`full`
or `lean`), writes `.dia/config.toml`, and adds a managed anchor
block to your existing `CLAUDE.md`, `AGENTS.md`, `GEMINI.md`,
`.cursorrules`, or similar agent files. Re-run any time to change
the mode or profile, or to remove the anchor.

Or ask a natural-language question like "help me analyse this business
problem". The agent should invoke the matching skill.

Troubleshooting:

- **Claude Code or Cursor:** restart the session, the SessionStart hook
  loads the skill overview automatically.
- **Codex:** verify the symlink with `ls -la ~/.agents/skills/digital-innovation-agents`.
- **OpenCode:** check logs with `opencode run --print-logs "hello" 2>&1 | grep -i digital-innovation`.
- **Gemini CLI:** run `gemini extensions list`.

## The skills

The thirteen skills split into three groups: V-Model phase skills
(the ones that own a phase or move you between phases), foundation
skills (rules and consistency), and the bootstrap skill
(`dia-bootstrap` loads on session start to introduce the workflow).

### V-Model phase skills

| Phase | What it does | Claude Code | Copilot |
|---|---|---|---|
| **DIA Realign** | One entry point for brownfield codebases and legacy DIA repos. Detects the repo state, then runs a full reverse walk, the migration script pass, or a gap walk. Every claim sourced, idempotent, branch-safe. | `/dia-realign` | `@reverse-engineer` |
| **Business Analysis** | Exploration, Ideation, and Validation cycle with structured interviews, probing techniques, and the 32-method discovery catalog. Condenses the dialog into a 40-line BA record. | `/business-analysis` | `@business-analyst` |
| **Requirements Engineering** | Epics, FEAT-EE-FF features, tech-agnostic success criteria, user stories across functional / emotional / social levels, critical hypotheses. | `/requirements-engineering` | `@requirements-engineer` |
| **Architecture** | ADRs with kinds (post-hoc as the normal case, choice, constraint) and the abstraction rule (no code paths in core sections), arc42 constraints doc, navigation artifacts (SYSTEM-MAP, decisions router), wayfinder maintenance, plan-context ref index. | `/architecture` | `@architect` |
| **Coding** | Context handoff, critical review against the real codebase, PLAN-NN persistence with coverage gate, TDD by default (opt-out `--no-tdd` with user confirmation), bug-capture entry, artifact writeback during implementation. | `/coding` | `@developer` |
| **Testing** | Unit and integration tests with the AAA pattern, FIRST principles, coverage targets, and a fix-loop until green. Test edits under "the spec changed" require three pieces of evidence. | `/testing` | built-in |
| **Security Audit** | OWASP Top 10, LLM Top 10, SAST, SCA, supply-chain checks, Zero Trust review with a fix-loop. Two modes: per-item audit and periodic full-codebase audit. | `/security-audit` | `@security-auditor` |
| **V-Model Workflow Guide** | Explicit orientation command (never auto-invoked): reads project state and the DIA commit trailers, recommends the next phase skill, audits the last phase-end commit, and emits the Closing Handoff after a green security audit. The guide does not drive transitions; phase skills are autonomous. | `/dia-guide` | built-in |
| **Debugging** | Root-cause analysis, systematic error resolution, causal chain documentation. Bugs land as FIX-EE-FF-NN rows in the backlog plus detail files in `_devprocess/requirements/fixes/`. | default agent | `@debugger` |

### Foundation skills

| Skill | What it does | Claude Code |
|---|---|---|
| **Project Conventions** | Three-layer documentation model (Wayfinder, Rule sets, Backlog, Detail artifacts), directory structure, naming standards, writing-style rules. | `/project-conventions` |
| **Consistency Check** | Explicit command that verifies the V-Model artifact graph: dead links, orphan features, status drift, missing references. Modes A (syntactic), B (semantic), C (interactive fix-loop). Mandatory once per cycle before release; the pre-commit hook covers the drift-critical invariants between runs. | `/consistency-check` |
| **Humanizer** | Strips AI vocabulary, em dashes, negative parallelisms, and filler from every artifact. Enforces sentence case and active voice. | `/humanizer` |
| **DIA Bootstrap** | Loads automatically on session start. Carries the entry-point catalog, helper-script path resolution rule, activation contract, opt-out behaviour. Not invoked manually. | `dia-bootstrap` |

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

## The lean profile

Besides the workflow mode, `.dia/config.toml` carries a `profile`
field: `full` (default) or `lean`. The lean profile makes only three
things binding: durable decisions, stable navigation, and backlog
status. Rules live consolidated in AGENTS.md (CLAUDE.md points at
it), navigation lives in `_devprocess/SYSTEM-MAP.md`, decisions are
post-hoc ADRs behind a `decisions/README.md` router table, and
status lives in GitHub Issues (github-sync) or a thin BACKLOG
(git-only). All other phase skills stay available but advisory.
Pick lean when the team will not run BA/RE ceremony anyway; a thin
layer that is maintained beats a full layer that drifts.

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
`_devprocess/context/BACKLOG.md` file is the single source of truth
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
- [DIA Realign guide](https://pssah4.github.io/digital-innovation-agents/guides/dia-realign)

## Versions

| Version | Status | Install |
|---|---|---|
| **v3** (main) | Active, recommended. Three-layer documentation model, FEAT-EE-FF IDs, FIX/IMP detail files, PLAN-NN persistence, GitHub flow.py integration, subtype-aware Done-definition. | See Quick start above |
| **v2.x** | Frozen snapshot, no longer maintained | `git clone --branch v2.4.0 https://github.com/pssah4/digital-innovation-agents.git` |
| **v1.0.0** | Frozen snapshot, no longer maintained | `git clone --branch v1.0.0 https://github.com/pssah4/digital-innovation-agents.git` |

See [CHANGELOG.md](CHANGELOG.md) for details. Existing v1 or v2 projects
upgrade through `/dia-realign` (Mode B). v1 and v2 are historical
snapshots and not actively maintained; for current behaviour use the
marketplace or platform-specific install on v3.

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
