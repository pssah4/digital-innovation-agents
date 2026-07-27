"""Tests for security-audit/tools/lib/skip_rules.py.

Assertion-based, runnable without pytest.

    python3 skills/security-audit/tools/tests/test_skip_rules.py

Verifies that pattern-based scanners (grep-fallback, secret patterns)
correctly skip:
  * test fixtures under tests/, test_*.py, *_test.py, *.test.ts, *.spec.js
  * minified/bundled assets (*.min.js, *.bundle.js)
  * build outputs (dist/, build/, coverage/, vendor/, node_modules/)
  * any file whose first ~50 lines carry `security-audit-scan: skip`
And that normal source files are still scanned.
"""
from __future__ import annotations
import importlib.util
import sys
import tempfile
from pathlib import Path


LIB_DIR = Path(__file__).resolve().parents[1] / "lib"


def _load(module_name: str):
    if str(LIB_DIR) not in sys.path:
        sys.path.insert(0, str(LIB_DIR))
    path = LIB_DIR / f"{module_name}.py"
    spec = importlib.util.spec_from_file_location(f"sa_{module_name}", path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[f"sa_{module_name}"] = mod
    spec.loader.exec_module(mod)
    return mod


def test_test_files_are_skipped() -> None:
    m = _load("skip_rules")
    for rel in [
        "tests/test_findings.py",
        "src/foo/tests/test_x.py",
        "src/test_utils.py",
        "src/utils_test.py",
        "packages/a/__tests__/foo.ts",
        "src/components/Button.test.ts",
        "src/components/Button.spec.js",
    ]:
        assert m.is_path_skipped(rel), f"expected skip: {rel}"
    print("OK: test files across common conventions are skipped")


def test_minified_and_build_outputs_are_skipped() -> None:
    m = _load("skip_rules")
    for rel in [
        "vendor/cytoscape.min.js",
        "public/app.bundle.js",
        "dist/index.js",
        "build/static/main.js",
        "coverage/lcov.info",
        "node_modules/foo/index.js",
    ]:
        assert m.is_path_skipped(rel), f"expected skip: {rel}"
    print("OK: minified + build outputs are skipped")


def test_normal_source_files_are_not_skipped() -> None:
    m = _load("skip_rules")
    for rel in [
        "src/index.ts",
        "app/main.py",
        "lib/helpers.js",
        "server/routes/user.ts",
    ]:
        assert not m.is_path_skipped(rel), f"expected scan: {rel}"
    print("OK: normal source files are scanned")


def test_header_marker_opts_out_arbitrary_file() -> None:
    m = _load("skip_rules")
    with tempfile.TemporaryDirectory() as raw:
        root = Path(raw)
        good = root / "src" / "clean.py"
        good.parent.mkdir(parents=True)
        good.write_text('"""Clean module."""\ndef f(): pass\n', encoding="utf-8")

        marked = root / "src" / "detector.py"
        marked.write_text(
            '"""Detector module."""\n'
            "# security-audit-scan: skip -- stores regex patterns as data\n"
            "PATTERNS = [r'eval\\(']\n",
            encoding="utf-8",
        )

        assert not m.has_skip_header(good), "clean file must not carry marker"
        assert m.has_skip_header(marked), "marked file must be recognized"
        # should_scan combines both mechanisms.
        assert m.should_scan("src/clean.py", root) is True
        assert m.should_scan("src/detector.py", root) is False
    print("OK: security-audit-scan header marker opts a file out")


def test_header_marker_bounded_read() -> None:
    """Marker beyond the header window must NOT skip the file."""
    m = _load("skip_rules")
    with tempfile.TemporaryDirectory() as raw:
        root = Path(raw)
        deep = root / "deep.py"
        # 100 blank lines, then the marker at line 100+
        body = "\n" * 100 + "# security-audit-scan: skip\n"
        deep.write_text(body, encoding="utf-8")
        assert not m.has_skip_header(deep), \
            "marker past the 50-line window must not trigger skip"
    print("OK: header marker read is bounded")


def test_should_scan_missing_file_defaults_scan() -> None:
    """A file that fails to read (missing, permission) still gets scanned
    by the caller; the header check just returns False (no marker)."""
    m = _load("skip_rules")
    with tempfile.TemporaryDirectory() as raw:
        root = Path(raw)
        # File does not exist -> has_skip_header returns False (no crash),
        # is_path_skipped only depends on the string, so should_scan True.
        assert m.should_scan("src/does_not_exist.py", root) is True
    print("OK: missing file does not crash should_scan")


ALL_TESTS = [
    test_test_files_are_skipped,
    test_minified_and_build_outputs_are_skipped,
    test_normal_source_files_are_not_skipped,
    test_header_marker_opts_out_arbitrary_file,
    test_header_marker_bounded_read,
    test_should_scan_missing_file_defaults_scan,
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
    print("\nAll skip_rules tests passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
