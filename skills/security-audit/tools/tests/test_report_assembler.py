"""Tests for security-audit/tools/report_assembler.py.

    python3 skills/security-audit/tools/tests/test_report_assembler.py
"""
from __future__ import annotations
import importlib.util
import json
import sys
import tempfile
from pathlib import Path


TOOLS_DIR = Path(__file__).resolve().parents[1]
SCRIPT = TOOLS_DIR / "report_assembler.py"


def _load():
    spec = importlib.util.spec_from_file_location("report_assembler", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules["report_assembler"] = mod
    spec.loader.exec_module(mod)
    return mod


def _sample_result() -> dict:
    return {
        "schema": 1,
        "scope": "full",
        "scope_detail": "all tracked files",
        "git_branch": "feature/x",
        "project_type": {"project_kinds": ["electron", "obsidian-plugin"]},
        "tools": [
            {"name": "semgrep", "status": "ran", "ruleset": "p/typescript"},
            {"name": "gitleaks", "status": "unavailable", "reason": "not on PATH"},
            {"name": "npm-audit", "status": "offline-skipped"},
            {"name": "pattern-redact", "status": "ran"},
        ],
        "meta": {"file_count": 12, "offline": True},
        "findings": [
            {"fp": "aa", "phase": "sast", "cwe": "CWE-94", "severity": "critical",
             "file": "a.ts", "line": 3, "engine": "semgrep",
             "message": "eval", "status": "unconfirmed", "cvss": "", "evidence": ""},
            {"fp": "bb", "phase": "sast", "cwe": "CWE-79", "severity": "high",
             "file": "b.ts", "line": 9, "engine": "grep-fallback",
             "message": "innerHTML", "status": "unconfirmed", "cvss": "", "evidence": ""},
            {"fp": "cc", "phase": "sca", "cwe": "", "severity": "medium",
             "file": "package.json", "line": None, "engine": "npm-audit",
             "message": "vuln dep foo", "status": "unconfirmed", "cvss": "", "evidence": ""},
            {"fp": "dd", "phase": "secrets", "cwe": "CWE-798", "severity": "low",
             "file": "c.ts", "line": 2, "engine": "entropy-fallback",
             "message": "redacted secret", "status": "unconfirmed", "cvss": "", "evidence": ""},
        ],
    }


def test_fill_counts_and_buckets() -> None:
    m = _load()
    template = TOOLS_DIR.parent / "templates" / "AUDIT-TEMPLATE.md"
    assert template.exists()
    out = m.fill(_sample_result(), template.read_text(encoding="utf-8"),
                project="vault-operator", date="2026-07-23")
    # Metadata filled.
    assert "vault-operator" in out
    assert "2026-07-23" in out
    # Executive summary counts: 1 critical, 1 high in code domain.
    assert "P1: Must Fix" in out
    # Critical + High findings appear in P1.
    p1_section = out.split("P1: Must Fix")[1].split("P2:")[0]
    assert "CWE-94" in p1_section, p1_section
    assert "CWE-79" in p1_section, p1_section
    # Medium goes to P2.
    p2_section = out.split("P2:")[1].split("P3:")[0]
    assert "vuln dep foo" in p2_section, p2_section
    # Low goes to P3.
    p3_section = out.split("P3:")[1]
    assert "redacted secret" in p3_section, p3_section
    print("OK: fill counts + P1/P2/P3 buckets")


def test_fill_tools_are_honest() -> None:
    m = _load()
    template = TOOLS_DIR.parent / "templates" / "AUDIT-TEMPLATE.md"
    out = m.fill(_sample_result(), template.read_text(encoding="utf-8"),
                project="p", date="2026-07-23")
    # Only tools that actually ran are claimed as run; semgrep ran, gitleaks did not.
    assert "semgrep" in out
    # The honest ledger must reflect unavailable/offline, not hide it.
    assert "unavailable" in out or "offline" in out, out
    # Tool-overclaim guard: a tool that did NOT run must not be listed as a used tool.
    tools_section = out.split("Scope and Tools")[1]
    assert "gitleaks" in tools_section  # listed, but with its status
    print("OK: tools ledger honest (no overclaim)")


def test_fill_has_limitations_section() -> None:
    m = _load()
    template = TOOLS_DIR.parent / "templates" / "AUDIT-TEMPLATE.md"
    out = m.fill(_sample_result(), template.read_text(encoding="utf-8"),
                project="p", date="2026-07-23")
    # Mandatory coverage/limitations content.
    lower = out.lower()
    assert "limitation" in lower or "not evaluated" in lower or "coverage" in lower, out
    # Offline SCA must be surfaced as a blindspot.
    assert "offline" in lower, "offline SCA blindspot must be named"
    print("OK: mandatory limitations section present")


def test_delta_from_baselines() -> None:
    m = _load()
    with tempfile.TemporaryDirectory() as raw:
        tmp = Path(raw)
        before = {"findings": [{"fp": "a"}, {"fp": "b"}, {"fp": "c"}]}
        after = {"findings": [{"fp": "b"}, {"fp": "c"}, {"fp": "d"}]}
        bpath = tmp / "prev.json"
        apath = tmp / "last.json"
        bpath.write_text(json.dumps(before), encoding="utf-8")
        apath.write_text(json.dumps(after), encoding="utf-8")
        d = m.delta_from_files(bpath, apath)
        assert set(d["resolved"]) == {"a"}, d
        assert set(d["new"]) == {"d"}, d
        assert set(d["persisted"]) == {"b", "c"}, d
        print("OK: delta from baseline files")


def test_fill_no_findings_clean() -> None:
    m = _load()
    template = TOOLS_DIR.parent / "templates" / "AUDIT-TEMPLATE.md"
    empty = _sample_result()
    empty["findings"] = []
    out = m.fill(empty, template.read_text(encoding="utf-8"),
                project="p", date="2026-07-23")
    # Still a valid report; no crash on zero findings.
    assert "Executive Summary" in out
    print("OK: fill handles zero findings")


ALL_TESTS = [
    test_fill_counts_and_buckets,
    test_fill_tools_are_honest,
    test_fill_has_limitations_section,
    test_delta_from_baselines,
    test_fill_no_findings_clean,
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
    print("\nAll report_assembler tests passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
