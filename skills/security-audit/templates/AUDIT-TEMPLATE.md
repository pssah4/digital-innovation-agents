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

Inline format pro Finding: `**{ID}** - Severity / CWE-{n} / `path/to/file.ts:LineNN` - Risk: {1 Satz} - Remediation: {1 Satz} - Effort: S/M/L`

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
