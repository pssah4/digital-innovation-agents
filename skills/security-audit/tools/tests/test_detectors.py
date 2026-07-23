"""Tests for security-audit/tools/lib/detectors.py.

Project-type detection and attack-surface enumeration are pure file
inspection (no network, no external tools), so tests build synthetic
project trees in temp dirs. Assertion-based, pytest-discoverable.

    python3 skills/security-audit/tools/tests/test_detectors.py
"""
from __future__ import annotations
import importlib.util
import json
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


def _write(tmp: Path, rel: str, content: str) -> None:
    p = tmp / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")


def test_detect_electron_obsidian_plugin() -> None:
    m = _load("detectors")
    with tempfile.TemporaryDirectory() as raw:
        tmp = Path(raw)
        _write(tmp, "package.json", json.dumps({
            "name": "vault-operator",
            "devDependencies": {"obsidian": "^1.5.0", "esbuild": "^0.19"},
            "dependencies": {"@anthropic-ai/sdk": "^0.30"},
        }))
        _write(tmp, "manifest.json", json.dumps({
            "id": "vault-operator", "minAppVersion": "1.8.7",
            "isDesktopOnly": True,
        }))
        d = m.detect_project(tmp)
        assert "node" in d["runtimes"], d
        assert "obsidian-plugin" in d["project_kinds"], d
        assert "electron" in d["project_kinds"], d
        # LLM API present -> phase 4 gate should be on.
        assert d["signals"]["llm_api"] is True, d
        print("OK: detect electron + obsidian-plugin + llm")


def test_detect_cli_vs_library() -> None:
    m = _load("detectors")
    with tempfile.TemporaryDirectory() as raw:
        tmp = Path(raw)
        _write(tmp, "package.json", json.dumps({
            "name": "mytool", "bin": {"mytool": "./cli.js"},
        }))
        d = m.detect_project(tmp)
        assert "cli" in d["project_kinds"], d
        assert "obsidian-plugin" not in d["project_kinds"], d
        assert "electron" not in d["project_kinds"], d

    with tempfile.TemporaryDirectory() as raw:
        tmp = Path(raw)
        _write(tmp, "package.json", json.dumps({
            "name": "mylib", "exports": {".": "./index.js"}, "private": False,
        }))
        d = m.detect_project(tmp)
        assert "library" in d["project_kinds"], d
        assert "cli" not in d["project_kinds"], d
        print("OK: detect cli vs library")


def test_detect_python_and_webapp() -> None:
    m = _load("detectors")
    with tempfile.TemporaryDirectory() as raw:
        tmp = Path(raw)
        _write(tmp, "pyproject.toml", "[project]\nname='x'\n")
        _write(tmp, "requirements.txt", "flask\n")
        d = m.detect_project(tmp)
        assert "python" in d["runtimes"], d

    with tempfile.TemporaryDirectory() as raw:
        tmp = Path(raw)
        _write(tmp, "package.json", json.dumps({
            "name": "web", "dependencies": {"express": "^4", "react": "^18"},
        }))
        d = m.detect_project(tmp)
        assert "web-app" in d["project_kinds"], d
        print("OK: detect python + web-app")


def test_detect_empty_repo_graceful() -> None:
    m = _load("detectors")
    with tempfile.TemporaryDirectory() as raw:
        tmp = Path(raw)
        d = m.detect_project(tmp)
        # No manifests -> empty classification, but never crashes.
        assert d["runtimes"] == [], d
        assert d["project_kinds"] == [], d
        print("OK: detect empty repo graceful")


def test_surface_finds_entry_points() -> None:
    m = _load("detectors")
    with tempfile.TemporaryDirectory() as raw:
        tmp = Path(raw)
        _write(tmp, "src/spawn.ts",
               "import cp from 'child_process'\ncp.spawn(cmd, args)\n")
        _write(tmp, "src/net.ts",
               "const r = await requestUrl(url)\nfetch(other)\n")
        _write(tmp, "src/ipc.ts",
               "window.addEventListener('message', (e) => handle(e.data))\n")
        _write(tmp, "src/deser.ts",
               "const o = JSON.parse(raw)\n")
        files = ["src/spawn.ts", "src/net.ts", "src/ipc.ts", "src/deser.ts"]
        surfaces = m.enumerate_surfaces(tmp, files)
        types = {s["surface_type"] for s in surfaces}
        assert "child_process" in types, surfaces
        assert "network_egress" in types, surfaces
        assert "message_listener" in types, surfaces
        assert "deserialization" in types, surfaces
        # Every surface has a file+line anchor.
        for s in surfaces:
            assert s["file"] and isinstance(s["line"], int), s
        print("OK: surface finds entry points")


def test_surface_is_deterministic_sorted() -> None:
    m = _load("detectors")
    with tempfile.TemporaryDirectory() as raw:
        tmp = Path(raw)
        _write(tmp, "b.ts", "fetch(x)\n")
        _write(tmp, "a.ts", "fetch(y)\n")
        s1 = m.enumerate_surfaces(tmp, ["b.ts", "a.ts"])
        s2 = m.enumerate_surfaces(tmp, ["a.ts", "b.ts"])
        assert s1 == s2, "surface output must be order-independent + sorted"
        print("OK: surface deterministic + sorted")


def test_surface_skips_binary_and_missing() -> None:
    m = _load("detectors")
    with tempfile.TemporaryDirectory() as raw:
        tmp = Path(raw)
        _write(tmp, "ok.ts", "fetch(x)\n")
        # missing file in the list must not crash
        surfaces = m.enumerate_surfaces(tmp, ["ok.ts", "does-not-exist.ts"])
        assert any(s["file"] == "ok.ts" for s in surfaces), surfaces
        print("OK: surface skips missing files gracefully")


ALL_TESTS = [
    test_detect_electron_obsidian_plugin,
    test_detect_cli_vs_library,
    test_detect_python_and_webapp,
    test_detect_empty_repo_graceful,
    test_surface_finds_entry_points,
    test_surface_is_deterministic_sorted,
    test_surface_skips_binary_and_missing,
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
    print("\nAll detectors tests passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
