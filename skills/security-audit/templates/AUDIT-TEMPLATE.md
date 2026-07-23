<!-- See skills/security-audit/SKILL.md for how to fill -->

# Security Audit Report

| Field | Value |
|-------|-------|
| Project | {Projektname} |
| Date | {YYYY-MM-DD} |
| Scan Scope | {Full / Partial, welche Phasen} |
| Risk Rating | {Critical / High / Medium / Low} |

---

## Executive Summary

| Analysis Domain | Critical | High | Medium | Low | Info |
|-----------------|----------|------|--------|-----|------|
| Code findings (SAST, OWASP, Zero Trust, Quality) | {n} | {n} | {n} | {n} | {n} |
| SCA (Dependencies) | {n} | {n} | {n} | {n} | {n} |
| License Compliance | {n} | {n} | {n} | {n} | {n} |
| Total | {n} | {n} | {n} | {n} | {n} |

{2-3 Sätze Gesamtbewertung.}

---

## Findings (nach Priorität)

Inline format pro Finding: `**{FP}** - Severity / CWE-{n} / CVSS {vector}={score} / `file.ts:LineNN` - Risk: {1 Satz} - Evidence: {snippet/PoC} - Remediation: {1 Satz} - Effort: S/M/L`. CVSS mandatory for High+; Evidence mandatory (snippet, source->sink trace, or PoC result). Status one of Confirmed / Unverified / False Positive / Resolved.

### P1: Must Fix (Critical + High)

- {Finding-Zeile}

### P2: Should Fix (Medium)

- {Finding-Zeile}

### P3: Consider (Low + Info)

- {Finding-Zeile}

---

## SCA: Vulnerable Dependencies

| Package | Version | CVE | Severity | Fix Version |
|---------|---------|-----|----------|-------------|
| {pkg} | {ver} | {CVE-ID} | {sev} | {fix} |

## License Compliance

| Package | License | Risk |
|---------|---------|------|
| {pkg} | {license} | {OK / Review / Blocked} |

---

## Scope and Tools

- Tools: {z.B. semgrep, npm audit, custom CWE patterns}
- Files analyzed: {Pfade oder Anzahl, kurz}
- Excluded: {Was bewusst nicht geprüft wurde, plus Grund}

---

## Coverage and limitations

Mandatory. `report_assembler.py fill` generates this from the scan; only
list what actually held. Names the method blindspots so a silent report
is never read as full coverage.

- SAST depth: {semgrep AST + grep, or grep-only = higher false-negative risk}
- Secrets: {dedicated scanner, or redacting fallback + history not scanned}
- SCA: {tools that ran; offline = CVE stale/absent; vendored/WASM unscanned}
- No DAST/runtime except opt-in isolated PoC probes
- Scope: {full / diff-scope + file count}
- Threat taxonomy snapshot: {OWASP / LLM / CWE editions used}
- Not evaluated: {CWE Top 25 entries or areas skipped}
