# skills/security-audit/tools/

Deterministic scan layer for the `security-audit` skill. Turns the
manual "grep for eval(), exec(), ..." checklist into reproducible,
scriptable scans with a stable finding identity and an honest tool
ledger, so a re-audit delta is computed, not eyeballed.

The skill calls these scripts; the LLM triages the JSON they emit
(source -> sink, false-positive review) and writes the report prose on
top. The scripts never decide severity narrative and never fetch the
network for threat lists (that is the skill's live-currency step).

## Design contract (binds every script)

- **stdlib-only Python** (3.9+), one Node ESM probe. No pip installs.
- **Offline-graceful.** Every external tool (semgrep, gitleaks,
  osv-scanner, npm) is optional. Missing tool -> honest entry in the
  `tools[]` ledger (`status: unavailable | offline-skipped | error`)
  and the scan continues. Nothing hard-aborts on a missing tool.
- **Never log secrets.** Secret matches are redacted to a 4-char
  preview + length + short sha1, in output and on stderr. No plaintext,
  ever.
- **Deterministic.** A finding's fingerprint is
  `sha1(cwe | path | normalized-snippet)[:8]`, with NO line number or
  timestamp, so it survives renumbering and two runs over the same code
  produce identical ids.
- **Scope-aware, not scope-blind.** A diff scope narrows WHERE findings
  are reported, never the reachability context the LLM reasons over.
- **Baseline under `.git/`.** `.git/security-audit/{last,prev}-run.json`,
  never committed. A diff-scope run never clobbers a `full` baseline.

## Files

| File | Role |
|------|------|
| `audit_scan.py` | Orchestrator. Subcommands `detect`, `surface`, `sast`, `secrets`, `sca`, `all`. |
| `report_assembler.py` | `fill` (pre-fill AUDIT-TEMPLATE from findings JSON) + `delta` (re-audit set diff by fingerprint). |
| `lib/findings.py` | `Finding` dataclass, `fingerprint`, `redact`, baseline read/write/rotate, `delta`. |
| `lib/scope.py` | Resolve a scope category (`full`/`working`/`commit`/`staged`/`branch`/`range`) to a file list via git. |
| `lib/detectors.py` | Project-type detection (electron/obsidian-plugin/web-app/cli/library, node/python/...) + attack-surface enumeration. |
| `poc/redos_probe.mjs` | Opt-in isolated ReDoS measurement of ONE suspect regex (worker_thread + hard deadline). |
| `tests/` | Assertion-based tests, runnable without pytest, also pytest-discoverable. |

## Path resolution

Skill text uses `python3 skills/security-audit/tools/audit_scan.py ...`;
the agent expands the leading `skills/...` against `$DIA_PLUGIN_ROOT`
(see `skills/dia-bootstrap/SKILL.md`). The scripts resolve the target
repo root themselves via `git rev-parse --show-toplevel`, so the first
positional argument (a project root) is optional.

## Quick reference

```bash
ROOT=/path/to/target/project   # optional; defaults to the git root

# What kind of project is this? (gates which references/tools apply)
python3 audit_scan.py detect "$ROOT"

# Enumerate trust-boundary entry points in scope
python3 audit_scan.py surface "$ROOT" --scope full

# Full scan, snapshot the live taxonomy set, write the baseline
python3 audit_scan.py all "$ROOT" --scope full \
    --taxonomy '{"owasp":"2025","owasp-llm":"2025","cwe-top-25":"2024"}' \
    > /tmp/audit-findings.json

# Scope a scan to the branch under review (vs merge-base with main)
python3 audit_scan.py all "$ROOT" --scope branch --base main

# Pre-fill the human report from the findings JSON
python3 report_assembler.py fill --findings /tmp/audit-findings.json \
    --project vault-operator --date 2026-07-23 > AUDIT-vault-operator-2026-07-23.md

# Re-audit delta: what got resolved / introduced since the last full run
python3 report_assembler.py delta \
    --before .git/security-audit/prev-run.json \
    --after  .git/security-audit/last-run.json

# Opt-in: measure whether a flagged regex actually backtracks catastrophically
node poc/redos_probe.mjs --pattern '(a+)+$' --pump-len 40 --pump-suffix '!' --deadline-ms 500
```

## Scope categories

| Scope | Files | git derivation | Use when |
|-------|-------|----------------|----------|
| `full` | all tracked | `git ls-files` | first audit, release gate, periodic |
| `working` | uncommitted + untracked | `git diff HEAD` + `ls-files -o` | mid-development |
| `commit` | last commit | `git diff HEAD~1..HEAD` | quick post-commit check |
| `branch` | branch vs merge-base | `git diff $(merge-base <base> HEAD)..HEAD` | before PR / merge |
| `range` | free range | `git diff A..B` | targeted investigation |
| `staged` | staged only | `git diff --cached` | pre-commit hook |

Only `full` advances the delta baseline. A diff scope reports against
the persisted full baseline without overwriting it.

## Exit codes

`0` no findings, `1` findings present, `2` usage/setup error. Matches
the convention in `tools/consistency-check.py`.

## Running the tests

```bash
for t in skills/security-audit/tools/tests/test_*.py; do python3 "$t" || break; done
```

`test_redos_probe.py` skips (passes) if `node` is not installed; every
other test is pure stdlib Python.

## Why a scan layer at all

The pre-existing skill asked the model to grep by hand. That is not
reproducible (two runs differ), it is token-expensive, it silently
misses hits, and the re-audit "what changed" step was done by eye. A
scriptable orchestrator with fingerprinted findings makes the scan
deterministic and the delta reliable, while the honest `tools[]` ledger
kills the tool-overclaim where a report lists `semgrep` although only a
grep fallback ran.
