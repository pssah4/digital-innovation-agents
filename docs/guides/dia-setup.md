---
title: dia-setup
description: Activate DIA in a project, change the mode later, deactivate cleanly. Manages `.dia/config.toml` and anchor blocks in agent files.
---

# `/dia-setup` guide

`/dia-setup` is the single entry point for activating DIA in a
project, changing the mode later, or deactivating the plugin
cleanly. It is the first command you run in a fresh project; you
never need it during the normal V-Model flow.

## What it does

The skill is a thin wrapper around two artifacts:

- `.dia/config.toml`: a small TOML file at the repo root that
  carries the project's mode (`off`, `git-only`, `github-sync`),
  the source branch for new feature branches (default `develop`),
  the list of agent files that should carry the anchor block, and
  optional GitHub project settings.
- One anchor block in each agent file the user has selected
  (`CLAUDE.md`, `AGENTS.md`, `GEMINI.md`, `.cursorrules`,
  `.github/copilot-instructions.md`, `.windsurfrules`). The block
  tells whichever agent reads the file that DIA is active and
  which mode is in effect.

The block is delimited by stable marker pairs so it can be
rewritten or removed without touching the surrounding content. The
skill calls `tools/dia-setup/anchor.py write` (or `remove`) for
the actual file work; `anchor.py` is idempotent and replaces an
existing block in place rather than appending.

## When to call it

| Situation | What you do |
|---|---|
| First DIA-aware session in a new project | Run `/dia-setup`, pick a mode, accept the detected agent files |
| You want to change the mode | Re-run `/dia-setup`, pick "Change mode" |
| You added a new agent file (e.g. `.cursorrules`) | Re-run `/dia-setup`, pick "Add or remove anchor files" |
| You upgraded the plugin and the templates changed | Re-run `/dia-setup`, pick "Refresh anchor blocks" |
| You want the plugin to leave this project alone | Re-run `/dia-setup`, pick "Deactivate" |

You do NOT need `/dia-setup` for the normal V-Model flow. The
phase skills (`/business-analysis`, `/requirements-engineering`,
`/architecture`, `/coding`, `/testing`, `/security-audit`) call
`flow.py` directly; the mode in `.dia/config.toml` controls which
of those calls actually do something.

## Activation flow

When `.dia/config.toml` does not yet exist:

1. **Mode question.** AskUserQuestion with three options. See
   [Three modes](../concepts/three-modes) for the details. The
   recommendation depends on your situation: solo work without
   GitHub Issues -> `git-only`, team with GitHub Issues / Projects
   -> `github-sync`, plugin should stay neutral -> `off`.
2. **Agent file detection.** The skill scans the repo root for the
   six known agent files and lists them. You confirm or adjust the
   selection. Pre-selected: every detected file.
3. **Source branch question** (skipped in `off`). Default
   `develop`. Pick another branch (`main`, `dev`, or a custom
   name) if your project does not use Git Flow.
4. **Write `.dia/config.toml`.** The skill renders the template
   `skills/dia-setup/templates/dia-config.toml.tmpl` with your
   chosen values and writes it to `.dia/config.toml`. The file is
   committed alongside your code so the team shares the mode.
5. **Write anchor blocks** (skipped in `off`). The skill calls
   `tools/dia-setup/anchor.py write --mode <mode> --files <list>`,
   which renders one template per agent file (full block in
   CLAUDE.md, slim pointer in GEMINI.md, YAML-frontmatter variant
   in `.cursorrules`, etc.) and inserts it between the marker
   pair.
6. **Confirmation.** The skill reports which files were written
   and what the next step is (typically `/dia-guide` for an
   orientation read).

## Reconfigure flow

When `.dia/config.toml` already exists:

1. **Read current state.** The skill prints the active mode and
   the anchored files.
2. **Action question.** AskUserQuestion with five options:
   - **Change mode** (the most common case)
   - **Refresh anchor blocks** (after a plugin update)
   - **Add or remove anchor files**
   - **Deactivate** (sets mode to `off` and removes all blocks)
   - **Cancel**
3. **Apply the chosen action.** All actions go through the same
   `anchor.py write` / `anchor.py remove` calls so the diff stays
   minimal and predictable.

## Verification

Every successful run ends with `tools/dia-setup/anchor.py verify`,
which checks that every file listed under `anchor_files` in
`.dia/config.toml` actually carries a matching block. If anything
drifted, the skill surfaces the discrepancy and offers a refresh.

## What the skill does NOT do

`/dia-setup` is the activation surface, not the workflow. It does
not:

- invoke phase skills,
- write to `BACKLOG.md`,
- start a Handoff Ritual,
- call `flow.py` (other than via the mode that flow.py reads
  later),
- talk to GitHub.

After `/dia-setup` finishes, the project is configured. The next
slash command you usually want is `/dia-guide` for orientation.

## Files written or removed

Only these files:

- `.dia/config.toml` (created or updated)
- one or more of the six anchor targets

The skill never touches files outside this set.

## See also

- [Three modes](../concepts/three-modes) for the conceptual
  picture
- [Commands reference](../reference/commands) for the slash-
  command catalog
- [DIA Bootstrap](./dia-bootstrap) for the broader
  bootstrap context
