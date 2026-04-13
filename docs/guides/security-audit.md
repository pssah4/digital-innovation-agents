---
title: Security Audit
description: Comprehensive security audit covering OWASP Top 10, OWASP LLM Top 10, SAST, SCA, and Zero Trust.
---

# Security Audit

`/security-audit` runs a full security audit on the implemented
codebase and produces a prioritized remediation plan.

**Input:** Codebase, dependencies, configuration
**Output:** Security report in `_devprocess/analysis/security/AUDIT-{PROJECT}-{DATE}.md`

## Six audit phases

1. **Reconnaissance** -- identify tech stack, dependencies, existing
   security measures
2. **SAST (Static Application Security Testing)** -- CWE-based static
   analysis with grep/analysis patterns from `references/cwe-patterns.md`
3. **OWASP Top 10** -- all 10 categories (A01-A10) with concrete patterns
4. **OWASP LLM Top 10** -- LLM01-LLM10, relevant when the project uses
   LLM APIs
5. **SCA (Software Composition Analysis)** -- dependency vulnerabilities
   (`npm audit`, `pip-audit`), license check
6. **Zero Trust & Code Quality** -- input validation, least privilege,
   fail-closed defaults, audit trail, hardcoded credentials, debug code
   in production

## Severity schema

- **Critical**: immediately exploitable, data loss / RCE possible
- **High**: exploitable with low effort, significant impact
- **Medium**: exploitable under specific conditions
- **Low**: low risk, best-practice improvement
- **Info**: note, no direct threat

## Fix-loop

Identical to `/testing`: 4 user options (fix all, fix only P1, approve
one-by-one, report only). Deferred findings land in
`_devprocess/context/10_backlog.md` with full traceability.

## Handoff

Ends with the 3-part Handoff Ritual. Next phase: **Phase 7 Release
Closure** via `/v-model-workflow`. The handoff context includes the
release readiness verdict (green/yellow/red).

## Source

Full skill content in
[`skills/security-audit/SKILL.md`](https://github.com/pssah4/digital-innovation-agents/blob/main/skills/security-audit/SKILL.md).
