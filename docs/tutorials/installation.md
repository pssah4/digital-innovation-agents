---
title: Installation
description: Install Digital Innovation Agents on your AI coding platform of choice in under 3 minutes.
---

# Installation

Digital Innovation Agents works on multiple AI coding platforms. Pick
the one you use and follow the steps below. All installations give you
the same set of V-Model skills. Only the registration mechanism differs.

## Claude Code (recommended)

```
/plugin marketplace add pssah4/digital-innovation-agents
/plugin install digital-innovation-agents@pssah4-skills
```

Start a new session and type `/`. The skills appear in autocomplete.
The `using-digital-innovation-agents` skill loads automatically at
session start to give you an orientation of the workflow.

## Cursor

In Cursor Agent chat:

```
/add-plugin digital-innovation-agents
```

Or search for **digital-innovation-agents** in the Cursor plugin marketplace.

## GitHub Copilot CLI

```bash
copilot plugin marketplace add pssah4/digital-innovation-agents
copilot plugin install digital-innovation-agents@pssah4-skills
```

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

## GitHub Copilot Chat (VS Code)

Copy the `.github/` directory from the repository to your project root.
Copilot Chat auto-detects the agents.

Usage:

```
@business-analyst I want to build a tool that helps teams run better retrospectives
@requirements-engineer Create epics and features from this BA
@architect Design the architecture based on the requirements handoff
```

## Legacy shell script install

For platforms without plugin marketplace support, or if you need a specific
version like v1.0.0:

```bash
git clone https://github.com/pssah4/digital-innovation-agents.git
cd digital-innovation-agents
./scripts/install-skills.sh
```

To pin v1.0.0 (the Classic, frozen release):

```bash
./scripts/install-skills.sh --version v1.0.0
```

## Verify the installation

Start a new session on your platform and try one of these:

```
/v-model-workflow          Orchestrator for the full cycle
/business-analyse          Problem exploration, ideation, validation
```

Or ask a natural-language question like "help me analyze this
business problem" or "let's plan this feature". The agent should
invoke the relevant skill.

## What's next

- [Run your first Business Analysis](./first-business-analysis): a
  concrete walkthrough of `/business-analyse`
- [A full V-Model run](./full-v-model-run): the whole cycle end to end,
  from raw idea to release closure
- [V-Model workflow guide](../guides/v-model-workflow): how the
  orchestrator treats phase transitions
