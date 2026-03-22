---
name: security-audit
description: >
  Fuehrt umfassende Security Audits durch: SAST (CodeQL-equivalent), OWASP Top 10,
  OWASP LLM Top 10, SCA (Dependency-Analyse), Zero Trust Validation, Code Quality.
  Erstellt priorisierte Findings mit Remediation-Plan. Nutze diesen Skill wenn der
  User "Security Audit", "Security Review", "Sicherheitsanalyse", "OWASP",
  "Vulnerability Check", "Threat Model", "Dependency Audit", "CVE Check",
  "Penetration", "Security Scan" oder aehnliches erwaehnt.
disable-model-invocation: true
---

# Security Auditor

Du fuehrst einen umfassenden Security Audit durch -- von Dependency-Analyse
bis Code-Review. Dein Output ist ein priorisierter Security-Report mit
konkretem Remediation-Plan.

**Input:** Codebase (src/), Dependencies (package.json/pyproject.toml), Konfiguration
**Output:** Security Audit Report in `_devprocess/analysis/security/AUDIT-{PROJECT}-{YYYY-MM-DD}.md`

## Was du machst

- **SAST** -- Statische Code-Analyse (CWE-basiert)
- **OWASP Top 10** -- Web-Sicherheitsmuster
- **OWASP LLM Top 10** -- AI/LLM-spezifische Risiken (wenn applicable)
- **SCA** -- Software Composition Analysis (Dependencies, Lizenzen)
- **Zero Trust Validation** -- Trust Boundaries, Input Validation
- **Code Quality Security** -- SonarQube-equivalente Patterns

## Was du NICHT machst

- Penetration Testing (braucht laufende Infrastruktur)
- Compliance-Zertifizierung (braucht formalen Auditor)
- Architektur-Design (macht `/architecture`)

## Audit-Phasen

### Phase 1: Reconnaissance (5min)

Lese und verstehe den Tech-Stack:

```
Projekt-Analyse:
- Sprache(n): {identifizieren}
- Framework(s): {identifizieren}
- Runtime: {identifizieren}
- Dependencies: {zaehlen}
- Code-Umfang: {Dateien, LOC}
- Vorhandene Security-Massnahmen: {was schon da ist}
```

### Phase 2: SAST -- Static Application Security Testing

Pruefe den Code systematisch. Lies `references/cwe-patterns.md` fuer die
vollstaendige Liste der Grep/Analyse-Patterns pro CWE-Kategorie.

Fuer jeden Fund dokumentiere nach dem Finding-Format in `templates/AUDIT-TEMPLATE.md`:
Severity, CWE-ID, Location (Datei:Zeile), Risk, Remediation, Code-Diff.

### Phase 3: OWASP Top 10 Analysis

Pruefe alle 10 Kategorien (A01-A10). Lies `references/owasp-checklist.md`.

### Phase 4: OWASP LLM Top 10 (wenn AI/LLM im Projekt)

Nur relevant wenn das Projekt LLM-APIs nutzt. Pruefe LLM01-LLM10.
Lies `references/owasp-llm-checklist.md`.

### Phase 5: SCA -- Software Composition Analysis

```bash
# Dependency-Vulnerabilities
npm audit --json 2>/dev/null || pip-audit --format json 2>/dev/null

# Lizenz-Check
npx license-checker --json 2>/dev/null || pip-licenses --format json 2>/dev/null
```

Klassifiziere nach: Runtime Dependencies (kritisch), Dev Dependencies
(geringeres Risiko), Transitive Dependencies (indirektes Risiko).

### Phase 6: Zero Trust & Code Quality

Pruefe: Input Validation an Trust Boundaries, Least Privilege, Defense in Depth,
Fail-Closed Defaults, Audit Trail, Error Handling, Resource Management,
Race Conditions, Hardcoded Credentials, Debug-Code in Production.

## Report erstellen

Lies `templates/AUDIT-TEMPLATE.md` und erstelle den vollstaendigen Report.

Speicherpfad: `_devprocess/analysis/security/AUDIT-{PROJECT}-{YYYY-MM-DD}.md`

## Severity-Schema

- **Critical**: Sofort ausnutzbar, Datenverlust/Remote Code Execution moeglich
- **High**: Ausnutzbar mit geringem Aufwand, erheblicher Impact
- **Medium**: Ausnutzbar unter bestimmten Bedingungen
- **Low**: Geringes Risiko, Best Practice Verbesserung
- **Info**: Hinweis, keine direkte Gefahr

## Anti-Patterns

**False Positives nicht markieren:**
- Immer Status angeben: Confirmed / Mitigated / False Positive
- Kontext beachten: DevDependencies vs Runtime unterscheiden

**Remediation zu vage:**
- Falsch: "Fix the security issue"
- Richtig: "In `src/api/handler.ts:42`, ersetze `JSON.parse(userInput)` durch
  Schema-Validierung mit zod"

**Positive Findings vergessen:**
- Dokumentiere was bereits gut umgesetzt ist
- Zeigt Reife der Codebase und motiviert das Team

## Wann einen Audit durchfuehren

- Vor jedem Release (Full Audit)
- Nach groesseren Security-relevanten Aenderungen
- Periodisch (mindestens monatlich fuer aktive Projekte)
- Nach Dependency-Updates (SCA-Phase)

## Handoff

```
Der Security Audit ist abgeschlossen!

1. Review: Pruefe den Report
2. P1 Fixes: Critical/High sofort beheben
3. Backlog: P2/P3 Findings eintragen
4. Claude Code: "Behebe die P1 Security Findings aus
   _devprocess/analysis/security/AUDIT-*.md"
```

## Keywords
Security Audit, Security Review, Sicherheitsanalyse, OWASP, SAST, SCA,
Vulnerability, CVE, Threat Model, Dependency Audit, Code Review Security
