---
name: dia-setup
description: Activates, reconfigures, or deactivates the Digital Innovation Agents workflow in a project. Writes the .dia/config.toml settings file and manages anchor blocks in agent-facing files (CLAUDE.md, AGENTS.md, GEMINI.md, .cursorrules, .github/copilot-instructions.md, .windsurfrules). Use this skill when the user mentions "DIA aktivieren", "DIA installieren", "DIA initialisieren", "DIA setup", "DIA settings", "Workflow-Modus", "Modus wechseln", "DIA off", "DIA deaktivieren", "Plugin aktivieren". Single skill that covers both first-time activation and later reconfiguration; the skill detects which path applies from the presence of .dia/config.toml.
---

# DIA Setup

This skill is the activation and configuration entry point for the
Digital Innovation Agents plugin in a user project. It manages a
single configuration file (`.dia/config.toml`) and a set of anchor
blocks in agent-facing files. It does not run any phase skill, does
not read or modify the backlog, and does not call flow.py.

The skill is split into two paths driven by a single check at the
start: does `.dia/config.toml` already exist? If no, run the
**activation flow**. If yes, run the **reconfigure flow**.

## Modes

The plugin supports three modes, written into `.dia/config.toml` as
the field `mode`:

- **`off`**: plugin is neutral. Anchor blocks are removed from
  agent-facing files, the SessionStart hook does not inject the
  bootstrap skill, and phase-skills that probe the mode skip their
  GitHub-side calls.
- **`git-only`**: anchor blocks are present, the SessionStart hook
  injects the bootstrap, the local git hooks (pre-commit,
  pre-merge-commit) and `scripts/merge-to-dev.sh` are recommended.
  No GitHub issue or PR synchronization.
- **`github-sync`**: as `git-only`, plus `flow.py` is invoked from
  phase-skills to mirror backlog state to GitHub issues and project
  cards, run `promote-to-epic` after requirements engineering, and
  keep status in sync.

## Activation flow (no `.dia/config.toml` yet)

1. **Mode question.** Use `AskUserQuestion` with three options:
   `git-only` (recommended for most projects with a single
   developer), `github-sync` (recommended for teams that already
   work with GitHub Issues / Projects), `off` (recommended when the
   user wants to install the plugin without active behavior). Each
   option must list a `+ Pro:` line and a `- Con:` line in its
   description per the project User Interaction Protocol.

2. **Anchor file detection.** Scan the repo root for the known agent
   files. Show the user which files were detected and ask
   (single `AskUserQuestion`, multiSelect) which ones should carry
   the anchor block. Pre-select all detected files. Known list:
   - `CLAUDE.md`
   - `AGENTS.md`
   - `GEMINI.md`
   - `.cursorrules`
   - `.github/copilot-instructions.md`
   - `.windsurfrules`

3. **Source branch question (only if mode != off).** Default
   `develop`. Ask the user via `AskUserQuestion` whether to keep
   `develop` or use a different branch (`main`, `dev`, custom).
   This value goes into `.dia/config.toml` as `source_branch`.

4. **GitHub Project question (only if mode = github-sync).** Ask
   the user via `AskUserQuestion` whether they want backlog Status
   mirrored to a GitHub Project Status field. If yes, ask for the
   ProjectV2 number (the integer at the end of the project URL,
   for example 7 for `github.com/users/X/projects/7`). Optionally
   ask for the project owner login (when empty, flow.py resolves
   it from the repository) and the status field name (default
   `Status`). These values go into `.dia/config.toml` under
   `[github]`. If the user skips, leave `project_number = 0`; the
   issue itself still syncs, only the project Status field stays
   untouched.

5. **Write configuration.** Create `.dia/` directory if missing and
   write `.dia/config.toml` from the template
   `skills/dia-setup/templates/dia-config.toml.tmpl`, substituting
   `{{mode}}`, the chosen `anchor_files`, `source_branch`, and the
   `[github]` block.

6. **Write anchor blocks (only if mode != off).** Run
   `python3 tools/dia-setup/anchor.py write --mode <mode> --files
   <selected list>`. The script is idempotent; it creates or
   replaces blocks in the selected files.

7. **Confirmation.** Print a short confirmation to the user:
   - mode now active
   - which files received an anchor block
   - that `/dia-setup` can be re-run any time to change the mode
   - a hint that `/dia-guide` is the natural next step for actual
     work

## Reconfigure flow (`.dia/config.toml` exists)

1. **Read current state.** Parse `.dia/config.toml`, extract `mode`
   and `anchor_files`. Print the current state to the user.

2. **Action question.** Use `AskUserQuestion` with these options:
   - **Change mode** (Recommended if user invoked the skill to
     toggle behavior).
   - **Refresh anchor blocks** (rewrites blocks against the current
     mode, useful after a template update).
   - **Add or remove anchor files** (multi-step, see below).
   - **Deactivate (set mode to off and remove all anchor blocks)**.
   - **Cancel**.

   Each option requires a `+ Pro:` and `- Con:` line.

3. **Apply the chosen action.**

   - **Change mode**: ask new mode (Pro/Con per option), update
     `.dia/config.toml`, run
     `python3 tools/dia-setup/anchor.py write --mode <new>`.
   - **Refresh anchor blocks**: run anchor.py write with the
     existing mode and existing anchor_files list.
   - **Add or remove anchor files**: ask multiSelect with all known
     targets, mark currently anchored files as pre-selected, write
     the diff (anchor.py write for new entries, anchor.py remove
     for unselected entries), update `.dia/config.toml`.
   - **Deactivate**: write `mode = "off"` to `.dia/config.toml`,
     run `python3 tools/dia-setup/anchor.py remove --all`. Anchor
     files list in the config remains, so a later reactivation
     restores the same surface.
   - **Cancel**: do nothing.

4. **Confirmation.** Print which files changed and what the new
   state is.

## Verification (built-in self-check)

After every write or reconfigure flow, the skill calls
`python3 tools/dia-setup/anchor.py verify` and reports the result.
A non-zero exit code signals drift between `.dia/config.toml` and
the actual anchor blocks; if it occurs, surface the missing files
to the user and offer a refresh.

## Idempotency

The skill must be safe to invoke multiple times. The anchor script
detects existing blocks via a stable marker pair and replaces them
in place. Running `/dia-setup` twice with the same answers must
produce no diff in the working tree.

## Hand-off

`/dia-setup` does not invoke any phase skill, does not write to
`BACKLOG.md`, and does not start any handoff ritual. After a
successful run, the user typically continues with `/dia-guide`
for orientation or with a phase skill of their choice.

## Files written or removed

- `.dia/config.toml` (created or updated)
- one or more of: `CLAUDE.md`, `AGENTS.md`, `GEMINI.md`,
  `.cursorrules`, `.github/copilot-instructions.md`,
  `.windsurfrules` (anchor block written, replaced, or removed)

The skill never touches files outside this list.

## Settings file format

```toml
mode = "git-only"

anchor_files = [
  "CLAUDE.md",
  "AGENTS.md",
  "GEMINI.md",
  ".cursorrules",
]

source_branch = "develop"

[github]
project_number = 7
status_field = "Status"
project_owner = ""
```

`mode` is the only mandatory field. `anchor_files` defaults to the
list of files that carry a managed anchor block. `source_branch`
controls the base for new feature branches `/dia-guide` creates.

The `[github]` section is honored only when `mode = "github-sync"`:

- `project_number` is the GitHub ProjectV2 number (the integer at
  the end of the project URL, e.g. 7 for
  `github.com/users/X/projects/7`). Leave 0 to skip
  project-status mirroring; the issue itself still syncs, only
  the project Status field stays untouched.
- `status_field` is the single-select field name on the project
  that represents item status. Default `Status`.
- `project_owner` is optional. When empty, flow.py resolves the
  owner from the repository. Set explicitly when the project lives
  under a different owner than the repo (org-level projects, etc.).

## Reference

Full anchor format and idempotency rules:
`skills/dia-setup/references/anchor-format.md`.
