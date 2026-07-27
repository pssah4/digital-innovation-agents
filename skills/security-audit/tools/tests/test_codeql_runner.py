"""Tests for security-audit/tools/lib/codeql_runner.py.

Assertion-based, runnable without pytest but pytest-discoverable. No
third-party deps beyond stdlib (`unittest.mock` for patching).

    python3 skills/security-audit/tools/tests/test_codeql_runner.py

Covers the behaviours that keep the runner safe to slot into the SAST
cascade:
  * codeql_available reads PATH honestly
  * SARIF is mapped to Findings with CWE + severity + fingerprint
  * a missing query pack does NOT explode; it degrades to pack-missing
    so the caller can fall back
  * pack_age_check flags a stale pack (>90 days) via the mtime of its
    cached directory
"""
from __future__ import annotations
import importlib.util
import os
import sys
import tempfile
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest.mock import patch


LIB_DIR = Path(__file__).resolve().parents[1] / "lib"


def _load(module_name: str):
    """Same loader shape as test_findings.py, plus lib/ on sys.path so
    codeql_runner's `import findings as F` fallback resolves."""
    if str(LIB_DIR) not in sys.path:
        sys.path.insert(0, str(LIB_DIR))
    path = LIB_DIR / f"{module_name}.py"
    spec = importlib.util.spec_from_file_location(f"sa_{module_name}", path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[f"sa_{module_name}"] = mod
    spec.loader.exec_module(mod)
    return mod


def test_codeql_available_returns_bool() -> None:
    m = _load("codeql_runner")
    with patch.object(m.shutil, "which", return_value="/usr/bin/codeql"):
        assert m.codeql_available() is True
    with patch.object(m.shutil, "which", return_value=None):
        assert m.codeql_available() is False
    print("OK: codeql_available returns bool based on PATH")


def test_run_codeql_parses_sarif() -> None:
    m = _load("codeql_runner")
    sarif = {
        "runs": [{
            "tool": {"driver": {
                "name": "CodeQL",
                "rules": [
                    {"id": "js/code-injection",
                     "properties": {"tags": ["security", "external/cwe/cwe-094"]},
                     "defaultConfiguration": {"level": "error"}},
                    {"id": "js/reflected-xss",
                     "properties": {"tags": ["security", "external/cwe/cwe-079"]},
                     "defaultConfiguration": {"level": "error"}},
                    {"id": "js/incomplete-sanitization",
                     "properties": {"tags": ["correctness", "security"]},
                     "defaultConfiguration": {"level": "warning"}},
                ],
            }},
            "results": [
                {"ruleId": "js/code-injection", "level": "error",
                 "message": {"text": "This code execution depends on a user-provided value."},
                 "locations": [{"physicalLocation": {
                     "artifactLocation": {"uri": "src/vuln.js"},
                     "region": {"startLine": 6}}}]},
                {"ruleId": "js/reflected-xss", "level": "error",
                 "message": {"text": "Cross-site scripting vulnerability."},
                 "locations": [{"physicalLocation": {
                     "artifactLocation": {"uri": "src/vuln.js"},
                     "region": {"startLine": 12}}}]},
                {"ruleId": "js/incomplete-sanitization",
                 "message": {"text": "Partial sanitization."},
                 "locations": [{"physicalLocation": {
                     "artifactLocation": {"uri": "src/util.js"},
                     "region": {"startLine": 3}}}]},
            ],
        }],
    }
    findings = m._sarif_to_findings(sarif, Path("/tmp/whatever"))
    assert len(findings) == 3, findings

    by_rule = {f.message: f for f in findings}
    # CWE tags extracted correctly (leading zeros preserved as int).
    injection = next(f for f in findings if "code execution" in f.message)
    assert injection.cwe == "CWE-94", injection
    assert injection.severity == "high", injection  # SARIF error -> high
    assert injection.file == "src/vuln.js", injection
    assert injection.line == 6, injection
    assert injection.engine == "codeql", injection
    assert injection.phase == "sast", injection
    assert len(injection.fp) == 8, injection

    xss = next(f for f in findings if "Cross-site" in f.message)
    assert xss.cwe == "CWE-79", xss
    assert xss.severity == "high", xss

    # Rule without CWE tag + no explicit result-level: falls back to
    # driver defaultConfiguration.level ('warning') -> medium.
    partial = next(f for f in findings if "Partial" in f.message)
    assert partial.cwe == "", partial
    assert partial.severity == "medium", partial

    # Fingerprints stable and distinct across different rules on the same file.
    assert injection.fp != xss.fp, "same-file findings must have distinct fps"
    print("OK: SARIF mapped to Findings with CWE + severity + fingerprint")


def test_run_codeql_handles_missing_pack() -> None:
    m = _load("codeql_runner")
    with patch.object(m, "ensure_pack", return_value=False):
        findings, tool = m.run_codeql(
            Path("/tmp"), "javascript", Path("/tmp/db-that-must-not-exist"),
        )
    assert findings == [], findings
    assert tool["name"] == "codeql/javascript-queries", tool
    assert tool["status"] == "pack-missing", tool
    assert "codeql pack download" in tool["reason"], tool
    assert "javascript-queries" in tool["reason"], tool
    print("OK: missing pack -> pack-missing status, empty findings, actionable hint")


def test_pack_age_check_marks_old_pack_stale() -> None:
    m = _load("codeql_runner")
    with tempfile.TemporaryDirectory() as raw:
        # Simulate a cached pack dir at .../codeql/javascript-queries/2.3.2/
        pack_dir = Path(raw) / "2.3.2"
        pack_dir.mkdir()
        # Backdate mtime to 143 days ago.
        old = datetime.now(tz=timezone.utc) - timedelta(days=143)
        ts = old.timestamp()
        os.utime(str(pack_dir), (ts, ts))

        with patch.object(m, "_resolve_pack_path", return_value=pack_dir):
            info = m.pack_age_check("codeql/javascript-queries")

    assert info is not None, "pack_age_check returned None despite a valid dir"
    assert info["pack_version"] == "2.3.2", info
    # Filesystem timestamp precision can shave a day off in exact matches;
    # assert >= 142 to keep the test robust across TZ + fs quirks.
    assert info["pack_age_days"] >= 142, info
    assert info["stale"] is True, info
    print("OK: pack_age_check flags 143-day-old pack as stale")


def test_pack_age_check_returns_none_when_unresolvable() -> None:
    m = _load("codeql_runner")
    with patch.object(m, "_resolve_pack_path", return_value=None):
        info = m.pack_age_check("codeql/does-not-exist")
    assert info is None, info
    print("OK: pack_age_check returns None for unresolvable pack")


ALL_TESTS = [
    test_codeql_available_returns_bool,
    test_run_codeql_parses_sarif,
    test_run_codeql_handles_missing_pack,
    test_pack_age_check_marks_old_pack_stale,
    test_pack_age_check_returns_none_when_unresolvable,
]


def main() -> int:
    failed = 0
    for t in ALL_TESTS:
        try:
            t()
        except AssertionError as exc:
            print(f"FAIL: {t.__name__}: {exc}", file=sys.stderr)
            failed += 1
        except Exception as exc:  # noqa: BLE001
            print(f"ERROR: {t.__name__}: {exc!r}", file=sys.stderr)
            failed += 1
    if failed:
        print(f"\n{failed} test(s) failed.", file=sys.stderr)
        return 1
    print("\nAll codeql_runner tests passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
