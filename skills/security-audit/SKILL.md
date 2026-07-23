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
input validation), code quality security patterns. Desktop/Electron
runtime when detected. Safe local PoC verification (isolated).

Out of scope: penetration testing against systems you do not own,
compliance certification, architecture design (done by `/architecture`).

## Ask the scope first (before any scan)

Before running, ask the user WHAT to audit (AskUserQuestion). The scan
scripts take a matching `--scope`:

| Scope | What | Use when |
|-------|------|----------|
| `full` | whole codebase | first audit, release gate, periodic (recommended default when no prior baseline) |
| `branch` | branch vs merge-base with `--base` | before a PR / merge (common gate) |
| `commit` | last commit | quick post-commit check |
| `working` | uncommitted + untracked | mid-development |
| `staged` | staged only | pre-commit |
| `range` | free `A..B` | targeted investigation |

A diff scope narrows WHERE findings are reported, never the reachability
context: trace source->sink through the full tree even for a diff scan.
Only `full` advances the delta baseline.

## The scan layer (deterministic)

Phases 1-6 are driven by `tools/` (see `tools/README.md`), not manual
grep. Resolve `tools/...` against `$DIA_PLUGIN_ROOT`. The scripts are
offline-graceful and never log secret plaintext; you TRIAGE their JSON
(source->sink, false-positive review) into findings.

```
python3 skills/security-audit/tools/audit_scan.py all --scope <S> [--base main] \
    --taxonomy '{"owasp":"...","owasp-llm":"...","cwe-top-25":"..."}'
```

## Phase 0: Live threat currency (always)

The bundled `references/*.md` are the OFFLINE BASELINE. Before scanning,
fetch the CURRENT editions and reconcile:

1. WebSearch/WebFetch the current OWASP Top 10, OWASP Top 10 for LLM
   Apps, and MITRE CWE Top 25 (official domains: owasp.org,
   genai.owasp.org, cwe.mitre.org). Note new categories vs the baseline.
2. SCA CVEs come live from `npm audit` / `osv-scanner` in Phase 5.
3. SNAPSHOT the taxonomy set you used (editions + date) and pass it to
   `--taxonomy`; it lands in the report and the delta baseline. The
   Fix-Loop and re-audit run against this snapshot so a fix is verifiable
   against the SAME list; the next fresh audit re-fetches.
4. If offline: fall back to the bundled baseline and record
   `currency: offline` in the report. Never silently claim currency.

## Audit Phases

Feed each from `audit_scan.py` output; triage into findings.

| Phase | Activity | Reference |
|---|---|---|
| 1. Reconnaissance | `audit_scan.py detect` + `surface`. Map entry points, data flows, trust boundaries. Read the project's own threat doc if present (`REVIEWER_NOTES.md`, `SECURITY.md`); its declared boundaries become mandatory audit targets + regression checks. Internal analysis only. | `references/attack-surface.md`, `references/threat-modeling.md` |
| 2. SAST | `audit_scan.py sast` (semgrep or grep fallback). Triage source->sink. | `references/cwe-patterns.md` |
| 3. OWASP Top 10 | Check the Phase-0 current edition (baseline A01-A10). | `references/owasp-checklist.md` |
| 4. OWASP LLM Top 10 | Only if `detect` reports LLM APIs. Deepen with the agent/injection refs. | `references/owasp-llm-checklist.md`, `references/agent-approval-gate.md`, `references/prompt-injection-boundaries.md` |
| 4b. Desktop runtime | Only if `detect` reports `electron`. | `references/desktop-runtime.md` |
| 5. SCA | `audit_scan.py sca` (npm/pip audit + osv-scanner; license). Classify Runtime / Dev / Transitive. Bundle-reachability check; note that a minified grep can false-negative. | -- |
| 6. Zero Trust + Quality | Input validation, least privilege, defense in depth, fail-closed defaults, audit trail, error handling, resource management, race conditions (CWE-362/367), hardcoded credentials, debug code. Optional isolated PoC. | `references/local-dast.md` |

## Finding format (binding)

Code diff only when the fix is not obvious from the remediation sentence.

```
H-N: <title>
- Severity: Critical | High | Medium | Low | Info
- CWE-ID:   CWE-XXX
- CVSS:     <v3.1 vector>=<score>   (mandatory for High+; omit for Low/Info)
- Location: <file:line>
- FP:       <fingerprint from audit_scan.py>
- Evidence: <snippet / source->sink trace / PoC result>
- Risk:     <one sentence>
- Remediation: <one sentence with concrete action>
```

Status values: `Confirmed`, `Unverified`, `Mitigated`, `False Positive`,
`Resolved`. State the status, never leave a false positive silent.
Consider context (DevDependency vs. Runtime).

**Verification before `Confirmed` (binding).** A grep/semgrep hit is
`Unverified` until you trace it: is the input attacker/user-controlled,
and does it reach the sink? Record the source->sink path in Evidence,
then set `Confirmed`. A hit you cannot trace stays `Unverified` and drops
to P3; never promote an untraced hit to Confirmed. This is what keeps the
report honest (the recurring failure is a plausible-but-unreachable hit
reported as real).

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

Pre-fill the template deterministically from the scan JSON, then write
the narrative (Risk/Remediation prose, executive summary) on top:

```
python3 skills/security-audit/tools/report_assembler.py fill \
    --findings <scan.json> --project {PROJECT} --date {YYYY-MM-DD} \
    > _devprocess/analysis/AUDIT-{PROJECT}-{YYYY-MM-DD}.md
```

`fill` produces the count matrix, P1/P2/P3 buckets, an HONEST tools
ledger (only tools that ran; kills the semgrep-overclaim), and the
mandatory "Coverage and limitations" section. Keep the report within the
`audit` artefact cap; move detail to child FIX/IMP rows if it grows.

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
affected tests (no regressions). Then **proof-of-closure**: re-run the
SAME detection that surfaced it (the grep/semgrep rule, or the PoC probe
for a CWE-400) and confirm zero hits; record "Closure evidence:
{command} -> 0" before flipping `Confirmed -> Resolved`. A fix without a
re-detection that comes back clean stays `Confirmed`. On Option C: show
each fix before continuing.

### Step 4: Re-audit (automatic, script-driven delta)

Re-run affected phases against the SAME taxonomy snapshot, then compute
the delta by fingerprint (not by eye):

```
python3 skills/security-audit/tools/report_assembler.py delta \
    --before .git/security-audit/prev-run.json \
    --after  .git/security-audit/last-run.json
```

```
=== Re-Audit Delta ===

Before: {N} P1, {N} P2, {N} P3
After:  {N} P1, {N} P2, {N} P3
Resolved: {fingerprints}
New: {if a fix introduced new findings}
```

Adversarial check on any NEW finding a fix introduced: try to refute it
(is it reachable?) before reporting it, so a fix-bypass is caught. Loop
until all in-scope findings resolve or the user aborts. Do not re-render
the full summary block.

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
