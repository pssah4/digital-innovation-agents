"""Static supply-chain checks for the security-audit skill (stage 1).

Pure file inspection: no network, no subprocesses, deterministic. The
clean-room rebuild (stage 2) and release attestation verify (stage 3)
live in lib/cleanroom.py because they execute external commands.

What each check proves, and what it does not:
  * Lockfile provenance proves registry fidelity (every package resolves
    to an allowed registry host with an integrity hash). It does NOT
    prove the package is benign; a compromised release passes with a
    valid hash.
  * Action pinning proves a workflow cannot be silently retargeted via a
    mutable tag. Unpinned actions in workflows that hold write
    permissions are the high-severity case.
  * The install-script inventory is not a policy violation by itself; it
    is emitted as delta-able info findings so a NEWLY appearing
    postinstall package shows up as `new` in the re-audit delta, which
    is the actual alarm case.

stdlib-only, offline-graceful, never raises out of a check.

Public API:
    check_lockfile_provenance(root, registry_hosts=None) -> (findings, tool)
    check_install_scripts(root) -> (findings, tool)
    check_action_pinning(root) -> (findings, tool)
    check_manifest_hygiene(root) -> (findings, tool)
    check_python_pins(root) -> (findings, tool)
    run_supply_chain_static(root, config=None) -> (findings, tools)
"""
# security-audit-scan: skip -- this module stores policy-detection
# patterns as data literals; scanning it against those same patterns
# only produces self-referential false positives.
from __future__ import annotations
import json
import re
import sys
from pathlib import Path
from typing import Optional
from urllib.parse import urlparse

try:
    from . import findings as F
except ImportError:  # pragma: no cover
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import findings as F  # type: ignore

PHASE = "supply-chain"
ENGINE = "supply-chain"
DEFAULT_REGISTRY_HOSTS = ("registry.npmjs.org",)

_USES_RE = re.compile(r"uses:\s*([^\s#]+)@([^\s#]+)")
_SHA_RE = re.compile(r"^[0-9a-f]{40}$")
_PERMISSIONS_RE = re.compile(r"^\s*permissions:", re.MULTILINE)
_WRITE_PERM_RE = re.compile(r"^\s*[a-z-]+:\s*write\b", re.MULTILINE)
_RUN_NPM_INSTALL_RE = re.compile(r"\bnpm\s+install\b")
_RUN_PIP_INSTALL_RE = re.compile(r"\bpip3?\s+install\b")


def _finding(cwe: str, severity: str, file: str, snippet: str,
             message: str, line: Optional[int] = None) -> F.Finding:
    return F.Finding(
        fp=F.fingerprint(cwe, file, snippet),
        phase=PHASE, cwe=cwe, severity=severity,
        file=file, line=line, engine=ENGINE, message=message,
    )


def _read_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def _lockfile_packages(root: Path) -> Optional[dict]:
    """The `packages` map of a v2/v3 package-lock.json, or None when the
    lockfile is absent or unparseable. The root entry ("") is dropped."""
    lock = _read_json(root / "package-lock.json")
    if not lock:
        return None
    packages = lock.get("packages")
    if not isinstance(packages, dict):
        return None
    return {k: v for k, v in packages.items()
            if k and isinstance(v, dict) and not v.get("link")}


def _pkg_name(pkg_path: str) -> str:
    """`node_modules/a/node_modules/b` -> `b` (scoped names keep both
    segments: `node_modules/@scope/pkg` -> `@scope/pkg`)."""
    parts = pkg_path.split("node_modules/")
    tail = parts[-1].strip("/")
    return tail or pkg_path


# ---------- lockfile provenance --------------------------------------------

def check_lockfile_provenance(root: Path, registry_hosts=None) -> tuple:
    hosts = tuple(registry_hosts or DEFAULT_REGISTRY_HOSTS)
    packages = _lockfile_packages(root)
    if packages is None:
        return [], {"name": "lockfile-provenance", "status": "not-applicable",
                    "reason": "no parseable package-lock.json"}
    out: list = []
    for pkg_path in sorted(packages):
        entry = packages[pkg_path]
        name = _pkg_name(pkg_path)
        resolved = entry.get("resolved", "")
        integrity = entry.get("integrity", "")
        if resolved.startswith(("git+", "git://")):
            out.append(_finding(
                "CWE-829", "high", "package-lock.json",
                f"{pkg_path}|provenance|git",
                f"Git dependency bypasses the registry: {name} ({resolved})"))
            continue
        if resolved.startswith("http://"):
            out.append(_finding(
                "CWE-829", "high", "package-lock.json",
                f"{pkg_path}|provenance|http",
                f"Plain-HTTP dependency source: {name} ({resolved})"))
            continue
        if resolved.startswith("https://"):
            host = urlparse(resolved).hostname or ""
            if host not in hosts:
                out.append(_finding(
                    "CWE-829", "medium", "package-lock.json",
                    f"{pkg_path}|provenance|host|{host}",
                    f"Dependency resolved from non-allowlisted host {host}: {name}"
                    " (add the host to registry_hosts if this registry is intended)"))
        if resolved and not str(integrity).startswith("sha512-"):
            out.append(_finding(
                "CWE-494", "medium", "package-lock.json",
                f"{pkg_path}|integrity",
                f"Lockfile entry without sha512 integrity: {name}"))
    return out, {"name": "lockfile-provenance", "status": "ran",
                 "packages": len(packages)}


def check_install_scripts(root: Path) -> tuple:
    packages = _lockfile_packages(root)
    if packages is None:
        return [], {"name": "install-scripts", "status": "not-applicable",
                    "reason": "no parseable package-lock.json"}
    out: list = []
    scripted = sorted(_pkg_name(p) for p, e in packages.items()
                      if e.get("hasInstallScript"))
    for name in scripted:
        out.append(_finding(
            "CWE-829", "info", "package-lock.json",
            f"install-script {name}",
            f"Package runs install scripts: {name}"))
    return out, {"name": "install-scripts", "status": "ran",
                 "count": len(scripted)}


# ---------- GitHub workflow checks -----------------------------------------

def _workflow_files(root: Path) -> list:
    wf_dir = root / ".github" / "workflows"
    if not wf_dir.is_dir():
        return []
    return sorted(p for p in wf_dir.iterdir()
                  if p.suffix in (".yml", ".yaml") and p.is_file())


def check_action_pinning(root: Path) -> tuple:
    """Line-based workflow policy checks. Deliberately regex-based (no
    YAML parser in stdlib); exotic syntax (anchors, folded scalars) can
    slip through and is documented as a limitation in the references."""
    files = _workflow_files(root)
    if not files:
        return [], {"name": "action-pinning", "status": "not-applicable",
                    "reason": "no .github/workflows directory"}
    has_lockfile = (root / "package-lock.json").is_file()
    out: list = []
    for path in files:
        rel = str(path.relative_to(root))
        try:
            text = path.read_text(encoding="utf-8")
        except Exception:
            continue
        has_permissions = bool(_PERMISSIONS_RE.search(text))
        has_write = bool(_WRITE_PERM_RE.search(text))
        uses_checkout = False
        for ln, line in enumerate(text.splitlines(), start=1):
            m = _USES_RE.search(line)
            if m:
                action, ref = m.group(1), m.group(2)
                if action.startswith("./") or action.startswith("docker://"):
                    continue
                if action.startswith("actions/checkout"):
                    uses_checkout = True
                if not _SHA_RE.match(ref):
                    sev = "high" if has_write else "medium"
                    out.append(_finding(
                        "CWE-829", sev, rel, f"uses {action}@{ref}",
                        f"Action pinned to mutable ref: {action}@{ref}"
                        " (pin to a full commit SHA)", line=ln))
            stripped = line.strip()
            if stripped.startswith("- run:") or stripped.startswith("run:"):
                if (_RUN_NPM_INSTALL_RE.search(line) and "npm ci" not in line
                        and has_lockfile):
                    out.append(_finding(
                        "CWE-829", "low", rel, "run npm install",
                        "Workflow uses `npm install` although a lockfile exists;"
                        " use `npm ci` for lockfile fidelity", line=ln))
                if (_RUN_PIP_INSTALL_RE.search(line) and "==" not in line
                        and " -r" not in line):
                    out.append(_finding(
                        "CWE-829", "medium", rel, "run pip install unpinned",
                        "Workflow installs a Python package without a pinned"
                        " version (`pip install pkg==x.y.z`)", line=ln))
        if not has_permissions:
            out.append(_finding(
                "CWE-250", "medium", rel, "no permissions block",
                "Workflow has no `permissions:` block; the default token"
                " grant is broader than needed"))
        if has_write and uses_checkout and "persist-credentials" not in text:
            out.append(_finding(
                "CWE-522", "low", rel, "checkout persist-credentials",
                "checkout on a write-permission workflow without"
                " `persist-credentials: false`"))
    return out, {"name": "action-pinning", "status": "ran",
                 "workflows": len(files)}


# ---------- manifest hygiene -----------------------------------------------

def _npmrc_ignores_scripts(root: Path) -> bool:
    npmrc = root / ".npmrc"
    if not npmrc.is_file():
        return False
    try:
        for line in npmrc.read_text(encoding="utf-8").splitlines():
            if re.match(r"^\s*ignore-scripts\s*=\s*true\s*$", line):
                return True
    except Exception:
        pass
    return False


def check_manifest_hygiene(root: Path) -> tuple:
    packages = _lockfile_packages(root)
    pkg = _read_json(root / "package.json")
    if packages is None and not pkg:
        return [], {"name": "manifest-hygiene", "status": "not-applicable",
                    "reason": "no npm manifest"}
    out: list = []
    if packages is not None:
        scripted = [p for p, e in packages.items() if e.get("hasInstallScript")]
        if scripted and not _npmrc_ignores_scripts(root):
            out.append(_finding(
                "CWE-829", "info", ".npmrc",
                "no ignore-scripts policy",
                f"{len(scripted)} package(s) may run install scripts and no"
                " .npmrc sets ignore-scripts=true"))
        tree_names = {_pkg_name(p) for p in packages}
        for override in sorted((pkg.get("overrides") or {}).keys()):
            if override not in tree_names:
                out.append(_finding(
                    "CWE-829", "low", "package.json",
                    f"override {override}",
                    f"Stale override: {override} is not in the lockfile tree"))
    return out, {"name": "manifest-hygiene", "status": "ran"}


# ---------- python pinning -------------------------------------------------

def check_python_pins(root: Path) -> tuple:
    req_files = sorted(root.glob("requirements*.txt"))
    if not req_files:
        return [], {"name": "python-pins", "status": "not-applicable",
                    "reason": "no requirements*.txt"}
    out: list = []
    for path in req_files:
        rel = str(path.relative_to(root))
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except Exception:
            continue
        for ln, line in enumerate(lines, start=1):
            spec = line.strip()
            if not spec or spec.startswith(("#", "-")):
                continue
            if "==" not in spec:
                name = re.split(r"[<>=\[; ]", spec, 1)[0]
                out.append(_finding(
                    "CWE-829", "low", rel, f"unpinned {name}",
                    f"Unpinned Python requirement: {name}", line=ln))
    return out, {"name": "python-pins", "status": "ran",
                 "files": len(req_files)}


# ---------- orchestration --------------------------------------------------

def run_supply_chain_static(root: Path, config: dict | None = None) -> tuple:
    """Run every static check, merge findings and ledger entries.
    `config` may carry `registry_hosts` (from [audit.supply_chain] in
    .dia/config.toml or CLI flags)."""
    cfg = config or {}
    hosts = cfg.get("registry_hosts") or list(DEFAULT_REGISTRY_HOSTS)
    findings: list = []
    tools: list = []
    for check in (
        lambda: check_lockfile_provenance(root, registry_hosts=hosts),
        lambda: check_install_scripts(root),
        lambda: check_action_pinning(root),
        lambda: check_manifest_hygiene(root),
        lambda: check_python_pins(root),
    ):
        try:
            fs, tool = check()
        except Exception as exc:  # noqa: BLE001
            tools.append({"name": "supply-chain", "status": "error",
                          "reason": str(exc)[:120]})
            continue
        findings.extend(fs)
        tools.append(tool)
    # De-dupe by fingerprint, preserving order.
    seen: set = set()
    deduped = [f for f in findings if not (f.fp in seen or seen.add(f.fp))]
    return deduped, tools
