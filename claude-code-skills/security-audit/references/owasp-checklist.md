# OWASP Top 10 (2021) Checklist

## A01: Broken Access Control

- Fehlende Autorisierung auf Endpunkten
- Insecure Direct Object References (IDOR)
- Path Traversal
- CORS Misconfiguration
- Zugriff auf Admin-Funktionen ohne Rollenpruefung

## A02: Cryptographic Failures

- Schwache oder veraltete Verschluesselungsalgorithmen
- Klartext-Credentials in Code oder Config
- Fehlende Verschluesselung at Rest oder in Transit
- Schwache Passwort-Hashing (MD5, SHA1 ohne Salt)

## A03: Injection

- SQL/NoSQL Injection
- OS Command Injection
- LDAP Injection
- XSS (Cross-Site Scripting)
- Template Injection

## A04: Insecure Design

- Fehlende Threat Models
- Architektur-Schwaechen (z.B. Trust ohne Validation)
- Fehlende Rate Limiting
- Keine Defense-in-Depth

## A05: Security Misconfiguration

- Default-Credentials aktiv
- Unnoetige Features/Ports offen
- Fehlende Security Headers
- Verbose Error Messages an User
- Directory Listing aktiv

## A06: Vulnerable and Outdated Components

- Bekannte CVEs in Dependencies
- Veraltete Frameworks/Libraries
- Nicht gepatchte Komponenten
- Keine Dependency-Monitoring (z.B. Dependabot)

## A07: Identification and Authentication Failures

- Schwaches Session-Management
- Fehlender Brute-Force-Schutz
- Credential Stuffing moeglich
- Session Tokens in URL

## A08: Software and Data Integrity Failures

- Unsichere Deserialisierung
- Fehlende Signaturpruefung bei Updates
- CI/CD Pipeline ohne Integrity Checks
- Unsichere Auto-Update-Mechanismen

## A09: Security Logging and Monitoring Failures

- Fehlende Security Event Logs
- Sensitive Data in Logs (Tokens, Passwoerter)
- Kein Alerting bei verdaechtigen Aktivitaeten
- Logs nicht manipulationssicher

## A10: Server-Side Request Forgery (SSRF)

- URL-Input ohne Validierung
- Fehlende Allowlist fuer ausgehende Requests
- Zugriff auf interne Services via User-Input
- Cloud Metadata Endpoint erreichbar
