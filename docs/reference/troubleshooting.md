---
title: Troubleshooting
description: Common installation issues and their solutions per platform.
---

# Troubleshooting

## Installation issues

### Claude Code: skills don't appear in autocomplete

1. Verify the plugin is installed: `/plugin list`
2. Restart the Claude Code session (quit and relaunch the CLI or reload
   the VS Code extension)
3. Check that the marketplace was added: `/plugin marketplace list`
4. If using the legacy script, verify `~/.claude/skills/` contains the
   9 skill directories (8 phases + `using-digital-innovation-agents`)

### Cursor: plugin not recognized

1. Check `.cursor-plugin/plugin.json` exists in the repo you installed from
2. Restart Cursor
3. Search for the plugin name in the Cursor plugin marketplace

### Codex: skills not discovered

1. Verify the symlink exists:
   ```bash
   ls -la ~/.agents/skills/digital-innovation-agents
   ```
2. The symlink must point to `~/.codex/digital-innovation-agents/skills`
3. Restart Codex (quit and relaunch the CLI)
4. On Windows, use `mklink /J` (directory junction) instead of a symlink

### OpenCode: plugin not loading

1. Check the `plugin` array in `opencode.json`:
   ```json
   { "plugin": ["digital-innovation-agents@git+https://github.com/pssah4/digital-innovation-agents.git"] }
   ```
2. Check logs:
   ```bash
   opencode run --print-logs "hello" 2>&1 | grep -i digital-innovation
   ```
3. Make sure you're running a recent OpenCode version

### Gemini CLI: extension not active

1. List installed extensions: `gemini extensions list`
2. If missing, reinstall:
   ```bash
   gemini extensions install https://github.com/pssah4/digital-innovation-agents
   ```
3. Verify `GEMINI.md` was loaded (check the first user message for
   the `using-digital-innovation-agents` content)

## Runtime issues

### SessionStart hook doesn't inject the bootstrap skill

- Check the hook is executable: `ls -la hooks/session-start`
  (should show `-rwxr-xr-x`)
- Check `hooks/hooks.json` exists and is valid JSON
- On Windows, verify `hooks/run-hook.cmd` finds `bash.exe` (Git for
  Windows usually provides it at `C:\Program Files\Git\bin\bash.exe`)

### The agent doesn't follow the workflow

This is by design. The workflow is advisory, not enforcing. If
you want the agent to follow it, explicitly invoke `/v-model-workflow`
or a specific phase skill. If you do not want the workflow, you can
opt out at any point:

- "stop" / "exit" / "I want to do something else": leaves the current loop
- "ignore the V-Model today": disables the skills for the session
- `/plugin disable digital-innovation-agents`: permanent disable

### Artifacts aren't written to `_devprocess/`

Check that your project has a `_devprocess/` directory. The
`/project-conventions` skill creates it. If it doesn't exist, the
skills fall back to asking you where to put the artifact, which slows
the workflow.

Initialize manually:

```bash
mkdir -p _devprocess/{analysis/security,requirements/{epics,features,handoff},architecture,context}
touch _devprocess/context/20_bugs.md _devprocess/context/30_handoffs.md
cp skills/requirements-engineering/templates/BACKLOG-TEMPLATE.md \
   _devprocess/context/10_backlog.md
```

## Version mismatch

If you want the frozen v1.0.0 (Classic) release explicitly:

```bash
./scripts/install-skills.sh --version v1.0.0
```

The v1.0.0 snapshot is not available through the plugin marketplace.
It remains installable via the legacy script for historical reference
or to reproduce v1 behavior.

## Still stuck?

Open a discussion or issue on
[GitHub](https://github.com/pssah4/digital-innovation-agents/issues).
