---
applies-when: detect reports LLM/agent APIs (reference_gates.owasp-llm true)
read-when: Phase 4, deepening LLM01 (prompt injection) in both directions
---

# Prompt-injection boundaries

Gated on an LLM/agent codebase. LLM01 in the checklist asks whether
indirect injection was "considered"; this is the enumeration and the two
non-obvious failure modes.

## Enumerate untrusted -> trusted transitions

Every place where attacker-influenced text reaches the model as if it
were trusted context:

- MCP tool `name` / `description` fields (a hostile server controls them)
- Skill / plugin names and descriptions
- Attached files, pasted content, fetched web/document text
- Memory / stored facts / conversation history replayed into the prompt
- Sub-agent / sub-role instructions assembled from the above

For each, name the single choke point where it is neutralized. One
shared defang at a choke point beats per-path sanitizing that drifts.

## Failure mode 1: reassembly-unsafe defang

A single-pass `.replace()` that strips a marker can REBUILD a nested
one. Example: stripping `<available_skills>` once turns
`<available_<available_skills>skills>` back into the live tag. The defang
must iterate to a fixpoint (repeat until the string stops changing), and
guard on `content.length` so a huge payload cannot exhaust it. Also
check join/concat reassembly, where two sanitized fragments form a live
marker after concatenation. Flag any single-pass strip on untrusted
text: High.

## Failure mode 2: the emitter direction (agent as server)

The checklist assumes the LLM is a CONSUMER. When the codebase is itself
an MCP/agent server, check the OUTPUT direction too:

- Tool descriptions and `initialize.instructions` it exposes must carry
  no coercive language, no PII, no persona, no internal IDs.
- Tool responses must not be auto-augmented with system-prompt-like text
  (that is injection into the CALLER's model).
- Persona / memory must not leak outbound through exposed surfaces.

## Marker anchoring

Machine markers placed into user- or sync-writable regions must be
line-anchored (`^\s*<marker>\s*$`) so injected text cannot forge them
(second-order injection). Neutralize the markers again on the way out.
