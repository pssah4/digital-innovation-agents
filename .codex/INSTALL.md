# Installing Digital Innovation Agents for Codex

Enable the V-Model skill set in Codex via native skill discovery.
The skills call helper scripts under `tools/`, so the install needs
both the skills directory and `DIA_PLUGIN_ROOT` so the helpers can
be resolved at runtime.

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

3. **Export `DIA_PLUGIN_ROOT`** so skills can find `tools/`:
   ```bash
   echo 'export DIA_PLUGIN_ROOT="$HOME/.codex/digital-innovation-agents"' >> ~/.zshrc
   # or ~/.bashrc, depending on your shell
   ```

   **Windows (PowerShell):**
   ```powershell
   [Environment]::SetEnvironmentVariable("DIA_PLUGIN_ROOT", "$env:USERPROFILE\.codex\digital-innovation-agents", "User")
   ```

4. **Restart Codex** (quit and relaunch the CLI) and reopen your
   shell so the new variable is picked up.

## Verify

```bash
ls -la ~/.agents/skills/digital-innovation-agents
echo "$DIA_PLUGIN_ROOT"
ls "$DIA_PLUGIN_ROOT/tools/github-integration/flow.py"
```

You should see a symlink (or junction on Windows) pointing to your
skills directory, the `DIA_PLUGIN_ROOT` variable resolves to the
clone, and `flow.py` is reachable through it.

In a new Codex session, ask "what skills do you have available?".
The agent should list entries including `dia-setup`,
`business-analysis`, `requirements-engineering`, `architecture`,
`coding`, `testing`, `security-audit`, and `dia-guide`.

## Updating

```bash
cd ~/.codex/digital-innovation-agents && git pull
```

Skills update instantly through the symlink. `tools/`, `hooks/`,
and `scripts/` update with the same `git pull` since they live in
the same repository.

## Uninstalling

```bash
rm ~/.agents/skills/digital-innovation-agents
# Remove the DIA_PLUGIN_ROOT line from ~/.zshrc or ~/.bashrc
```

Optionally delete the clone:

```bash
rm -rf ~/.codex/digital-innovation-agents
```

## Entry points

Once installed, start with:

- `dia-guide` -- Guided cycle through all phases
- `business-analysis` -- Problem exploration, ideation, validation (greenfield)
- `reverse-engineering` -- Walks the V backwards over an existing codebase (brownfield)
- `dia-migration` -- Migrate a legacy DIA project or pre-existing V-Model variant to current conventions
- Other phase skills -- requirements-engineering, architecture, coding, testing, security-audit

The Digital Innovation Agents workflow is advisory, not enforcing. You can opt out at any time by telling the agent "skip the workflow" or "just help me with X directly".

## Getting help

- Repository: https://github.com/pssah4/digital-innovation-agents
- Issues: https://github.com/pssah4/digital-innovation-agents/issues
