---
cwe-basis: MITRE CWE Top 25 (name the year in the report); the list below
  is the curated core plus stack-adaptive additions, not the full CWE corpus.
---

# CWE analysis patterns for SAST

Systematic grep/analysis patterns per CWE category. The `audit_scan.py sast`
grep fallback mirrors these; when semgrep is available it runs alongside.
These are heuristics: every hit is triaged (source -> sink) before it
becomes Confirmed.

## CWE-79: Cross-Site Scripting (XSS)

Search for: `innerHTML`, `outerHTML`, `dangerouslySetInnerHTML`, `document.write`
Context: user input written unfiltered into the DOM.

## CWE-94: Code Injection

Search for: `eval()`, `new Function()`, `vm.runInNewContext`, `vm.runInThisContext`
Context: dynamic code execution with variable input. Note: `vm.*` is not a
security boundary (see `desktop-runtime.md`).

## CWE-78: Command Injection

Search for: `exec()`, `spawn()`, `execSync()`, `child_process`
Context: shell commands with user input without escaping. Check for a
spawn allowlist choke point.

## CWE-22: Path Traversal

Search for: path construction with `+` or template literals, `../`
Context: missing path normalization, no `path.resolve()` + prefix check.
Note whether symlink resolution is intentionally omitted (that is a
deliberate design in some file-access choke points, not a bug).

## CWE-918: Server-Side Request Forgery (SSRF)

Search for: `fetch()`, `requestUrl()`, `axios`, `http.get` with a variable URL
Context: URL from user input without allowlist check.
Bypass classes the allowlist must fold BEFORE comparing:
- alternate IP encodings: decimal (`2130706433`), hex (`0x7f000001`),
  octal, IPv4-mapped IPv6 (`::ffff:127.0.0.1`)
- DNS rebinding: resolve, then re-check every A/AAAA record, and pin the
  socket to the validated IP
- per-hop redirect validation (each redirect target re-checked)
Remediation: resolve -> re-check resolved IP (not the hostname string)
-> pin -> re-validate on redirect.

## CWE-1321: Prototype Pollution

Search for: `Object.assign({}, userInput)`, `{...userInput}`, `lodash.merge`,
`__proto__`, `constructor.prototype`
Context: deep-merge or spread over unvalidated user input; payload guards
on bridge/deserialization boundaries.

## CWE-400: Denial of Service, incl. ReDoS

Search for: `new RegExp(userInput)`, nested quantifiers `(a+)+`,
bounded-outer `(a+){n}`, sequential overlap `\d+\d+`
Context: regex with user input or catastrophic backtracking.
A static blocklist of "evil regex" shapes LEAKS (it guesses, it does not
measure). Prefer runtime measurement: `poc/redos_probe.mjs` runs the
suspect regex against a pump string with a hard deadline and reports
whether it actually hangs. Also check resource limits BEFORE allocation
(count before concat) and a task-wide token/cost budget.

## CWE-362 / CWE-367: Race Condition / TOCTOU

Search for: an `existsSync`/`stat`/access check followed by a `readFile`/
`writeFile`/`open` on the same path; non-atomic read-modify-write on a
shared JSON/state file; a warm singleton reused across concurrent
executions (last-writer-wins slot)
Context: the state can change between check and use. Prefer atomic ops
(open with flags, rename-into-place) and per-execution binding instead of
a shared mutable slot. Two instances on one working tree is a real
trigger.

## CWE-312 / CWE-532: Sensitive Data Exposure / Log Exposure

Search for: `console.log`/`.debug`/`.info` with token/key/password;
API keys in source; a persisting logger that stores tool RESULTS (not
just params); `JSON.stringify(err)` on an OAuth/error object
Context: credentials in logs or source instead of env/secret store.
For persisting loggers, redact/hash results, not just params. For OAuth
errors, use a field allowlist (RFC 6749) instead of dumping the object.

## CWE-502: Insecure Deserialization

Search for: `JSON.parse()` without schema validation, `yaml.load()`,
`pickle.loads()`
Context: deserialization of untrusted input.

## CWE-863: Authorization Bypass

Search for: missing access-control checks, role checks only in the
frontend, an identity/privilege claim taken from the request payload
Context: server-side authorization missing. Hard rule (Zero Trust): an
identity or privilege claim must never originate from the request body;
enumerate every such claim and its source.

## CWE-74 / CWE-116: Injection via improper neutralization (second-order)

Search for: machine markers written into user- or sync-writable regions
without line anchoring; single-pass `.replace()` defang on untrusted text
Context: injected text can forge an un-anchored marker (second-order
injection). Anchor markers `^\s*<marker>\s*$`; defang must iterate to a
fixpoint. See `prompt-injection-boundaries.md`.

## Stack-adaptive additions

`audit_scan.py detect` reports the stack; add the relevant block and note
in the report which CWE Top 25 entries were NOT evaluated:
- Electron/renderer: CWE-1188 (insecure default / contextIsolation),
  CWE-829 (untrusted functionality inclusion: plugins/MCP)
- Export/data features: CWE-1236 (CSV/formula injection)
- Web app: CWE-352 (CSRF), CWE-434 (unrestricted upload), CWE-611 (XXE)

## Finding format

For each hit:

```markdown
### {Severity}-{N}: {Title} ({CWE-ID})

| Field | Value |
|-------|-------|
| **Severity** | Critical / High / Medium / Low / Info |
| **CWE** | CWE-{ID} |
| **CVSS** | {v3.1 vector}={score} (mandatory for High+) |
| **Location** | `src/path/file.ts:{line}` |
| **FP** | {fingerprint from audit_scan.py} |
| **Status** | Confirmed / Mitigated / False Positive / Unverified |

**Finding:** {what was found}
**Evidence:** {snippet / trace / PoC result}
**Risk:** {the risk}
**Remediation:** {how to fix}

**Code suggestion (only when the fix is non-obvious):**
- {insecure code}
+ {secure code}
```
