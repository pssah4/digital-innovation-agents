"""Tests for security-audit/tools/lib/supply_chain.py (stage 1, static).

Assertion-based, runnable without pytest but pytest-discoverable. Offline,
tempdir fixtures only, stdlib-only.

    python3 skills/security-audit/tools/tests/test_supply_chain.py

Covers the static supply-chain checks:
  * lockfile provenance (registry host, integrity, git/http deps)
  * install-script inventory as delta-able info findings
  * GitHub Action pinning + permissions + persist-credentials
  * npm install vs npm ci and unpinned pip installs in workflows
  * manifest hygiene (.npmrc policy, stale overrides)
  * python requirement pinning
  * fingerprint stability and honest not-applicable ledger entries
"""
from __future__ import annotations
import importlib.util
import json
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


def _write_lockfile(root: Path, packages: dict) -> None:
    (root / "package-lock.json").write_text(json.dumps({
        "name": "fixture", "lockfileVersion": 3,
        "packages": {"": {"name": "fixture"}, **packages},
    }, indent=2), encoding="utf-8")


def _write_workflow(root: Path, name: str, text: str) -> Path:
    wf_dir = root / ".github" / "workflows"
    wf_dir.mkdir(parents=True, exist_ok=True)
    path = wf_dir / name
    path.write_text(text, encoding="utf-8")
    return path


GOOD_PKG = {
    "version": "1.0.0",
    "resolved": "https://registry.npmjs.org/good/-/good-1.0.0.tgz",
    "integrity": "sha512-deadbeef",
}


def test_lockfile_git_dependency_is_high() -> None:
    m = _load("supply_chain")
    with tempfile.TemporaryDirectory() as raw:
        root = Path(raw)
        _write_lockfile(root, {
            "node_modules/good": dict(GOOD_PKG),
            "node_modules/evil": {
                "version": "0.0.1",
                "resolved": "git+ssh://git@github.com/x/evil.git#abc123",
            },
        })
        findings, tool = m.check_lockfile_provenance(root)
    assert tool["status"] == "ran", tool
    git_hits = [f for f in findings if "evil" in f.message and f.severity == "high"]
    assert len(git_hits) == 1, findings
    assert git_hits[0].cwe == "CWE-829", git_hits[0]
    assert all("good" not in f.message for f in findings), findings
    print("OK: git+ssh dependency -> single high CWE-829 finding")


def test_lockfile_http_and_foreign_host() -> None:
    m = _load("supply_chain")
    with tempfile.TemporaryDirectory() as raw:
        root = Path(raw)
        _write_lockfile(root, {
            "node_modules/good": dict(GOOD_PKG),
            "node_modules/plain": {
                "version": "1.0.0",
                "resolved": "http://evil.example/plain-1.0.0.tgz",
                "integrity": "sha512-x",
            },
            "node_modules/mirror": {
                "version": "1.0.0",
                "resolved": "https://npm.corp.example/mirror-1.0.0.tgz",
                "integrity": "sha512-y",
            },
        })
        findings, _tool = m.check_lockfile_provenance(root)
    assert any("plain" in f.message and f.severity == "high" for f in findings), findings
    assert any("mirror" in f.message and f.severity == "medium" for f in findings), findings
    assert not any("good" in f.message for f in findings), findings
    print("OK: http resolved -> high; foreign https host -> medium; registry clean")


def test_lockfile_missing_integrity() -> None:
    m = _load("supply_chain")
    with tempfile.TemporaryDirectory() as raw:
        root = Path(raw)
        _write_lockfile(root, {
            "node_modules/good": dict(GOOD_PKG),
            "node_modules/nointegrity": {
                "version": "2.0.0",
                "resolved": "https://registry.npmjs.org/nointegrity/-/nointegrity-2.0.0.tgz",
            },
        })
        findings, _tool = m.check_lockfile_provenance(root)
    hits = [f for f in findings if "nointegrity" in f.message]
    assert len(hits) == 1, findings
    assert hits[0].severity == "medium", hits[0]
    assert hits[0].cwe == "CWE-494", hits[0]
    print("OK: missing integrity -> medium CWE-494; sha512 entry clean")


def test_install_script_inventory_is_info_and_sorted() -> None:
    m = _load("supply_chain")
    with tempfile.TemporaryDirectory() as raw:
        root = Path(raw)
        _write_lockfile(root, {
            "node_modules/zeta": {**GOOD_PKG, "hasInstallScript": True},
            "node_modules/alpha": {**GOOD_PKG, "hasInstallScript": True},
            "node_modules/good": dict(GOOD_PKG),
        })
        findings, tool = m.check_install_scripts(root)
    assert tool["status"] == "ran", tool
    assert [f.severity for f in findings] == ["info", "info"], findings
    names = [f.message for f in findings]
    assert names == sorted(names), "inventory must be deterministically sorted"
    assert all(f.cwe == "CWE-829" for f in findings), findings
    print("OK: install-script inventory -> sorted info findings")


def test_action_pinning_tag_vs_sha_and_write_permissions() -> None:
    m = _load("supply_chain")
    sha = "a" * 40
    with tempfile.TemporaryDirectory() as raw:
        root = Path(raw)
        _write_workflow(root, "writer.yml", (
            "name: writer\n"
            "permissions:\n  contents: write\n"
            "jobs:\n  j:\n    runs-on: ubuntu-latest\n    steps:\n"
            "      - uses: actions/checkout@v4\n"
        ))
        _write_workflow(root, "reader.yml", (
            "name: reader\n"
            "permissions:\n  contents: read\n"
            "jobs:\n  j:\n    runs-on: ubuntu-latest\n    steps:\n"
            "      - uses: actions/checkout@v4\n"
        ))
        _write_workflow(root, "pinned.yml", (
            "name: pinned\n"
            "permissions:\n  contents: read\n"
            "jobs:\n  j:\n    runs-on: ubuntu-latest\n    steps:\n"
            f"      - uses: actions/checkout@{sha}  # v4\n"
        ))
        findings, tool = m.check_action_pinning(root)
    assert tool["status"] == "ran", tool
    unpinned = [f for f in findings if "actions/checkout@v4" in f.message]
    by_file = {f.file: f for f in unpinned}
    assert by_file[".github/workflows/writer.yml"].severity == "high", by_file
    assert by_file[".github/workflows/reader.yml"].severity == "medium", by_file
    assert ".github/workflows/pinned.yml" not in by_file, by_file
    print("OK: unpinned action -> high with write perms, medium without, SHA clean")


def test_missing_permissions_block() -> None:
    m = _load("supply_chain")
    with tempfile.TemporaryDirectory() as raw:
        root = Path(raw)
        _write_workflow(root, "noperm.yml", (
            "name: noperm\n"
            "jobs:\n  j:\n    runs-on: ubuntu-latest\n    steps:\n"
            "      - run: echo hi\n"
        ))
        _write_workflow(root, "hasperm.yml", (
            "name: hasperm\npermissions:\n  contents: read\n"
            "jobs:\n  j:\n    runs-on: ubuntu-latest\n    steps:\n"
            "      - run: echo hi\n"
        ))
        findings, _tool = m.check_action_pinning(root)
    noperm = [f for f in findings if f.cwe == "CWE-250"]
    assert len(noperm) == 1, findings
    assert noperm[0].file == ".github/workflows/noperm.yml", noperm[0]
    assert noperm[0].severity == "medium", noperm[0]
    print("OK: missing permissions block -> one medium CWE-250 finding")


def test_persist_credentials_hint_on_write_workflows() -> None:
    m = _load("supply_chain")
    with tempfile.TemporaryDirectory() as raw:
        root = Path(raw)
        _write_workflow(root, "writer.yml", (
            "name: writer\npermissions:\n  contents: write\n"
            "jobs:\n  j:\n    runs-on: ubuntu-latest\n    steps:\n"
            "      - uses: actions/checkout@" + "b" * 40 + "\n"
        ))
        _write_workflow(root, "safe.yml", (
            "name: safe\npermissions:\n  contents: write\n"
            "jobs:\n  j:\n    runs-on: ubuntu-latest\n    steps:\n"
            "      - uses: actions/checkout@" + "c" * 40 + "\n"
            "        with:\n          persist-credentials: false\n"
        ))
        findings, _tool = m.check_action_pinning(root)
    hints = [f for f in findings if f.cwe == "CWE-522"]
    assert len(hints) == 1, findings
    assert hints[0].file == ".github/workflows/writer.yml", hints[0]
    assert hints[0].severity == "low", hints[0]
    print("OK: checkout without persist-credentials:false on write workflow -> low")


def test_npm_install_and_unpinned_pip_in_workflows() -> None:
    m = _load("supply_chain")
    with tempfile.TemporaryDirectory() as raw:
        root = Path(raw)
        _write_lockfile(root, {"node_modules/good": dict(GOOD_PKG)})
        _write_workflow(root, "build.yml", (
            "name: build\npermissions:\n  contents: read\n"
            "jobs:\n  j:\n    runs-on: ubuntu-latest\n    steps:\n"
            "      - run: npm install\n"
            "      - run: pip install --quiet anthropic\n"
        ))
        _write_workflow(root, "clean.yml", (
            "name: clean\npermissions:\n  contents: read\n"
            "jobs:\n  j:\n    runs-on: ubuntu-latest\n    steps:\n"
            "      - run: npm ci\n"
            "      - run: pip install anthropic==1.2.3\n"
            "      - run: pip install -r requirements.txt\n"
        ))
        findings, _tool = m.check_action_pinning(root)
    npm_hits = [f for f in findings if "npm install" in f.message]
    assert len(npm_hits) == 1 and npm_hits[0].file.endswith("build.yml"), findings
    assert npm_hits[0].severity == "low", npm_hits[0]
    pip_hits = [f for f in findings if "pip install" in f.message]
    assert len(pip_hits) == 1 and pip_hits[0].file.endswith("build.yml"), findings
    assert pip_hits[0].severity == "medium", pip_hits[0]
    print("OK: npm install despite lockfile -> low; unpinned pip -> medium; clean file clean")


def test_python_requirements_pinning() -> None:
    m = _load("supply_chain")
    with tempfile.TemporaryDirectory() as raw:
        root = Path(raw)
        (root / "requirements.txt").write_text(
            "# comment\nrequests==2.31.0\nflask\n-e ./local\n", encoding="utf-8")
        findings, tool = m.check_python_pins(root)
    assert tool["status"] == "ran", tool
    assert len(findings) == 1, findings
    assert "flask" in findings[0].message, findings[0]
    assert findings[0].severity == "low", findings[0]
    print("OK: unpinned requirement -> low; pinned + editable skipped")


def test_manifest_hygiene_npmrc_and_stale_override() -> None:
    m = _load("supply_chain")
    with tempfile.TemporaryDirectory() as raw:
        root = Path(raw)
        _write_lockfile(root, {
            "node_modules/scripted": {**GOOD_PKG, "hasInstallScript": True},
        })
        (root / "package.json").write_text(json.dumps({
            "name": "fixture",
            "overrides": {"ghost-package": "^1.0.0", "scripted": "^2.0.0"},
        }), encoding="utf-8")
        findings, tool = m.check_manifest_hygiene(root)
    assert tool["status"] == "ran", tool
    npmrc_hits = [f for f in findings if "ignore-scripts" in f.message]
    assert len(npmrc_hits) == 1 and npmrc_hits[0].severity == "info", findings
    stale = [f for f in findings if "ghost-package" in f.message]
    assert len(stale) == 1 and stale[0].severity == "low", findings
    assert not any("scripted" in f.message and "override" in f.message.lower()
                   for f in findings), findings
    print("OK: no ignore-scripts policy -> info; stale override -> low")


def test_manifest_hygiene_quiet_with_npmrc() -> None:
    m = _load("supply_chain")
    with tempfile.TemporaryDirectory() as raw:
        root = Path(raw)
        _write_lockfile(root, {
            "node_modules/scripted": {**GOOD_PKG, "hasInstallScript": True},
        })
        (root / ".npmrc").write_text("ignore-scripts=true\n", encoding="utf-8")
        findings, _tool = m.check_manifest_hygiene(root)
    assert not any("ignore-scripts" in f.message for f in findings), findings
    print("OK: ignore-scripts=true silences the .npmrc policy hint")


def test_fingerprints_stable_across_reformat() -> None:
    m = _load("supply_chain")
    with tempfile.TemporaryDirectory() as raw:
        root = Path(raw)
        pkgs = {"node_modules/evil": {
            "version": "0.0.1",
            "resolved": "git+https://github.com/x/evil.git",
        }}
        _write_lockfile(root, pkgs)
        first, _ = m.check_lockfile_provenance(root)
        # Rewrite the lockfile with different formatting (indent 4).
        (root / "package-lock.json").write_text(json.dumps({
            "name": "fixture", "lockfileVersion": 3,
            "packages": {"": {"name": "fixture"}, **pkgs},
        }, indent=4), encoding="utf-8")
        second, _ = m.check_lockfile_provenance(root)
    assert [f.fp for f in first] == [f.fp for f in second], (first, second)
    assert all(len(f.fp) == 8 for f in first), first
    print("OK: fingerprints stable across lockfile reformat")


def test_not_applicable_ledger_without_manifests() -> None:
    m = _load("supply_chain")
    with tempfile.TemporaryDirectory() as raw:
        root = Path(raw)
        findings, tools = m.run_supply_chain_static(root)
    assert findings == [], findings
    statuses = {t["name"]: t["status"] for t in tools}
    assert statuses.get("lockfile-provenance") == "not-applicable", tools
    assert statuses.get("action-pinning") == "not-applicable", tools
    assert statuses.get("python-pins") == "not-applicable", tools
    assert all("reason" in t for t in tools if t["status"] == "not-applicable"), tools
    print("OK: empty project -> honest not-applicable ledger, no crash")


def test_registry_allowlist_from_config() -> None:
    m = _load("supply_chain")
    with tempfile.TemporaryDirectory() as raw:
        root = Path(raw)
        _write_lockfile(root, {
            "node_modules/mirror": {
                "version": "1.0.0",
                "resolved": "https://npm.corp.example/mirror-1.0.0.tgz",
                "integrity": "sha512-y",
            },
        })
        strict, _ = m.check_lockfile_provenance(root)
        relaxed, _ = m.check_lockfile_provenance(
            root, registry_hosts=["registry.npmjs.org", "npm.corp.example"])
    assert any("mirror" in f.message for f in strict), strict
    assert not any("mirror" in f.message for f in relaxed), relaxed
    print("OK: config allowlist suppresses private-registry host finding")


def test_run_supply_chain_static_merges_and_phases() -> None:
    m = _load("supply_chain")
    with tempfile.TemporaryDirectory() as raw:
        root = Path(raw)
        _write_lockfile(root, {
            "node_modules/evil": {"version": "1", "resolved": "git+https://g/x.git"},
        })
        _write_workflow(root, "w.yml", (
            "name: w\njobs:\n  j:\n    runs-on: ubuntu-latest\n    steps:\n"
            "      - uses: actions/checkout@v4\n"
        ))
        findings, tools = m.run_supply_chain_static(root)
    assert findings, "expected findings from lockfile + workflow fixtures"
    assert all(f.phase == "supply-chain" for f in findings), findings
    assert all(f.engine == "supply-chain" for f in findings), findings
    names = {t["name"] for t in tools}
    assert {"lockfile-provenance", "install-scripts", "action-pinning",
            "manifest-hygiene", "python-pins"} <= names, tools
    fps = [f.fp for f in findings]
    assert len(fps) == len(set(fps)), "fingerprints must be unique"
    print("OK: static runner merges checks, phase/engine tagged, fps unique")


ALL_TESTS = [
    test_lockfile_git_dependency_is_high,
    test_lockfile_http_and_foreign_host,
    test_lockfile_missing_integrity,
    test_install_script_inventory_is_info_and_sorted,
    test_action_pinning_tag_vs_sha_and_write_permissions,
    test_missing_permissions_block,
    test_persist_credentials_hint_on_write_workflows,
    test_npm_install_and_unpinned_pip_in_workflows,
    test_python_requirements_pinning,
    test_manifest_hygiene_npmrc_and_stale_override,
    test_manifest_hygiene_quiet_with_npmrc,
    test_fingerprints_stable_across_reformat,
    test_not_applicable_ledger_without_manifests,
    test_registry_allowlist_from_config,
    test_run_supply_chain_static_merges_and_phases,
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
    print("\nAll supply_chain tests passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
