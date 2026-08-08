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
| `audit_scan.py` | Orchestrator. Subcommands `detect`, `surface`, `sast`, `secrets`, `sca`, `supply-chain`, `all`. |
| `report_assembler.py` | `fill` (pre-fill AUDIT-TEMPLATE from findings JSON) + `delta` (re-audit set diff by fingerprint). |
| `lib/findings.py` | `Finding` dataclass, `fingerprint`, `redact`, baseline read/write/rotate, `delta`. |
| `lib/scope.py` | Resolve a scope category (`full`/`working`/`commit`/`staged`/`branch`/`range`) to a file list via git. |
| `lib/detectors.py` | Project-type detection (electron/obsidian-plugin/web-app/cli/library, node/python/...) + attack-surface enumeration. |
| `lib/supply_chain.py` | Static supply-chain checks: lockfile provenance, action pinning, install-script inventory, manifest hygiene, python pins. Offline, no subprocesses. |
| `lib/cleanroom.py` | Opt-in stages: clean-room rebuild (scratch clone, scrubbed env, hash compare) + `gh attestation verify` of release assets. |
| `poc/redos_probe.mjs` | Opt-in isolated ReDoS measurement of ONE suspect regex (worker_thread + hard deadline). |
| `tests/` | Assertion-based tests, runnable without pytest, also pytest-discoverable. |

## CodeQL setup (optional, recommended)

Without CodeQL the SAST layer runs semgrep (if installed) plus the
bundled grep-fallback. That covers pattern-level bugs but misses ones
that require real source-to-sink taint analysis. Installing CodeQL
adds a third layer that catches the taint-only class.

The skill never breaks when CodeQL is absent: the tool ledger records
`codeql: unavailable` and the cascade falls through to semgrep and
grep. If CodeQL is on PATH but the language pack is not cached, the
ledger records `pack-missing` with the exact download command as its
reason.

```bash
# One-time install (macOS)
brew install --cask codeql

# Download the language packs the project needs
codeql pack download codeql/javascript-queries    # JS + TS
codeql pack download codeql/python-queries        # Python
codeql pack download codeql/go-queries            # Go
codeql pack download codeql/rust-queries          # Rust

# Refresh periodically; the report flags packs older than 90 days
codeql pack upgrade codeql/javascript-queries
```

The per-language CodeQL DB lives at
`.git/security-audit/codeql-db-<lang>/`. The scan orchestrator
idempotently adds the pattern to `.git/info/exclude` on first run so
these directories never show up as untracked.

### Grep-fallback limits

The pattern-based grep-fallback in [audit_scan.py](audit_scan.py) is
intentionally broad: it flags any occurrence of `\.\./`, `path.join(...,
req...)`, `eval(...)`, `.innerHTML =`, etc., without checking whether the
input is actually attacker-controlled. That is fine when CodeQL runs
alongside (the taint layer rejects unreachable hits), but on
CodeQL-less runs the grep layer will produce known false positives for
path-manipulation code (`path.join(homeDir, 'foo')`) and for
documentation strings that contain a literal `../`. Two mechanisms
reduce the noise:

* [`lib/skip_rules.py`](lib/skip_rules.py) skips test fixtures,
  minified/bundled assets, and `dist/`/`build/` outputs by path glob.
* A per-file header `# security-audit-scan: skip` opts a specific file
  out (used by the detector modules that store the CWE patterns as data
  literals and would otherwise self-match).

Beyond these, path-manipulation false positives on grep-only runs are
the known trade-off for pattern breadth. Install CodeQL to remove the
false-positive class entirely for supported languages.

## Supply-chain checks

Stage 1 is static and part of every `all` run: lockfile provenance
(registry host allowlist, sha512 integrity, git/http dependencies),
GitHub Action pinning (mutable tag vs commit SHA, permissions blocks,
persist-credentials, `npm install` vs `npm ci`, unpinned pip installs),
install-script inventory (delta-able info findings), manifest hygiene
(`.npmrc` ignore-scripts policy, stale overrides), and Python
requirement pins.

Stages 2 and 3 execute external commands and are opt-in only:

```bash
# Static checks (also included in `all`)
python3 audit_scan.py supply-chain

# Stage 2: clean-room rebuild (runs the project's build in a scratch clone)
python3 audit_scan.py supply-chain --rebuild \
    --build-cmd "node esbuild.config.mjs production" \
    --artifact main.js --artifact styles.css

# Stage 3: verify provenance attestations of the latest release assets
python3 audit_scan.py supply-chain --release-verify
```

Config precedence: CLI flags > `[audit.supply_chain]` in the target
repo's `.dia/config.toml` > defaults. See
`references/supply-chain.md` for what each stage proves, the triage
guidance, and the safety notes for the rebuild (allowlist env,
`--ignore-scripts`, scratch clone). Workflow/lockfile YAML checks are
regex-based; exotic syntax can slip through and the report's
limitations block says so honestly.

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
