---
edition: "2025"
authority: >
  This bundled list is the OFFLINE BASELINE. Phase 0 live-currency
  (SKILL.md) fetches the current published OWASP Top 10 from owasp.org,
  reconciles it against this file, and snapshots the edition actually
  used into the report. If the live step ran, its snapshot wins; if it
  did not (offline), this baseline applies and the report says so.
---

# OWASP Top 10 Checklist (baseline edition 2025)

The 2021->2025 revision folds SSRF into Broken Access Control, splits out
supply-chain and exceptional-condition handling, and keeps the core
categories. Verify the exact category set via Phase 0 before relying on
the codes; the substance below is stable regardless of numbering.

## A01: Broken Access Control (incl. SSRF)

- Missing authorization on endpoints
- Insecure Direct Object References (IDOR)
- Path traversal
- CORS misconfiguration
- Access to admin functions without a role check
- SSRF: variable outbound URL without allowlist (see cwe-patterns CWE-918)
- Identity/privilege claim taken from the request payload (Zero Trust breach)

## A02: Cryptographic Failures

- Weak or outdated encryption algorithms
- Cleartext credentials in code or config
- Missing encryption at rest or in transit
- Weak password hashing (MD5, SHA1 without salt)
- Secrets not held in the OS keychain where available

## A03: Injection

- SQL/NoSQL injection
- OS command injection
- LDAP injection
- XSS
- Template injection
- Second-order injection via un-anchored markers (see CWE-74/116)

## A04: Insecure Design

- Missing threat models
- Architectural weaknesses (e.g. trust without validation)
- Missing rate limiting
- No defense in depth
- Ungated second path around an approval gate (see agent-approval-gate.md)

## A05: Security Misconfiguration

- Default credentials active
- Unnecessary features/ports open
- Missing security headers / weak CSP (see desktop-runtime.md)
- Verbose error messages to the user
- Directory listing enabled

## A06: Vulnerable and Outdated Components

- Known CVEs in dependencies
- Outdated frameworks/libraries
- Unpatched components
- No dependency monitoring (e.g. Dependabot)
- Vendored / WASM / native deps that package audit does not see

## A07: Identification and Authentication Failures

- Weak session management
- Missing brute-force protection
- Credential stuffing possible
- Session tokens in the URL
- Non-timing-safe token comparison

## A08: Software and Data Integrity Failures (incl. supply chain)

- Insecure deserialization
- Missing signature check on updates
- CI/CD pipeline without integrity checks
- Insecure auto-update mechanisms
- Unpinned lockfiles, lifecycle-script execution, unpinned GitHub Action tags

## A09: Security Logging and Monitoring Failures

- Missing security event logs
- Sensitive data in logs (tokens, passwords, tool results)
- No alerting on suspicious activity
- Logs not tamper-evident

## A10: Mishandling of Exceptional Conditions

- Fail-open on error where it should fail-closed
- Swallowed exceptions hiding a security-relevant failure
- Partial state left committed after a cancel/abort (Esc != revert)
- Error objects dumped wholesale (leak) instead of a field allowlist
