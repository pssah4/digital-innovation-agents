# Installing Digital Innovation Agents for OpenCode

## Prerequisites

- [OpenCode.ai](https://opencode.ai) installed

## Installation

Add to the `plugin` array in your `opencode.json` (global or project-level):

```json
{
  "plugin": ["digital-innovation-agents@git+https://github.com/pssah4/digital-innovation-agents.git"]
}
```

Restart OpenCode. The plugin auto-installs and registers all skills.

Verify by asking: "Tell me about your digital innovation agents skills"

## Usage

Use OpenCode's native `skill` tool:

```
use skill tool to list skills
use skill tool to load digital-innovation-agents/dia-guide
```

Or start directly with one of the entry points:

- `/dia-guide` -- Guided cycle through all phases
- `/business-analysis` -- Problem exploration, ideation, validation (greenfield)
- `/reverse-engineering` -- Brownfield entry over an existing codebase
- `/dia-migration` -- Migrate legacy DIA project or pre-existing V-Model variant to current conventions
- `/requirements-engineering`
- `/architecture`
- `/coding`
- `/testing`
- `/security-audit`

The workflow is advisory -- you can opt out at any time by telling the agent "skip the workflow" or "just help me with X directly".

## Updating

Updates automatically when you restart OpenCode.

To pin a specific version:

```json
{
  "plugin": ["digital-innovation-agents@git+https://github.com/pssah4/digital-innovation-agents.git#v2.0.0"]
}
```

## Troubleshooting

### Plugin not loading

1. Check logs: `opencode run --print-logs "hello" 2>&1 | grep -i digital-innovation`
2. Verify the plugin line in your `opencode.json`
3. Make sure you're running a recent version of OpenCode

### Skills not found

1. Use `skill` tool to list what's discovered
2. Check that the plugin is loading (see above)

### Tool mapping

When skills reference Claude Code tools, use these OpenCode equivalents:

- `TodoWrite` -> `todowrite`
- `Task` with subagents -> OpenCode's subagent system (@mention syntax)
- `Skill` tool -> OpenCode's native `skill` tool
- `Read`, `Write`, `Edit`, `Bash` -> your native tools

## Getting Help

- Repository: https://github.com/pssah4/digital-innovation-agents
- Issues: https://github.com/pssah4/digital-innovation-agents/issues
