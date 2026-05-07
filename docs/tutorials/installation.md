---
title: Installation
description: Install Digital Innovation Agents on your AI coding platform of choice in under 3 minutes.
---

# Installation

Digital Innovation Agents works on multiple AI coding platforms. Pick
the one you use and follow the steps below. All installations give you
the same set of thirteen skills. Only the registration mechanism
differs.

## Claude Code (recommended)

### Step 0: install the Claude Code CLI

The `/plugin` command lives in the Claude Code CLI, not in the VS Code
or JetBrains extensions. Install the CLI first. Check whether it is
already there:

```bash
claude --version
```

If `command not found`, install one of the three ways:

```bash
# Variant 1: official installer (macOS, Linux, WSL)
curl -fsSL https://claude.ai/install.sh | bash

# Variant 2: Homebrew (macOS)
brew install --cask claude-code

# Variant 3: npm (any platform with Node.js)
npm install -g @anthropic-ai/claude-code
```

Reopen your shell or run `source ~/.zshrc` (or `~/.bashrc`), then
verify with `claude --version`.

### Step 1: install the plugin

Start the CLI and run the marketplace commands:

```
claude
```

```
/plugin marketplace add https://github.com/pssah4/digital-innovation-agents.git
/plugin install digital-innovation-agents@pssah4-skills
```

Type `/` in any new session. The skills appear in autocomplete. The
`using-digital-innovation-agents` skill loads automatically at session
start to give you an orientation of the workflow.

### VS Code, JetBrains, Cursor extensions

The Claude Code IDE extensions do **not** support `/plugin`. Running
`/plugin marketplace add ...` inside the VS Code extension returns
`/plugin isn't available in this environment`. The fix: install once
through the CLI (as shown above), and the IDE extension picks the
skills up from the same global directory `~/.claude/skills/` on the
next session.

### Windows without WSL

The Claude Code CLI is experimental on native Windows. Install through
WSL, or copy the skills manually:

```bash
git clone https://github.com/pssah4/digital-innovation-agents.git
mkdir -p ~/.claude/skills
cp -r digital-innovation-agents/skills/* ~/.claude/skills/
```

### Manual fallback (no CLI, any OS)

If the CLI installer fails, copy the skills directly. You give up
`/plugin update` but get the same thirteen skills:

```bash
git clone https://github.com/pssah4/digital-innovation-agents.git /tmp/dia
mkdir -p ~/.claude/skills
cp -r /tmp/dia/skills/* ~/.claude/skills/
```

## Cursor

In Cursor Agent chat:

```
/add-plugin digital-innovation-agents
```

Or search for **digital-innovation-agents** in the Cursor plugin marketplace.

## GitHub Copilot (CLI and VS Code)

GitHub Copilot has no plugin marketplace command. Install by copying
the `.github/` directory from the repository into your project root:

```bash
git clone https://github.com/pssah4/digital-innovation-agents.git /tmp/dia
cp -r /tmp/dia/.github/agents .github/agents
cp -r /tmp/dia/.github/chatmodes .github/chatmodes
cp -r /tmp/dia/.github/instructions .github/instructions
cp -r /tmp/dia/.github/templates .github/templates
cp /tmp/dia/.github/copilot-instructions.md .github/copilot-instructions.md
```

Copilot Chat picks the agents up automatically on the next session.
Usage in Copilot Chat:

```
@business-analyst I want to build a tool that helps teams run better retrospectives
@requirements-engineer Create epics and features from this BA
@architect Design the architecture based on the requirements handoff
@developer Implement the first feature
@debugger Tests are failing, analyze the error log
```

The Copilot agents run the same Exploration / Ideation / Validation
cycle, the same templates, and the same quality gates as the Claude
Code skills.

## Codex

Tell Codex:

```
Fetch and follow instructions from
https://raw.githubusercontent.com/pssah4/digital-innovation-agents/main/.codex/INSTALL.md
```

Codex uses a symlink-based discovery mechanism. Detailed steps are in
[`.codex/INSTALL.md`](https://github.com/pssah4/digital-innovation-agents/blob/main/.codex/INSTALL.md).

## OpenCode

Tell OpenCode:

```
Fetch and follow instructions from
https://raw.githubusercontent.com/pssah4/digital-innovation-agents/main/.opencode/INSTALL.md
```

OpenCode uses a JS plugin registered via `opencode.json`. Detailed steps
are in [`.opencode/INSTALL.md`](https://github.com/pssah4/digital-innovation-agents/blob/main/.opencode/INSTALL.md).

## Gemini CLI

```bash
gemini extensions install https://github.com/pssah4/digital-innovation-agents
```

To update:

```bash
gemini extensions update digital-innovation-agents
```

## Frozen historical versions

If you need a specific older release for reproducibility (v1.0.0 or
v2.4.0), clone the tag directly. v1 and v2 are no longer maintained;
for active development upgrade to v3 through `/dia-migration`.

```bash
git clone --branch v1.0.0 https://github.com/pssah4/digital-innovation-agents.git   # Classic
git clone --branch v2.4.0 https://github.com/pssah4/digital-innovation-agents.git   # Pre-drift-resistance
```

These checkouts are read-only references; they do not auto-install
into your platform. Use the platform-specific install paths above for
v3 (marketplace, gemini extensions, manual `cp -r` for Codex /
Copilot).

## Verify the installation

Start a new session on your platform and try one of these:

```
/dia-setup                 Activate the workflow in this project
/dia-guide                 Guide for the full cycle
/business-analysis         Problem exploration, ideation, validation
/reverse-engineering       Brownfield entry for an existing codebase
/dia-migration             Upgrade an older DIA project to v3 conventions
```

Or ask a natural-language question like "help me analyze this
business problem" or "let's plan this feature". The agent should
invoke the relevant skill.

## Activate the workflow in your project

`/dia-setup` is the first call in any new project. It asks for the
mode (`off`, `git-only`, or `github-sync`), creates
`.dia/config.toml`, and writes a managed anchor block into your
agent files (`CLAUDE.md`, `AGENTS.md`, `GEMINI.md`, `.cursorrules`,
`.github/copilot-instructions.md`, `.windsurfrules`).

```
/dia-setup
```

Pick `git-only` if you work solo or your team does not use GitHub
Issues / Projects. Pick `github-sync` for the full team layer
(per-item GitHub issues, Project Status field mirroring,
post-RE `promote-to-epic`). Pick `off` if you have the plugin
installed globally but want this particular project to stay
neutral.

Re-run `/dia-setup` any time to change the mode or remove the
anchor blocks.

See [Three modes](../concepts/three-modes) for what each mode
does and [dia-setup guide](../guides/dia-setup) for the full
flow.

## What's next

- [Run your first Business Analysis](./first-business-analysis): a
  concrete walkthrough of `/business-analysis`
- [A full V-Model run](./full-v-model-run): the whole cycle end to end,
  from raw idea to release closure
- [V-Model workflow guide](../guides/dia-guide): how the
  guide treats phase transitions
- [dia-setup guide](../guides/dia-setup): activation reference
