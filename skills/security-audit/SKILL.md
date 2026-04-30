---
name: security-audit
description: >
  Performs a COMPREHENSIVE, formal security audit of an entire codebase
  and produces a written audit report (AUDIT-{PROJECT}-{DATE}.md) with
  prioritized findings (H/M/L) and a remediation plan. Covers SAST, OWASP
  Top 10, OWASP LLM Top 10, SCA (dependency analysis), Zero Trust
  validation, code quality. Takes 30+ minutes. TRIGGER ONLY when the user
  explicitly requests a formal full-codebase audit producing a report:
  "security audit", "OWASP audit", "full security review", "AUDIT-Report
  erstellen", "Codebase auditieren", "SCA audit", "dependency audit",
  "CVE audit", "Sicherheitsaudit". DO NOT trigger for: PR-level security
  checks (use the built-in security-review skill), one-off security
  questions, threat-modeling discussions without an audit report,
  individual finding fixes, or generic mentions of "secure" / "security".
disable-model-invocation: false
---

# Security Auditor

You perform a comprehensive security audit covering dependency analysis
through to code review. Your output is a prioritized security report
with a concrete remediation plan.

**Input:** Codebase (`src/`), dependencies (`package.json`/`pyproject.toml`), configuration
**Output:** Security Audit Report in `_devprocess/analysis/security/AUDIT-{PROJECT}-{YYYY-MM-DD}.md`

**Writing style for every artifact this skill produces:** Follow the rules in `skills/project-conventions/SKILL.md` under "Writing style for every artifact". Zero em dashes of any form. No Unicode em dash (U+2014), no en dash (U+2013), no double-hyphen substitute. No AI vocabulary, no negative parallelisms. Every finding description, every causal chain, every remediation step, and every prioritisation rationale is written in that style. Before you save an artifact, scan it for U+2014 and U+2013 and fix any hit.

## MANDATORY Pre-Phase 0: Branch protection

Before writing the audit report or any FIX/IMP follow-ups, verify
the user is not on a protected branch (`main`, `master`, `dev`).
If protected, ask via `AskUserQuestion`:

- A) Create feature branch `feature/audit-{YYYY-MM-DD}` (recommended)
- B) Stay on `{current_branch}` (only when reading-only without writing)
- C) Custom branch name

Recommendation: A. Audits write a multi-section AUDIT report and
typically queue several FIX/IMP follow-ups; those need a feature
branch.

Full rules: `skills/project-conventions/references/branch-protection.md`.

## What you do

- **SAST** -- Static code analysis (CWE-based)
- **OWASP Top 10** -- Web security patterns
- **OWASP LLM Top 10** -- AI/LLM-specific risks (when applicable)
- **SCA** -- Software Composition Analysis (dependencies, licenses)
- **Zero Trust Validation** -- Trust boundaries, input validation
- **Code Quality Security** -- SonarQube-equivalent patterns

## What you do NOT do

- Penetration Testing (needs running infrastructure)
- Compliance certification (needs a formal auditor)
- Architecture design (done by `/architecture`)

## Audit Phases

### Phase 1: Reconnaissance (5 min)

Read and understand the tech stack:

```
Project analysis:
- Language(s): {identify}
- Framework(s): {identify}
- Runtime: {identify}
- Dependencies: {count}
- Code size: {files, LOC}
- Existing security measures: {what's already in place}
```

### Phase 2: SAST -- Static Application Security Testing

Systematically check the code. Read `references/cwe-patterns.md` for the
full list of grep/analysis patterns per CWE category.

For each finding, document according to the Finding format in
`templates/AUDIT-TEMPLATE.md`: Severity, CWE-ID, Location (file:line),
Risk, Remediation, Code diff.

### Phase 3: OWASP Top 10 Analysis

Check all 10 categories (A01-A10). Read `references/owasp-checklist.md`.

### Phase 4: OWASP LLM Top 10 (when AI/LLM is in the project)

Only relevant if the project uses LLM APIs. Check LLM01-LLM10.
Read `references/owasp-llm-checklist.md`.

### Phase 5: SCA -- Software Composition Analysis

```bash
# Dependency vulnerabilities
npm audit --json 2>/dev/null || pip-audit --format json 2>/dev/null

# License check
npx license-checker --json 2>/dev/null || pip-licenses --format json 2>/dev/null
```

Classify by: Runtime Dependencies (critical), Dev Dependencies (lower risk),
Transitive Dependencies (indirect risk).

### Phase 6: Zero Trust & Code Quality

Check: Input validation at trust boundaries, Least Privilege, Defense in
Depth, Fail-Closed Defaults, Audit Trail, Error Handling, Resource
Management, Race Conditions, Hardcoded Credentials, Debug code in production.

## Create report

Read `templates/AUDIT-TEMPLATE.md` and create the full report.

Save to: `_devprocess/analysis/security/AUDIT-{PROJECT}-{YYYY-MM-DD}.md`

## Severity schema

- **Critical**: Immediately exploitable, data loss / RCE possible
- **High**: Exploitable with low effort, significant impact
- **Medium**: Exploitable under specific conditions
- **Low**: Low risk, best-practice improvement
- **Info**: Note, no direct threat

## Anti-patterns

**Don't mark false positives silently:**
- Always state the status: Confirmed / Mitigated / False Positive
- Consider context: DevDependencies vs. Runtime

**Remediation too vague:**
- Wrong: "Fix the security issue"
- Right: "In `src/api/handler.ts:42`, replace `JSON.parse(userInput)` with
  schema validation using zod"

**Don't forget positive findings:**
- Document what is already well implemented
- Shows codebase maturity and motivates the team

## When to run an audit

- Before every release (Full Audit)
- After significant security-relevant changes
- Periodically (at least monthly for active projects)
- After dependency updates (SCA phase)

---

## Fix-Loop: Findings -> Fix -> Re-Audit

After the audit, a fix-loop starts. The user decides scope and approach.

### Step 1: Summarize findings

```
=== Security Audit Result ===

Overall risk: {Critical / High / Medium / Low}

P1 -- Must Fix (Critical + High): {N} findings
- {H-1}: {title} -- {file:line} -- effort: {S/M/L}
- {H-2}: {title} -- {file:line} -- effort: {S/M/L}

P2 -- Should Fix (Medium): {N} findings
- {M-1}: {title} -- {file:line} -- effort: {S/M/L}

P3 -- Consider (Low + Info): {N} findings
- {L-1}: {title} -- effort: {S/M/L}

Positive findings: {what is already well implemented}
```

### Step 2: Ask user how to proceed

```
How should I handle the findings?

A) Fix all findings (P1 + P2 + P3)
   -> I fix everything and run a re-audit

B) Fix only P1, defer P2/P3 to backlog
   -> Critical/High fixed immediately, rest documented

C) Approve fixes one by one
   -> I show each fix before implementation

D) Nothing to fix -- report only
   -> All findings go to the backlog
```

### Step 3: Fix implementation

For each finding to be fixed:

1. Implement the concrete fix (code diff from remediation plan)
2. Run affected tests (no regressions)
3. Update finding status in the audit report: `Confirmed` -> `Resolved`
4. On Option C: show the fix to the user before continuing

### Step 4: Re-audit (automatic)

After all fixes: re-run the affected audit phases.

```
=== Re-Audit Result ===

Before: {N} P1, {N} P2, {N} P3
After:  {N} P1, {N} P2, {N} P3

Resolved: {list of fixed findings}
New: {if a fix introduced new findings}

{If P1 still open: back to step 2}
{If P1 all resolved:}

All Critical/High findings resolved!
```

The loop repeats until all in-scope findings are resolved or the user aborts.

### Step 5: Deferred findings -> Backlog

Findings not fixed immediately (e.g. P2/P3 on Option B):

1. **Backlog**: each open finding gets a row in
   `_devprocess/context/BACKLOG.md` following the binding format
   from `skills/requirements-engineering/templates/BACKLOG-TEMPLATE.md`.
   Security findings live in the **Standalone Items** section with:
   - `Typ = Security`
   - `Source = SEC`
   - `Prio` mapped from finding severity (H -> P1, M -> P2, L -> P3)
   - `Status = Planned`
   - `Evidence = path:line`
   - `Notes` = finding ID (H-N / M-N / L-N) + short risk description
   After adding rows, refresh the dashboard counts and "Letztes Update".

2. **Audit report**: status stays `Confirmed` with note "Deferred to backlog"

### Step 6: Update artifacts

- Audit report: save final version with all status updates
- Feature specs: write back security-relevant changes
- ADRs: when security fixes affect architecture decisions
- Backlog: open findings documented

### Closing

```
Security Audit complete!

Resolved: {N} findings fixed
Deferred: {N} findings in backlog
Report: _devprocess/analysis/security/AUDIT-{PROJECT}-{DATE}.md
```

---

## Handoff Ritual (mandatory at end of phase)

After the fix-loop is closed, this skill always runs the handoff ritual,
regardless of how it was started (directly or via `/dia-orchestrator`).

### Part 1: Artifact report

```
Produced / updated:
- _devprocess/analysis/security/AUDIT-{PROJECT}-{DATE}.md: full report
- Findings resolved: {N} (P1: {N}, P2: {N}, P3: {N})
- Findings deferred: {N} (in backlog)
- _devprocess/context/BACKLOG.md: deferred findings added
```

### Part 2: Handoff context

Append a new entry to `_devprocess/context/HANDOFFS.md` with:

- **Overall risk verdict**: Critical / High / Medium / Low
- **Unresolved P0/P1**: any high-severity findings still open and why
- **Deferred items**: what went to backlog with reasons
- **Architectural security concerns**: patterns that should be revisited
  in a future `/architecture` cycle (e.g. trust-boundary issues that
  require redesign, not patching)
- **Release recommendation**: green / yellow / red for moving to Phase 7

### Part 3: Transition question

Ask the user:

> "Security audit complete. Report saved to:
> - `_devprocess/analysis/security/AUDIT-{PROJECT}-{DATE}.md`
>
> Release readiness: {green/yellow/red}
>
> The next step in the V-Model workflow is **Phase 7: Release Closure**
> (via `/dia-orchestrator`), which will:
> 1. Finalize all artifacts (BA, Features, ADRs, arc42)
> 2. Generate release notes
> 3. Update CHANGELOG
> 4. Clean up the backlog
> 5. Produce a closing report
>
> Shall I invoke `/dia-orchestrator` to run the Release Closure now, or
> would you like to review the audit first?"

**On agreement** ("yes" / "go" / "next") or when running inside
`/dia-orchestrator`:
-> Hand control back to `/dia-orchestrator` for Phase 7

**On rejection** ("no" / "stop" / "I want to check first"):
-> Pause and wait for user instruction

## Keywords
Security Audit, Security Review, OWASP, SAST, SCA, Vulnerability, CVE,
Threat Model, Dependency Audit, Code Review Security, Fix-Loop, Handoff
