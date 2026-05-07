# Anchor format reference

This file documents the format and idempotency rules of the DIA
anchor block. The behaviour described here is implemented in
`tools/dia-setup/anchor.py`.

## Block markers

Two marker pairs are supported. The script chooses one per file
based on the file syntax.

### Markdown-style files

Used in: `CLAUDE.md`, `AGENTS.md`, `GEMINI.md`,
`.github/copilot-instructions.md`.

```
<!-- DIA-WORKFLOW-START (managed by digital-innovation-agents) -->
...rendered template content...
<!-- DIA-WORKFLOW-END -->
```

### Hash-comment files

Used in: `.cursorrules`, `.windsurfrules`.

```
# === DIA-WORKFLOW-START (managed by digital-innovation-agents) ===
...rendered template content...
# === DIA-WORKFLOW-END ===
```

The marker strings are byte-stable. The script never edits content
outside these markers and never deletes the surrounding file.

## Idempotency

`anchor.py write` is safe to run multiple times. The detection rule
is: if a block matching the start and end marker exists, replace
its contents in place. If no block exists, append the block at the
end of the file with a single blank line of separation.

`anchor.py remove` removes only the block. The remainder of the
file is preserved. If the block was the only content, the file is
truncated to empty rather than deleted, so external tooling that
expects the file (e.g. Cursor) does not break.

## Templates

Each known target file maps to one template under
`skills/dia-setup/templates/`. Templates are plain text with two
placeholders:

- `{{mode}}` is replaced with the active mode string (`off`,
  `git-only`, `github-sync`).
- `{{repo_name}}` is replaced with the basename of the repo root.

No other templating is performed. Comments and headings inside
templates are passed through verbatim.

## Discovery

The script discovers the repo root by walking upwards until it
finds a `.git/` or `.dia/` directory. Inside the resolved root, it
operates only on the well-known target paths listed in
`KNOWN_TARGETS` in `tools/dia-setup/anchor.py`.

Adding a new target file means: extend `KNOWN_TARGETS`, add a
template under `skills/dia-setup/templates/`, and ensure the
template uses the appropriate marker style (Markdown or hash).

## Verification

`anchor.py verify` reads `.dia/config.toml` and confirms that every
file listed under `anchor_files` carries a matching block. Exit
code `0` means consistent, `1` means drift, `2` means no config
file present.

## Why a managed block instead of a separate file

User projects sometimes already have CLAUDE.md or AGENTS.md with
project-specific rules. A separate DIA file would split the
agent-facing context across multiple files and many tools only
read the canonical one. A managed block inside the canonical file
is the smallest intervention that gets the workflow visible to
the agent without taking ownership of the file as a whole.
