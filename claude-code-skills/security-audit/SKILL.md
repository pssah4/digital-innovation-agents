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

## Handoff und Fix-Loop

Nach Abschluss des Audits startet der Fix-Loop. Der User entscheidet
ueber Scope und Vorgehen.

### Schritt 1: Findings zusammenfassen

```
=== Security Audit Ergebnis ===

Gesamt-Risiko: {Critical / High / Medium / Low}

P1 -- Must Fix (Critical + High): {N} Findings
- {H-1}: {Titel} -- {Datei:Zeile} -- Aufwand: {S/M/L}
- {H-2}: {Titel} -- {Datei:Zeile} -- Aufwand: {S/M/L}

P2 -- Should Fix (Medium): {N} Findings
- {M-1}: {Titel} -- {Datei:Zeile} -- Aufwand: {S/M/L}

P3 -- Consider (Low + Info): {N} Findings
- {L-1}: {Titel} -- Aufwand: {S/M/L}

Positive Findings: {Was bereits gut umgesetzt ist}
```

### Schritt 2: User-Freigabe einholen

```
Wie soll ich mit den Findings umgehen?

A) Alle Findings fixen (P1 + P2 + P3)
   -> Ich fixe alles automatisch und fuehre danach einen Re-Audit durch

B) Nur P1 fixen, P2/P3 ins Backlog
   -> Critical/High werden sofort gefixt, Rest wird dokumentiert

C) Fixes einzeln freigeben
   -> Ich zeige dir jeden Fix vor der Implementierung

D) Nichts fixen -- nur Report erstellen
   -> Alle Findings werden ins Backlog eingetragen
```

### Schritt 3: Fix-Implementierung

Fuer jedes Finding das gefixt werden soll:

1. Konkreten Fix implementieren (Code-Diff aus dem Remediation-Plan)
2. Betroffene Tests ausfuehren (keine Regressions)
3. Finding-Status im Audit-Report aktualisieren: `Confirmed` -> `Resolved`
4. Bei Option C: Fix dem User zeigen bevor weiter

### Schritt 4: Re-Audit (automatisch)

Nach allen Fixes: Die betroffenen Audit-Phasen erneut ausfuehren.

```
=== Re-Audit Ergebnis ===

Vorher: {N} P1, {N} P2, {N} P3
Nachher: {N} P1, {N} P2, {N} P3

Resolved: {Liste der behobenen Findings}
New: {Falls der Fix neue Findings erzeugt hat}

{Wenn noch P1 offen: zurueck zu Schritt 2}
{Wenn P1 alle resolved:}

Alle Critical/High Findings behoben!
```

Der Loop wiederholt sich bis alle Findings im gewaehlten Scope
resolved sind oder der User abbricht.

### Schritt 5: Nicht-gefixte Findings ins Backlog

Findings die nicht sofort gefixt werden (z.B. P2/P3 bei Option B):

1. **Feature-Backlog**: Jedes offene Finding als Eintrag in
   `_devprocess/context/10_backlog.md` mit:
   - Finding-ID und Severity
   - Betroffene Datei und Zeile
   - Kurzbeschreibung des Risikos
   - Geschaetzter Fix-Aufwand

2. **Audit-Report**: Status bleibt `Confirmed` mit Vermerk
   "Deferred to backlog"

### Schritt 6: Artefakte aktualisieren

- Audit-Report: Finale Version mit allen Status-Updates speichern
- Feature-Specs: Security-relevante Aenderungen zurueckschreiben
- ADRs: Wenn Security-Fixes Architektur-Entscheidungen betreffen
- Backlog: Offene Findings dokumentiert

### Abschluss

```
Security Audit abgeschlossen!

Resolved: {N} Findings gefixt
Deferred: {N} Findings im Backlog
Report: _devprocess/analysis/security/AUDIT-{PROJECT}-{DATE}.md
```

## Keywords
Security Audit, Security Review, Sicherheitsanalyse, OWASP, SAST, SCA,
Vulnerability, CVE, Threat Model, Dependency Audit, Code Review Security
