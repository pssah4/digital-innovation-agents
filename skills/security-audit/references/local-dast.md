# Local dynamic verification (safe PoC)

Static analysis says "this pattern looks exploitable". Dynamic
verification MEASURES whether it actually is. This is opt-in, runs
locally, and is deliberately narrow: it exercises ONE flagged artifact,
never the whole application, never a real target. It is not penetration
testing (still out of scope) and never runs against a system you do not
own.

## When to use

During Fix-Loop triage, to turn a Confirmed/False-Positive guess into a
measurement, and after a fix as a regression check. Optional; a static
finding stands on its own if no safe probe exists.

## Available probe

- `poc/redos_probe.mjs` (opt-in): measures whether ONE suspect regex
  backtracks catastrophically. Runs the regex in a worker_thread with a
  hard deadline; if it blows the deadline it is terminated, so the probe
  itself never hangs. Reports `{hangs, elapsed_ms}`.

  ```bash
  node poc/redos_probe.mjs --pattern '(a+)+$' --pump-len 40 \
       --pump-suffix '!' --deadline-ms 500
  ```

  A non-matching suffix is what forces backtracking; tune `--pump-*` to
  the real input shape. A `hangs: true` result upgrades a static
  CWE-400 guess to Confirmed with a measured `elapsed_ms` as evidence.

## Safety rules (binding)

- Isolated execution only (worker/subprocess with a hard deadline).
- No network, no filesystem writes outside a temp dir.
- Only the flagged artifact is exercised (a regex, a path string), never
  arbitrary code and never the app under audit as a running service.
- If a safe, isolated probe cannot be constructed, do NOT improvise a
  risky one; keep the finding static and say so in the report.

## Local server surfaces (checklist, not automated)

If the project runs a loopback server, verify by hand (curl against
`127.0.0.1` with a spoofed `Host` header for DNS-rebinding; confirm
auth is real and not just CORS). Do not script a generic server-DAST
here; server bootstrap is too project-specific to generalize safely.
