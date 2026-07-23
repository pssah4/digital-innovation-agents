# Threat modeling: STRIDE per boundary + attack chains

A per-finding checklist misses the danger that lives in CHAINS
(prompt-injection -> tool call -> sink) and in whole categories the grep
never named. Apply this lightweight pass over the trust boundaries from
`attack-surface.md`, not over every line.

## STRIDE per boundary

For each trust boundary, ask the six STRIDE questions and map a hit to
the CWE/OWASP category it belongs to:

| STRIDE | Question at this boundary | Maps to |
|--------|---------------------------|---------|
| Spoofing | Can identity across this boundary be forged? | A07, CWE-287 |
| Tampering | Can data in transit / at rest be altered? | A08, CWE-345 |
| Repudiation | Is there an audit trail for actions here? | A09, CWE-778 |
| Information disclosure | Can data leak across it? | A01/A02, CWE-200 |
| Denial of service | Can it be exhausted (CPU/mem/cost/tokens)? | CWE-400, LLM04 |
| Elevation of privilege | Can a caller gain rights it should not? | A01, CWE-269 |

One line per (boundary, STRIDE hit). No hit -> no line. This is a
focusing tool, not a form to fill completely.

## Attack chains

Single findings scored in isolation understate multi-step risk. For each
untrusted entry point, sketch the shortest chain to material impact:

```
{untrusted source} -> {step} -> {step} -> {impact}
```

Chain severity is the impact of the END state, not the max of the steps.
A Medium prompt-injection that chains into an ungated write is a High
chain. Record the chain, then file the weakest link as the primary
finding with the chain as its Risk sentence.

## When to run

Full audits and any audit whose scope touches a trust boundary. Skip for
a narrow diff that stays inside one already-modeled component.
