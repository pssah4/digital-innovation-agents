"""Tests for security-audit/tools/lib/cleanroom.py (stages 2 + 3).

Assertion-based, runnable without pytest but pytest-discoverable. Offline:
every subprocess touchpoint is patched; no git clone, no npm, no gh runs.

    python3 skills/security-audit/tools/tests/test_cleanroom.py

Covers:
  * env scrubbing is an allowlist (kills PLUGIN_DIR-style deploy hooks)
  * hash comparison maps mismatch -> high CWE-494, match -> info
  * a failing rebuild degrades to an error ledger entry, never raises
  * tracked-artifact detection heuristics
  * repo-slug parsing for ssh and https remotes
  * gh absent -> release verify degrades to unavailable
  * attestation verify exit codes -> finding severity
  * [audit.supply_chain] config parsing incl. CLI override precedence
"""
from __future__ import annotations
import importlib.util
import subprocess
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch

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


def _cp(returncode: int = 0, stdout: str = "", stderr: str = "") -> subprocess.CompletedProcess:
    return subprocess.CompletedProcess(args=[], returncode=returncode,
                                       stdout=stdout, stderr=stderr)


def test_scrubbed_env_is_allowlist() -> None:
    m = _load("cleanroom")
    base = {
        "PATH": "/usr/bin", "HOME": "/Users/x", "LANG": "de_DE.UTF-8",
        "PLUGIN_DIR": "/Users/x/icloud/plugin",
        "npm_config_registry": "https://evil.example",
        "AWS_SECRET_ACCESS_KEY": "shh", "CI": "true", "TMPDIR": "/tmp/t",
    }
    env = m._scrubbed_env(base)
    assert "PLUGIN_DIR" not in env, env
    assert "npm_config_registry" not in env, env
    assert "AWS_SECRET_ACCESS_KEY" not in env, env
    assert "CI" not in env, env
    assert env["PATH"] == "/usr/bin" and env["HOME"] == "/Users/x", env
    assert env["TMPDIR"] == "/tmp/t", env
    assert env["npm_config_ignore_scripts"] == "true", env
    print("OK: scrubbed env keeps only the allowlist and forces ignore-scripts")


def test_compare_artifact_hashes() -> None:
    m = _load("cleanroom")
    findings = m.compare_artifact_hashes(
        built={"main.js": "a" * 64, "styles.css": "b" * 64},
        committed={"main.js": "a" * 64, "styles.css": "c" * 64},
    )
    by_file = {f.file: f for f in findings}
    assert by_file["styles.css"].severity == "high", by_file
    assert by_file["styles.css"].cwe == "CWE-494", by_file
    assert "mismatch" in by_file["styles.css"].message.lower(), by_file
    assert by_file["main.js"].severity == "info", by_file
    assert "reproducible" in by_file["main.js"].message.lower(), by_file
    assert len(by_file["main.js"].fp) == 8, by_file
    print("OK: hash mismatch -> high CWE-494, match -> info reproducible")


def test_rebuild_build_failure_degrades_to_error() -> None:
    m = _load("cleanroom")
    with tempfile.TemporaryDirectory() as raw:
        root = Path(raw)
        calls = []

        def fake_run(cmd, **kwargs):
            calls.append(cmd)
            if cmd[:2] == ["git", "clone"]:
                return _cp(0)
            return _cp(1, stderr="boom")

        with patch.object(m, "_run", side_effect=fake_run):
            findings, tool = m.run_cleanroom_rebuild(
                root,
                {"build_command": "npm run build", "artifacts": ["main.js"]},
                scratch_dir=root / "scratch",
            )
    assert findings == [], findings
    assert tool["name"] == "cleanroom-rebuild", tool
    assert tool["status"] == "error", tool
    assert "reason" in tool, tool
    print("OK: failing rebuild -> error ledger entry, no findings, no raise")


def test_rebuild_without_config_is_not_configured() -> None:
    m = _load("cleanroom")
    with tempfile.TemporaryDirectory() as raw:
        findings, tool = m.run_cleanroom_rebuild(Path(raw), {})
    assert findings == [], findings
    assert tool["status"] == "not-configured", tool
    print("OK: missing build_command/artifacts -> not-configured ledger entry")


def test_detect_tracked_artifacts() -> None:
    m = _load("cleanroom")
    tracked = [
        "src/index.ts", "dist/app.js", "build/out.css",
        "vendor/lib.min.js", "main.js", "esbuild.config.mjs",
        "docs/guide.md",
    ]
    hits = m.detect_tracked_artifacts(Path("/nonexistent"), tracked=tracked)
    assert "dist/app.js" in hits, hits
    assert "build/out.css" in hits, hits
    assert "vendor/lib.min.js" in hits, hits
    assert "main.js" in hits, hits  # bundler config present
    assert "src/index.ts" not in hits, hits
    assert "docs/guide.md" not in hits, hits
    print("OK: tracked-artifact heuristic finds dist/build/min/bundle outputs")


def test_repo_slug_parsing() -> None:
    m = _load("cleanroom")
    assert m._repo_slug("git@github.com:user/repo.git") == "user/repo"
    assert m._repo_slug("https://github.com/user/repo") == "user/repo"
    assert m._repo_slug("https://github.com/user/repo.git") == "user/repo"
    assert m._repo_slug("ssh://git@github.com/user/repo.git") == "user/repo"
    assert m._repo_slug("https://gitlab.example/user/repo") is None
    print("OK: repo slug parsed from ssh and https GitHub remotes")


def test_release_verify_without_gh_is_unavailable() -> None:
    m = _load("cleanroom")
    with patch.object(m.shutil, "which", return_value=None):
        findings, tools = m.run_release_verify(Path("/tmp"))
    assert findings == [], findings
    assert tools and tools[0]["name"] == "gh-attestation", tools
    assert tools[0]["status"] == "unavailable", tools
    print("OK: gh missing -> unavailable ledger entry, stage 3 no-op")


def test_verify_attestation_exit_codes() -> None:
    m = _load("cleanroom")
    asset = Path("/tmp/main.js")

    with patch.object(m, "_run", return_value=_cp(0, stdout="verified")):
        ok = m._verify_attestation(asset, "user/repo")
    assert ok.severity == "info", ok
    assert "main.js" in ok.file, ok

    with patch.object(m, "_run", return_value=_cp(1, stderr="attestation not found")):
        missing = m._verify_attestation(asset, "user/repo")
    assert missing.severity == "medium", missing

    with patch.object(m, "_run", return_value=_cp(1, stderr="verification failed: digest mismatch")):
        bad = m._verify_attestation(asset, "user/repo")
    assert bad.severity == "high", bad
    assert bad.cwe == "CWE-494", bad
    print("OK: attestation verify 0 -> info, missing -> medium, failure -> high")


def test_read_supply_chain_config_and_overrides() -> None:
    m = _load("cleanroom")
    with tempfile.TemporaryDirectory() as raw:
        root = Path(raw)
        (root / ".dia").mkdir()
        (root / ".dia" / "config.toml").write_text(
            'mode = "git-only"\n'
            "\n"
            "[audit.supply_chain]\n"
            'build_command = "npm run build"\n'
            'artifacts = ["main.js", "styles.css"]\n'
            'registry_hosts = ["registry.npmjs.org", "npm.corp.example"]\n',
            encoding="utf-8",
        )
        cfg = m.read_supply_chain_config(root)
        assert cfg["build_command"] == "npm run build", cfg
        assert cfg["artifacts"] == ["main.js", "styles.css"], cfg
        assert "npm.corp.example" in cfg["registry_hosts"], cfg

        cfg2 = m.read_supply_chain_config(
            root, cli_overrides={"build_command": "make dist", "artifacts": ["dist/a.js"]})
        assert cfg2["build_command"] == "make dist", cfg2
        assert cfg2["artifacts"] == ["dist/a.js"], cfg2
        assert "npm.corp.example" in cfg2["registry_hosts"], cfg2

    cfg3 = m.read_supply_chain_config(Path("/nonexistent-project-root"))
    assert cfg3["build_command"] is None, cfg3
    assert cfg3["artifacts"] == [], cfg3
    assert cfg3["registry_hosts"] == ["registry.npmjs.org"], cfg3
    print("OK: config.toml parsed, CLI overrides win, sane defaults without file")


ALL_TESTS = [
    test_scrubbed_env_is_allowlist,
    test_compare_artifact_hashes,
    test_rebuild_build_failure_degrades_to_error,
    test_rebuild_without_config_is_not_configured,
    test_detect_tracked_artifacts,
    test_repo_slug_parsing,
    test_release_verify_without_gh_is_unavailable,
    test_verify_attestation_exit_codes,
    test_read_supply_chain_config_and_overrides,
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
    print("\nAll cleanroom tests passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
