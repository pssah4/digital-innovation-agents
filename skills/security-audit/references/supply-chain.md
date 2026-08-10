# Supply chain: provenance and build integrity

Two kinds of package malware, two different defenses:

1. **Install-time** (postinstall scripts): runs during `npm install`.
   Contained by `--ignore-scripts`, `.npmrc` policy, and isolation.
2. **Bundle-time** (malicious code in the package itself): bundled into
   the shipped artifact and runs at the END USER, not the developer.
   No development isolation stops it; only provenance discipline and
   rebuild verification catch it.

## What each stage proves, and what it does not

| Stage | Proves | Does NOT prove |
|---|---|---|
| 1 Static (always) | Every locked package resolves to an allowed registry with a sha512 hash; workflows cannot be silently retargeted via mutable tags | Package benignity. A legitimately compromised release passes with a valid hash. Lockfile integrity is registry fidelity, not trust. |
| 2 Clean-room rebuild (opt-in) | The committed/shipped artifact falls byte-identically out of the committed sources; nothing was injected between source and artifact | Source benignity. A backdoor committed in src/ reproduces byte-exactly. The question moves from "is the bundle clean" to "are the sources clean". |
| 3 Release verify (opt-in) | Published release assets still carry the CI build's provenance attestation; no post-release asset swap | Anything about the build inputs. A compromised CI would attest its own poisoned output. |

## Triage guidance

- **Non-allowlisted registry host (medium):** a private/corporate mirror
  is legitimate. Confirm with the user, then add the host to
  `registry_hosts` in `[audit.supply_chain]` instead of waving the
  finding through each audit.
- **Git/HTTP dependency (high):** bypasses registry signing and
  immutability. An intentional git dependency needs an explicit,
  documented decision; otherwise treat as a red flag.
- **Install-script inventory (info):** not a violation. The alarm case
  is a NEW package appearing in the inventory: the re-audit delta flags
  it as `new`. That window (fresh compromise, no advisory yet) is
  exactly where supply-chain attacks ship.
- **Unpinned action (high on write-permission workflows):** a mutable
  tag lets whoever controls the action repo run code with your repo's
  write token. Pin to the full 40-char commit SHA with a `# vN` comment.
- **Rebuild mismatch (high):** either an injected artifact or a
  non-deterministic build. Diff the artifacts before concluding; embedded
  timestamps/versions are the common benign cause and worth fixing too
  (determinism is the audit anchor).

## Configuration

`[audit.supply_chain]` in the project's `.dia/config.toml`:

```toml
[audit.supply_chain]
build_command = "node esbuild.config.mjs production"
artifacts = ["main.js", "styles.css"]
registry_hosts = ["registry.npmjs.org"]
```

CLI flags (`--build-cmd`, `--artifact`, `--registry-host`) override the
file, which keeps the runner usable on non-DIA repos.

## Safety of the clean-room rebuild

The rebuild executes the project's build command. That is the price of
the measurement and why it is strictly opt-in. Mitigations built in:

- Fresh `git clone` of HEAD in a scratch directory; the working tree and
  the source repo's `.git` stay untouched.
- Dependency install runs with `--ignore-scripts`.
- The environment is an ALLOWLIST (PATH, HOME, LANG, LC_ALL, TMPDIR
  only) plus `npm_config_ignore_scripts=true`. Deploy hooks that key off
  env vars (iCloud plugin dirs, registry overrides, cloud credentials)
  are absent by construction.
- Residual risk: a malicious build script still runs with user
  privileges. Do not run `--rebuild` on untrusted code outside a sandbox.

## Known limitations

- Workflow and pnpm/yarn lockfile checks are line/regex-based (no YAML
  parser in stdlib). Exotic syntax (anchors, folded scalars, multi-line
  `uses:`) can slip through; the report's limitations block says so.
- Reproducibility needs a deterministic build. Embedded build dates or
  git SHAs cause benign mismatches; fix the build, do not skip the check.
- `pip-audit`/`cargo-audit` are gated in detectors but not yet wired
  into `run_sca`; Python coverage here is pin-checking only.
