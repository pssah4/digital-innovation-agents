"""Tests for artifact id parsing in tools/consistency-check.py.

Covers both id depths a project may use:

    epic-direct     FIX-44-12, IMP-54-03      fix hangs off the epic
    feature-scoped  FIX-19-01-01, IMP-19-31-04  fix hangs off a feature

and the matching feature depths (FEAT-44-01, FEAT-19-02-01). The deeper
form must win when both could match, otherwise FIX-19-01-01 would parse
as FIX-19-01 and collide with a real epic-direct id.

Runs without pytest (assertion-based) but is also discoverable by
pytest. No third-party deps. Invoke directly:

    python3 tools/tests/test_id_patterns.py
"""
from __future__ import annotations
import importlib.util
import sys
import tempfile
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


CASES = [
    # feature-scoped ids: the deeper form must win
    ("FIX-19-01-01-missing-tools-in-builtin-modes.md", "FIX-19-01-01"),
    ("IMP-19-31-04-ingest-skill-suite.md", "IMP-19-31-04"),
    ("FEAT-19-02-01-alle-befunde-abwaehlen.md", "FEAT-19-02-01"),
    # epic-direct ids
    ("FIX-44-12-checkpoint-marker-persistence.md", "FIX-44-12"),
    ("FIX-28-04-audit-034-followup.md", "FIX-28-04"),
    ("IMP-54-03-sticky-chat-model.md", "IMP-54-03"),
    ("FEAT-44-01-effekt-basiertes-approval-gate.md", "FEAT-44-01"),
    # three-digit epics stay supported at both depths
    ("FIX-100-02-something.md", "FIX-100-02"),
    ("FIX-100-02-03-something.md", "FIX-100-02-03"),
    # unchanged types
    ("EPIC-44-approval-governance.md", "EPIC-44"),
    ("ADR-153-approval-gate.md", "ADR-153"),
    ("PLAN-07-retrieval-wave.md", "PLAN-07"),
    # letter-suffixed ids stay unparsed on purpose: BACKLOG_ROW_RE does
    # not recognise them either, so both sides agree and neither an
    # orphan nor a missing-row finding is produced
    ("FEAT-44-02a-session-scope.md", None),
    # non-artifacts
    ("README.md", None),
    ("arc42.md", None),
]


def test_parse_artifact_id() -> None:
    mod = _load_module()
    failures = []
    for name, expected in CASES:
        got = mod.parse_artifact_id(Path(name))
        if got != expected:
            failures.append(f"  {name}: expected {expected!r}, got {got!r}")
    assert not failures, "parse_artifact_id mismatches:\n" + "\n".join(failures)
    print("OK: parse_artifact_id handles both id depths.")


def test_epic_direct_file_satisfies_backlog_row() -> None:
    """An epic-direct fix file must count as the artifact for its
    backlog row, so the row is not reported as an orphan.
    """
    mod = _load_module()
    with tempfile.TemporaryDirectory() as raw:
        tmp = Path(raw)
        fixes = tmp / "_devprocess" / "requirements" / "fixes"
        fixes.mkdir(parents=True)
        context = tmp / "_devprocess" / "context"
        context.mkdir(parents=True)

        (fixes / "FIX-44-12-checkpoint-marker-persistence.md").write_text(
            "---\nid: FIX-44-12\nepic: EPIC-44\n---\n\n# FIX-44-12\n",
            encoding="utf-8",
        )
        (context / "BACKLOG.md").write_text(
            "| ID | Type | Title | Status |\n"
            "|---|---|---|---|\n"
            "| FIX-44-12 | Fix | Checkpoint marker persistence | Done |\n",
            encoding="utf-8",
        )

        mod.ROOT = tmp
        mod.BACKLOG = context / "BACKLOG.md"
        mod.FIXES = fixes
        mod.FEATURES = tmp / "_devprocess" / "requirements" / "features"
        mod.EPICS = tmp / "_devprocess" / "requirements" / "epics"
        mod.IMPROVEMENTS = tmp / "_devprocess" / "requirements" / "improvements"
        mod.ARCHITECTURE = tmp / "_devprocess" / "architecture"
        mod.PLANS = tmp / "_devprocess" / "implementation" / "plans"

        findings = mod.check_backlog_completeness()
        types = [(f.type, f.message) for f in findings]
        assert not types, f"expected no findings, got {types}"
    print("OK: epic-direct file resolves its backlog row.")


if __name__ == "__main__":
    failed = False
    for fn in (test_parse_artifact_id, test_epic_direct_file_satisfies_backlog_row):
        try:
            fn()
        except AssertionError as exc:
            print(f"FAIL: {fn.__name__}\n{exc}", file=sys.stderr)
            failed = True
    sys.exit(1 if failed else 0)
