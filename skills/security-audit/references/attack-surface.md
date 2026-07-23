# Attack-surface enumeration (Phase 1.5)

Grep alone hits patterns but never maps the transitions where trust
changes. This step produces that map before SAST, so findings are
reasoned against real entry points, not just token matches.

Feed it from the scanner: `audit_scan.py surface --scope <S>` emits a
sorted list of `{surface_type, file, line, symbol}`. Turn that into the
three tables below. If the project ships a threat-model doc
(`REVIEWER_NOTES.md`, `SECURITY.md`), read it first and reconcile; do
not re-derive what the project already states.

## 1. Entry points

Where external input enters. From the `surface` scan plus manual review:

| Entry point | Source | Trust level | Reachable sinks |
|-------------|--------|-------------|-----------------|
| {e.g. MCP tool arg} | {LLM output} | untrusted | {fs, spawn, ...} |

Surface types the scanner tags: `code_execution`, `child_process`,
`network_egress`, `http_server`, `message_listener`, `deserialization`,
`dom_sink`, `filesystem`, `shell_open`, `protocol_handler`.

## 2. Data flows

For each untrusted entry point, trace to the dangerous sink it can
reach. A finding is only real if a flow connects untrusted source to
sink; a pattern with no reachable flow is Info at most.

```
{source} --> {transform/validation?} --> {sink file:line}
```

Note where validation exists (schema check, allowlist, escaping) and
where it is missing. Missing validation on a source->sink flow is the
finding; the grep hit alone is not.

## 3. Trust boundaries

List each boundary the data crosses and the control that governs it:

| Boundary | Control | Enforced at | Gap? |
|----------|---------|-------------|------|
| {app <-> LLM} | {input-schema validation} | {file:line} | {yes/no} |

Cross-check against the project's own boundary doc when present.

## Scope note

A diff scope reports findings only for changed files, but reachability
is traced through the FULL tree: a change in file A can become
exploitable only via file B. Never conclude "clean" from a diff scan
without tracing into unchanged code.
