"""Tests for security-audit/tools/audit_scan.py.

Focus on the behaviours that make the scanner trustworthy:
  * grep-fallback SAST finds CWE patterns without any external tool
  * the honest tools[] ledger records what actually ran
  * secret matches are redacted (never plaintext) in output
  * SCA degrades gracefully when the package manager / net is absent
  * scope drives which files are scanned

Assertion-based, pytest-discoverable.

    python3 skills/security-audit/tools/tests/test_audit_scan.py
"""
from __future__ import annotations
import importlib.util
import json
import subprocess
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch


TOOLS_DIR = Path(__file__).resolve().parents[1]
SCRIPT = TOOLS_DIR / "audit_scan.py"


def _load():
    spec = importlib.util.spec_from_file_location("audit_scan", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules["audit_scan"] = mod
    spec.loader.exec_module(mod)
    return mod


def _write(tmp: Path, rel: str, content: str) -> None:
    p = tmp / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")


def test_grep_sast_finds_cwe_patterns() -> None:
    m = _load()
    with tempfile.TemporaryDirectory() as raw:
        tmp = Path(raw)
        _write(tmp, "src/danger.ts",
               "eval(userInput)\n"
               "el.innerHTML = data\n"
               "child_process.exec(cmd)\n")
        findings = m.grep_sast(tmp, ["src/danger.ts"])
        cwes = {f.cwe for f in findings}
        assert "CWE-94" in cwes, cwes   # eval
        assert "CWE-79" in cwes, cwes   # innerHTML
        assert "CWE-78" in cwes, cwes   # exec
        for f in findings:
            assert f.engine == "grep-fallback", f
            assert f.fp and len(f.fp) == 8, f
        print("OK: grep SAST finds CWE patterns")


def test_grep_sast_skips_comments_optional() -> None:
    m = _load()
    with tempfile.TemporaryDirectory() as raw:
        tmp = Path(raw)
        # A line that is clearly a finding.
        _write(tmp, "a.ts", "const x = eval(s)\n")
        findings = m.grep_sast(tmp, ["a.ts"])
        assert any(f.cwe == "CWE-94" for f in findings), findings
        print("OK: grep SAST basic hit")


def test_tool_available_false_for_missing() -> None:
    m = _load()
    assert m.tool_available("definitely-not-a-real-binary-xyz") is False
    # python3 should exist in the test environment.
    assert m.tool_available("python3") is True
    print("OK: tool_available detects missing vs present")


def test_secrets_scan_redacts() -> None:
    m = _load()
    with tempfile.TemporaryDirectory() as raw:
        tmp = Path(raw)
        secret = "AKIA" + "1234567890ABCDEF"  # AWS-key-shaped
        _write(tmp, "cfg.ts", f'const key = "{secret}"\n')
        findings, tools = m.run_secrets(tmp, ["cfg.ts"])
        blob = json.dumps([f.to_dict() for f in findings])
        assert secret not in blob, f"secret leaked into findings: {blob}"
        # If the entropy fallback fired, there is at least a redacted record.
        # (gitleaks may or may not be installed; either way, no plaintext.)
        print("OK: secrets scan never emits plaintext")


def test_sca_graceful_without_npm(monkeypatch_env=None) -> None:
    m = _load()
    with tempfile.TemporaryDirectory() as raw:
        tmp = Path(raw)
        # No package.json at all -> nothing to scan, must not crash, must
        # record honest tool status.
        findings, tools = m.run_sca(tmp)
        assert isinstance(findings, list), findings
        assert isinstance(tools, list), tools
        # Every tool entry has a status field.
        for t in tools:
            assert "status" in t and "name" in t, t
        print("OK: SCA graceful without package.json")


def test_run_all_shape_and_honest_tools() -> None:
    m = _load()
    # CodeQL forced off for this test: a real DB build would take 30+s
    # and make the suite non-deterministic across machines. CodeQL-on
    # cascade is covered by test_run_all_sast_cascade_with_codeql below.
    with tempfile.TemporaryDirectory() as raw:
        tmp = Path(raw)
        subprocess.run(["git", "init", "-q", "-b", "main"], cwd=tmp, check=True)
        subprocess.run(["git", "config", "user.email", "t@t.t"], cwd=tmp, check=True)
        subprocess.run(["git", "config", "user.name", "t"], cwd=tmp, check=True)
        _write(tmp, "package.json", json.dumps({"name": "x", "dependencies": {}}))
        _write(tmp, "src/v.ts", "eval(x)\n")
        subprocess.run(["git", "add", "-A"], cwd=tmp, check=True)
        subprocess.run(["git", "commit", "-q", "-m", "init"], cwd=tmp, check=True)

        with patch.object(m.CQ, "codeql_available", return_value=False):
            result = m.run_all(tmp, scope="full")
        # Envelope shape.
        for key in ("schema", "scope", "project_type", "tools", "findings", "meta"):
            assert key in result, f"missing {key}: {list(result)}"
        assert result["scope"] == "full"
        # eval finding surfaced.
        assert any(f["cwe"] == "CWE-94" for f in result["findings"]), result["findings"]
        # tools ledger is honest: each entry declares a status.
        statuses = {t["name"]: t["status"] for t in result["tools"]}
        assert statuses, "tools ledger empty"
        for name, st in statuses.items():
            assert st in ("ran", "unavailable", "offline-skipped", "error",
                          "pack-missing"), (name, st)
        # codeql is now part of the ledger, even when unavailable.
        assert "codeql" in statuses, statuses
        assert statuses["codeql"] == "unavailable", statuses
        # findings are JSON-serializable.
        json.dumps(result)
        print("OK: run_all shape + honest tools ledger")


def test_run_all_sast_cascade_with_codeql() -> None:
    """CodeQL-on path uses mocked ensure_pack + run_codeql so the test
    stays fast and does not depend on a real query pack. Verifies:
      * codeql tool entry lands in the ledger with pack age metadata
      * semgrep + grep still run alongside (three-layer cascade)
      * pack-missing status is surfaced when a language pack is absent
    """
    m = _load()
    with tempfile.TemporaryDirectory() as raw:
        tmp = Path(raw)
        subprocess.run(["git", "init", "-q", "-b", "main"], cwd=tmp, check=True)
        subprocess.run(["git", "config", "user.email", "t@t.t"], cwd=tmp, check=True)
        subprocess.run(["git", "config", "user.name", "t"], cwd=tmp, check=True)
        _write(tmp, "package.json", json.dumps({"name": "x", "dependencies": {}}))
        _write(tmp, "src/v.ts", "eval(x)\n")
        subprocess.run(["git", "add", "-A"], cwd=tmp, check=True)
        subprocess.run(["git", "commit", "-q", "-m", "init"], cwd=tmp, check=True)

        fake_finding = m.F.Finding(
            fp="deadbeef", phase="sast", cwe="CWE-94", severity="high",
            file="src/v.ts", line=1, engine="codeql",
            message="Code injection (mock)",
        )

        def fake_run_codeql(root, lang, db_dir, timeout=1800):
            return [fake_finding], {"name": f"codeql/{lang}-queries", "status": "ran"}

        def fake_pack_age(name):
            return {"pack_version": "2.3.2", "pack_age_days": 47, "stale": False}

        with patch.object(m.CQ, "codeql_available", return_value=True), \
             patch.object(m.CQ, "run_codeql", side_effect=fake_run_codeql), \
             patch.object(m.CQ, "pack_age_check", side_effect=fake_pack_age):
            result = m.run_all(tmp, scope="full")

        statuses = {t["name"]: t["status"] for t in result["tools"]}
        # CodeQL tool entry present with the ran status.
        assert "codeql/javascript-queries" in statuses, statuses
        assert statuses["codeql/javascript-queries"] == "ran", statuses
        # Pack age metadata carried through to the ledger.
        codeql_entry = next(t for t in result["tools"]
                            if t["name"] == "codeql/javascript-queries")
        assert codeql_entry.get("pack_version") == "2.3.2", codeql_entry
        assert codeql_entry.get("pack_age_days") == 47, codeql_entry
        # CodeQL finding surfaced alongside grep's eval hit (both CWE-94:
        # dedup keeps them distinct because fingerprints differ).
        cwe_94 = [f for f in result["findings"] if f["cwe"] == "CWE-94"]
        assert any(f["engine"] == "codeql" for f in cwe_94), cwe_94
        assert any(f["engine"] == "grep-fallback" for f in cwe_94), cwe_94
        print("OK: run_all runs CodeQL alongside semgrep+grep, pack age surfaced")


def test_run_all_sast_pack_missing_falls_back() -> None:
    """CodeQL is available but the pack is not cached: pack-missing is
    reported, no findings from CodeQL, semgrep+grep continue normally."""
    m = _load()
    with tempfile.TemporaryDirectory() as raw:
        tmp = Path(raw)
        subprocess.run(["git", "init", "-q", "-b", "main"], cwd=tmp, check=True)
        subprocess.run(["git", "config", "user.email", "t@t.t"], cwd=tmp, check=True)
        subprocess.run(["git", "config", "user.name", "t"], cwd=tmp, check=True)
        _write(tmp, "package.json", json.dumps({"name": "x", "dependencies": {}}))
        _write(tmp, "src/v.ts", "eval(x)\n")
        subprocess.run(["git", "add", "-A"], cwd=tmp, check=True)
        subprocess.run(["git", "commit", "-q", "-m", "init"], cwd=tmp, check=True)

        with patch.object(m.CQ, "codeql_available", return_value=True), \
             patch.object(m.CQ, "ensure_pack", return_value=False):
            result = m.run_all(tmp, scope="full")

        statuses = {t["name"]: t["status"] for t in result["tools"]}
        assert statuses.get("codeql/javascript-queries") == "pack-missing", statuses
        pack_tool = next(t for t in result["tools"]
                         if t["name"] == "codeql/javascript-queries")
        assert "codeql pack download" in pack_tool["reason"], pack_tool
        # Grep still surfaces the eval finding.
        assert any(f["cwe"] == "CWE-94" and f["engine"] == "grep-fallback"
                   for f in result["findings"]), result["findings"]
        print("OK: pack-missing falls back to lower layers cleanly")


def test_run_all_records_taxonomy_snapshot() -> None:
    m = _load()
    with tempfile.TemporaryDirectory() as raw:
        tmp = Path(raw)
        subprocess.run(["git", "init", "-q", "-b", "main"], cwd=tmp, check=True)
        subprocess.run(["git", "config", "user.email", "t@t.t"], cwd=tmp, check=True)
        subprocess.run(["git", "config", "user.name", "t"], cwd=tmp, check=True)
        _write(tmp, "a.ts", "eval(x)\n")
        subprocess.run(["git", "add", "-A"], cwd=tmp, check=True)
        subprocess.run(["git", "commit", "-q", "-m", "c"], cwd=tmp, check=True)
        tax = {"owasp": "2025", "cwe-top-25": "2024"}
        result = m.run_all(tmp, scope="full", taxonomy=tax, write_baseline=False)
        # The snapshotted taxonomy must reach the envelope so the report's
        # limitations section can name the editions instead of "unrecorded".
        assert result.get("taxonomy") == tax, result.get("taxonomy")
        print("OK: run_all records taxonomy snapshot in envelope")


def test_run_all_diff_scope_limits_files() -> None:
    m = _load()
    with tempfile.TemporaryDirectory() as raw:
        tmp = Path(raw)
        subprocess.run(["git", "init", "-q", "-b", "main"], cwd=tmp, check=True)
        subprocess.run(["git", "config", "user.email", "t@t.t"], cwd=tmp, check=True)
        subprocess.run(["git", "config", "user.name", "t"], cwd=tmp, check=True)
        _write(tmp, "old.ts", "eval(a)\n")
        subprocess.run(["git", "add", "-A"], cwd=tmp, check=True)
        subprocess.run(["git", "commit", "-q", "-m", "c1"], cwd=tmp, check=True)
        _write(tmp, "new.ts", "eval(b)\n")
        subprocess.run(["git", "add", "-A"], cwd=tmp, check=True)
        subprocess.run(["git", "commit", "-q", "-m", "c2"], cwd=tmp, check=True)

        result = m.run_all(tmp, scope="commit")
        sast_files = {f["file"] for f in result["findings"] if f["phase"] == "sast"}
        # Only the last commit's file is in the reported SAST scope.
        assert sast_files <= {"new.ts"}, sast_files
        assert "new.ts" in sast_files, sast_files
        print("OK: diff scope limits reported SAST files")


ALL_TESTS = [
    test_grep_sast_finds_cwe_patterns,
    test_grep_sast_skips_comments_optional,
    test_tool_available_false_for_missing,
    test_secrets_scan_redacts,
    test_sca_graceful_without_npm,
    test_run_all_shape_and_honest_tools,
    test_run_all_sast_cascade_with_codeql,
    test_run_all_sast_pack_missing_falls_back,
    test_run_all_records_taxonomy_snapshot,
    test_run_all_diff_scope_limits_files,
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
    print("\nAll audit_scan tests passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
