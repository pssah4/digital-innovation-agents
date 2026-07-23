---
applies-when: detect reports LLM/agent APIs (reference_gates.owasp-llm true) and the codebase executes tools/actions
read-when: Phase 4, deepening LLM06 (sensitive info) and LLM08 (excessive agency)
---

# Agent approval gate / excessive agency

Gated on an agentic codebase (the app calls tools/actions on the user's
behalf). The OWASP LLM checklist asks yes/no questions here; this is the
procedure. The recurring real-world failure is not a missing gate but a
SECOND path around an existing one.

## Core procedure: enumerate every mutating/escalating sink

1. List every sink that writes, deletes, spawns, spends money/tokens, or
   escalates privilege.
2. For each sink, name the gating predicate (the approval/confirmation
   check) and the exact `file:line` where it is enforced.
3. Any sink reachable by a path that does NOT pass its predicate is a
   High finding. An ungated second path is the classic bug.

## Checklist (each an ungated-path candidate)

- Two entry points to one effect (e.g. a "write" tool and a generic
  "execute op" tool that also writes): does the gate cover BOTH?
- Compound operations: does a single approved action fan out into
  several un-approved sub-writes?
- Grant/permission resolution: is a read grant silently accepted where a
  write grant is required?
- Cancel semantics: does pressing Escape / X mean "revert", or does it
  leave a partial mutation committed? "Esc != revert-all" is a finding.
- Kill switch / default-deny: if the approval mechanism is disabled or
  errors, does the action fail closed (blocked) or fail open (proceeds)?
- Rate/quantity limits on tool execution and a task-wide token/cost
  budget across the whole subtask tree (not per-call only).
- Destructive operations require explicit confirmation, not a default-yes.

## Finding shape

Report the ungated path as the primary finding; cite both the gate that
exists and the path that bypasses it, with both `file:line`
coordinates. Severity is the impact of the ungated sink.
