# Installing Digital Innovation Agents for Codex

Enable the V-Model skill set in Codex via native skill discovery. Just clone and symlink.

## Prerequisites

- Git

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/pssah4/digital-innovation-agents.git ~/.codex/digital-innovation-agents
   ```

2. **Create the skills symlink:**
   ```bash
   mkdir -p ~/.agents/skills
   ln -s ~/.codex/digital-innovation-agents/skills ~/.agents/skills/digital-innovation-agents
   ```

   **Windows (PowerShell):**
   ```powershell
   New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.agents\skills"
   cmd /c mklink /J "$env:USERPROFILE\.agents\skills\digital-innovation-agents" "$env:USERPROFILE\.codex\digital-innovation-agents\skills"
   ```

3. **Restart Codex** (quit and relaunch the CLI) to discover the skills.

## Verify

```bash
ls -la ~/.agents/skills/digital-innovation-agents
```

You should see a symlink (or junction on Windows) pointing to your skills directory.

In a new Codex session, ask something like "what skills do you have available?" -- the agent should list entries including `business-analysis`, `requirements-engineering`, `architecture`, `coding`, `testing`, `security-audit`, and `dia-orchestrator`.

## Updating

```bash
cd ~/.codex/digital-innovation-agents && git pull
```

Skills update instantly through the symlink.

## Uninstalling

```bash
rm ~/.agents/skills/digital-innovation-agents
```

Optionally delete the clone:

```bash
rm -rf ~/.codex/digital-innovation-agents
```

## Entry points

Once installed, start with:

- `dia-orchestrator` -- Guided cycle through all phases
- `business-analysis` -- Problem exploration, ideation, validation (greenfield)
- `reverse-engineering` -- Walks the V backwards over an existing codebase (brownfield)
- `dia-migration` -- Migrate a legacy DIA project or pre-existing V-Model variant to current conventions
- Other phase skills -- requirements-engineering, architecture, coding, testing, security-audit

The Digital Innovation Agents workflow is advisory, not enforcing. You can opt out at any time by telling the agent "skip the workflow" or "just help me with X directly".

## Getting help

- Repository: https://github.com/pssah4/digital-innovation-agents
- Issues: https://github.com/pssah4/digital-innovation-agents/issues
