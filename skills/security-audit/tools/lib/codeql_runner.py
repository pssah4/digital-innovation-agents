"""CodeQL runner for the security-audit skill's SAST cascade.

Wraps `codeql database create` and `codeql database analyze`, then maps
the SARIF output into the shared Finding schema. Never auto-downloads
query packs; a missing pack is reported honestly so the caller can fall
back on the next SAST engine (semgrep, then grep).

stdlib-only. Offline-graceful when codeql is absent or a pack is missing.
Nothing here ever hard-aborts on a tool failure.

Public API:
    codeql_available() -> bool
    ensure_pack(language: str) -> bool
    pack_age_check(pack_name: str) -> dict | None
    run_codeql(root, language, db_dir, timeout=1800) -> tuple[list[Finding], dict]
"""
from __future__ import annotations
import json
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

# Sibling import: works both as a package member (lib.codeql_runner) and
# as a standalone file loaded by importlib (used by the test loader).
try:
    from . import findings as F
except ImportError:  # pragma: no cover
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import findings as F  # type: ignore

STALE_PACK_DAYS = 90

# SARIF level -> our severity vocabulary. Mirrors the mapping in
# _semgrep_sast so cross-engine severity stays comparable.
_SARIF_LEVEL_TO_SEVERITY = {
    "error": "high",
    "warning": "medium",
    "note": "low",
    "none": "info",
}

_CWE_TAG = re.compile(r"external/cwe/cwe-(\d+)", re.IGNORECASE)


def _now() -> datetime:
    """Extraction point so tests can patch the clock deterministically."""
    return datetime.now(tz=timezone.utc)


def _run(cmd: list, timeout: int = 60) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, text=True, capture_output=True, timeout=timeout)


# ---------- availability + pack resolution ---------------------------------

def codeql_available() -> bool:
    """True if the `codeql` CLI is on PATH."""
    return shutil.which("codeql") is not None


def _resolve_pack_path(pack_name: str) -> Optional[Path]:
    """Run `codeql resolve queries <pack>` and pluck the pack's cached
    directory out of the output. Returns None if the pack is not cached
    or the codeql call fails for any reason.

    stdout lists the absolute paths of every .ql file in the pack,
    starting with `<cache>/codeql/<language>-queries/<version>/...`. We
    take the first line, walk up until the segment right after the pack
    name, and return that directory. This is more stable than parsing
    the "Recording pack reference" lines (which go to stderr and are
    log-format, not a documented contract).
    """
    try:
        cp = _run(["codeql", "resolve", "queries", pack_name], timeout=30)
    except Exception:
        return None
    if cp.returncode != 0:
        return None
    for line in (cp.stdout or "").splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        # Look for the pack_name as a path segment; the segment right
        # after it is the version directory we want.
        parts = Path(stripped).parts
        needle = pack_name.split("/")
        for i in range(len(parts) - len(needle)):
            if list(parts[i:i + len(needle)]) == needle and i + len(needle) < len(parts):
                return Path(*parts[:i + len(needle) + 1])
    return None


def ensure_pack(language: str) -> bool:
    """True if codeql/<language>-queries is resolvable locally.
    Does NOT auto-download. The skill emits the exact download command in
    its tools[] ledger instead, so nothing is fetched behind the user's back.
    """
    return _resolve_pack_path(f"codeql/{language}-queries") is not None


def pack_age_check(pack_name: str) -> Optional[dict]:
    """Look up a pack's version + age from its cached directory.

    Version comes from the directory name (packs live at
    ~/.codeql/packages/<pack>/<version>/), age from the directory mtime.
    Returns:
        {"pack_version": str, "pack_age_days": int, "stale": bool}
    or None when the pack can not be resolved.
    """
    path = _resolve_pack_path(pack_name)
    if path is None:
        return None
    try:
        mtime = datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc)
    except OSError:
        return None
    age_days = (_now() - mtime).days
    return {
        "pack_version": path.name,
        "pack_age_days": age_days,
        "stale": age_days > STALE_PACK_DAYS,
    }


# ---------- SARIF -> Finding mapping ---------------------------------------

def _cwe_from_tags(tags) -> str:
    """Pick the first CWE-N tag from a SARIF rule's properties.tags list."""
    if not isinstance(tags, list):
        return ""
    for tag in tags:
        if not isinstance(tag, str):
            continue
        m = _CWE_TAG.search(tag)
        if m:
            return f"CWE-{int(m.group(1))}"
    return ""


def _sarif_to_findings(sarif: dict, root: Path) -> list:
    """Map SARIF v2.1.0 results[] to Finding objects using the shared
    fingerprint. Unknown CWE -> empty string. Unknown severity -> medium.

    Fingerprint is over (cwe-or-ruleId, path, ruleId + message tail) so
    two hits on the same line with different rules stay distinct while
    line movement stays invisible to the fingerprint (matches the
    existing convention in tools/lib/findings.py).
    """
    findings = []
    for run in sarif.get("runs", []) or []:
        # Build ruleId -> {cwe, default_level} map from the driver metadata.
        rules = {}
        driver = (run.get("tool") or {}).get("driver") or {}
        for rule in driver.get("rules") or []:
            rid = rule.get("id", "")
            tags = (rule.get("properties") or {}).get("tags", [])
            default_level = ((rule.get("defaultConfiguration") or {}).get("level")
                             or rule.get("level") or "warning")
            rules[rid] = {"cwe": _cwe_from_tags(tags), "level": default_level}

        for res in run.get("results") or []:
            rid = res.get("ruleId", "")
            rmeta = rules.get(rid, {})
            cwe = rmeta.get("cwe", "")
            level = res.get("level") or rmeta.get("level") or "warning"
            severity = _SARIF_LEVEL_TO_SEVERITY.get(level, "medium")
            msg = (res.get("message") or {}).get("text", rid)
            loc = ((res.get("locations") or [{}])[0].get("physicalLocation") or {})
            uri = (loc.get("artifactLocation") or {}).get("uri", "?")
            line = (loc.get("region") or {}).get("startLine")
            snippet = f"{rid}|{msg[:60]}"
            findings.append(F.Finding(
                fp=F.fingerprint(cwe or rid, uri, snippet),
                phase="sast", cwe=cwe, severity=severity,
                file=uri, line=line, engine="codeql",
                message=msg,
            ))
    return findings


# ---------- end-to-end runner ----------------------------------------------

def run_codeql(root: Path, language: str, db_dir: Path,
               timeout: int = 1800) -> tuple:
    """Build a CodeQL DB for `language`, analyze with the standard
    queries pack, parse SARIF, map to Findings.

    Returns (findings, tool_entry). tool_entry always has 'name' + 'status'.
    Status values:
        'ran'           -> analysis completed, findings may be empty
        'pack-missing'  -> query pack not cached; hint in 'reason'
        'error'         -> any other failure; short reason in 'reason'
    Never raises.
    """
    pack = f"codeql/{language}-queries"
    if not ensure_pack(language):
        return [], {"name": pack, "status": "pack-missing",
                    "reason": f"pack not cached; run: codeql pack download {pack}"}

    db_dir.parent.mkdir(parents=True, exist_ok=True)
    try:
        cp = _run(
            ["codeql", "database", "create", str(db_dir),
             f"--language={language}", f"--source-root={root}", "--overwrite"],
            timeout=timeout,
        )
        if cp.returncode != 0:
            return [], {"name": pack, "status": "error",
                        "reason": f"database create failed (exit {cp.returncode})"}
    except subprocess.TimeoutExpired:
        return [], {"name": pack, "status": "error",
                    "reason": f"database create timeout ({timeout}s)"}
    except Exception as exc:  # noqa: BLE001
        return [], {"name": pack, "status": "error", "reason": str(exc)[:120]}

    sarif_path = db_dir.parent / f"{db_dir.name}.sarif"
    try:
        cp = _run(
            ["codeql", "database", "analyze", str(db_dir), pack,
             "--format=sarif-latest", f"--output={sarif_path}"],
            timeout=timeout,
        )
        # codeql analyze exits 0 on success; there is no separate "findings
        # present" exit code, unlike our own scripts.
        if cp.returncode != 0:
            return [], {"name": pack, "status": "error",
                        "reason": f"analyze failed (exit {cp.returncode})"}
    except subprocess.TimeoutExpired:
        return [], {"name": pack, "status": "error",
                    "reason": f"analyze timeout ({timeout}s)"}
    except Exception as exc:  # noqa: BLE001
        return [], {"name": pack, "status": "error", "reason": str(exc)[:120]}

    try:
        sarif = json.loads(sarif_path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        return [], {"name": pack, "status": "error",
                    "reason": f"sarif parse failed: {str(exc)[:80]}"}
    findings = _sarif_to_findings(sarif, root)
    return findings, {"name": pack, "status": "ran"}
