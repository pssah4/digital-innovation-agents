"""Project-type detection and attack-surface enumeration.

Pure file inspection: no network, no external tools, deterministic.

detect_project(root) -> dict
    Classifies runtimes (node/python/...) and project kinds
    (electron/obsidian-plugin/web-app/cli/library). Multiple kinds may
    apply at once (an Obsidian plugin is also electron). This is what
    makes the audit projekttyp-adaptiv: the detected kinds gate which
    reference checklists and which SAST rulesets apply.

enumerate_surfaces(root, files) -> list[dict]
    Deterministic grep of trust-boundary entry points across the given
    files. Feeds the attack-surface reference section. Not findings --
    context. Output is sorted so two runs match byte-for-byte.
"""
from __future__ import annotations
import json
import re
from pathlib import Path
from typing import Iterable

# ---------- project-type detection -----------------------------------------

# Frameworks whose presence in dependencies marks a web application.
_WEBAPP_DEPS = (
    "express", "koa", "fastify", "next", "nuxt", "react", "vue",
    "svelte", "@angular/core", "vite", "hapi", "@nestjs/core",
    "flask", "django", "fastapi", "starlette",
)
# Dependency names that indicate an LLM/agent API is used (gates phase 4).
_LLM_DEPS = (
    "@anthropic-ai/sdk", "anthropic", "openai", "@google/generative-ai",
    "@mistralai/mistralai", "cohere-ai", "langchain", "@langchain/core",
    "ollama", "llamaindex",
)


def _read_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def detect_project(root: Path) -> dict:
    pkg_path = root / "package.json"
    pkg = _read_json(pkg_path)
    deps = {}
    deps.update(pkg.get("dependencies", {}) or {})
    dev = pkg.get("devDependencies", {}) or {}
    all_deps = dict(deps)
    all_deps.update(dev)

    has_pkg = pkg_path.is_file()
    manifest = _read_json(root / "manifest.json")
    is_obsidian_manifest = bool(
        manifest.get("id") and manifest.get("minAppVersion")
    ) or ("obsidian" in dev)

    runtimes: list = []
    if has_pkg:
        runtimes.append("node")
    if (root / "pyproject.toml").is_file() or (root / "requirements.txt").is_file() \
            or (root / "setup.py").is_file():
        runtimes.append("python")
    if (root / "go.mod").is_file():
        runtimes.append("go")
    if (root / "Cargo.toml").is_file():
        runtimes.append("rust")

    kinds: list = []
    electron = "electron" in all_deps
    if is_obsidian_manifest:
        kinds.append("obsidian-plugin")
        # Obsidian plugins run inside Electron's renderer even without an
        # explicit electron dependency.
        electron = True
    if electron:
        kinds.append("electron")
    if any(d in all_deps for d in _WEBAPP_DEPS):
        kinds.append("web-app")
    # CLI: a bin field. Library: exports/module and not private, no bin.
    if has_pkg and pkg.get("bin"):
        kinds.append("cli")
    if has_pkg and not pkg.get("bin") and (pkg.get("exports") or pkg.get("module")) \
            and pkg.get("private") is not True:
        kinds.append("library")

    # De-dupe while preserving first-seen order.
    seen = set()
    kinds = [k for k in kinds if not (k in seen or seen.add(k))]

    llm_api = any(d in all_deps for d in _LLM_DEPS)

    applicable_tools = _applicable_tools(runtimes, kinds)

    return {
        "runtimes": runtimes,
        "project_kinds": kinds,
        "signals": {
            "package_json": has_pkg,
            "obsidian_manifest": is_obsidian_manifest,
            "electron_dep": "electron" in all_deps,
            "bin_field": bool(pkg.get("bin")),
            "exports_field": bool(pkg.get("exports") or pkg.get("module")),
            "llm_api": llm_api,
            "lockfiles": sorted(
                n for n in ("package-lock.json", "yarn.lock", "pnpm-lock.yaml",
                            "poetry.lock", "Cargo.lock", "go.sum")
                if (root / n).is_file()
            ),
        },
        "applicable_tools": applicable_tools,
        "reference_gates": _reference_gates(kinds, llm_api),
    }


def _applicable_tools(runtimes: list, kinds: list) -> dict:
    sast = []
    sca = []
    if "node" in runtimes:
        sast.append("semgrep:p/typescript")
        sast.append("semgrep:p/javascript")
        sca.extend(["npm-audit", "osv-scanner"])
    if "python" in runtimes:
        sast.append("semgrep:p/python")
        sca.extend(["pip-audit", "osv-scanner"])
    if "go" in runtimes:
        sca.append("osv-scanner")
    if "rust" in runtimes:
        sca.append("cargo-audit")
    # de-dupe preserving order
    def _dedupe(xs):
        s = set()
        return [x for x in xs if not (x in s or s.add(x))]
    return {"sast": _dedupe(sast), "sca": _dedupe(sca), "secrets": ["gitleaks", "trufflehog"]}


def _reference_gates(kinds: list, llm_api: bool) -> dict:
    """Which reference checklists apply for this project."""
    return {
        "desktop-runtime": "electron" in kinds,
        "owasp-llm": llm_api,
        "web": "web-app" in kinds,
    }


# ---------- attack-surface enumeration -------------------------------------

# (surface_type, compiled regex). Order does not matter; output is sorted.
_SURFACE_PATTERNS = [
    ("code_execution", re.compile(r"\b(eval|new\s+Function|vm\.runIn\w+)\s*\(")),
    ("child_process", re.compile(r"\b(child_process|execSync|spawnSync|\.spawn|\.exec|execFile)\b")),
    ("network_egress", re.compile(r"\b(fetch|requestUrl|axios|http\.get|https\.get|http\.request)\s*\(")),
    ("http_server", re.compile(r"\b(createServer|app\.(get|post|put|delete|patch)|listen)\s*\(")),
    ("message_listener", re.compile(r"addEventListener\s*\(\s*['\"]message['\"]|ipcMain\.(on|handle)|ipcRenderer\.(on|invoke)")),
    ("deserialization", re.compile(r"\b(JSON\.parse|yaml\.load|pickle\.loads|unserialize)\s*\(")),
    ("dom_sink", re.compile(r"\.(innerHTML|outerHTML)\b|dangerouslySetInnerHTML|document\.write\s*\(")),
    ("filesystem", re.compile(r"\bfs\.(read|write|append|unlink|rm|mkdir)\w*\s*\(|readFileSync|writeFileSync")),
    ("shell_open", re.compile(r"\bshell\.(openExternal|openPath)\s*\(")),
    ("protocol_handler", re.compile(r"registerProtocol|setAsDefaultProtocolClient|registerObsidianProtocol")),
]

# Text-file extensions worth scanning; anything else is skipped as binary.
_TEXT_EXT = {
    ".ts", ".tsx", ".js", ".jsx", ".mjs", ".cjs", ".py", ".go", ".rs",
    ".java", ".rb", ".php", ".vue", ".svelte",
}


def enumerate_surfaces(root: Path, files: Iterable[str]) -> list:
    """Grep the given files for trust-boundary entry points. Returns a
    sorted list of {surface_type, file, line, symbol}. Missing/binary
    files are skipped, never fatal.
    """
    out: list = []
    for rel in files:
        path = root / rel
        if path.suffix not in _TEXT_EXT:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except Exception:
            continue
        for ln, line in enumerate(text.splitlines(), start=1):
            for surface_type, rx in _SURFACE_PATTERNS:
                m = rx.search(line)
                if m:
                    out.append({
                        "surface_type": surface_type,
                        "file": rel,
                        "line": ln,
                        "symbol": m.group(0).strip(),
                    })
    # Deterministic ordering, independent of input file order.
    out.sort(key=lambda s: (s["file"], s["line"], s["surface_type"]))
    return out
