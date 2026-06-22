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
through code review. Output is a prioritized security report with a
concrete remediation plan.

**Input:** Codebase (`src/`), dependencies, configuration.
**Output:** `_devprocess/analysis/AUDIT-{PROJECT}-{YYYY-MM-DD}.md`.

See `skills/project-conventions/SKILL.md#canonical-specs` (Writing style)
and (Frontmatter spec). Both apply to every artifact this skill produces.

## Pre-Phase 0: Branch and item check

Two modes:

- **Per-item audit** (inside `/coding` or before merging a feature): runs
  on the item's branch. `sec-done` tag goes on the same branch.
- **Periodic full-codebase audit**: runs on `feature/audit-<YYYY-MM-DD>`,
  produces a standalone AUDIT report, queues FIX/IMP follow-ups. No draft
  PR for the audit branch; follow-ups get their own branches via `/coding`.

Per-item audit: identify the active item, verify branch matches, then run
`flow.py create-issue` and `flow.py open-draft-pr` (idempotent). At the
Handoff Ritual end, run `flow.py tag-phase --item <ID> --phase sec`.

Full rules: `skills/project-conventions/references/team-workflow.md`.

## Scope

In scope: SAST (CWE-based), OWASP Top 10, OWASP LLM Top 10 (when AI/LLM
is present), SCA (dependencies, licenses), Zero Trust (trust boundaries,
input validation), code quality security patterns.

Out of scope: penetration testing, compliance certification, architecture
design (done by `/architecture`).

## Audit Phases

| Phase | Activity | Reference |
|---|---|---|
| 1. Reconnaissance | Identify stack, framework, runtime, dependency count, existing measures. Internal analysis only; nothing from this phase appears as a standalone report section. | -- |
| 2. SAST | Grep and analyze code per CWE patterns. | `references/cwe-patterns.md` |
| 3. OWASP Top 10 | Check A01-A10. | `references/owasp-checklist.md` |
| 4. OWASP LLM Top 10 | Only if LLM APIs are used. Check LLM01-LLM10. | `references/owasp-llm-checklist.md` |
| 5. SCA | `npm audit --json` or `pip-audit --format json`; license check. Classify by Runtime / Dev / Transitive. | -- |
| 6. Zero Trust + Quality | Input validation, least privilege, defense in depth, fail-closed defaults, audit trail, error handling, resource management, race conditions, hardcoded credentials, debug code. | -- |

## Finding format (binding)

Each finding caps at five fields. Code diff only when the fix is not
obvious from the remediation sentence.

```
H-N: <title>
- Severity: Critical | High | Medium | Low | Info
- CWE-ID:   CWE-XXX
- Location: <file:line>
- Risk:     <one sentence>
- Remediation: <one sentence with concrete action>
```

Status values: `Confirmed`, `Mitigated`, `False Positive`, `Resolved`.
State the status, never leave a false positive silent. Consider context
(DevDependency vs. Runtime).

**Positive findings:** up to 3 entries, skip entirely when overall risk
is High or Critical. The team needs the negative list, not encouragement.

Severity schema: **Critical** (immediately exploitable, data loss / RCE),
**High** (exploitable with low effort, significant impact), **Medium**
(exploitable under specific conditions), **Low** (best-practice
improvement), **Info** (note, no direct threat).

## Audit summary block (canonical, define once)

Defined here. Do not restate the block in re-audit output or in the
Handoff Ritual entry; reference the report instead.

```
=== Security Audit Result ===

Overall risk: {Critical / High / Medium / Low}

P1 (Must Fix, Critical + High): {N} findings
- {H-1}: {title}, {file:line}, effort {S/M/L}

P2 (Should Fix, Medium): {N} findings
- {M-1}: {title}, {file:line}, effort {S/M/L}

P3 (Consider, Low + Info): {N} findings
- {L-1}: {title}, effort {S/M/L}

Positive findings: {up to 3, omitted when overall risk High or Critical}
```

## When to run

Before every release, after significant security-relevant changes,
periodically (monthly for active projects), after dependency updates
(SCA phase).

## Create the report

Read `templates/AUDIT-TEMPLATE.md`, fill it, save to
`_devprocess/analysis/AUDIT-{PROJECT}-{YYYY-MM-DD}.md`.

---

## Fix-Loop

After the audit, the user picks scope.

### Step 1: Show the summary

Render the audit summary block defined above. Once.

### Step 2: Ask the user

```
How should I handle the findings?

A) Fix all findings (P1 + P2 + P3), then re-audit.
B) Fix only P1, defer P2/P3 to backlog.
C) Approve fixes one by one.
D) Nothing to fix, report only. All findings go to backlog.
```

### Step 3: Fix implementation

For each finding to be fixed: implement the concrete remediation, run
affected tests (no regressions), flip status `Confirmed -> Resolved` in
the report. On Option C: show each fix before continuing.

### Step 4: Re-audit (automatic)

Re-run affected audit phases. Report deltas only:

```
=== Re-Audit Delta ===

Before: {N} P1, {N} P2, {N} P3
After:  {N} P1, {N} P2, {N} P3
Resolved: {list}
New: {if a fix introduced new findings}
```

Loop until all in-scope findings resolve or the user aborts. Do not
re-render the full summary block.

### Step 5: Deferred findings -> Backlog

Each open finding becomes a row in `_devprocess/context/BACKLOG.md` per
`skills/requirements-engineering/templates/BACKLOG-TEMPLATE.md`. Place
under **Standalone Items** with: `Typ = Security`, `Source = SEC`,
priority from severity (H -> P1, M -> P2, L -> P3), `Status = Ready`,
`Evidence = path:line`, `Notes = <H/M/L-ID> + short risk`. Refresh
dashboard counts. Audit report keeps status `Confirmed` with note
"Deferred to backlog".

### Step 6: Update artifacts

Audit report (final version), feature specs (security-relevant changes),
ADRs (when fixes affect decisions), backlog (open findings).

### Step 7: Run `/consistency-check` mode A

Catches deferred findings without backlog rows, FIX rows missing
`feature:`/`epic:` frontmatter, drifted dashboard counts, dead links.

---

## Handoff Ritual

### Part 1: Artifact report

```
Produced / updated:
- _devprocess/analysis/AUDIT-{PROJECT}-{DATE}.md
- Findings resolved: {N}
- Findings deferred: {N}
- _devprocess/context/BACKLOG.md: deferred rows added
```

### Part 2: Handoff context

Append a new entry to `_devprocess/context/HANDOFFS.md`. Reference the
audit summary block by file path; do not restate it. Add:

- **Unresolved P0/P1**: open high-severity findings and why.
- **Architectural concerns**: patterns for a future `/architecture`
  cycle (trust-boundary issues that need redesign, not patching).
- **Release recommendation**: green / yellow / red verdict.

### Part 3: Phase-end commit

Per `skills/project-conventions/references/team-workflow.md` section
"Phase-end commit (binding)". Canonical message:

```
chore(audit): <ITEM-ID> audit complete

<one-line: risk verdict, N findings (P1/P2/P3), release recommendation>

Refs: <ITEM-ID>[, FIX-..., FIX-...]
```

After the commit:

```
python3 tools/github-integration/flow.py tag-phase --item <ID> --phase sec
python3 tools/github-integration/flow.py sync-status --item <ID>
```

`sync-status` mirrors BACKLOG Status to the GitHub issue and project
(and Assignee back into Claim). No-op outside `mode = "github-sync"`.
Skip the commit silently if the working tree has no changes.

### Part 4: Transition

> "Security audit complete. Report: `_devprocess/analysis/AUDIT-{PROJECT}-{DATE}.md`.
> Release readiness: {green/yellow/red}.
> Recommended next: `/consistency-check` mode B finalises the artifact
> graph and returns a Release-Ready verdict.
> Run `/consistency-check` mode B now, or review the audit first?"

On agreement (or when running inside `/dia-guide`): run
`/consistency-check` mode B; on Release-Ready: yes the `/dia-guide`
Closing Handoff fires. On rejection: pause.

## Keywords
Security Audit, Security Review, OWASP, SAST, SCA, Vulnerability, CVE,
Threat Model, Dependency Audit, Code Review Security, Fix-Loop, Handoff
