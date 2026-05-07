---
title: Troubleshooting
description: Common installation issues and their solutions per platform.
---

# Troubleshooting

## Installation issues

### `/plugin isn't available in this environment` in VS Code or JetBrains

The `/plugin` command lives only in the Claude Code **CLI**, not in
the IDE extensions. Install the plugin once through the CLI; the
extension picks the skills up from `~/.claude/skills/` on the next
session.

```bash
# install the CLI if not yet present
curl -fsSL https://claude.ai/install.sh | bash
# or: brew install --cask claude-code
# or: npm install -g @anthropic-ai/claude-code

claude
```

```
/plugin marketplace add https://github.com/pssah4/digital-innovation-agents.git
/plugin install digital-innovation-agents@pssah4-skills
```

### `Host key verification failed` / `No ED25519 host key is known for github.com`

`/plugin marketplace add` fails with a git clone error mentioning
host key verification. Cause: the GitHub shorthand form
(`owner/repo`) clones via SSH (`git@github.com:...`), and your
machine has never trusted GitHub's SSH host key. The fix is to use
the explicit HTTPS URL instead, which avoids SSH altogether:

```
/plugin marketplace add https://github.com/pssah4/digital-innovation-agents.git
```

If you need the SSH form for other reasons, populate
`~/.ssh/known_hosts` first:

```bash
mkdir -p ~/.ssh && chmod 700 ~/.ssh
ssh-keyscan -t rsa,ecdsa,ed25519 github.com >> ~/.ssh/known_hosts
chmod 644 ~/.ssh/known_hosts
```

### `claude: command not found`

The Claude Code CLI is not installed or not on PATH. Install it:

```bash
curl -fsSL https://claude.ai/install.sh | bash
# or: brew install --cask claude-code
# or: npm install -g @anthropic-ai/claude-code
```

Reopen the shell or `source ~/.zshrc` (or `~/.bashrc`), then verify
with `claude --version`.

### Claude Code: skills don't appear in autocomplete

1. Verify the plugin is installed: `/plugin list` (in the CLI)
2. Restart the Claude Code session (quit and relaunch the CLI or
   reload the VS Code extension)
3. Check that the marketplace was added: `/plugin marketplace list`
4. If using the manual fallback, verify `~/.claude/skills/` contains
   all **thirteen** skill directories: `architecture`,
   `business-analysis`, `coding`, `consistency-check`, `dia-bootstrap`,
   `dia-guide`, `dia-migration`, `dia-setup`, `humanizer`,
   `project-conventions`, `requirements-engineering`,
   `reverse-engineering`, `security-audit`, `testing`.

### Cursor: plugin not recognized

1. Check `.cursor-plugin/plugin.json` exists in the repo you installed
   from
2. Restart Cursor
3. Search for the plugin name in the Cursor plugin marketplace

### GitHub Copilot: agents not found

GitHub Copilot has no plugin marketplace command. Copy the `.github/`
directory from the repository into your project root:

```bash
git clone https://github.com/pssah4/digital-innovation-agents.git /tmp/dia
cp -r /tmp/dia/.github/agents .github/agents
cp -r /tmp/dia/.github/chatmodes .github/chatmodes
cp -r /tmp/dia/.github/instructions .github/instructions
cp -r /tmp/dia/.github/templates .github/templates
cp /tmp/dia/.github/copilot-instructions.md .github/copilot-instructions.md
```

Restart the Copilot session. The `@business-analyst`,
`@requirements-engineer`, `@architect`, `@developer`,
`@security-auditor`, `@reverse-engineer`, `@debugger` agents appear
in Copilot Chat.

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
   the `dia-bootstrap` content)

## Runtime issues

### SessionStart hook doesn't inject the bootstrap skill

- Check the hook is executable: `ls -la hooks/session-start`
  (should show `-rwxr-xr-x`)
- Check `hooks/hooks.json` exists and is valid JSON
- On Windows, verify `hooks/run-hook.cmd` finds `bash.exe` (Git for
  Windows usually provides it at `C:\Program Files\Git\bin\bash.exe`)

### The agent doesn't follow the workflow

This is by design. The workflow is advisory, not enforcing. If you
want the agent to follow it, explicitly invoke `/dia-guide` or
a specific phase skill. To opt out at any point:

- "stop" / "exit" / "I want to do something else": leaves the current loop
- "ignore the V-Model today": disables the skills for the session
- `/plugin disable digital-innovation-agents`: permanent disable
  (CLI only)

### Artifacts aren't written to `_devprocess/`

Check that your project has a `_devprocess/` directory. The
`/project-conventions` skill creates it. If it doesn't exist, the
skills fall back to asking you where to put the artifact, which slows
the workflow.

Initialize manually:

```bash
mkdir -p _devprocess/{analysis/sources,requirements/{epics,features,fixes,improvements,handoff},architecture,rules,implementation/plans,context}
touch _devprocess/context/HANDOFFS.md
cp skills/requirements-engineering/templates/BACKLOG-TEMPLATE.md \
   _devprocess/context/BACKLOG.md
cp skills/dia-guide/templates/METRICS-TEMPLATE.md \
   _devprocess/context/METRICS.md
touch src/ARCHITECTURE.map
```

There is no `analysis/security/` subfolder anymore (audit reports
live flat under `analysis/`), and there is no `20_bugs.md` (bugs are
`FIX-{ee}-{ff}-{nn}` rows in `BACKLOG.md` plus detail files under
`requirements/fixes/`).

### Backlog drift: status says Planned but the code shipped

Run `/consistency-check` Mode A. It compares the backlog row of every
artifact against the artifact body and flags drift. Mode B adds a
semantic agent pass that checks reasoning coherence.

Status drift is the most common doc-vs-code drift class. The v3
three-layer model is the structural fix: status, phase, last-change,
and claim live in the backlog row only, never in the artifact
frontmatter.

## Version mismatch

If you need a frozen historical release for reproducibility, clone
the tag directly:

```bash
git clone --branch v1.0.0 https://github.com/pssah4/digital-innovation-agents.git   # Classic
git clone --branch v2.4.0 https://github.com/pssah4/digital-innovation-agents.git   # Pre-drift-resistance
```

These checkouts are read-only references. v1 and v2 are no longer
maintained. To upgrade an existing v1 or v2 project to v3 conventions,
use `/dia-migration`. It is idempotent and branch-safe.

## Still stuck?

Open a discussion or issue on
[GitHub](https://github.com/pssah4/digital-innovation-agents/issues).
