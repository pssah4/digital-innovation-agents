---
edition: "2025"
authority: >
  Offline baseline. Phase 0 live-currency fetches the current OWASP Top
  10 for LLM Applications from genai.owasp.org, reconciles, and snapshots
  the edition used. Live snapshot wins when it ran; else this applies and
  the report says so.
---

# OWASP Top 10 for LLM Applications (baseline edition 2025)

Relevant only when the project uses LLM/agent APIs (`detect` reports
`reference_gates.owasp-llm = true`). The 2025 list adds System Prompt
Leakage (LLM07) and Vector/Embedding Weaknesses (LLM08); confirm the
exact set via Phase 0.

## LLM01: Prompt Injection

- Is the system prompt protected?
- Is user input filtered before it reaches the LLM?
- Indirect injection via documents/web/tool metadata considered?
- Defang iterates to a fixpoint (not single-pass); markers line-anchored?
  (see prompt-injection-boundaries.md)
- Emitter direction: if this app is an MCP/agent server, are its exposed
  tool descriptions/responses free of coercive text, PII, internal IDs?

## LLM02: Sensitive Information Disclosure

- PII kept out of prompts?
- API keys never in logs?
- Conversation history retention policy?

## LLM03: Supply Chain

- API keys stored securely (not in code)?
- Model versions pinned?
- Fallback on provider outage?
- Third-party model/plugin provenance checked?

## LLM04: Data and Model Poisoning

- Pre-trained models: usually not directly relevant
- If fine-tuning: training-data integrity checked?

## LLM05: Improper Output Handling

- LLM output validated before use in code/UI?
- No direct execution of LLM-generated code?
- HTML/DOM output sanitized?

## LLM06: Excessive Agency

- Tools scoped to least privilege?
- Destructive operations require confirmation?
- Rate limits on tool execution + task-wide cost budget?
- Every mutating sink gated on all reachable paths?
  (see agent-approval-gate.md)

## LLM07: System Prompt Leakage

- System prompt not recoverable via crafted input?
- No secrets/credentials embedded in the system prompt?
- Prompt content that leaks is treated as disclosed?

## LLM08: Vector and Embedding Weaknesses

- RAG sources access-controlled (no cross-tenant leakage)?
- Embedded/retrieved content treated as untrusted (indirect injection)?
- Poisoned-document detection where feasible?

## LLM09: Misinformation / Overreliance

- LLM output validated (not blindly trusted)?
- Critical decisions gated on human review?
- Hallucination detection where possible?

## LLM10: Unbounded Consumption

- Rate limiting on LLM API calls?
- Token/output limits set?
- Timeout handling for LLM requests?
- Cost controls (max spend) across the subtask tree?
- Model-extraction / theft via bulk querying mitigated?
