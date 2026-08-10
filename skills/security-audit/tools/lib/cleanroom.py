"""Clean-room rebuild (stage 2) and release attestation verify (stage 3)
for the security-audit skill's supply-chain phase.

Stage 2 answers: does the committed build artifact fall byte-identically
out of the committed sources? A fresh `git clone` of HEAD lands in a
scratch directory, dependencies install with --ignore-scripts, the
project's build command runs under a scrubbed environment, and the
rebuilt artifacts are hashed against their pre-build (= committed)
state. Reproducibility proves mapping fidelity, not benignity: a
backdoor committed in src/ reproduces byte-exactly.

The environment scrub is an ALLOWLIST, not a blocklist. Only PATH, HOME,
LANG, LC_ALL and TMPDIR survive; everything else (deploy hooks like
PLUGIN_DIR, npm_config_registry overrides, cloud credentials) is gone by
construction, so a build cannot deploy into an iCloud sync dir or leak
credentials as a side effect.

Stage 3 answers: do the published release assets still carry the
provenance attestation from the CI build, or has an asset been swapped
after the fact? Needs the `gh` CLI and network; both absent cases
degrade to an honest ledger entry, never an abort.

Both stages execute external commands and are therefore strictly opt-in
(--rebuild / --release-verify); `audit_scan.py all` never triggers them.

stdlib-only. Config comes from [audit.supply_chain] in .dia/config.toml
(tomllib on Python 3.11+, regex fallback below that, mirroring
tools/github-integration/flow.py).
"""
from __future__ import annotations
import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Optional

try:
    from . import findings as F
except ImportError:  # pragma: no cover
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import findings as F  # type: ignore

PHASE = "supply-chain"
_ENV_ALLOWLIST = ("PATH", "HOME", "LANG", "LC_ALL", "TMPDIR")
_BUNDLER_CONFIG_RE = re.compile(
    r"(^|/)(esbuild|rollup|vite|webpack)\.config\.[cm]?[jt]s$")
_GITHUB_SLUG_RES = (
    re.compile(r"^git@github\.com:([^/]+)/([^/]+?)(?:\.git)?$"),
    re.compile(r"^ssh://git@github\.com/([^/]+)/([^/]+?)(?:\.git)?$"),
    re.compile(r"^https://github\.com/([^/]+)/([^/]+?)(?:\.git)?$"),
)


def _run(cmd: list, timeout: int = 300, cwd: Optional[Path] = None,
         env: Optional[dict] = None) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, text=True, capture_output=True,
                          timeout=timeout, cwd=str(cwd) if cwd else None,
                          env=env)


def _scrubbed_env(base: Optional[dict] = None) -> dict:
    """Allowlist environment for clean-room build steps. Forces
    npm_config_ignore_scripts so even a direct npm invocation inside the
    build command cannot run lifecycle scripts."""
    import os
    src = base if base is not None else dict(os.environ)
    env = {k: v for k, v in src.items() if k in _ENV_ALLOWLIST}
    env["npm_config_ignore_scripts"] = "true"
    return env


def _sha256(path: Path) -> Optional[str]:
    try:
        return hashlib.sha256(path.read_bytes()).hexdigest()
    except Exception:
        return None


# ---------- config ---------------------------------------------------------

def _toml_section_fallback(text: str, section: str) -> dict:
    """Minimal TOML subset parser for one [section]: string and
    string-array values only. Used when tomllib (3.11+) is absent."""
    out: dict = {}
    in_section = False
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("["):
            in_section = stripped == f"[{section}]"
            continue
        if not in_section or "=" not in stripped or stripped.startswith("#"):
            continue
        key, _, raw = stripped.partition("=")
        key = key.strip()
        raw = raw.split("#")[0].strip()
        if raw.startswith("["):
            out[key] = re.findall(r'"([^"]*)"', raw)
        elif raw.startswith('"') and raw.endswith('"'):
            out[key] = raw[1:-1]
    return out


def read_supply_chain_config(root: Path,
                             cli_overrides: Optional[dict] = None) -> dict:
    """[audit.supply_chain] from .dia/config.toml with CLI precedence.
    Keys: build_command (str|None), artifacts (list), registry_hosts
    (list, defaults to the public npm registry)."""
    cfg: dict = {"build_command": None, "artifacts": [],
                 "registry_hosts": ["registry.npmjs.org"]}
    toml_path = root / ".dia" / "config.toml"
    if toml_path.is_file():
        try:
            text = toml_path.read_text(encoding="utf-8")
        except Exception:
            text = ""
        section: dict = {}
        try:
            import tomllib  # Python 3.11+
            data = tomllib.loads(text)
            section = ((data.get("audit") or {}).get("supply_chain") or {})
        except Exception:
            section = _toml_section_fallback(text, "audit.supply_chain")
        for key in ("build_command", "artifacts", "registry_hosts"):
            if key in section and section[key]:
                cfg[key] = section[key]
    for key, val in (cli_overrides or {}).items():
        if val:
            cfg[key] = val
    return cfg


# ---------- artifact detection ---------------------------------------------

def detect_tracked_artifacts(root: Path,
                             tracked: Optional[list] = None) -> list:
    """Git-tracked files that look like build outputs: anything under
    dist/ or build/, minified assets, and root-level bundles when a
    bundler config is tracked. Detection only, no verdict."""
    if tracked is None:
        try:
            out = subprocess.check_output(
                ["git", "ls-files"], cwd=str(root), text=True,
                stderr=subprocess.DEVNULL)
            tracked = out.splitlines()
        except Exception:
            return []
    has_bundler = any(_BUNDLER_CONFIG_RE.search(t) for t in tracked)
    hits = []
    for rel in tracked:
        base = rel.rsplit("/", 1)[-1]
        if rel.startswith(("dist/", "build/")):
            hits.append(rel)
        elif ".min." in base:
            hits.append(rel)
        elif has_bundler and "/" not in rel and base in (
                "main.js", "bundle.js", "styles.css"):
            hits.append(rel)
    return hits


# ---------- stage 2: clean-room rebuild ------------------------------------

def compare_artifact_hashes(built: dict, committed: dict) -> list:
    """Pure comparison: {relpath: sha256} for the rebuilt and committed
    states. Mismatch -> high CWE-494; match -> info (the positive proof
    belongs in the report, and the delta flags a NEW mismatch)."""
    out = []
    for rel in sorted(built):
        b, c = built[rel], committed.get(rel)
        if b is not None and b == c:
            out.append(F.Finding(
                fp=F.fingerprint("CWE-494", rel, "cleanroom-match"),
                phase=PHASE, cwe="CWE-494", severity="info",
                file=rel, line=None, engine="cleanroom",
                message=f"Reproducible: clean-room rebuild of {rel} is"
                        " byte-identical to the committed artifact"))
        else:
            out.append(F.Finding(
                fp=F.fingerprint("CWE-494", rel, "cleanroom-mismatch"),
                phase=PHASE, cwe="CWE-494", severity="high",
                file=rel, line=None, engine="cleanroom",
                message=f"Clean-room rebuild MISMATCH for {rel}: committed"
                        " artifact does not fall out of the committed sources"))
    return out


def run_cleanroom_rebuild(root: Path, cfg: dict,
                          scratch_dir: Optional[Path] = None) -> tuple:
    """Clone HEAD into a scratch dir, install with --ignore-scripts,
    run the configured build command under a scrubbed env, compare the
    artifact hashes before (= committed state, fresh checkout) and after
    the build. Returns (findings, tool_entry). Never raises."""
    build_command = cfg.get("build_command")
    artifacts = cfg.get("artifacts") or []
    if not build_command or not artifacts:
        return [], {"name": "cleanroom-rebuild", "status": "not-configured",
                    "reason": "set [audit.supply_chain] build_command +"
                              " artifacts in .dia/config.toml or pass"
                              " --build-cmd/--artifact"}
    own_scratch = scratch_dir is None
    scratch = Path(tempfile.mkdtemp(prefix="sa-cleanroom-")) if own_scratch \
        else Path(scratch_dir)
    clone_dir = scratch / "src"
    try:
        try:
            cp = _run(["git", "clone", "--no-hardlinks", "--quiet",
                       f"file://{root.resolve()}", str(clone_dir)],
                      timeout=300)
        except Exception as exc:  # noqa: BLE001
            return [], {"name": "cleanroom-rebuild", "status": "error",
                        "reason": f"clone failed: {str(exc)[:100]}"}
        if cp.returncode != 0:
            return [], {"name": "cleanroom-rebuild", "status": "error",
                        "reason": f"clone failed (exit {cp.returncode})"}

        # Committed state: the fresh checkout IS HEAD, hash before building.
        committed = {rel: _sha256(clone_dir / rel) for rel in artifacts}

        env = _scrubbed_env()
        if (clone_dir / "package.json").is_file():
            try:
                cp = _run(["npm", "ci", "--ignore-scripts",
                           "--include=optional"],
                          timeout=900, cwd=clone_dir, env=env)
            except Exception as exc:  # noqa: BLE001
                return [], {"name": "cleanroom-rebuild", "status": "error",
                            "reason": f"npm ci failed: {str(exc)[:100]}"}
            if cp.returncode != 0:
                return [], {"name": "cleanroom-rebuild", "status": "error",
                            "reason": "npm ci failed: "
                                      + (cp.stderr or "")[-160:].strip()}
        try:
            cp = _run(["/bin/sh", "-c", build_command],
                      timeout=1800, cwd=clone_dir, env=env)
        except Exception as exc:  # noqa: BLE001
            return [], {"name": "cleanroom-rebuild", "status": "error",
                        "reason": f"build failed: {str(exc)[:100]}"}
        if cp.returncode != 0:
            return [], {"name": "cleanroom-rebuild", "status": "error",
                        "reason": "build failed: "
                                  + (cp.stderr or "")[-160:].strip()}

        built = {rel: _sha256(clone_dir / rel) for rel in artifacts}
        findings = compare_artifact_hashes(built, committed)
        mismatches = sum(1 for f in findings if f.severity == "high")
        return findings, {"name": "cleanroom-rebuild", "status": "ran",
                          "artifacts": len(artifacts),
                          "mismatches": mismatches,
                          "built_hashes": {k: v for k, v in built.items() if v}}
    finally:
        if own_scratch:
            shutil.rmtree(scratch, ignore_errors=True)


# ---------- stage 3: release attestation verify ----------------------------

def _repo_slug(url: str) -> Optional[str]:
    url = (url or "").strip()
    for rx in _GITHUB_SLUG_RES:
        m = rx.match(url)
        if m:
            return f"{m.group(1)}/{m.group(2)}"
    return None


def _origin_slug(root: Path) -> Optional[str]:
    try:
        cp = _run(["git", "remote", "get-url", "origin"], timeout=30,
                  cwd=root)
    except Exception:
        return None
    if cp.returncode != 0:
        return None
    return _repo_slug(cp.stdout)


def _verify_attestation(asset_path: Path, slug: str):
    """One `gh attestation verify` call mapped to a Finding.
    exit 0 -> info (verified); 'not found' in stderr -> medium (asset has
    no attestation); any other failure -> high (verification FAILED)."""
    name = asset_path.name
    try:
        cp = _run(["gh", "attestation", "verify", str(asset_path),
                   "--repo", slug], timeout=120)
    except Exception as exc:  # noqa: BLE001
        return F.Finding(
            fp=F.fingerprint("CWE-494", name, "attestation-error"),
            phase=PHASE, cwe="CWE-494", severity="medium",
            file=name, line=None, engine="gh-attestation",
            message=f"Attestation check errored for {name}: {str(exc)[:80]}")
    if cp.returncode == 0:
        return F.Finding(
            fp=F.fingerprint("CWE-494", name, "attestation-ok"),
            phase=PHASE, cwe="CWE-494", severity="info",
            file=name, line=None, engine="gh-attestation",
            message=f"Attestation verified: {name}")
    stderr = (cp.stderr or "").lower()
    if "not found" in stderr or "no attestation" in stderr:
        return F.Finding(
            fp=F.fingerprint("CWE-494", name, "attestation-missing"),
            phase=PHASE, cwe="CWE-494", severity="medium",
            file=name, line=None, engine="gh-attestation",
            message=f"No attestation found for release asset {name};"
                    " enable artifact attestation in the release workflow")
    return F.Finding(
        fp=F.fingerprint("CWE-494", name, "attestation-failed"),
        phase=PHASE, cwe="CWE-494", severity="high",
        file=name, line=None, engine="gh-attestation",
        message=f"Attestation verification FAILED for {name}:"
                f" {(cp.stderr or '')[-120:].strip()}")


def run_release_verify(root: Path,
                       rebuilt_hashes: Optional[dict] = None) -> tuple:
    """Verify provenance attestations for every asset of the latest
    GitHub release; optionally cross-check asset hashes against the
    stage-2 rebuild. Returns (findings, tools). Never raises."""
    if shutil.which("gh") is None:
        return [], [{"name": "gh-attestation", "status": "unavailable",
                     "reason": "gh CLI not on PATH"}]
    slug = _origin_slug(root)
    if not slug:
        return [], [{"name": "gh-attestation", "status": "not-applicable",
                     "reason": "no GitHub origin remote"}]
    try:
        cp = _run(["gh", "release", "view", "--json", "tagName,assets",
                   "--repo", slug], timeout=60)
    except Exception as exc:  # noqa: BLE001
        return [], [{"name": "gh-attestation", "status": "error",
                     "reason": str(exc)[:120]}]
    if cp.returncode != 0:
        return [], [{"name": "gh-attestation", "status": "not-applicable",
                     "reason": "no releases found (or offline)"}]
    try:
        release = json.loads(cp.stdout or "{}")
    except Exception:
        return [], [{"name": "gh-attestation", "status": "error",
                     "reason": "unparseable gh release output"}]
    tag = release.get("tagName", "?")
    assets = release.get("assets") or []
    if not assets:
        return [], [{"name": "gh-attestation", "status": "not-applicable",
                     "reason": f"release {tag} has no assets"}]

    findings: list = []
    scratch = Path(tempfile.mkdtemp(prefix="sa-release-"))
    try:
        cp = _run(["gh", "release", "download", tag, "--repo", slug,
                   "-D", str(scratch), "--clobber"], timeout=600)
        if cp.returncode != 0:
            return [], [{"name": "gh-attestation", "status": "error",
                         "reason": "asset download failed: "
                                   + (cp.stderr or "")[-120:].strip()}]
        for asset_path in sorted(scratch.iterdir()):
            if not asset_path.is_file():
                continue
            findings.append(_verify_attestation(asset_path, slug))
            name = asset_path.name
            if rebuilt_hashes and name in rebuilt_hashes:
                asset_hash = _sha256(asset_path)
                if asset_hash and asset_hash != rebuilt_hashes[name]:
                    findings.append(F.Finding(
                        fp=F.fingerprint("CWE-494", name, "release-rebuild-mismatch"),
                        phase=PHASE, cwe="CWE-494", severity="high",
                        file=name, line=None, engine="gh-attestation",
                        message=f"Release asset {name} differs from the"
                                " clean-room rebuild of HEAD (expected for"
                                " older releases; alarming for the release"
                                " that matches HEAD)"))
    finally:
        shutil.rmtree(scratch, ignore_errors=True)
    return findings, [{"name": "gh-attestation", "status": "ran",
                       "release": tag, "assets": len(assets)}]
