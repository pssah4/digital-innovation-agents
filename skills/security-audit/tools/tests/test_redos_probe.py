"""Tests for security-audit/tools/poc/redos_probe.mjs.

Shells out to node. If node is unavailable, the test SKIPS (prints a
notice and passes) rather than failing -- the probe is opt-in and its
absence must never break the suite.

    python3 skills/security-audit/tools/tests/test_redos_probe.py
"""
from __future__ import annotations
import json
import shutil
import subprocess
import sys
from pathlib import Path


PROBE = Path(__file__).resolve().parents[1] / "poc" / "redos_probe.mjs"


def _node() -> str | None:
    return shutil.which("node")


def _run(args) -> dict:
    cp = subprocess.run(
        [_node(), str(PROBE), *args],
        text=True, capture_output=True, timeout=30,
    )
    return json.loads(cp.stdout.strip().splitlines()[-1])


def test_catastrophic_regex_hangs_and_is_terminated() -> None:
    node = _node()
    if not node:
        print("SKIP: node not available")
        return
    # (a+)+$ against 'a'*30 + '!' backtracks catastrophically; the probe
    # must hit the deadline and report hangs=true WITHOUT the test itself
    # hanging (worker.terminate enforces the deadline).
    out = _run(["--pattern", "(a+)+$", "--pump-len", "30",
                "--pump-suffix", "!", "--deadline-ms", "300"])
    assert out["hangs"] is True, out
    assert out["elapsed_ms"] >= 300 - 50, out  # roughly the deadline
    print("OK: catastrophic regex reported as hanging + terminated")


def test_benign_regex_does_not_hang() -> None:
    node = _node()
    if not node:
        print("SKIP: node not available")
        return
    out = _run(["--pattern", "^a+$", "--pump-len", "30",
                "--pump-suffix", "", "--deadline-ms", "300"])
    assert out["hangs"] is False, out
    assert out["elapsed_ms"] < 300, out
    print("OK: benign regex does not hang")


def test_invalid_regex_reports_error_not_crash() -> None:
    node = _node()
    if not node:
        print("SKIP: node not available")
        return
    out = _run(["--json", '{"pattern":"(","pumpLen":5}'])
    assert out["hangs"] is False, out
    assert out["error"], out
    print("OK: invalid regex reports error, no crash")


ALL_TESTS = [
    test_catastrophic_regex_hangs_and_is_terminated,
    test_benign_regex_does_not_hang,
    test_invalid_regex_reports_error_not_crash,
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
    print("\nAll redos_probe tests passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
