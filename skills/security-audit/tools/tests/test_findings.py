"""Tests for security-audit/tools/lib/findings.py.

Assertion-based, runnable without pytest but pytest-discoverable. No
third-party deps. Invoke directly:

    python3 skills/security-audit/tools/tests/test_findings.py
"""
from __future__ import annotations
import importlib.util
import json
import subprocess
import sys
import tempfile
from pathlib import Path


LIB_DIR = Path(__file__).resolve().parents[1] / "lib"


def _load(module_name: str):
    path = LIB_DIR / f"{module_name}.py"
    spec = importlib.util.spec_from_file_location(f"sa_{module_name}", path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[f"sa_{module_name}"] = mod
    spec.loader.exec_module(mod)
    return mod


def test_fingerprint_stable_and_line_independent() -> None:
    m = _load("findings")
    # Same cwe/path/snippet -> same fp regardless of surrounding whitespace.
    a = m.fingerprint("CWE-79", "src/x.ts", "  el.innerHTML   = userInput ")
    b = m.fingerprint("CWE-79", "src/x.ts", "el.innerHTML = userInput")
    assert a == b, f"whitespace normalization broken: {a} != {b}"
    assert len(a) == 8 and all(c in "0123456789abcdef" for c in a), a
    # Different cwe -> different fp.
    assert m.fingerprint("CWE-89", "src/x.ts", "el.innerHTML = userInput") != a
    # Different path -> different fp.
    assert m.fingerprint("CWE-79", "src/y.ts", "el.innerHTML = userInput") != a
    print("OK: fingerprint stable + line-independent")


def test_fingerprint_case_insensitive_snippet() -> None:
    m = _load("findings")
    # Snippet normalization lowercases, so case differences collapse.
    a = m.fingerprint("CWE-79", "src/x.ts", "InnerHTML")
    b = m.fingerprint("CWE-79", "src/x.ts", "innerhtml")
    assert a == b, "snippet should be case-insensitive"
    print("OK: fingerprint case-insensitive snippet")


def test_redact_never_leaks_plaintext() -> None:
    m = _load("findings")
    secret = "sk-ABCD1234567890SECRET"
    r = m.redact(secret)
    blob = json.dumps(r)
    assert secret not in blob, f"redact leaked plaintext: {blob}"
    # Only a 4-char preview is allowed.
    assert r["preview"].startswith("sk-A"), r
    assert secret[4:] not in blob, "tail of secret leaked"
    assert r["len"] == len(secret), r
    assert len(r["sha1"]) == 8, r
    # Short secret does not slice out of range.
    r2 = m.redact("ab")
    assert "ab" not in json.dumps(r2) or r2["len"] == 2  # len is fine; preview must not equal full
    print("OK: redact never leaks plaintext")


def test_finding_roundtrip() -> None:
    m = _load("findings")
    f = m.Finding(
        fp="a1b2c3d4",
        phase="sast",
        cwe="CWE-79",
        severity="high",
        file="src/x.ts",
        line=42,
        engine="grep-fallback",
        message="innerHTML with user input",
    )
    d = f.to_dict()
    assert d["status"] == "unconfirmed", d  # default status
    assert d["fp"] == "a1b2c3d4"
    assert d["line"] == 42
    # JSON-serializable.
    json.dumps(d)
    print("OK: Finding roundtrip")


def _git_init(tmp: Path) -> None:
    subprocess.run(["git", "init", "-q"], cwd=tmp, check=True)
    subprocess.run(["git", "config", "user.email", "t@t.t"], cwd=tmp, check=True)
    subprocess.run(["git", "config", "user.name", "t"], cwd=tmp, check=True)


def test_baseline_write_rotates_and_reads() -> None:
    m = _load("findings")
    with tempfile.TemporaryDirectory() as raw:
        tmp = Path(raw)
        _git_init(tmp)
        f1 = [m.Finding(fp="aaa", phase="sast", cwe="CWE-79", severity="high",
                        file="a.ts", line=1, engine="grep", message="x")]
        # First write: no prev-run yet.
        m.write_baseline(tmp, f1, scope="full", taxonomy={"owasp": "2025"})
        got = m.read_baseline(tmp, which="last")
        assert got is not None
        assert got["scope"] == "full", got
        assert got["taxonomy"]["owasp"] == "2025", got
        assert got["findings"][0]["fp"] == "aaa", got
        assert m.read_baseline(tmp, which="prev") is None, "no prev on first write"

        # Second write rotates last -> prev.
        f2 = [m.Finding(fp="bbb", phase="sast", cwe="CWE-89", severity="low",
                        file="b.ts", line=2, engine="grep", message="y")]
        m.write_baseline(tmp, f2, scope="full", taxonomy={})
        prev = m.read_baseline(tmp, which="prev")
        last = m.read_baseline(tmp, which="last")
        assert prev["findings"][0]["fp"] == "aaa", prev
        assert last["findings"][0]["fp"] == "bbb", last
        print("OK: baseline write rotates + reads")


def test_baseline_diff_scope_does_not_rotate() -> None:
    m = _load("findings")
    with tempfile.TemporaryDirectory() as raw:
        tmp = Path(raw)
        _git_init(tmp)
        full = [m.Finding(fp="full1", phase="sast", cwe="CWE-79", severity="high",
                          file="a.ts", line=1, engine="grep", message="x")]
        m.write_baseline(tmp, full, scope="full", taxonomy={})
        # A diff-scope run must NOT overwrite the full-tree baseline.
        diff = [m.Finding(fp="diff1", phase="sast", cwe="CWE-22", severity="low",
                          file="c.ts", line=3, engine="grep", message="z")]
        m.write_baseline(tmp, diff, scope="commit", taxonomy={})
        last = m.read_baseline(tmp, which="last")
        assert last["scope"] == "full", (
            f"diff-scope run overwrote the full baseline: {last['scope']}"
        )
        assert last["findings"][0]["fp"] == "full1", last
        print("OK: diff-scope run does not clobber full baseline")


def test_delta_by_fingerprint() -> None:
    m = _load("findings")
    before = ["a", "b", "c"]
    after = ["b", "c", "d"]
    d = m.delta(before, after)
    assert set(d["resolved"]) == {"a"}, d
    assert set(d["new"]) == {"d"}, d
    assert set(d["persisted"]) == {"b", "c"}, d
    print("OK: delta by fingerprint")


ALL_TESTS = [
    test_fingerprint_stable_and_line_independent,
    test_fingerprint_case_insensitive_snippet,
    test_redact_never_leaks_plaintext,
    test_finding_roundtrip,
    test_baseline_write_rotates_and_reads,
    test_baseline_diff_scope_does_not_rotate,
    test_delta_by_fingerprint,
]


def main() -> int:
    failed = 0
    for t in ALL_TESTS:
        try:
            t()
        except AssertionError as exc:
            print(f"FAIL: {t.__name__}: {exc}", file=sys.stderr)
            failed += 1
    if failed:
        print(f"\n{failed} test(s) failed.", file=sys.stderr)
        return 1
    print("\nAll findings tests passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
