---
title: Security Audit
description: "Comprehensive security audit covering OWASP Top 10, OWASP LLM Top 10, SAST, SCA, and Zero Trust. Two modes: per-item audit and periodic full-codebase audit."
---

# Security Audit

`/security-audit` runs a security audit on the codebase and
produces a prioritised remediation plan with traceable findings.

**Input:** Codebase, dependencies, configuration, the FEAT or
release scope being audited
**Output:** Audit report at
`_devprocess/analysis/AUDIT-{PROJECT}-{YYYY-MM-DD}.md` (flat under
`analysis/`, no subfolder), plus `H-N`, `M-N`, `L-N` finding rows in
`BACKLOG.md`

## Two modes

### Per-item audit

Triggered as part of a normal V-Model run. The audit scope is the
FEAT (or set of FEATs) shipped in the current cycle. Branch:
`feature/<ITEM-ID>-<short-slug>` (the same branch as the FEAT). The
audit happens after `/testing` and before release closure.

### Periodic full-codebase audit

A scheduled deep audit across the whole codebase, independent of any
single FEAT. Branch convention:
`feature/audit-{YYYY-MM-DD}`. Triggered manually or on a calendar
cadence (quarterly, before a major release, after a significant
dependency upgrade).

The two modes share the same six audit phases below; only the scope
differs.

## Six audit phases

1. **Reconnaissance.** Identify tech stack, dependencies, existing
   security measures, threat model assumptions.
2. **SAST (Static Application Security Testing).** CWE-based static
   analysis with grep / pattern matching from
   `references/cwe-patterns.md`.
3. **OWASP Top 10.** All 10 categories (A01 to A10) with concrete
   patterns.
4. **OWASP LLM Top 10.** LLM01 to LLM10, relevant when the project
   uses LLM APIs.
5. **SCA (Software Composition Analysis).** Dependency
   vulnerabilities (`npm audit`, `pip-audit`, `cargo audit`, ...),
   license check.
6. **Zero Trust and Code Quality.** Input validation, least
   privilege, fail-closed defaults, audit trail, hardcoded
   credentials, debug code in production.

## Supply-chain phase

Between SCA and Zero Trust, the audit runs a supply-chain phase
(`audit_scan.py supply-chain`) in up to three stages:

- **Static checks (always part of a full audit).** Lockfile
  provenance, CI action pinning, and an inventory of install
  scripts. No network, no build execution.
- **Clean-room rebuild (opt-in, `--rebuild`).** Rebuilds the
  project in a scratch clone and compares the artifact against the
  distributed one. It executes the project's build command, so it
  runs only after explicit confirmation and needs a configured
  build command (`[audit.supply_chain]` in the config or
  `--build-cmd`/`--artifact`).
- **Release verification (opt-in, `--release-verify`).** Verifies
  the GitHub attestation of release assets via the `gh` CLI; needs
  network access.

The report keeps an honest ledger: only tools and stages that
actually ran are claimed, and declined or unavailable stages appear
explicitly as not-run instead of silently vanishing. A skipped
rebuild is a documented gap, not a passed check.

## Severity schema

- **H (High)**: exploitable, significant impact, fix immediately
- **M (Medium)**: exploitable under specific conditions, fix in
  this cycle
- **L (Low)**: low risk, best-practice improvement, schedule
- **Info**: note, no direct threat, optional context

Each finding gets an id of the form `H-N`, `M-N`, `L-N` (severity
plus a counter local to the audit report).

## Findings as backlog rows

Every finding lands in `BACKLOG.md` as a row with the same
backlog-row-first writeback discipline as FIX rows. The detail
lives in the audit report. Status, phase, last-change, claim, and
commit SHA live in the backlog row.

A High finding that the team explicitly decides not to fix in this
cycle stays in the backlog with `Status: Backlog` and a reason
recorded in the audit report (Notes column). There is no silent
"we'll get to it" state.

## Fix-loop

Findings trigger a fix-loop with 4 user options:

- **A)** Fix all findings automatically
- **B)** Fix only High findings, defer the rest
- **C)** Approve fixes one by one
- **D)** Report only, no fixes in this run

Each iteration re-runs the audit phase for the affected category
with fresh output before claiming the finding is closed. See
[Verification Gates](../concepts/verification-gates).

## Handoff

Ends with the 3-part [Handoff Ritual](../concepts/handoff-rituals):
artifact report, phase-end commit (`chore(sec): {ITEM-ID} security
complete` with the `DIA-Phase: sec-done` trailer) plus
`tag-phase --phase sec` and `sync-status --item {ITEM-ID}` (no-op
outside `mode = "github-sync"`), transition question. Before the
handoff, Step 7 runs the mandatory pre-release `/consistency-check`;
this is the once-per-cycle full graph check.

The next phase is the Closing Handoff via `/dia-guide`. The commit
body includes the release readiness verdict (green, yellow, or red)
and any deferred findings that the release ships with.

## Read the skill file

[`skills/security-audit/SKILL.md`](https://github.com/pssah4/digital-innovation-agents/blob/main/skills/security-audit/SKILL.md) on GitHub.
