"""Tests for STUB_NOTE_RE in tools/consistency-check.py.

N-19 pairs a backlog row that documents an unfinished implementation
with a FIXME(stub) marker in the source tree. The row is recognised by
its wording, so the wording test has to separate an unfinished
implementation from a test double that merely shares the word.

Runs without pytest (assertion-based) but is also discoverable by
pytest. Invoke directly:

    python3 tools/tests/test_stub_notes.py
"""
from __future__ import annotations
import importlib.util
import sys
from pathlib import Path


TOOLS_DIR = Path(__file__).resolve().parents[1]
SCRIPT = TOOLS_DIR / "consistency-check.py"


def _load_module():
    spec = importlib.util.spec_from_file_location("cc_module", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules["cc_module"] = mod
    spec.loader.exec_module(mod)
    return mod


SHOULD_MATCH = [
    "| FIX-01-01-01 | Fix | Wiring offen, Tool ist noch nicht verkabelt |",
    "| FIX-01-01-02 | Fix | deferred-stub bis EPIC-09 |",
    "| FIX-01-01-03 | Fix | Die Implementierung ist ein stub |",
    "| FIX-01-01-04 | Fix | Zwei stubs warten auf das Gate |",
    "| FIX-01-01-05 | Fix | STUB: kommt in Welle 2 |",
]

SHOULD_NOT_MATCH = [
    # test doubles: finished code that shares the word
    "| FIX-44-14 | Fix | Regressionstest plus Modal-Stub in tests/stubs/obsidian.ts |",
    "| FIX-44-15 | Fix | createEl-Shim in tests/stubs/createElGlobal.ts |",
    "| FIX-44-16 | Fix | Der stub-loader wurde ersetzt |",
    # unrelated rows
    "| FIX-44-17 | Fix | Approval-Gate settled das Promise nicht |",
]


def test_stub_note_wording() -> None:
    mod = _load_module()
    failures = []
    for line in SHOULD_MATCH:
        if not mod.STUB_NOTE_RE.search(line):
            failures.append(f"  should match but did not: {line}")
    for line in SHOULD_NOT_MATCH:
        if mod.STUB_NOTE_RE.search(line):
            failures.append(f"  should NOT match but did: {line}")
    assert not failures, "STUB_NOTE_RE mismatches:\n" + "\n".join(failures)
    print("OK: stub wording separates unfinished work from test doubles.")


if __name__ == "__main__":
    try:
        test_stub_note_wording()
    except AssertionError as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        sys.exit(1)
    sys.exit(0)
