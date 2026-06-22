"""Smoke tests for N-20 (artefact-cap-exceeded) and N-21
(forbidden-section-resurfaced) in tools/consistency-check.py.

Runs without pytest (assertion-based) but is also discoverable by
pytest. No third-party deps. Invoke directly:

    python3 tools/tests/test_artifact_caps.py
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


def _make_synthetic_breach(tmp: Path) -> Path:
    """Build a FIX-EE-FF-NN file that violates both N-20 (over cap) and
    N-21 (forbidden frontmatter key, '## Status', '## Next Steps',
    'Backlog row pointer').
    """
    p = tmp / "FIX-01-01-01-synthetic.md"
    body_lines = ["filler"] * 60  # FIX cap = 28; 60 > 28 * 1.1
    content = (
        "---\n"
        "id: FIX-01-01-01\n"
        "feature: FEAT-01-01\n"
        "epic: EPIC-01\n"
        "status: In Progress\n"      # N-21 forbidden key
        "last_updated: 2026-06-22\n"  # N-21 forbidden key
        "---\n"
        "\n"
        "# FIX-01-01-01\n"
        "\n"
        "## Status\n"                 # N-21 forbidden section
        "\n"
        "In Progress.\n"
        "\n"
        "> Backlog row pointer: see BACKLOG.md\n"  # N-21 forbidden block
        "\n"
        "## Next Steps\n"             # N-21 forbidden in FIX
        "\n"
        "- do the thing\n"
        "\n"
        + "\n".join(body_lines)
        + "\n"
    )
    p.write_text(content, encoding="utf-8")
    return p


def _make_shrunk_template_copy(tmp: Path, src: Path) -> Path:
    """Copy a shrunk template into a synthetic feature filename so
    classify_artifact picks the right cap key.
    """
    dst = tmp / "FEAT-01-01-shrunk.md"
    dst.write_text(src.read_text(encoding="utf-8"), encoding="utf-8")
    return dst


def test_n20_n21() -> None:
    mod = _load_module()

    template = TOOLS_DIR.parent / "skills" / "requirements-engineering" / "templates" / "FEATURE-TEMPLATE.md"
    assert template.exists(), f"template not found: {template}"

    with tempfile.TemporaryDirectory() as raw:
        tmp = Path(raw)
        # Patch ROOT so Finding.file paths are relative.
        mod.ROOT = tmp

        clean = _make_shrunk_template_copy(tmp, template)
        breach = _make_synthetic_breach(tmp)

        cap_findings = mod.check_artifact_cap([clean, breach])
        sec_findings = mod.check_forbidden_sections([clean, breach])

        cap_files = {f.file for f in cap_findings}
        sec_files = {f.file for f in sec_findings}

        # Clean template is within FEATURE cap (65 + 10%).
        assert clean.name not in cap_files, (
            f"shrunk FEATURE template should not exceed cap; got {cap_findings}"
        )
        # Breach file is over the FIX cap.
        assert breach.name in cap_files, f"synthetic FIX should be over cap; got {cap_findings}"

        # Clean template carries no forbidden sections / keys.
        assert clean.name not in sec_files, (
            f"shrunk FEATURE template should be clean; got {sec_findings}"
        )

        # Breach must produce findings for each forbidden facet.
        breach_msgs = [f.message for f in sec_findings if f.file == breach.name]
        assert any("'## Status' section" in m for m in breach_msgs), breach_msgs
        assert any("Backlog row pointer" in m for m in breach_msgs), breach_msgs
        assert any("'## Next Steps' section" in m for m in breach_msgs), breach_msgs
        assert any("'status'" in m for m in breach_msgs), breach_msgs
        assert any("'last_updated'" in m for m in breach_msgs), breach_msgs

    print("OK: N-20 and N-21 smoke tests passed.")


if __name__ == "__main__":
    try:
        test_n20_n21()
    except AssertionError as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        sys.exit(1)
    sys.exit(0)
