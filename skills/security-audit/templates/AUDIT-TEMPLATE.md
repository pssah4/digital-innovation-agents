# Security Audit Report

| Field | Value |
|-------|-------|
| **Project** | {Projektname} |
| **Date** | {YYYY-MM-DD} |
| **Auditor** | Security Audit Skill |
| **Scan Scope** | {Full / Partial, welche Phasen} |
| **Risk Rating** | {Critical / High / Medium / Low} |
| **Languages** | {TypeScript / Python / etc.} |
| **Previous Audit** | {Datum oder "First Audit"} |

---

## Executive Summary

| Analysis Domain | Critical | High | Medium | Low | Info |
|-----------------|----------|------|--------|-----|------|
| SAST (CodeQL-equiv.) | {n} | {n} | {n} | {n} | {n} |
| OWASP Top 10 | {n} | {n} | {n} | {n} | {n} |
| OWASP LLM Top 10 | {n} | {n} | {n} | {n} | {n} |
| Zero Trust | {n} | {n} | {n} | {n} | {n} |
| Code Quality | {n} | {n} | {n} | {n} | {n} |
| SCA (Dependencies) | {n} | {n} | {n} | {n} | {n} |
| License Compliance | {n} | {n} | {n} | {n} | {n} |
| **Total** | **{n}** | **{n}** | **{n}** | **{n}** | **{n}** |

{2-3 Saetze Gesamtbewertung}

### Delta from Previous Audit (wenn vorhanden)

| Finding | Previous | Current | Change |
|---------|----------|---------|--------|
| {Finding-ID} | {Status} | {Status} | {Resolved/New/Unchanged} |

---

## Findings (nach Prioritaet)

### P1: Must Fix (Critical + High)

{Detaillierte Findings. Format siehe references/cwe-patterns.md}

### P2: Should Fix (Medium)

{Detaillierte Findings}

### P3: Consider (Low + Info)

{Findings mit geringem Risiko}

---

## Remediation Plan

| Priority | Finding | Remediation | Effort |
|----------|---------|-------------|--------|
| P1 | {Finding} | {Fix} | {S/M/L} |
| P2 | {Finding} | {Fix} | {S/M/L} |
| P3 | {Finding} | {Fix} | {S/M/L} |

---

## Positive Findings

{Was bereits gut umgesetzt ist. Defense in Depth, vorhandene Massnahmen, etc.}

---

## SCA Details

### Vulnerable Dependencies

| Package | Version | CVE | Severity | Fix Version |
|---------|---------|-----|----------|-------------|
| {pkg} | {ver} | {CVE-ID} | {sev} | {fix} |

### License Compliance

| Package | License | Risk |
|---------|---------|------|
| {pkg} | {license} | {OK/Review/Blocked} |

---

## Appendix

### A. Tools Used
{Welche Tools/Patterns wurden fuer die Analyse verwendet}

### B. Files Analyzed
{Scope der analysierten Dateien}

### C. Excluded from Analysis
{Was wurde nicht geprueft und warum}
